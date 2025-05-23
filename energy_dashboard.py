

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# --- Load data ---
st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("gebaeude_batiment_edificio.csv")
    return df
df = load_data()

# --- Load population data ---
@st.cache_data
def load_population():
    pop_df = pd.read_csv("population_statistics.csv")
    return pop_df
pop_df = load_population()

# --- Load municipality names
# added by networkscientist to work with pruned building table
@st.cache_data
def load_muni_names():
    return pd.read_csv("gemeindestand_2025_pruned.csv")

df['GGDENAME'] = df.join(load_muni_names().set_index('BFS Gde-nummer'), on='GGDENR')['Gemeindename']

# Keep only 2023 entries
pop_2023 = pop_df[pop_df["year"] == 2023].copy()

# Strip spaces for safety
pop_2023["municipality"] = pop_2023["municipality"].str.strip()
df["GGDENAME"] = df["GGDENAME"].str.strip()

# Build lookup: municipality → population
pop_lookup = dict(zip(pop_2023["municipality"], pop_2023["population"]))



# --- Filter for valid GENH1 and GSTAT == 1004 ---
df_valid = df[(df["GENH1"].notna()) & (df["GSTAT"] == 1004)].copy()
df_valid["GENH1"] = df_valid["GENH1"].astype(int)

# --- Your handwritten GENH1 → label mapping ---
GENH1_LABELS = {
    7500: "Keine",
    7501: "Luft",
    7510: "Geothermie", 7511: "Geothermie", 7512: "Geothermie",
    7513: "Wasser",
    7520: "Gas",
    7530: "Heizöl",
    7540: "Holz", 7541: "Holz", 7542: "Holz", 7543: "Holz",
    7570: "Abwärme",
    7560: "Elektrizität",
    7570: "Sonne",
    7580: "Fernwärme", 7581: "Fernwärme", 7582: "Fernwärme",
    7598: "Weitere", 7599: "Weitere"
}

df_valid["Energieträger_Label"] = df_valid["GENH1"].map(GENH1_LABELS)
df_valid = df_valid[df_valid["Energieträger_Label"].notna()]

# --- Grouping logic for categories ---
LABEL_GROUPS = {
    "Heizöl": "Fossile Energieträger",
    "Gas": "Fossile Energieträger",
    "Luft": "Erneuerbare Energieträger",
    "Holz": "Erneuerbare Energieträger",
    "Geothermie": "Erneuerbare Energieträger",
    "Fernwärme": "Erneuerbare Energieträger",
    "Sonne": "Erneuerbare Energieträger",
    "Wasser": "Erneuerbare Energieträger",
    "Elektrizität": "Elektrizität",
    "Keine": "Keine",
    "Weitere": "Weitere"
}
# --- Chart builder ---
def render_chart_block(html_id, chart_config):
    return f"""
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/drilldown.js"></script>
        <div id="{html_id}" style="height: 500px; min-width: 100%;"></div>
        <script>
        Highcharts.chart('{html_id}', {json.dumps(chart_config)});
        </script>
    """

# --- Chart config builder ---
def build_chart_config(title, data):
    data["Kategorie"] = data["Energieträger_Label"].map(LABEL_GROUPS)
    main = data.groupby("Kategorie").size().reset_index(name="y")
    sub = data.groupby(["Kategorie", "Energieträger_Label"]).size().reset_index(name="y")

    main_data = []
    drill = []
    for _, row in main.iterrows():
        e = {"name": row["Kategorie"], "y": int(row["y"])}
        if e["name"] in ["Fossile Energieträger", "Erneuerbare Energieträger"]:
            e["drilldown"] = e["name"]
        main_data.append(e)

    for group in ["Fossile Energieträger", "Erneuerbare Energieträger"]:
        subdata = sub[sub["Kategorie"] == group]
        if not subdata.empty:
            drill.append({
                "name": group,
                "id": group,
                "data": [[row["Energieträger_Label"], int(row["y"])] for _, row in subdata.iterrows()]
            })

    return {
        "chart": {"type": "pie"},
        "title": {"text": title},
                "colors": [  # 🎨 CUSTOM COLORS (order must match main_data)
            "#FFFF00",  # Elektrizität
            "#008000",  # Erneuerbare Energieträger
            "#FF0000",  # Fossile Energieträger
            "#111111",  # Keine
            "#D3D3D3"   # Weitere
        ],

        "plotOptions": {
            "pie": {
                "dataLabels": {
                    "enabled": True,
                    "format": "<b>{point.name}</b>: {point.percentage:.1f}%",
                    "style": {"fontSize": "0.9em"}
                },
                "showInLegend": True
            }
        },
        "series": [{
            "name": "Kategorie",
            "colorByPoint": True,
            "data": main_data
        }],
        "drilldown": {"series": drill}
    }
