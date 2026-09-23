
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Real Estate Buyer Segmentation",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Real Estate Buyer Segmentation & Investment Profiling")

st.write(
    "Interactive dashboard for analyzing buyer segments, "
    "investment behavior, spending patterns, and geographic distribution."
)

# Load public datasets
buyer_data = pd.read_csv("data/buyer_segments_public.csv")
segment_profile = pd.read_csv("outputs/segment_profile.csv")

st.success("Data loaded successfully!")

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Buyers", len(buyer_data))

with col2:
    st.metric("Buyer Segments", buyer_data["segment"].nunique())

with col3:
    st.metric("Countries", buyer_data["country"].nunique())

st.subheader("Buyer Segment Profile")

st.dataframe(
    segment_profile,
    use_container_width=True
)
