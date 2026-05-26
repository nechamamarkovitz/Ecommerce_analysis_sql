
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

df = pd.read_csv("E_Commerce_Orders.csv") 

st.title("📊 E-commerce Orders Analysis Dashboard")

st.sidebar.header("Filters")

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df["PaymentMethod"].unique(),
    default=df["PaymentMethod"].unique()
)

referral_filter = st.sidebar.multiselect(
    "Referral Source",
    options=df["ReferralSource"].unique(),
    default=df["ReferralSource"].unique()
)

# Coupon logic
df["CouponStatus"] = df["CouponCode"].apply(
    lambda x: "No Coupon" if pd.isna(x) or x == "" else "Coupon Used"
)

coupon_filter = st.sidebar.multiselect(
    "Coupon Status",
    options=df["CouponStatus"].unique(),
    default=df["CouponStatus"].unique()
)

# Filtered Data
filtered_df = df[
    (df["PaymentMethod"].isin(payment_filter)) &
    (df["ReferralSource"].isin(referral_filter)) &
    (df["CouponStatus"].isin(coupon_filter))
]

# KPIs
st.header("Key Metrics")

col1, col2, col3 = st.columns(3)

total_revenue = filtered_df["TotalPrice"].sum()
total_orders = filtered_df.shape[0]
cancellation_rate = (filtered_df["OrderStatus"] == "Cancelled").mean()

col1.metric("Revenue", f"{total_revenue:,.0f}")
col2.metric("Orders", total_orders)
col3.metric("Cancellation Rate", f"{cancellation_rate:.2%}")

# Revenue by Payment Method
st.header("Revenue by Payment Method")

payment_fig = px.bar(
    filtered_df.groupby("PaymentMethod", as_index=False)["TotalPrice"].sum(),
    x="PaymentMethod",
    y="TotalPrice"
)

st.plotly_chart(payment_fig, use_container_width=False)

# Referral Source Analysis
st.header("Revenue by Referral Source")

ref_fig = px.bar(
    filtered_df.groupby("ReferralSource", as_index=False)["TotalPrice"].sum(),
    x="ReferralSource",
    y="TotalPrice"
)

st.plotly_chart(ref_fig, use_container_width=False)

# Coupon Impact
st.header("Coupon Impact")

coupon_fig = px.bar(
    filtered_df.groupby("CouponStatus", as_index=False)["TotalPrice"].sum(),
    x="CouponStatus",
    y="TotalPrice"
)

st.plotly_chart(coupon_fig, use_container_width=False)
    
# Raw Data
st.header("Raw Data Preview")
st.dataframe(filtered_df.head(50))
