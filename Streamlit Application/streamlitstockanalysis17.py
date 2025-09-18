import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import altair as alt


# Connect to TiDB
#TiDB connection details
user = "3LBRyXkYRgoP1FS.root"
password = "fwJACxECJe0b7ZlM"
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
port = 4000
database = "Stock_Analysis"

# SSL CA certificate path (downloaded from TiDB Cloud)
ssl_ca_path = "C:/Users/pavit/ca.pem"

# Create connection engine
connection_string = (
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?ssl_ca={ssl_ca_path}"
)
engine = create_engine(connection_string)

# Load data from TiDB
@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM stocks_with_sector"
    df = pd.read_sql(query, engine, parse_dates=["date"])
    return df

df = load_data()




# ---------- Dashboard UI ----------
st.set_page_config(page_title="📈 Stock Analysis Dashboard", layout="wide")

st.title("📊 Stock Analysis Dashboard")
st.markdown(
    "Welcome to the **Stock Analysis Dashboard**. "
    "Use the filters and charts (coming next) to explore stock performance by sector, ticker, and month."
)

# ---------- Key Metrics ----------
total_tickers = df["ticker"].nunique()
total_sectors = df["sector"].nunique()
total_rows = len(df)
avg_return = df["daily_return"].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("💹 Total Stocks", total_tickers)
col2.metric("🏢 Total Sectors", total_sectors)
col3.metric("📁 Total Records", total_rows)
col4.metric("📈 Avg Daily Return", f"{avg_return:.2f}%")

st.markdown(
    '<hr style="height:3px; border:none; color:#333; background-color:#333;" />',
    unsafe_allow_html=True
)

# Sidebar month filter
st.sidebar.header("📂 Stock Analysis Filters")
available_months = sorted(df["month"].unique())
selected_month = st.sidebar.selectbox("Select Month", available_months)

# Filter data for selected month
filtered_df = df[df["month"] == selected_month]

# Calculate average return per stock for this month
avg_return_per_stock = (
    filtered_df.groupby("ticker")["daily_return"]
    .mean()
    .reset_index()
)

# Calculate overall metrics
green_count = (avg_return_per_stock["daily_return"] > 0).sum()
red_count   = (avg_return_per_stock["daily_return"] < 0).sum()
total_count = len(avg_return_per_stock)

green_percent = (green_count / total_count) * 100 if total_count else 0
red_percent   = (red_count / total_count) * 100 if total_count else 0
avg_return    = filtered_df["daily_return"].mean()

# --- Display metrics ---

st.subheader(f"📈 Market Summary — {selected_month}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Daily Return", value=f"{avg_return:.2%}")

with col2:
    st.metric(label="Green Stocks (%)", value=f"{green_percent:.1f}%")

with col3:
    st.metric(label="Red Stocks (%)", value=f"{red_percent:.1f}%")
    


# --- Individual stock selector in a box ---
st.markdown(
    '<hr style="height:3px; border:none; color:#333; background-color:#333;" />',
    unsafe_allow_html=True
)
with st.container():
    st.subheader("📍 Check a Specific Stock")
    
    col1, col2 = st.columns([2, 1])  # dropdown and metric side by side

    with col1:
        selected_stock = st.selectbox(
            "Choose a Stock",
            sorted(filtered_df["ticker"].unique())
        )

    with col2:
        if selected_stock:
            stock_avg = filtered_df[
                filtered_df["ticker"] == selected_stock
            ]["daily_return"].mean()
            # Color metric based on positive/negative
            if stock_avg >= 0:
                value_display = f"🟢 {stock_avg:.2%}"
            else:
                value_display = f"🔴 {stock_avg:.2%}"
            st.metric(
                label=f"{selected_stock} Avg Return",
                value=value_display
            )

st.markdown("---")

#Stock performance summary

# --- Calculate average yearly return per stock ---
daily = df.copy()
daily["daily_return"] = daily["daily_return"].astype(float)

yearly_returns = daily.groupby("ticker")["daily_return"].mean().reset_index()
yearly_returns.columns = ["ticker", "avg_daily_return"]

