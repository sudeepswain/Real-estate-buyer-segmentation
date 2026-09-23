import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.express as px


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Real Estate Buyer Segmentation",
    page_icon="🏠",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🏠 Real Estate Buyer Segmentation & Investment Profiling")

st.write(
    "Interactive dashboard for analyzing buyer segments, "
    "investment behavior, spending patterns, and geographic distribution."
)


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

st.header("🌍 Interactive World Map")

st.write(
    "Explore the distribution of buyers across countries. "
    "Use the selector below to change the metric displayed on the map."
)

# Country name to ISO-3 country code
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

# Create country-level summary
country_summary = (
    buyer_data
    .groupby("country")
    .agg(
        buyer_count=("client_id", "count"),
        avg_total_spend=("total_spend", "mean"),
        avg_property_price=("average_property_price", "mean"),
        avg_properties=("total_properties", "mean"),
        avg_satisfaction=("satisfaction_score", "mean")
    )
    .reset_index()
)

# Add ISO country codes
country_summary["iso_code"] = (
    country_summary["country"].map(country_codes)
)

# Map metric selector
map_metric = st.selectbox(
    "Select map metric",
    [
        "Number of Buyers",
        "Average Total Spend",
        "Average Property Price",
        "Average Properties",
        "Average Satisfaction"
    ]
)

# Match the selected option to a dataframe column
metric_mapping = {
    "Number of Buyers": "buyer_count",
    "Average Total Spend": "avg_total_spend",
    "Average Property Price": "avg_property_price",
    "Average Properties": "avg_properties",
    "Average Satisfaction": "avg_satisfaction"
}

selected_metric = metric_mapping[map_metric]

# Create interactive world map
fig_map = px.choropleth(
    country_summary,
    locations="iso_code",
    color=selected_metric,
    hover_name="country",
    locationmode="ISO-3",
    projection="natural earth",
    color_continuous_scale="Blues"
)

# Map appearance
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

# Display map
st.plotly_chart(
    fig_map,
    use_container_width=True
)


# Country summary table
st.subheader("Country-Level Summary")

country_display = country_summary[
    [
        "country",
        "buyer_count",
        "avg_total_spend",
        "avg_property_price",
        "avg_properties",
        "avg_satisfaction"
    ]
].copy()

country_display.columns = [
    "Country",
    "Buyers",
    "Average Total Spend",
    "Average Property Price",
    "Average Properties",
    "Average Satisfaction"
]

st.dataframe(
    country_display,
    use_container_width=True,
    hide_index=True
)
# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Real Estate Buyer Segmentation & Investment Profiling | "
    "K-Means based buyer segmentation"
)
