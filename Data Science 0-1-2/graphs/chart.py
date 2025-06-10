import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("postgresql://lmattern:mysecretpassword@"
                       "localhost:5432/piscineds")

query = """
SELECT
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    category_code,
    brand
FROM customers
WHERE event_type = 'purchase'
    AND event_time >= '2022-09-30'
    AND event_time < '2023-03-01'
    AND price IS NOT NULL
    AND price > 0
ORDER BY event_time
"""

df = pd.read_sql(query, engine)
df["event_time"] = pd.to_datetime(df["event_time"])
df["month"] = df["event_time"].dt.to_period("M")

plt.style.use("default")
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
fig.delaxes(axs[1, 1])
fig.patch.set_facecolor("#f8f9fa")

fig.suptitle("E-commerce Purchase Analysis\nData in Altairian Dollars (Oct 2022 - Feb 2023)", y=0.98)
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]

ax1 = axs[0, 0]
daily_customers = df.groupby(df["event_time"].dt.date)["user_id"].nunique()
ax1.plot(daily_customers.index, daily_customers.values)
ax1.set_ylabel("Number of customers")
ax1.set_title("Unique Customers per Day")
xticks = pd.date_range(df["event_time"].min(),
                       df["event_time"].max(),
                       freq="MS")
ax1.set_xticks(xticks)
ax1.set_xticklabels([d.strftime("%b") for d in xticks])
ax1.grid(True, alpha=0.3)
ax1.set_facecolor("#fafafa")

ax2 = axs[0, 1]
monthly_sales = df.groupby(df["event_time"].dt.to_period("M"))["price"].sum()
months = monthly_sales.index.strftime("%b")
bars = ax2.bar(months, monthly_sales.values / 1_000_000, color=colors[1])

for bar, value in zip(bars, monthly_sales.values / 1_000_000):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.02,
             f"{value:.1f}")

ax2.set_ylabel("total sales in million of ₳")
ax2.set_title("Monthly Revenue")
ax2.grid(True, alpha=0.3, axis="y")
ax2.set_facecolor("#fafafa")

ax3 = axs[1, 0]
daily_avg = df.groupby(df["event_time"].dt.date).apply(lambda x: x["price"].sum() / x["user_id"].nunique())
ax3.fill_between(daily_avg.index, daily_avg.values)
ax3.set_ylabel("average spend/customers in ₳")
ax3.set_title("Average Spend per Customer")
ax3.set_xticks(xticks)
ax3.set_xticklabels([d.strftime("%b") for d in xticks])
ax3.grid(True, alpha=0.3)
ax3.set_facecolor("#fafafa")

for ax in [ax1, ax2, ax3]:
    for spine in ax.spines.values():
        spine.set_color("#cccccc")
        spine.set_linewidth(1)

plt.tight_layout()
plt.subplots_adjust(top=0.85)

plt.show()