# --- Classify stocks ---
# Positive avg return → growth, negative avg return → decline
growth_stocks = yearly_returns[yearly_returns["avg_daily_return"] > 0]
decline_stocks = yearly_returns[yearly_returns["avg_daily_return"] < 0]

# --- Display in dashboard ---
st.subheader("🚀 Stock Performance Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Consistent Growth Stocks (Positive Avg Return)**: {len(growth_stocks)}")
    st.dataframe(
        growth_stocks.sort_values("avg_daily_return", ascending=False)
        .style.format({"avg_daily_return": "{:.2%}"})
    )

with col2:
    st.markdown(f"**Significant Decline Stocks (Negative Avg Return)**: {len(decline_stocks)}")
    st.dataframe(
        decline_stocks.sort_values("avg_daily_return")
        .style.format({"avg_daily_return": "{:.2%}"})
    )




# --- Calculate yearly return per stock ---
daily = df.copy()
daily["daily_return"] = daily["daily_return"].astype(float)

grouped = daily.groupby("ticker")["daily_return"]
yearly_returns = grouped.apply(
    lambda x: (np.prod(1 + x) ** (252 / len(x)) - 1) * 100
).reset_index(name="yearly_return")

# --- Top 10 Green Stocks ---
top10_green = yearly_returns.sort_values(by="yearly_return", ascending=False).head(10)

# --- Side by side layout ---
st.subheader("💹 Top 10 Green Stocks (Yearly Return)")
col1, col2 = st.columns([2, 1])  # Wider for chart, narrower for table

