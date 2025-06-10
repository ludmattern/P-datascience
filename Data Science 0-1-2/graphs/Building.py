import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("postgresql://lmattern:mysecretpassword@"
                       "localhost:5432/piscineds")

query1 = """
SELECT user_id, COUNT(*) as nb_achats
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id
"""
df_achats = pd.read_sql(query1, engine)

query2 = """
SELECT user_id, SUM(price) as montant_total
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id
"""
df_montant = pd.read_sql(query2, engine)

quartiles_achats = df_achats["nb_achats"].quantile([0, 0.25, 0.5,
                                                    0.75, 1.0])
quartiles_montant = df_montant["montant_total"].quantile([0, 0.25, 0.5,
                                                          0.75, 1.0])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

achats_capped = df_achats["nb_achats"].clip(upper=50)
ax1.hist(achats_capped, bins=5, range=(0, 50),
         edgecolor="white", linewidth=1)
ax1.set_xlabel("frequency")
ax1.set_ylabel("customers")
ax1.grid(True, alpha=0.3)

montant_capped = df_montant["montant_total"].clip(upper=200)
ax2.hist(montant_capped, bins=5, range=(0, 200),
         edgecolor="white", linewidth=1)
ax2.set_xlabel("monetary value in ₳")
ax2.set_ylabel("customers")
ax2.set_xticks([0, 40, 80, 120, 160, 200])
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
