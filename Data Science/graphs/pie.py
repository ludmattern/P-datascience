import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("postgresql://lmattern:mysecretpassword@"
                       "localhost:5432/piscineds")

query = """
SELECT event_type,COUNT(*) as count
FROM customers
GROUP BY event_type
ORDER BY count DESC
"""
df = pd.read_sql(query, engine)

plt.style.use("default")
fig, ax = plt.subplots(figsize=(12, 10))
fig.patch.set_facecolor("#f8f9fa")

colors = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#98D8C8"
]
explode = [0.05 if i == 0 else 0.02 for i in range(len(df))]

wedges, texts, autotexts = ax.pie(
    df["count"],
    labels=df["event_type"].astype(str),
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    explode=explode,
    shadow=True,
    wedgeprops=dict(width=0.7, edgecolor="white", linewidth=2),
    textprops={"fontsize": 11, "fontweight": "bold"},
    pctdistance=0.85
)

for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

for text in texts:
    text.set_fontsize(12)
    text.set_fontweight("bold")
    text.set_color("#2c3e50")

ax.set_title(
    "User Behavior Analysis on E-commerce Site\n"
    "Interaction Analysis (Oct 2022 - Feb 2023)",
    fontsize=16, fontweight="bold", color="#2c3e50", pad=30
)

centre_circle = plt.Circle(
    (0, 0), 0.40, fc="white", edgecolor="#ecf0f1", linewidth=3
)
fig.gca().add_artist(centre_circle)

ax.legend(
    wedges,
    [f"{label}\n({count:,} interactions)"
     for label, count in zip(df["event_type"], df["count"])],
    title="Event Types",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=10,
    title_fontsize=12,
    frameon=True,
    fancybox=True,
    shadow=True
)

total_interactions = df["count"].sum()
ax.text(
    0, 0,
    f"Total\n{total_interactions:,}\ninteractions",
    horizontalalignment="center",
    verticalalignment="center",
    fontsize=14,
    fontweight="bold",
    color="#2c3e50"
)

plt.tight_layout()
plt.axis("equal")

plt.show()