# --- Always show Kanton Bern chart at the top ---
st.title("Energieträger im Kanton Bern (Übersicht)")
st.subheader("Population: 134,290 (2021)")

bern_data = df_valid[df_valid["KT"] == "BE"] if "KT" in df_valid.columns else df_valid  # fallback if KT not present
bern_chart_top = render_chart_block("bern_top", build_chart_config("Energieträger im Kanton Bern", bern_data))
components.html(bern_chart_top, height=550)
# --- Load cantonal electricity data (already done earlier) ---
@st.cache_data
def load_canton_energyreport():
    df = pd.read_csv("energyreporter_canton_historized.csv")
    df["energyreporter_date"] = pd.to_datetime(df["energyreporter_date"])
    return df

canton_elec = load_canton_energyreport()
bern_canton_elec = canton_elec[canton_elec["canton"] == "BE"].sort_values("energyreporter_date")
latest_bern = bern_canton_elec.iloc[-1] if not bern_canton_elec.empty else None

# --- Elektrizitätsprofil für Kanton Bern (oben anzeigen) ---
if latest_bern is not None:
    st.subheader("Elektrizitätsprofil für Kanton Bern  – Aktuellste Werte")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔋 Anteil Elektroautos", f"{latest_bern['electric_car_share'] * 100:.2f} %")
        st.metric("🚗 Anzahl Elektroautos", f"{int(latest_bern['electric_car_count']):,}".replace(",", "'"))
        st.metric("⚡ Ladepunkte", int(latest_bern["electric_car_charging_spot_count"]))
        st.metric("🚘 Autos pro Ladepunkt", f"{latest_bern['electric_cars_per_charging_spot']:.1f}")

    with col2:
        st.metric("☀️ Solarpotenzial-Nutzung", f"{latest_bern['solar_potential_usage'] * 100:.1f} %")
        st.metric("🌱 Erneuerbarer Heizanteil", f"{latest_bern['renewable_heating_share'] * 100:.1f} %")
        st.metric("🔌 Stromverbrauch", f"{latest_bern['elec_consumption_mwh_per_year_per_capita']:.1f} MWh/Person")
        st.metric("⚡ Erneuerbare Stromproduktion", f"{latest_bern['renelec_production_mwh_per_year_per_capita']:.1f} MWh/Person")


    with st.expander("Zeitliche Entwicklung für Kanton Bern anzeigen"):
        bern_tabs = st.tabs([
            "Anteil Elektroautos", "Solarpotenzial", "Heizanteil", 
            "Stromverbrauch", "Ern. Stromproduktion", "Autos pro Ladepunkt"
        ])

        bern_charts = [
    ("electric_car_share", "%", True),
    ("solar_potential_usage", "%", True),
    ("renewable_heating_share", "%", True),
    ("elec_consumption_mwh_per_year_per_capita", "MWh", False),
    ("renelec_production_mwh_per_year_per_capita", "MWh", False),
    ("electric_cars_per_charging_spot", "", False)
]

for tab, (col, unit, is_percentage) in zip(bern_tabs, bern_charts):
    with tab:
        ts = bern_canton_elec[["energyreporter_date", col]].dropna().set_index("energyreporter_date")
        if not ts.empty:
            if is_percentage:
                ts[col] *= 100
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(ts.index, ts[col], label="Kanton Bern", color="tab:blue")
            ax.set_ylabel(f"{col} ({unit})")
            ax.set_xlabel("Datum")
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("Keine Zeitreihen verfügbar.")


