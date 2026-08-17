import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Earthquake Analytics Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM BACKGROUND + DESIGN
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 20%, rgba(37, 99, 235, 0.12), transparent 25%),
            radial-gradient(circle at 90% 10%, rgba(14, 165, 233, 0.10), transparent 25%),
            radial-gradient(circle at 50% 90%, rgba(30, 64, 175, 0.10), transparent 30%),
            linear-gradient(135deg, #07111f 0%, #0b1b2b 50%, #07111f 100%);
        color: #f8fafc;
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Main title */
    .dashboard-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }

    .dashboard-subtitle {
        text-align: center;
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        transition: 0.2s;
        border-color: rgba(56, 189, 248, 0.5);
    }

    /* Filter area */
    .filter-box {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Info message */
    .stAlert {
        border-radius: 12px;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #07111f 0%,
            #0b1b2b 100%
        );
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border-color: rgba(148, 163, 184, 0.15);
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">🌍 Earthquake Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive analysis of global earthquake activity using USGS data'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# MYSQL CONNECTION
# =========================================================

import streamlit as st
from sqlalchemy import create_engine

host = st.secrets["DB_HOST"]
port = st.secrets["DB_PORT"]
username = st.secrets["DB_USERNAME"]
password = st.secrets["DB_PASSWORD"]
database = st.secrets["DB_DATABASE"]

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}",
    connect_args={"ssl": {}}
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("usgs_earthquakes_26_features.csv")

df["time"] = pd.to_datetime(df["time"])

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌍 Earthquake Dashboard")

st.sidebar.markdown("---")

st.sidebar.write(
    "Use the filters below to explore earthquake activity."
)

# =========================================================
# KEY METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📌 Key Earthquake Statistics</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌍 Total Earthquakes",
    f"{len(df):,}"
)

col2.metric(
    "📈 Maximum Magnitude",
    f"{df['mag'].max():.2f}"
)

col3.metric(
    "📊 Average Magnitude",
    f"{df['mag'].mean():.2f}"
)

col4.metric(
    "⬇️ Maximum Depth",
    f"{df['depth_km'].max():.2f} km"
)

# =========================================================
# FILTERS
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🔎 Filter Earthquakes</div>',
    unsafe_allow_html=True
)

filter1, filter2, filter3 = st.columns(3)

with filter1:

    min_mag = st.slider(
        "Minimum Magnitude",
        min_value=float(df["mag"].min()),
        max_value=float(df["mag"].max()),
        value=float(df["mag"].min()),
        step=0.1
    )

with filter2:

    start_date = st.date_input(
        "Start Date",
        df["time"].min().date()
    )

with filter3:

    end_date = st.date_input(
        "End Date",
        df["time"].max().date()
    )

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["mag"] >= min_mag) &
    (df["time"].dt.date >= start_date) &
    (df["time"].dt.date <= end_date)
]

st.info(
    f"Showing {len(filtered_df):,} earthquakes "
    f"with magnitude ≥ {min_mag:.1f} "
    f"between {start_date} and {end_date}."
)

# =========================================================
# CHARTS
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📊 Earthquake Analysis</div>',
    unsafe_allow_html=True
)

chart1, chart2 = st.columns(2)

# Magnitude Distribution
with chart1:

    st.write("### 📈 Magnitude Distribution")

    magnitude_counts = (
        filtered_df["mag"]
        .round(1)
        .value_counts()
        .sort_index()
    )

    st.bar_chart(magnitude_counts)

# Yearly Trend
with chart2:

    st.write("### 📅 Yearly Earthquake Trend")

    yearly_counts = (
        filtered_df
        .groupby(filtered_df["time"].dt.year)
        .size()
    )

    st.line_chart(yearly_counts)

# =========================================================
# EARTHQUAKE MAP
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🌍 Global Earthquake Locations</div>',
    unsafe_allow_html=True
)

map_data = filtered_df[
    ["latitude", "longitude"]
].dropna()

st.map(map_data)

# =========================================================
# DATA TABLE
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📋 Earthquake Data</div>',
    unsafe_allow_html=True
)