with col1:
    chart = (
        alt.Chart(top10_green)
        .mark_bar()
        .encode(
            x=alt.X("ticker:N", sort="-y"),
            y=alt.Y("yearly_return:Q", title="Yearly Return (%)"),
            tooltip=["ticker", "yearly_return"]
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    # Display table without extra subheader to align it with chart
    st.dataframe(top10_green.style.format({"yearly_return": "{:.2f}%"}))
    
# --- Top 10 Loss Stocks ---
top10_loss = yearly_returns.sort_values(by="yearly_return", ascending=True).head(10)

# --- Side by side layout ---
st.subheader("📉 Top 10 Loss Stocks (Yearly Return)")
col1, col2 = st.columns([2, 1])  # Wider for chart, narrower for table

with col1:
    chart = (
        alt.Chart(top10_loss)
        .mark_bar(color="red")
        .encode(
            x=alt.X("ticker:N", sort="y"),
            y=alt.Y("yearly_return:Q", title="Yearly Return (%)"),
            tooltip=["ticker", "yearly_return"]
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    # Table aligned with chart
    st.dataframe(top10_loss.style.format({"yearly_return": "{:.2f}%"}))

# --- Calculate volatility per stock ---
volatility_df = df.groupby("ticker")["daily_return"].std().reset_index()
volatility_df.columns = ["ticker", "volatility"]

# --- Top 10 Most Volatile Stocks ---
top10_volatile = volatility_df.sort_values(by="volatility", ascending=False).head(10)

# --- Side by side layout ---
st.subheader("⚡ Top 10 Most Volatile Stocks (Past Year)")
col1, col2 = st.columns([2, 1])  # Wider for chart, narrower for table

with col1:
    chart = (
        alt.Chart(top10_volatile)
        .mark_bar(color="orange")
        .encode(
            x=alt.X("ticker:N", sort="-y"),
            y=alt.Y("volatility:Q", title="Volatility (Std Dev of Daily Returns)"),
            tooltip=["ticker", "volatility"]
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.dataframe(top10_volatile.style.format({"volatility": "{:.4f}"}))

# --- Sidebar filter ---
sectors = df["sector"].dropna().unique()
selected_sector = st.sidebar.selectbox("Select Sector", ["All"] + list(sectors))

if selected_sector != "All":
    filtered_df = df[df["sector"] == selected_sector]
else:
    filtered_df = df
    

# --- Calculate yearly volatility for each stock ---
volatility_df = (
    df.groupby("ticker")["daily_return"]
    .std()
    .reset_index()
)
volatility_df.columns = ["ticker", "volatility"]

# --- Sort and pick top 10 ---
top_10_volatility = volatility_df.sort_values("volatility", ascending=False).head(10)


# --- Filter DataFrame ---
filtered_df = df.copy()
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["sector"] == selected_sector]


# --- Calculate volatility ---
volatility_df = filtered_df.groupby("ticker")["daily_return"].std().reset_index()
volatility_df.columns = ["ticker", "volatility"]

# --- Top 10 or all based on filter ---
top_volatility = volatility_df.sort_values(by="volatility", ascending=False).head(10)

# --- Side by side layout ---
st.subheader("📊 Interactive Stock Volatility")
col1, col2 = st.columns([2, 1])

with col1:
    chart = (
        alt.Chart(top_volatility)
        .mark_bar(color="orange")
        .encode(
            x=alt.X("ticker:N", sort="-y"),
            y=alt.Y("volatility:Q", title="Volatility (Std Dev of Daily Returns)"),
            tooltip=["ticker", "volatility"]
        )
        .interactive()  # enables zoom & pan
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.dataframe(top_volatility.style.format({"volatility": "{:.4f}"}))
    
st.markdown(
    '<hr style="height:3px; border:none; color:#333; background-color:#333;" />',
    unsafe_allow_html=True
)

#CUMULATIVE RETURN

# --- Prepare data ---
df["daily_return"] = df["daily_return"].astype(float)
df["date"] = pd.to_datetime(df["date"])

# Sort by ticker and date
df_sorted = df.sort_values(["ticker", "date"])

# Calculate cumulative return per stock using transform (avoids index mismatch)
df_sorted["cumulative_return"] = df_sorted.groupby("ticker")["daily_return"].transform(lambda x: (1 + x).cumprod() - 1)

# --- Identify Top 5 Performing Stocks based on final cumulative return ---
final_cum_return = df_sorted.groupby("ticker").agg(final_return=("cumulative_return", "last")).reset_index()
top5_stocks = final_cum_return.sort_values("final_return", ascending=False).head(5)["ticker"].tolist()

# Filter data for top 5 stocks
top5_df = df_sorted[df_sorted["ticker"].isin(top5_stocks)]

# --- Side by side layout ---
st.subheader("📈 Top 5 Performing Stocks Over the Year Based on Cumulative return")
col1, col2 = st.columns([2, 1])  # Wider for chart, narrower for table

with col1:
    # Line chart of cumulative return over time
    line_chart = (
        alt.Chart(top5_df)
        .mark_line(point=True)
        .encode(
            x="date:T",
            y=alt.Y("cumulative_return:Q", title="Cumulative Return"),
            color="ticker:N",
            tooltip=["ticker", "date", alt.Tooltip("cumulative_return:Q", format=".2%")]
        )
        .interactive()  # enables zoom & pan
        .properties(height=400)
    )
    st.altair_chart(line_chart, use_container_width=True)

with col2:
    # Table of top 5 stocks with final cumulative return
    table_df = final_cum_return[final_cum_return["ticker"].isin(top5_stocks)]
    table_df = table_df.sort_values("final_return", ascending=False)
    st.dataframe(table_df.style.format({"final_return": "{:.2%}"}))
    
st.markdown(
    '<hr style="height:3px; border:none; color:#333; background-color:#333;" />',
    unsafe_allow_html=True
)
    

#SECTOR WISE PERFORMANCE

# --- Prepare data ---
df["daily_return"] = df["daily_return"].astype(float)

# Calculate cumulative return per stock for the year
cumulative_return = df.groupby("ticker")["daily_return"].apply(lambda x: (1 + x).prod() - 1).reset_index()
cumulative_return.columns = ["ticker", "yearly_return"]

# Merge with sector information
sector_return = cumulative_return.merge(df[["ticker", "sector"]].drop_duplicates(), on="ticker")

# Calculate average yearly return per sector
avg_sector_return = sector_return.groupby("sector")["yearly_return"].mean().reset_index()

# --- Side by side layout ---
st.subheader("🏢 Average Yearly Return by Sector")
col1, col2 = st.columns([2, 1])  # Wider for chart, narrower for table

with col1:
    # Bar chart
    sector_chart = (
        alt.Chart(avg_sector_return)
        .mark_bar(color="steelblue")
        .encode(
            x=alt.X("sector:N", sort="-y", title="Sector"),
            y=alt.Y("yearly_return:Q", title="Average Yearly Return"),
            tooltip=["sector", alt.Tooltip("yearly_return:Q", format=".2%")]
        )
        .properties(height=400)
    )
    st.altair_chart(sector_chart, use_container_width=True)

with col2:
    # Table of sector average yearly returns
    st.dataframe(
        avg_sector_return.sort_values("yearly_return", ascending=False)
        .style.format({"yearly_return": "{:.2%}"})
    )

st.markdown(
    '<hr style="height:3px; border:none; color:#333; background-color:#333;" />',
    unsafe_allow_html=True
)

#Correlation heat map
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- Prepare data ---
# Pivot the data: rows = date, columns = ticker, values = closing price
price_df = df.pivot(index="date", columns="ticker", values="close")

# Calculate correlation matrix
corr_matrix = price_df.corr()

# --- Plot heatmap ---
st.subheader("📊 Stock Price Correlation Heatmap")

plt.figure(figsize=(12, 8))
sns.heatmap(
    corr_matrix,
    annot=False,       # Remove numeric labels
    cmap="coolwarm",   # Blue = low, Red = high correlation
    linewidths=0.5
)
plt.title("Correlation Between Stock Closing Prices", fontsize=16)

st.pyplot(plt.gcf())  # Display the plot in Streamlit
plt.clf()  # Clear figure after displaying


st.markdown(
    "**This heatmap shows how closely the closing prices of different stocks move together. "
    "Darker red indicates higher positive correlation, while darker blue indicates lower or negative correlation."
)

st.markdown(
    '<hr style="height:3px; border:none; color:#333; background-color:#333;" />',
    unsafe_allow_html=True
)

#MONTH WISE TOP PERFORMERS

# --- Prepare data ---
df["daily_return"] = df["daily_return"].astype(float)
df["date"] = pd.to_datetime(df["date"])
df["month_name"] = df["date"].dt.strftime('%B')  # e.g., 'January'

# --- Calculate monthly return per stock ---
monthly_return = (
    df.groupby(["month_name", "ticker"])["daily_return"]
    .apply(lambda x: (np.prod(1 + x) - 1) * 100)  # percentage return
    .reset_index(name="monthly_return")
)

# Sort months in calendar order
months_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
monthly_return["month_name"] = pd.Categorical(monthly_return["month_name"], categories=months_order, ordered=True)
monthly_return = monthly_return.sort_values("month_name")

# --- Display bar charts for each month ---
st.subheader("📊 Monthly Top 5 Gainers and Losers")

for month in months_order:
    st.markdown(f"### {month}")
    month_df = monthly_return[monthly_return["month_name"] == month]
    
    # Top 5 gainers
    top5_gainers = month_df.sort_values("monthly_return", ascending=False).head(5)
    # Top 5 losers
    top5_losers = month_df.sort_values("monthly_return").head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top 5 Gainers**")
        chart_gainers = (
            alt.Chart(top5_gainers)
            .mark_bar(color="green")
            .encode(
                x=alt.X("ticker:N", sort="-y"),
                y=alt.Y("monthly_return:Q", title="Return (%)"),
                tooltip=["ticker", alt.Tooltip("monthly_return:Q", format=".2f")]
            )
            .properties(height=300)
        )
        st.altair_chart(chart_gainers, use_container_width=True)
    
    with col2:
        st.markdown("**Top 5 Losers**")
        chart_losers = (
            alt.Chart(top5_losers)
            .mark_bar(color="red")
            .encode(
                x=alt.X("ticker:N", sort="y"),
                y=alt.Y("monthly_return:Q", title="Return (%)"),
                tooltip=["ticker", alt.Tooltip("monthly_return:Q", format=".2f")]
            )
            .properties(height=300)
        )
        st.altair_chart(chart_losers, use_container_width=True)



    



