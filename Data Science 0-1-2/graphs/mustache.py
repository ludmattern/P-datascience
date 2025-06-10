import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://lmattern:mysecretpassword@"
                       "localhost:5432/piscineds")

query = """
SELECT price, user_id, user_session
FROM customers
WHERE event_type = 'purchase'
    AND price IS NOT NULL
"""
df = pd.read_sql(query, engine)

desc = df["price"].describe()
q1, q2, q3 = df["price"].quantile([0.25, 0.50, 0.75])

print(f"""
count  {desc["count"]:,.0f}
mean   {desc["mean"]:.6f}
std    {desc["std"]:.6f}
min    {desc["min"]:.6f}
25%    {q1:.6f}
50%    {q2:.6f}
75%    {q3:.6f}
max    {desc["max"]:.6f}
""")


sns.set_style("whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(7, 10), dpi=120)

sns.boxplot(x=df["price"],
            ax=axes[0],
            color="#7ecf7d",
            showfliers=True,
            orient="h",
            flierprops=dict(markersize=1, markerfacecolor="grey"))

axes[0].set_xlabel("price")
axes[0].set_title("Price distribution – with outliers")

sns.boxplot(x=df["price"],
            ax=axes[1],
            color="#7ecf7d",
            showfliers=False)

axes[1].set_xlabel("price")
axes[1].set_title("Price distribution – without outliers")

session_totals = (
    df
    .groupby(["user_id", "user_session"])["price"]
    .sum()
    .rename("basket_total")
)

avg_basket_per_user = (
    session_totals
    .reset_index()
    .groupby("user_id")["basket_total"]
    .mean()
)

sns.boxplot(
    x=avg_basket_per_user,
    ax=axes[2],
    color="#5dade2",
    showfliers=True,
    orient="h",
    flierprops=dict(markersize=1, markerfacecolor="grey")
)
axes[2].set_xlabel("price")
axes[2].set_title("Average basket price per user")
axes[2].set_xlim(-20, 110)


plt.tight_layout()
plt.show()