st.write(
    f"Showing **{len(filtered_df):,}** filtered records"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

# =========================================================
# DATASET INFORMATION
# =========================================================

st.markdown("---")

with st.expander("ℹ️ Dataset Information"):

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Rows:**", len(df))
        st.write("**Columns:**", len(df.columns))

    with col2:

        st.write(
            "**Earliest Date:**",
            df["time"].min()
        )

        st.write(
            "**Latest Date:**",
            df["time"].max()
        )

    st.write("**Columns:**")

    st.write(df.columns.tolist())
    # ==== Magnitude & Depth ====
# ===== QUERY 1 Top 10 strongest earthquakes (mag) =====

query1 = """
SELECT
    id,
    time,
    place,
    country,
    mag,
    magType,
    depth_km
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;
"""

df_query1 = pd.read_sql(query1, engine)

st.write("### QUERY 1 Top 10 strongest earthquakes (mag)")
st.dataframe(df_query1)

# ===== Query 2 — Top 10 Deepest Earthquakes (depth_km) =====
query2 = """
SELECT
    id,
    time,
    place,
    country,
    depth_km,
    mag,
    magType
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;
"""

df_query2 = pd.read_sql(query2, engine)
st.write("### Query 2 — Top 10 Deepest Earthquakes (depth_km)")
st.dataframe(df_query2)

# ===== QUERY 3 Shallow earthquakes < 50 km and mag > 7.5. =====

query3 = """
SELECT
    id,
    time,
    place,
    country,
    depth_km,
    mag,
    magType,
    tsunami
FROM earthquakes
WHERE depth_km < 50
  AND mag > 7.5
ORDER BY mag DESC, depth_km ASC;
"""

df_query3 = pd.read_sql(query3, engine)
st.write("### QUERY 3 Shallow earthquakes < 50 km and mag > 7.5.")
st.dataframe(df_query3)

# ===== Query 4 — Average depth per continent =====
query4 = """
SELECT
    CASE
        WHEN country IN (
            'India', 'Indonesia', 'Philippines', 'Japan',
            'China', 'Russia', 'New Zealand', 'Iran',
            'Turkey', 'Nepal', 'Pakistan', 'Taiwan',
            'Papua New Guinea', 'Fiji'
        ) THEN 'Asia'

        WHEN country IN (
            'United States', 'Canada', 'Mexico',
            'Alaska Earthquake'
        ) THEN 'North America'

        WHEN country IN (
            'Chile', 'Peru', 'Argentina', 'Brazil',
            'Colombia', 'Ecuador', 'Bolivia'
        ) THEN 'South America'

        WHEN country IN (
            'South Africa', 'Kenya', 'Ethiopia',
            'Tanzania', 'Madagascar'
        ) THEN 'Africa'

        WHEN country IN (
            'France', 'Germany', 'Italy', 'Greece',
            'Spain', 'Iceland', 'Norway',
            'New Zealand Earthquake'
        ) THEN 'Europe'

        WHEN country IN (
            'Australia'
        ) THEN 'Oceania'

        ELSE 'Unknown'
    END AS continent,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(depth_km), 2) AS average_depth_km
FROM earthquakes
GROUP BY continent
ORDER BY average_depth_km DESC;
"""

df_query4 = pd.read_sql(query4, engine)
st.write("### Query 4 — Average depth per continent.")
df_query4

# ===== Query 5 — Average magnitude per magnitude type (magType). =====
query5 = """
SELECT
    magType,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE magType IS NOT NULL
  AND magType <> ''
GROUP BY magType
ORDER BY average_magnitude DESC;
"""

df_query5 = pd.read_sql(query5, engine)
st.write("### Query 5 — Average magnitude per magnitude type (magType)")
df_query5

# ===== TIME ANALYSIS =====
# ===== Query 6 — Year with most earthquakes =====
query6 = """
SELECT
    year,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE year IS NOT NULL
GROUP BY year
ORDER BY earthquake_count DESC
LIMIT 1;
"""

df_query6 = pd.read_sql(query6, engine)
st.write("### Query 6 — Year with most earthquakes")
df_query6

# ===== Query 7 — Month with highest number of earthquakes. =====
query7 = """
SELECT
    month,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE month IS NOT NULL
GROUP BY month
ORDER BY earthquake_count DESC
LIMIT 1;
"""

df_query7 = pd.read_sql(query7, engine)
st.write("### Query 7 — Month with highest number of earthquakes")
df_query7

# ===== Query 8 — Day of week with most earthquakes =====
query8 = """
SELECT
    day_of_week,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE day_of_week IS NOT NULL
GROUP BY day_of_week
ORDER BY earthquake_count DESC
LIMIT 1;
"""

df_query8 = pd.read_sql(query8, engine)
st.write("### Query 8 — Day of week with most earthquakes")
df_query8

# ===== Query 9 — Count of earthquakes per hour of day =====
query9 = """
SELECT
    HOUR(time) AS hour_of_day,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE time IS NOT NULL
GROUP BY HOUR(time)
ORDER BY hour_of_day ASC;
"""

df_query9 = pd.read_sql(query9, engine)
st.write("### Query 9 — Count of earthquakes per hour of day")
df_query9

# ===== Query 10 — Most active reporting network (net) =====
query10 = """
SELECT
    net,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE net IS NOT NULL
  AND net <> ''
GROUP BY net
ORDER BY earthquake_count DESC
LIMIT 1;
"""

df_query10 = pd.read_sql(query10, engine)
st.write("### Query 10 — Most active reporting network (net)")
df_query10

# ===== Casualties & Economic Loss =====

# ===== Query 11 — Top 5 places with highest casualties. =====

query11 = """
SELECT
    place,
    MAX(sig) AS highest_significance
FROM earthquakes
WHERE place IS NOT NULL
GROUP BY place
ORDER BY highest_significance DESC
LIMIT 5;
"""

df_query11 = pd.read_sql(query11, engine)
st.write("### Query 11 — Top 5 places with highest casualties.")
df_query11

# ===== Query 12 — Total estimated economic loss per continent. =====

query12 = """
SELECT
    country,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE country IS NOT NULL
  AND country <> ''
  AND country <> 'unknown'
GROUP BY country
ORDER BY earthquake_count DESC
LIMIT 10;
"""

df_query12 = pd.read_sql(query12, engine)

st.write("### Query 12 — Total estimated economic loss per continent.")

st.dataframe(df_query12, use_container_width=True)

# ===== Query 13 — Average economic loss by alert level. =====

query13 = """
SELECT
    status,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE status IS NOT NULL
GROUP BY status
ORDER BY average_magnitude DESC;
"""

df_query13 = pd.read_sql(query13, engine)

st.write("### Query 13 — Average Magnitude by Earthquake Status")

st.dataframe(df_query13, use_container_width=True)
# ===== Event Type & Quality Metrics =====

# ===== Query 14 — Count of reviewed vs automatic earthquakes (status). =====
query14 = """
SELECT
    status,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE status IS NOT NULL
  AND status <> ''
GROUP BY status
ORDER BY earthquake_count DESC;
"""

df_query14 = pd.read_sql(query14, engine)
st.write("### Query 14 — Count of reviewed vs automatic earthquakes (status).")
df_query14

# ===== Query 15 — Count by earthquake type (type). =====

query15 = """
SELECT
    type,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE type IS NOT NULL
  AND type <> ''
GROUP BY type
ORDER BY earthquake_count DESC;
"""

df_query15 = pd.read_sql(query15, engine)
st.write("### Query 15 — Count by earthquake type (type).")
df_query15

# ===== Query 16 — Number of earthquakes by data type (types) =====
query16 = """
SELECT
    types,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE types IS NOT NULL
  AND types <> ''
GROUP BY types
ORDER BY earthquake_count DESC;
"""

df_query16 = pd.read_sql(query16, engine)
st.write("### Query 16 — Number of earthquakes by data type (types)")
df_query16
# ===== Query 17 — Average RMS and gap per continent. =====
query17 = """
SELECT
    CASE
        WHEN country IN (
            'India', 'Indonesia', 'Philippines', 'Japan',
            'China', 'Russia', 'New Zealand', 'Iran',
            'Turkey', 'Nepal', 'Pakistan', 'Taiwan',
            'Papua New Guinea', 'Fiji'
        ) THEN 'Asia'

        WHEN country IN (
            'United States', 'Canada', 'Mexico',
            'Alaska Earthquake'
        ) THEN 'North America'

        WHEN country IN (
            'Chile', 'Peru', 'Argentina', 'Brazil',
            'Colombia', 'Ecuador', 'Bolivia'
        ) THEN 'South America'

        WHEN country IN (
            'South Africa', 'Kenya', 'Ethiopia',
            'Tanzania', 'Madagascar'
        ) THEN 'Africa'

        WHEN country IN (
            'France', 'Germany', 'Italy', 'Greece',
            'Spain', 'Iceland', 'Norway',
            'New Zealand Earthquake'
        ) THEN 'Europe'

        WHEN country = 'Australia'
        THEN 'Oceania'

        ELSE 'Unknown'
    END AS continent,

    COUNT(*) AS earthquake_count,

    ROUND(AVG(rms), 3) AS average_rms,

    ROUND(AVG(gap), 3) AS average_gap

FROM earthquakes

WHERE rms IS NOT NULL
  AND gap IS NOT NULL

GROUP BY continent

ORDER BY average_rms DESC;
"""

df_query17 = pd.read_sql(query17, engine)
st.write("### Query 17 — Average RMS and gap per continent.")
df_query17

# ===== Query 18 — Events with high station coverage (nst > threshold) =====
query18_threshold = """
SELECT
    AVG(nst) AS average_nst
FROM earthquakes
WHERE nst > 0;
"""

df_threshold = pd.read_sql(query18_threshold, engine)
st.write("### Query 18 — Events with high station coverage (nst > threshold)")
df_threshold

# ===== Tsunamis & Alerts =====
# ===== Query 19 — Events with high station coverage (nst > threshold) =====
query19 = """
SELECT
    year,
    COUNT(*) AS tsunami_count
FROM earthquakes
WHERE tsunami = 1
  AND year IS NOT NULL
GROUP BY year
ORDER BY year ASC;
"""

df_query19 = pd.read_sql(query19, engine)
st.write("### Query 19 — Events with high station coverage (nst > threshold)")
df_query19

# ===== Query 20 — Count earthquakes by alert levels (red, orange, etc.). =====

query20 = """
SELECT
    magnitude_category,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE magnitude_category IS NOT NULL
GROUP BY magnitude_category
ORDER BY earthquake_count DESC;
"""

df_query20 = pd.read_sql(query20, engine)
st.write("### Query 20 — Count Earthquakes by Magnitude Category")
st.dataframe(df_query20, use_container_width=True)

# ===== Seismic Pattern & Trends Analysis. =====
# ===== Query 21 — Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years  =====
query21 = """
SELECT
    country,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE year BETWEEN 2022 AND 2026
  AND country IS NOT NULL
  AND TRIM(country) <> ''
  AND LOWER(country) NOT IN ('unknown', 'unknown region')
GROUP BY country
HAVING COUNT(*) >= 10
ORDER BY average_magnitude DESC
LIMIT 5;
"""

df_query21 = pd.read_sql(query21, engine)
st.write("### Query 21 — Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years")
df_query21

# ===== Query 22 — Find countries that have experienced both shallow and deep earthquakes within the same month. =====
query22 = """
SELECT
    country,
    year,
    month,
    SUM(CASE WHEN depth_km < 50 THEN 1 ELSE 0 END) AS shallow_count,
    SUM(CASE WHEN depth_km >= 50 THEN 1 ELSE 0 END) AS deep_count
FROM earthquakes
WHERE country IS NOT NULL
  AND TRIM(country) <> ''
  AND LOWER(country) <> 'unknown'
  AND depth_km IS NOT NULL
GROUP BY country, year, month
HAVING shallow_count > 0
   AND deep_count > 0
ORDER BY country, year, month;
"""

df_query22 = pd.read_sql(query22, engine)
st.write("### Query 22 — Find countries that have experienced both shallow and deep earthquakes within the same month.")
df_query22

# ===== Query 23 — Compute the year-over-year growth rate in the total number of earthquakes globally. =====
query23 = """
WITH yearly_counts AS (
    SELECT
        year,
        COUNT(*) AS earthquake_count
    FROM earthquakes
    WHERE year IS NOT NULL
    GROUP BY year
),
growth_calculation AS (
    SELECT
        year,
        earthquake_count,
        LAG(earthquake_count) OVER (ORDER BY year) AS previous_year_count
    FROM yearly_counts
)
SELECT
    year,
    earthquake_count,
    previous_year_count,
    ROUND(
        ((earthquake_count - previous_year_count)
        / previous_year_count) * 100,
        2
    ) AS yoy_growth_percent
FROM growth_calculation
ORDER BY year;
"""

df_query23 = pd.read_sql(query23, engine)
st.write("### Query 23 — Compute the year-over-year growth rate in the total number of earthquakes globally.")
df_query23

# ===== Query 24 — List the 3 most seismically active regions by combining both frequency and average magnitude. =====
query24 = """
WITH region_stats AS (
    SELECT
        country,
        COUNT(*) AS earthquake_count,
        AVG(mag) AS average_magnitude
    FROM earthquakes
    WHERE country IS NOT NULL
      AND TRIM(country) <> ''
      AND LOWER(country) <> 'unknown'
      AND mag IS NOT NULL
    GROUP BY country
),
ranked AS (
    SELECT
        country,
        earthquake_count,
        ROUND(average_magnitude, 2) AS average_magnitude,
        RANK() OVER (ORDER BY earthquake_count DESC) AS frequency_rank,
        RANK() OVER (ORDER BY average_magnitude DESC) AS magnitude_rank
    FROM region_stats
)
SELECT
    country,
    earthquake_count,
    average_magnitude,
    frequency_rank,
    magnitude_rank,
    (frequency_rank + magnitude_rank) AS combined_rank
FROM ranked
ORDER BY combined_rank ASC
LIMIT 3;
"""

df_query24 = pd.read_sql(query24, engine)
st.write("### Query 24 — List the 3 most seismically active regions by combining both frequency and average magnitude.")
df_query24

# ===== Depth, Location & Distance-Based  Analysis.  =====

# ===== Query 25 — For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator. =====
query25 = """
SELECT
    country,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(depth_km), 2) AS average_depth_km
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
  AND depth_km IS NOT NULL
  AND country IS NOT NULL
  AND TRIM(country) <> ''
  AND LOWER(country) <> 'unknown'
GROUP BY country
ORDER BY average_depth_km DESC;
"""

df_query25 = pd.read_sql(query25, engine)
st.write("### Query 25 — For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.")
df_query25

# ===== Query 26 — Identify countries having the highest ratio of shallow to deep earthquakes. =====
query26 = """
SELECT
    country,
    SUM(CASE WHEN depth_km < 50 THEN 1 ELSE 0 END) AS shallow_count,
    SUM(CASE WHEN depth_km >= 50 THEN 1 ELSE 0 END) AS deep_count,
    ROUND(
        SUM(CASE WHEN depth_km < 50 THEN 1 ELSE 0 END)
        /
        NULLIF(SUM(CASE WHEN depth_km >= 50 THEN 1 ELSE 0 END), 0),
        2
    ) AS shallow_deep_ratio
FROM earthquakes
WHERE country IS NOT NULL
  AND TRIM(country) <> ''
  AND LOWER(country) <> 'unknown'
  AND depth_km IS NOT NULL
GROUP BY country
HAVING deep_count > 0
ORDER BY shallow_deep_ratio DESC
LIMIT 10;
"""

df_query26 = pd.read_sql(query26, engine)
st.write("### Query 26 — Identify countries having the highest ratio of shallow to deep earthquakes.")
df_query26

# ===== Query 27 — Find the average magnitude difference between earthquakes with tsunami alerts and those without. =====
query27 = """
SELECT
    CASE
        WHEN tsunami = 1 THEN 'Tsunami'
        ELSE 'No Tsunami'
    END AS tsunami_status,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS average_magnitude
FROM earthquakes
WHERE mag IS NOT NULL
GROUP BY tsunami_status
ORDER BY tsunami_status;
"""

df_query27 = pd.read_sql(query27, engine)
st.write("### Query 27 — Find the average magnitude difference between earthquakes with tsunami alerts and those without.")
df_query27

# ===== Query 28 — Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).=====
query28 = """
SELECT
    id,
    time,
    place,
    country,
    mag,
    depth_km,
    rms,
    gap,
    ROUND((rms + gap) / 2, 2) AS reliability_error_score
FROM earthquakes
WHERE rms IS NOT NULL
  AND gap IS NOT NULL
ORDER BY reliability_error_score DESC
LIMIT 20;
"""

df_query28 = pd.read_sql(query28, engine)
st.write("### Query 28 — Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)")
df_query28


# ===== Query 29 =====

st.write("### Query 29 — Consecutive Earthquakes Within 50 km and 1 Hour")

st.info(
    "This analysis is excluded from the interactive dashboard "
    "to maintain dashboard performance."
)

# ===== Query 30 — Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km). =====
query30 = """
SELECT
    country,
    COUNT(*) AS deep_focus_count,
    ROUND(AVG(depth_km), 2) AS average_depth_km,
    ROUND(AVG(mag), 2) AS average_magnitude,
    MAX(depth_km) AS maximum_depth_km
FROM earthquakes
WHERE depth_km > 300
  AND country IS NOT NULL
  AND TRIM(country) <> ''
  AND LOWER(country) <> 'unknown'
GROUP BY country
ORDER BY deep_focus_count DESC
LIMIT 10;
"""

df_query30 = pd.read_sql(query30, engine)
st.write("### Query 30 — Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).")
df_query30