# --- Section toggle for detailed comparison ---
st.markdown("## Wo steht meine Gemeinde?")
show_details = st.checkbox("Gemeinde Details einblenden", value=True)

if show_details:


    # --- UI: Search bar for municipality ---
    city_list = sorted(df_valid["GGDENAME"].unique())
    city_name = st.selectbox("", city_list, placeholder="Gemeinde wählen")

    # --- Filter data for selected city ---
    city_data = df_valid[df_valid["GGDENAME"] == city_name]
    label_summary = city_data.groupby("Energieträger_Label").size().reset_index(name="Anzahl")
    label_summary = label_summary.sort_values("Anzahl", ascending=False)
    total = label_summary["Anzahl"].sum()

    # --- Display ---
    population = pop_lookup.get(city_name, "k.A.")
    if isinstance(population, (int, float)):
        population_str = f"{int(population):,}".replace(",", "'")
    else:
        population_str = population

    st.title(f"{city_name}")
    st.subheader(f"Bevölkerung: {population_str}")



    # Map category to each entry
    city_data["Kategorie"] = city_data["Energieträger_Label"].map(LABEL_GROUPS)

    # --- Main categories ---
    main_groups = city_data.groupby("Kategorie").size().reset_index(name="y")

    # --- Subcategories for drilldown ---
    sub_groups = city_data.groupby(["Kategorie", "Energieträger_Label"]).size().reset_index(name="y")


    # Format main pie chart data
    main_data = []
    for _, row in main_groups.iterrows():
        cat = row["Kategorie"]
        entry = {"name": cat, "y": int(row["y"])}
        if cat in ["Fossile Energieträger", "Erneuerbare Energieträger"]:
            entry["drilldown"] = cat
        main_data.append(entry)

    # Format drilldown series
    drilldown_series = []
    for group in ["Fossile Energieträger", "Erneuerbare Energieträger"]:
        subdata = sub_groups[sub_groups["Kategorie"] == group]
        if not subdata.empty:
            drilldown_series.append({
                "name": group,
                "id": group,
                "data": [[row["Energieträger_Label"], int(row["y"])] for _, row in subdata.iterrows()]
            })



    # --- Comparison controls ---
    compare_bern = st.checkbox("Mit Berner Durchschnitt vergleichen")
    compare_other = st.checkbox("Mit anderer Gemeinde vergleichen")

    compare_city = None
    if compare_other:
        compare_city = st.selectbox(
            "Vergleichsgemeinde wählen",
            [c for c in df_valid["GGDENAME"].unique() if c != city_name],
            key="compare_city"
        )



    # --- Build charts ---
    charts = []

    # Main city
    charts.append(render_chart_block("main_city", build_chart_config(f"Energieträger in {city_name}", city_data)))

    # Berner Durchschnitt
    if compare_bern:
        charts.append(render_chart_block("bern", build_chart_config("Energieträger im Kanton Bern", df_valid)))

    # Comparison city
    if compare_city:
        comp_data = df_valid[df_valid["GGDENAME"] == compare_city]
        charts.append(render_chart_block("compare_city", build_chart_config(f"Energieträger in {compare_city}", comp_data)))

    # --- Render charts with adaptive layout ---
    if len(charts) == 1:
        # Centered
        st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
        components.html(charts[0], height=550)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Side-by-side
        cols = st.columns(len(charts))
        for col, chart in zip(cols, charts):
            with col:
                components.html(chart, height=550)

    st.subheader("Energieträger Heizsystem")
    st.metric("Total", total)
    # Show summary table
    st.table(label_summary.set_index("Energieträger_Label"))
    # Load electricity data
    @st.cache_data
    def load_energyreport():
        return pd.read_csv("bern_energyreporter.csv")



    # --- Electricity Summary Cards ---
st.markdown("---")
st.header("Elektrizitätsprofil")

