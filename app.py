
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

df = pd.read_csv("E_Commerce_Orders.csv") 

st.title("E-commerce Orders Analysis Dashboard")

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

# Filtered Data
filtered_df = df[
    (df["PaymentMethod"].isin(payment_filter)) &
    (df["ReferralSource"].isin(referral_filter)) 
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

def insight_box(text):
    st.markdown(
        f"""
        <div style="
            padding: 12px;
            background-color: #f4f6f8;
            border-left: 5px solid #4CAF50;
            border-radius: 8px;
            margin-bottom: 15px;
        ">
        {text}
        """,
        unsafe_allow_html=True
    )

# Revenue by Payment Method & copons
    
st.header("Revenue by Payment Method & Coupon Usage")

payment_data = filtered_df.groupby(
    ["PaymentMethod", "CouponStatus"],
    as_index=False
).agg(
    revenue=("TotalPrice", "sum"),
    cancellation_rate=("OrderStatus", lambda x: (x == "Cancelled").mean())
)

payment_order = payment_data.groupby("PaymentMethod")["revenue"] \
    .sum() \
    .sort_values(ascending=False) \
    .index

payment_fig = px.bar(
    payment_data,
    x="PaymentMethod",
    y="revenue",
    color="CouponStatus",
    barmode="group",
)

st.plotly_chart(payment_fig, use_container_width=False)

insight_box("""
<b>Key Insight:</b><br>
We observe differences in revenue contribution between payment methods depending on coupon usage.<br>
This may indicate that discounts affect purchasing behavior differently across payment types.<br>
in adission, it can be seen that credit card payments generate the highest revenue, ut in another analysis it exhibit the highest cancellation rate, indicating potential post purchase behavior issues.
""")

# Referral Source Analysis
st.header("Revenue by Referral Source & Coupon Usage")

ref_data = filtered_df.groupby(
    ["ReferralSource", "CouponStatus"],
    as_index=False
)["TotalPrice"].sum()

ref_fig = px.bar(
    ref_data,
    x="ReferralSource",
    y="TotalPrice",
    color="CouponStatus",
    barmode="group",
)

st.plotly_chart(ref_fig, use_container_width=False)

insight_box("""
<b>Key Insight:</b><br>
Instagram is the leading referral source in terms of order volume, with or without coupon usage, suggesting strong acquisition performance.<br> 
Marketing efforts via Instagram should be further analyzed for customer lifetime value, not only acquisition volume.
""")

# Raw Data
st.header("Raw Data Preview")
st.dataframe(filtered_df.head(50))
