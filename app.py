
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

# Revenue + cancellation data
payment_data = filtered_df.groupby(
    ["PaymentMethod", "CouponStatus"],
    as_index=False
).agg(
    revenue=("TotalPrice", "sum"),
    cancellation_rate=("OrderStatus", lambda x: (x == "Cancelled").mean())
)

# Sort payment methods by total revenue
payment_order = payment_data.groupby("PaymentMethod")["revenue"] \
    .sum() \
    .sort_values(ascending=False) \
    .index

payment_data["PaymentMethod"] = pd.Categorical(
    payment_data["PaymentMethod"],
    categories=payment_order,
    ordered=True
)

payment_data = payment_data.sort_values("PaymentMethod")

# Create figure
payment_fig = go.Figure()

# Revenue bars
for coupon in payment_data["CouponStatus"].unique():
    subset = payment_data[payment_data["CouponStatus"] == coupon]
    payment_fig.add_trace(
        go.Bar(
            x=subset["PaymentMethod"],
            y=subset["revenue"],
            name=f"{coupon} Revenue",
            yaxis="y1"
        )
    )

# Cancellation rate lines
for coupon in payment_data["CouponStatus"].unique():
    subset = payment_data[payment_data["CouponStatus"] == coupon]
    payment_fig.add_trace(
        go.Scatter(
            x=subset["PaymentMethod"],
            y=subset["cancellation_rate"],
            mode="lines+markers",
            name=f"{coupon} Cancellation Rate",
            line=dict(dash="dash", width=3),
            yaxis="y2"
        )
    )

# Layout
payment_fig.update_layout(
    title="Revenue & Cancellation Rate by Payment Method and Coupon Usage",
    barmode="group",
    width=850,
    height=450,
    margin=dict(r=220),
    xaxis=dict(title="Payment Method"),
    yaxis=dict(title="Revenue"),
    yaxis2=dict(
        title="Cancellation Rate",
        overlaying="y",
        side="right",
        tickformat=".0%",
        range=[0, 1]
    ),
    legend=dict(x=1.15, y=1, xanchor="left", yanchor="top")
)

st.plotly_chart(payment_fig, use_container_width=False)

insight_box("""
<b>Key Insight:</b><br>
We observe differences in revenue contribution between payment methods depending on coupon usage. This may indicate that discounts affect purchasing behavior differently across payment types.<br>
Additionally, credit card payments generate the highest revenue but also exhibit the highest cancellation rate, indicating potential post-purchase behavior issues.
""")

# Revenue + cancellation data
referral_data = filtered_df.groupby(
    ["ReferralSource", "CouponStatus"],
    as_index=False
).agg(
    revenue=("TotalPrice", "sum"),
    cancellation_rate=("OrderStatus", lambda x: (x == "Cancelled").mean())
)

# Sort Referral Source by total revenue
referral_order = referral_data.groupby("ReferralSource")["revenue"] \
    .sum() \
    .sort_values(ascending=False) \
    .index

referral_data["ReferralSource"] = pd.Categorical(
    referral_data["ReferralSource"],
    categories=referral_order,
    ordered=True
)

referral_data = referral_data.sort_values("ReferralSource")

# Create figure
referral_fig = go.Figure()

# Revenue bars
for coupon in referral_data["CouponStatus"].unique():
    subset = referral_data[referral_data["CouponStatus"] == coupon]
    referral_fig.add_trace(
        go.Bar(
            x=subset["ReferralSource"],
            y=subset["revenue"],
            name=f"{coupon} Revenue",
            yaxis="y1"
        )
    )

# Cancellation rate lines
for coupon in referral_data["CouponStatus"].unique():
    subset = referral_data[referral_data["CouponStatus"] == coupon]
    referral_fig.add_trace(
        go.Scatter(
            x=subset["ReferralSource"],
            y=subset["cancellation_rate"],
            mode="lines+markers",
            name=f"{coupon} Cancellation Rate",
            line=dict(dash="dash", width=3),
            yaxis="y2"
        )
    )

# Layout
referral_fig.update_layout(
    title="Revenue & Cancellation Rate by Referral Source and Coupon Usage",
    barmode="group",
    width=850,
    height=450,
    margin=dict(r=220),    
    xaxis=dict(title="Referral Source"),
    yaxis=dict(title="Revenue"),
    yaxis2=dict(
        title="Cancellation Rate",
        overlaying="y",
        side="right",
        tickformat=".0%",
        range=[0, 1]
    ),
    legend=dict(x=1.15, y=1, xanchor="left", yanchor="top")
)

st.plotly_chart(referral_fig, use_container_width=False)

insight_box("""
<b>Key Insight:</b><br>
Instagram is the leading referral source in terms of order volume, with or without coupon usage, suggesting strong acquisition performance.<br> 
Marketing efforts via Instagram should be further analyzed for customer lifetime value, not only acquisition volume.
""")

# Raw Data
st.header("Raw Data Preview")
st.dataframe(filtered_df.head(50))