# Load electricity data
@st.cache_data
def load_energyreport():
    return pd.read_csv("bern_energyreporter.csv")

elec_df = load_energyreport()

# Prepare matching
elec_df["municipality"] = elec_df["municipality"].str.strip()
elec_df["energyreporter_date"] = pd.to_datetime(elec_df["energyreporter_date"])

# Filter for selected city
city_elec = elec_df[elec_df["municipality"] == city_name].sort_values("energyreporter_date")
latest = city_elec.iloc[-1] if not city_elec.empty else None

if latest is not None:
    st.subheader(f"{city_name} – Aktuellste Werte")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔋 Anteil Elektroautos", f"{latest['electric_car_share'] * 100:.1f} %")
        st.metric("🚗 Anzahl Elektroautos", f"{int(latest['electric_car_count']):,}".replace(",", "'"))
        st.metric("⚡ Ladepunkte", int(latest["electric_car_charging_spot_count"]))
        st.metric("🚘 Autos pro Ladepunkt", f"{latest['electric_cars_per_charging_spot']:.1f}")

    with col2:
        st.metric("☀️ Solarpotenzial-Nutzung", f"{latest['solar_potential_usage'] * 100:.1f} %")
        st.metric("🌱 Erneuerbarer Heizanteil", f"{latest['renewable_heating_share'] * 100:.1f} %")
        st.metric("🔌 Stromverbrauch", f"{latest['elec_consumption_mwh_per_year_per_capita']:.1f} MWh/Person")
        st.metric("⚡ Erneuerbare Stromproduktion", f"{latest['renelec_production_mwh_per_year_per_capita']:.1f} MWh/Person")

    with st.expander(" Zeitliche Entwicklung anzeigen"):
        tabs = st.tabs([
            "Anteil Elektroautos", "Solarpotenzial", "Heizanteil", 
            "Stromverbrauch", "Ern. Stromproduktion", "Autos pro Ladepunkt"
        ])

        charts = [
            ("electric_car_share", "%", True),
            ("solar_potential_usage", "%", True),
            ("renewable_heating_share", "%", True),
            ("elec_consumption_mwh_per_year_per_capita", "MWh", False),
            ("renelec_production_mwh_per_year_per_capita", "MWh", False),
            ("electric_cars_per_charging_spot", "", False)
        ]

# Load national and cantonal data once
@st.cache_data
def load_national_energyreport():
    df = pd.read_csv("energyreporter_national_historized.csv")
    df["energyreporter_date"] = pd.to_datetime(df["energyreporter_date"])
    return df

@st.cache_data
def load_canton_energyreport():
    df = pd.read_csv("energyreporter_canton_historized.csv")
    df["energyreporter_date"] = pd.to_datetime(df["energyreporter_date"])
    return df

national_elec = load_national_energyreport()
canton_elec = load_canton_energyreport()
canton_elec = canton_elec[canton_elec["canton"] == "BE"]  # Bern

# Plot
for tab, (col, unit, is_percentage) in zip(tabs, charts):
    with tab:
        city_ts = city_elec[["energyreporter_date", col]].dropna().set_index("energyreporter_date")
        national_ts = national_elec[["energyreporter_date", col]].dropna().set_index("energyreporter_date")
        canton_ts = canton_elec[["energyreporter_date", col]].dropna().set_index("energyreporter_date")

        if is_percentage:
            city_ts[col] *= 100
            national_ts[col] *= 100
            canton_ts[col] *= 100

        fig, ax = plt.subplots(figsize=(10, 4))

        if not city_ts.empty:
            ax.plot(city_ts.index, city_ts[col], label=f"{city_name}", linewidth=2)
        if not canton_ts.empty:
            ax.plot(canton_ts.index, canton_ts[col], label="Kanton Bern", linestyle="--")
        if not national_ts.empty:
            ax.plot(national_ts.index, national_ts[col], label="Schweiz", linestyle=":")

        ax.set_ylabel(f"{col} ({unit})")
        ax.set_xlabel("Datum")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
