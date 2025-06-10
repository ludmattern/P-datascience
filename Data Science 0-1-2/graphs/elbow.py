import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

engine = create_engine("postgresql://lmattern:mysecretpassword@localhost:5432/piscineds")

query = """
SELECT
    user_id,
    COUNT(*) as total_interactions,
    SUM(price) as total_spent,
    COUNT(DISTINCT event_type) as event_types_count,
    COUNT(DISTINCT product_id) as products_viewed
FROM customers
WHERE user_id IS NOT NULL
GROUP BY user_id
HAVING COUNT(*) > 1
"""

df = pd.read_sql(query, engine)

features = ["total_interactions",
            "total_spent",
            "event_types_count",
            "products_viewed"]
X = df[features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
sns.lineplot(x=list(K_range), y=inertias, marker="o")
plt.xlabel("Number of clusters")
plt.title("The Elbow Method")
plt.show()
