import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Real Estate Buyer Segmentation",
    page_icon="🏠",
    layout="wide"
)
# =========================================================
# PROFESSIONAL DASHBOARD STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .dashboard-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    /* Section headers */
    .section-header {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* KPI cards */
    .kpi-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
        min-height: 120px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    .kpi-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #111827;
    }

    .kpi-description {
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 5px;
    }

    /* Insight cards */
    .insight-card {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .insight-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 5px;
    }

    .insight-value {
        font-size: 1rem;
        font-weight: 650;
        color: #111827;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    /* Remove excessive top spacing */
    div.block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">'
    'Real Estate Buyer Intelligence Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Buyer segmentation, investment behavior and geographic market intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    buyer_data = pd.read_csv(
        "data/buyer_segments_public.csv"
    )

    segment_profile = pd.read_csv(
        "outputs/segment_profile.csv"
    )

    return buyer_data, segment_profile


buyer_data, segment_profile = load_data()


st.success("Data loaded successfully!")


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("🔎 Dashboard Filters")

st.sidebar.write(
    "Use the filters below to analyze specific buyer groups."
)


# Country filter
country_options = sorted(
    buyer_data["country"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    options=country_options,
    default=country_options
)


# Region filter
filtered_for_regions = buyer_data[
    buyer_data["country"].isin(selected_countries)
]

region_options = sorted(
    filtered_for_regions["region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=region_options,
    default=region_options
)


# Acquisition purpose filter
purpose_options = sorted(
    buyer_data["acquisition_purpose"].dropna().unique()
)

selected_purposes = st.sidebar.multiselect(
    "Acquisition Purpose",
    options=purpose_options,
    default=purpose_options
)


# Client type filter
client_type_options = sorted(
    buyer_data["client_type"].dropna().unique()
)

selected_client_types = st.sidebar.multiselect(
    "Client Type",
    options=client_type_options,
    default=client_type_options
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_data = buyer_data[
    buyer_data["country"].isin(selected_countries)
    & buyer_data["region"].isin(selected_regions)
    & buyer_data["acquisition_purpose"].isin(selected_purposes)
    & buyer_data["client_type"].isin(selected_client_types)
].copy()


# ---------------------------------------------------------
# DASHBOARD OVERVIEW
# ---------------------------------------------------------

st.header("📊 Buyer Segmentation Overview")


total_buyers = len(filtered_data)

number_segments = (
    filtered_data["segment"].nunique()
    if total_buyers > 0
    else 0
)

number_countries = (
    filtered_data["country"].nunique()
    if total_buyers > 0
    else 0
)

average_spend = (
    filtered_data["total_spend"].mean()
    if total_buyers > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Buyers",
        f"{total_buyers:,}"
    )


with col2:
    st.metric(
        "Buyer Segments",
        number_segments
    )


with col3:
    st.metric(
        "Countries",
        number_countries
    )


with col4:
    st.metric(
        "Average Total Spend",
        f"${average_spend:,.0f}"
    )


# ---------------------------------------------------------
# STOP IF NO DATA
# ---------------------------------------------------------

if total_buyers == 0:

    st.warning(
        "No buyers match the selected filters. "
        "Please change the filters in the sidebar."
    )

    st.stop()
# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-header">Executive Overview</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CALCULATE KPI VALUES
# ---------------------------------------------------------

overview_buyers = len(filtered_data)

overview_investment_rate = (
    filtered_data["is_investor"].mean() * 100
)

overview_avg_spend = (
    filtered_data["total_spend"].mean()
)

overview_avg_properties = (
    filtered_data["total_properties"].mean()
)


# ---------------------------------------------------------
# CREATE FOUR KPI COLUMNS
# ---------------------------------------------------------

overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)


# ---------------------------------------------------------
# KPI 1 — TOTAL BUYERS
# ---------------------------------------------------------

with overview_col1:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Total Buyers
            </div>

            <div class="kpi-value">
                {overview_buyers:,}
            </div>

            <div class="kpi-description">
                Current filtered population
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# KPI 2 — INVESTMENT RATE
# ---------------------------------------------------------

with overview_col2:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Investment Rate
            </div>

            <div class="kpi-value">
                {overview_investment_rate:.1f}%
            </div>

            <div class="kpi-description">
                Buyers acquiring for investment
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# KPI 3 — AVERAGE TOTAL SPEND
# ---------------------------------------------------------

with overview_col3:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Average Total Spend
            </div>

            <div class="kpi-value">
                ${overview_avg_spend:,.0f}
            </div>

            <div class="kpi-description">
                Average cumulative property spend
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# KPI 4 — AVERAGE PROPERTIES
# ---------------------------------------------------------

with overview_col4:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Average Properties
            </div>

            <div class="kpi-value">
                {overview_avg_properties:.2f}
            </div>

            <div class="kpi-description">
                Properties per buyer
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# SEGMENT DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Buyer Segment Distribution")


segment_counts = (
    filtered_data["segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "segment",
    "buyer_count"
]


fig_segment = px.bar(
    segment_counts,
    x="segment",
    y="buyer_count",
    title="Number of Buyers by Segment",
    text="buyer_count"
)

fig_segment.update_layout(
    xaxis_title="Buyer Segment",
    yaxis_title="Number of Buyers",
    showlegend=False
)

st.plotly_chart(
    fig_segment,
    use_container_width=True
)


# ---------------------------------------------------------
# INVESTOR BEHAVIOR
# ---------------------------------------------------------

st.header("💰 Investor Behavior Dashboard")


behavior_col1, behavior_col2 = st.columns(2)


# Investment vs Home
with behavior_col1:

    purpose_data = (
        filtered_data["acquisition_purpose"]
        .value_counts()
        .reset_index()
    )

    purpose_data.columns = [
        "purpose",
        "buyer_count"
    ]

    fig_purpose = px.pie(
        purpose_data,
        names="purpose",
        values="buyer_count",
        title="Acquisition Purpose"
    )

    st.plotly_chart(
        fig_purpose,
        use_container_width=True
    )


# Average spend
with behavior_col2:

    spend_data = (
        filtered_data.groupby("segment")
        ["total_spend"]
        .mean()
        .reset_index()
    )

    fig_spend = px.bar(
        spend_data,
        x="segment",
        y="total_spend",
        title="Average Total Spend by Segment",
        text_auto=".2s"
    )

    fig_spend.update_layout(
        xaxis_title="Buyer Segment",
        yaxis_title="Average Total Spend ($)"
    )

    st.plotly_chart(
        fig_spend,
        use_container_width=True
    )


# ---------------------------------------------------------
# PROPERTY ACTIVITY
# ---------------------------------------------------------

st.subheader("🏘️ Property Purchase Activity")


property_data = (
    filtered_data.groupby("segment")
    ["total_properties"]
    .mean()
    .reset_index()
)


fig_properties = px.bar(
    property_data,
    x="segment",
    y="total_properties",
    title="Average Number of Properties Purchased",
    text_auto=".2f"
)

fig_properties.update_layout(
    xaxis_title="Buyer Segment",
    yaxis_title="Average Properties"
)

st.plotly_chart(
    fig_properties,
    use_container_width=True
)


# ---------------------------------------------------------
# INVESTMENT RATE BY SEGMENT
# ---------------------------------------------------------

investment_data = (
    filtered_data.groupby("segment")
    ["is_investor"]
    .mean()
    .reset_index()
)

investment_data["investment_rate"] = (
    investment_data["is_investor"] * 100
)


fig_investment = px.bar(
    investment_data,
    x="segment",
    y="investment_rate",
    title="Investment Rate by Buyer Segment",
    text_auto=".1f"
)

fig_investment.update_layout(
    xaxis_title="Buyer Segment",
    yaxis_title="Investment Rate (%)"
)

st.plotly_chart(
    fig_investment,
    use_container_width=True
)


# ---------------------------------------------------------
# GEOGRAPHIC BUYER ANALYSIS
# ---------------------------------------------------------

st.header("🌎 Geographic Buyer Analysis")


geo_col1, geo_col2 = st.columns(2)


# Country distribution
with geo_col1:

    country_data = (
        filtered_data["country"]
        .value_counts()
        .reset_index()
    )

    country_data.columns = [
        "country",
        "buyer_count"
    ]

    fig_country = px.bar(
        country_data,
        x="country",
        y="buyer_count",
        title="Buyers by Country",
        text="buyer_count"
    )

    fig_country.update_layout(
        xaxis_title="Country",
        yaxis_title="Buyer Count"
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


# Region distribution
with geo_col2:

    region_data = (
        filtered_data["region"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    region_data.columns = [
        "region",
        "buyer_count"
    ]

    fig_region = px.bar(
        region_data,
        x="buyer_count",
        y="region",
        orientation="h",
        title="Top 15 Regions by Buyer Count"
    )

    fig_region.update_layout(
        xaxis_title="Buyer Count",
        yaxis_title="Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ---------------------------------------------------------
# COUNTRY SEGMENT ANALYSIS
# ---------------------------------------------------------

st.subheader("Buyer Segments by Country")


country_segment = (
    filtered_data.groupby(
        ["country", "segment"]
    )
    .size()
    .reset_index(name="buyer_count")
)


fig_country_segment = px.bar(
    country_segment,
    x="country",
    y="buyer_count",
    color="segment",
    title="Buyer Segment Distribution by Country"
)

fig_country_segment.update_layout(
    xaxis_title="Country",
    yaxis_title="Buyer Count"
)

st.plotly_chart(
    fig_country_segment,
    use_container_width=True
)


# ---------------------------------------------------------
# SEGMENT INSIGHTS
# ---------------------------------------------------------

st.header("🔎 Segment Insights Panel")


segment_options = sorted(
    filtered_data["segment"].unique()
)


selected_segment = st.selectbox(
    "Select a buyer segment",
    segment_options
)


selected_segment_data = filtered_data[
    filtered_data["segment"] == selected_segment
]


insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)


with insight_col1:

    st.metric(
        "Buyers",
        f"{len(selected_segment_data):,}"
    )


with insight_col2:

    st.metric(
        "Average Age",
        f"{selected_segment_data['age'].mean():.1f}"
    )


with insight_col3:

    st.metric(
        "Average Properties",
        f"{selected_segment_data['total_properties'].mean():.2f}"
    )


with insight_col4:

    st.metric(
        "Investment Rate",
        f"{selected_segment_data['is_investor'].mean() * 100:.1f}%"
    )


# Detailed segment table

st.subheader("Selected Segment Profile")


segment_insight = pd.DataFrame({
    "Metric": [
        "Buyer Count",
        "Average Age",
        "Average Satisfaction",
        "Average Properties",
        "Average Total Spend",
        "Average Property Price",
        "Average Area",
        "Investment Rate",
        "Loan Rate"
    ],

    "Value": [
        len(selected_segment_data),

        round(
            selected_segment_data["age"].mean(),
            2
        ),

        round(
            selected_segment_data["satisfaction_score"].mean(),
            2
        ),

        round(
            selected_segment_data["total_properties"].mean(),
            2
        ),

        f"${selected_segment_data['total_spend'].mean():,.2f}",

        f"${selected_segment_data['average_property_price'].mean():,.2f}",

        f"{selected_segment_data['average_area_sqft'].mean():,.2f} sqft",

        f"{selected_segment_data['is_investor'].mean() * 100:.2f}%",

        f"{selected_segment_data['loan_flag'].mean() * 100:.2f}%"
    ]
})


st.dataframe(
    segment_insight,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------

st.header("📋 Filtered Buyer Data")

st.write(
    f"Showing {len(filtered_data):,} buyers based on the selected filters."
)


display_columns = [
    "client_id",
    "client_type",
    "gender",
    "country",
    "region",
    "acquisition_purpose",
    "loan_applied",
    "referral_channel",
    "age",
    "total_properties",
    "total_spend",
    "average_property_price",
    "segment"
]


st.dataframe(
    filtered_data[display_columns],
    use_container_width=True,
    hide_index=True
)

# =========================================================
# INTERACTIVE WORLD MAP BY COUNTRY
# =========================================================

# =========================================================
# INTERACTIVE WORLD MAP BY COUNTRY
# =========================================================

st.header("🌍 Interactive World Map")

st.write(
    "Explore buyer activity, spending, property values, "
    "and investment behavior across countries."
)

# ---------------------------------------------------------
# COUNTRY NAME → ISO-3 CODE
# ---------------------------------------------------------

country_codes = {
    "USA": "USA",
    "UK": "GBR",
    "Canada": "CAN",
    "Germany": "DEU",
    "France": "FRA",
    "Belgium": "BEL",
    "Mexico": "MEX",
    "Australia": "AUS",
    "Russia": "RUS",
    "Denmark": "DNK"
}


# ---------------------------------------------------------
# USE FILTERED DATA
# ---------------------------------------------------------

map_data = filtered_data.copy()


# ---------------------------------------------------------
# COUNTRY-LEVEL SUMMARY
# ---------------------------------------------------------

country_summary = (
    map_data
    .groupby("country")
    .agg(
        buyer_count=("client_id", "count"),
        avg_total_spend=("total_spend", "mean"),
        avg_property_price=("average_property_price", "mean"),
        avg_properties=("total_properties", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        investment_rate=("is_investor", "mean")
    )
    .reset_index()
)


# Convert investment rate to percentage
country_summary["investment_rate"] = (
    country_summary["investment_rate"] * 100
)


# Add ISO-3 country codes
country_summary["iso_code"] = (
    country_summary["country"].map(country_codes)
)


# ---------------------------------------------------------
# REMOVE COUNTRIES WITHOUT ISO CODES
# ---------------------------------------------------------

country_summary = country_summary[
    country_summary["iso_code"].notna()
].copy()


# ---------------------------------------------------------
# MAP METRIC SELECTOR
# ---------------------------------------------------------

map_metric = st.selectbox(
    "Select map metric",
    [
        "Number of Buyers",
        "Average Total Spend",
        "Average Property Price",
        "Average Properties",
        "Average Satisfaction",
        "Investment Rate"
    ],
    key="country_map_metric"
)


# Map metric → dataframe column
metric_mapping = {
    "Number of Buyers": "buyer_count",
    "Average Total Spend": "avg_total_spend",
    "Average Property Price": "avg_property_price",
    "Average Properties": "avg_properties",
    "Average Satisfaction": "avg_satisfaction",
    "Investment Rate": "investment_rate"
}


selected_metric = metric_mapping[map_metric]


# ---------------------------------------------------------
# CREATE INTERACTIVE WORLD MAP
# ---------------------------------------------------------

fig_map = px.choropleth(
    country_summary,

    locations="iso_code",

    color=selected_metric,

    hover_name="country",

    locationmode="ISO-3",

    projection="natural earth",

    color_continuous_scale="Blues",

    custom_data=[
        "buyer_count",
        "avg_total_spend",
        "avg_property_price",
        "avg_properties",
        "avg_satisfaction",
        "investment_rate"
    ]
)


# ---------------------------------------------------------
# PROFESSIONAL HOVER INFORMATION
# ---------------------------------------------------------

fig_map.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br><br>"

        "👥 Buyers: %{customdata[0]:,.0f}<br>"

        "💰 Average Total Spend: "
        "$%{customdata[1]:,.0f}<br>"

        "🏠 Average Property Price: "
        "$%{customdata[2]:,.0f}<br>"

        "🏘️ Average Properties: "
        "%{customdata[3]:.2f}<br>"

        "⭐ Average Satisfaction: "
        "%{customdata[4]:.2f}<br>"

        "📈 Investment Rate: "
        "%{customdata[5]:.1f}%"

        "<extra></extra>"
    )
)


# ---------------------------------------------------------
# MAP DESIGN
# ---------------------------------------------------------

fig_map.update_layout(
    height=600,

    margin=dict(
        l=0,
        r=0,
        t=30,
        b=0
    ),

    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth"
    ),

    coloraxis_colorbar=dict(
        title=map_metric
    )
)


# ---------------------------------------------------------
# DISPLAY MAP
# ---------------------------------------------------------

st.plotly_chart(
    fig_map,
    use_container_width=True
)


# ---------------------------------------------------------
# FILTER STATUS
# ---------------------------------------------------------

st.caption(
    f"Map based on {len(map_data):,} buyers "
    "after applying the selected dashboard filters."
)


# ---------------------------------------------------------
# COUNTRY SUMMARY TABLE
# ---------------------------------------------------------

st.subheader("🌎 Country-Level Buyer Summary")


country_display = country_summary[
    [
        "country",
        "buyer_count",
        "avg_total_spend",
        "avg_property_price",
        "avg_properties",
        "avg_satisfaction",
        "investment_rate"
    ]
].copy()


country_display.columns = [
    "Country",
    "Buyers",
    "Average Total Spend",
    "Average Property Price",
    "Average Properties",
    "Average Satisfaction",
    "Investment Rate"
]


st.dataframe(
    country_display,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# COUNTRY → SEGMENT ANALYSIS

# =========================================================
# COUNTRY → SEGMENT ANALYSIS
# =========================================================

st.header("🎯 Country → Buyer Segment Analysis")

st.write(
    "Select a country to examine its buyer segments, "
    "investment behavior, spending patterns, and property activity."
)


# ---------------------------------------------------------
# COUNTRY SELECTION
# ---------------------------------------------------------

available_countries = sorted(
    filtered_data["country"].dropna().unique()
)

selected_country = st.selectbox(
    "Select a country",
    available_countries,
    key="country_segment_analysis"
)


# ---------------------------------------------------------
# FILTER DATA FOR SELECTED COUNTRY
# ---------------------------------------------------------

country_data = filtered_data[
    filtered_data["country"] == selected_country
].copy()


# ---------------------------------------------------------
# COUNTRY OVERVIEW
# ---------------------------------------------------------

st.subheader(
    f"📍 {selected_country} Buyer Overview"
)


country_col1, country_col2, country_col3, country_col4 = st.columns(4)


with country_col1:

    st.metric(
        "Total Buyers",
        f"{len(country_data):,}"
    )


with country_col2:

    st.metric(
        "Investment Rate",
        f"{country_data['is_investor'].mean() * 100:.1f}%"
    )


with country_col3:

    st.metric(
        "Average Total Spend",
        f"${country_data['total_spend'].mean():,.0f}"
    )


with country_col4:

    st.metric(
        "Average Properties",
        f"{country_data['total_properties'].mean():.2f}"
    )


# ---------------------------------------------------------
# SEGMENT DISTRIBUTION
# ---------------------------------------------------------

st.subheader(
    f"Buyer Segments in {selected_country}"
)


country_segment_counts = (
    country_data["segment"]
    .value_counts()
    .reset_index()
)

country_segment_counts.columns = [
    "segment",
    "buyer_count"
]


# Segment percentage
country_segment_counts["percentage"] = (
    country_segment_counts["buyer_count"]
    / country_segment_counts["buyer_count"].sum()
    * 100
)


# ---------------------------------------------------------
# SEGMENT PIE CHART
# ---------------------------------------------------------

segment_pie = px.pie(
    country_segment_counts,
    names="segment",
    values="buyer_count",
    title=f"Buyer Segment Distribution — {selected_country}",
    hole=0.35
)


segment_pie.update_traces(
    textinfo="percent+label"
)


st.plotly_chart(
    segment_pie,
    use_container_width=True
)


# ---------------------------------------------------------
# SEGMENT BEHAVIOR
# ---------------------------------------------------------

st.subheader(
    f"Segment Behavior in {selected_country}"
)


country_segment_profile = (
    country_data
    .groupby("segment")
    .agg(
        buyers=("client_id", "count"),

        avg_age=("age", "mean"),

        avg_properties=("total_properties", "mean"),

        avg_total_spend=("total_spend", "mean"),

        avg_property_price=(
            "average_property_price",
            "mean"
        ),

        avg_area=(
            "average_area_sqft",
            "mean"
        ),

        investment_rate=(
            "is_investor",
            "mean"
        ),

        loan_rate=(
            "loan_flag",
            "mean"
        ),

        avg_satisfaction=(
            "satisfaction_score",
            "mean"
        )
    )
    .reset_index()
)


# Convert rates to percentages
country_segment_profile["investment_rate"] = (
    country_segment_profile["investment_rate"] * 100
)

country_segment_profile["loan_rate"] = (
    country_segment_profile["loan_rate"] * 100
)


# ---------------------------------------------------------
# FORMAT DISPLAY TABLE
# ---------------------------------------------------------

country_segment_display = (
    country_segment_profile.copy()
)


country_segment_display.columns = [
    "Buyer Segment",
    "Buyers",
    "Average Age",
    "Average Properties",
    "Average Total Spend",
    "Average Property Price",
    "Average Area",
    "Investment Rate",
    "Loan Rate",
    "Average Satisfaction"
]


country_segment_display[
    "Average Age"
] = country_segment_display[
    "Average Age"
].round(1)


country_segment_display[
    "Average Properties"
] = country_segment_display[
    "Average Properties"
].round(2)


country_segment_display[
    "Average Total Spend"
] = country_segment_display[
    "Average Total Spend"
].round(0)


country_segment_display[
    "Average Property Price"
] = country_segment_display[
    "Average Property Price"
].round(0)


country_segment_display[
    "Average Area"
] = country_segment_display[
    "Average Area"
].round(0)


country_segment_display[
    "Investment Rate"
] = country_segment_display[
    "Investment Rate"
].round(1)


country_segment_display[
    "Loan Rate"
] = country_segment_display[
    "Loan Rate"
].round(1)


country_segment_display[
    "Average Satisfaction"
] = country_segment_display[
    "Average Satisfaction"
].round(2)


st.dataframe(
    country_segment_display,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# SPENDING BY SEGMENT
# ---------------------------------------------------------

st.subheader(
    f"Average Spending by Segment — {selected_country}"
)


country_spend_chart = px.bar(
    country_segment_profile,
    x="segment",
    y="avg_total_spend",
    title="Average Total Spend by Buyer Segment",
    text_auto=".2s"
)


country_spend_chart.update_layout(
    xaxis_title="Buyer Segment",
    yaxis_title="Average Total Spend ($)"
)


st.plotly_chart(
    country_spend_chart,
    use_container_width=True
)

# =========================================================
# PROFESSIONAL DASHBOARD SUMMARY / KEY INSIGHTS
# =========================================================

st.header("💡 Professional Dashboard Summary")

st.write(
    "Automatically generated insights based on the "
    "currently selected dashboard filters."
)


# ---------------------------------------------------------
# PREPARE SUMMARY DATA
# ---------------------------------------------------------

summary_data = filtered_data.copy()


# ---------------------------------------------------------
# BASIC SUMMARY METRICS
# ---------------------------------------------------------

summary_total_buyers = len(summary_data)

summary_investment_rate = (
    summary_data["is_investor"].mean() * 100
)

summary_average_spend = (
    summary_data["total_spend"].mean()
)

summary_average_properties = (
    summary_data["total_properties"].mean()
)


# ---------------------------------------------------------
# LARGEST SEGMENT
# ---------------------------------------------------------

summary_segment_counts = (
    summary_data["segment"]
    .value_counts()
)

largest_segment = (
    summary_segment_counts.idxmax()
)

largest_segment_count = (
    summary_segment_counts.max()
)

largest_segment_percentage = (
    largest_segment_count
    / summary_total_buyers
    * 100
)


# ---------------------------------------------------------
# HIGHEST-SPENDING SEGMENT
# ---------------------------------------------------------

summary_segment_spend = (
    summary_data
    .groupby("segment")["total_spend"]
    .mean()
)

highest_spending_segment = (
    summary_segment_spend.idxmax()
)

highest_spending_value = (
    summary_segment_spend.max()
)


# ---------------------------------------------------------
# MOST ACTIVE SEGMENT
# ---------------------------------------------------------

summary_segment_properties = (
    summary_data
    .groupby("segment")["total_properties"]
    .mean()
)

most_active_segment = (
    summary_segment_properties.idxmax()
)

most_active_properties = (
    summary_segment_properties.max()
)


# ---------------------------------------------------------
# LARGEST COUNTRY
# ---------------------------------------------------------

summary_country_counts = (
    summary_data["country"]
    .value_counts()
)

largest_country = (
    summary_country_counts.idxmax()
)

largest_country_count = (
    summary_country_counts.max()
)

largest_country_percentage = (
    largest_country_count
    / summary_total_buyers
    * 100
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

insight_col1, insight_col2, insight_col3 = st.columns(3)


with insight_col1:

    st.metric(
        "👥 Filtered Buyers",
        f"{summary_total_buyers:,}"
    )


with insight_col2:

    st.metric(
        "📈 Investment Rate",
        f"{summary_investment_rate:.1f}%"
    )


with insight_col3:

    st.metric(
        "💰 Average Total Spend",
        f"${summary_average_spend:,.0f}"
    )


# ---------------------------------------------------------
# KEY BUSINESS INDICATORS
# ---------------------------------------------------------

st.subheader("📊 Key Business Indicators")


indicator_col1, indicator_col2 = st.columns(2)


with indicator_col1:

    st.info(
        f"🏆 **Largest Buyer Segment**\n\n"
        f"{largest_segment}\n\n"
        f"{largest_segment_count:,} buyers "
        f"({largest_segment_percentage:.1f}% of the "
        f"filtered population)"
    )


with indicator_col2:

    st.info(
        f"💰 **Highest Average Spending Segment**\n\n"
        f"{highest_spending_segment}\n\n"
        f"Average total spend: "
        f"${highest_spending_value:,.0f}"
    )


indicator_col3, indicator_col4 = st.columns(2)


with indicator_col3:

    st.info(
        f"🏠 **Most Active Segment**\n\n"
        f"{most_active_segment}\n\n"
        f"Average properties purchased: "
        f"{most_active_properties:.2f}"
    )


with indicator_col4:

    st.info(
        f"🌎 **Largest Buyer Country**\n\n"
        f"{largest_country}\n\n"
        f"{largest_country_count:,} buyers "
        f"({largest_country_percentage:.1f}% of the "
        f"filtered population)"
    )


# ---------------------------------------------------------
# AUTOMATIC KEY INSIGHTS
# ---------------------------------------------------------

st.subheader("🔎 Key Insights")


insight_text_1 = (
    f"The largest buyer segment is **{largest_segment}**, "
    f"representing {largest_segment_percentage:.1f}% "
    f"of the currently filtered buyer population."
)


insight_text_2 = (
    f"**{highest_spending_segment}** has the highest "
    f"average total spend at "
    f"${highest_spending_value:,.0f} per buyer."
)


insight_text_3 = (
    f"**{most_active_segment}** shows the highest average "
    f"property activity, with "
    f"{most_active_properties:.2f} properties per buyer."
)


insight_text_4 = (
    f"**{largest_country}** represents the largest "
    f"buyer population in the current filtered dataset, "
    f"with {largest_country_count:,} buyers."
)


insight_text_5 = (
    f"The current filtered population has an overall "
    f"investment rate of {summary_investment_rate:.1f}% "
    f"and average total spend of "
    f"${summary_average_spend:,.0f}."
)


st.markdown(
    f"""
- {insight_text_1}
- {insight_text_2}
- {insight_text_3}
- {insight_text_4}
- {insight_text_5}
"""
)


# ---------------------------------------------------------
# MANAGEMENT INTERPRETATION
# ---------------------------------------------------------

st.subheader("📌 Management Interpretation")

st.write(
    "The dashboard summarizes observable buyer behavior "
    "within the selected population. Segment differences "
    "should be interpreted as descriptive patterns in the "
    "available data rather than causal relationships."
)


st.caption(
    "Insights update automatically when dashboard filters "
    "are changed."
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Real Estate Buyer Segmentation & Investment Profiling | "
    "K-Means based buyer segmentation"
)
