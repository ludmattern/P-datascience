import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://lmattern:mysecretpassword@localhost:5432/piscineds"

CUSTOMER_SEGMENTATION_QUERY = """
WITH analysis_params AS (
    SELECT 
        DATE '2023-03-01' AS reference_date,
        INTERVAL '1 month' AS inactivity_threshold
),
customer_purchase_metrics AS (
    SELECT
        user_id,
        COUNT(DISTINCT DATE_TRUNC('month', event_time)) AS months_with_purchases,
        MIN(DATE_TRUNC('month', event_time)) AS first_purchase_month,
        MAX(DATE_TRUNC('month', event_time)) AS last_purchase_month,
        COUNT(*) AS total_purchases,
        -- Ajout de la date de référence pour les calculs
        (SELECT reference_date FROM analysis_params) AS ref_date,
        (SELECT inactivity_threshold FROM analysis_params) AS inactivity_limit
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id
),
customer_segments AS (
    SELECT
        user_id,
        months_with_purchases,
        first_purchase_month,
        last_purchase_month,
        total_purchases,
        CASE
            -- Clients loyaux (basé sur la récurrence d'achat)
            WHEN months_with_purchases >= 5 THEN 'platinum'
            WHEN months_with_purchases = 4 THEN 'gold'
            WHEN months_with_purchases = 3 THEN 'silver'
            
            -- Clients avec 2 mois d'achat
            WHEN months_with_purchases = 2 THEN 'new'
            
            -- Clients avec 1 seul mois d'achat (distinction actif/inactif)
            WHEN months_with_purchases = 1 AND 
                 last_purchase_month >= DATE_TRUNC('month', ref_date) - inactivity_limit 
                 THEN 'new'
            WHEN months_with_purchases = 1 THEN 'inactive'
            
            -- Cas par défaut (ne devrait pas arriver)
            ELSE 'other'
        END AS customer_segment
    FROM customer_purchase_metrics
)
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(months_with_purchases::NUMERIC), 2) AS avg_months_purchased,
    ROUND(AVG(total_purchases::NUMERIC), 2) AS avg_purchase_frequency
FROM customer_segments
WHERE customer_segment != 'other'
GROUP BY customer_segment
ORDER BY customer_count DESC;
"""


def fetch_customer_data():
    """Retrieves customer segment data from database using SQLAlchemy"""
    engine = create_engine(DATABASE_URL)
    if not engine:
        return None

    df = pd.read_sql_query(text(CUSTOMER_SEGMENTATION_QUERY), engine)

    customer_segments_data = {
        "segment_names": df['customer_segment'].tolist(),
        "customer_counts": df['customer_count'].astype(int).tolist(),
        "avg_months_purchased": df['avg_months_purchased'].astype(float).tolist(),
        "avg_purchase_frequency": df['avg_purchase_frequency'].astype(float).tolist()
    }
    engine.dispose()

    return customer_segments_data



def perform_kmeans_clustering(customer_data, num_clusters=5):
    """Performs K-means clustering on customer data"""

    clustering_features = np.array([[count] for count in customer_data["customer_counts"]])

    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(clustering_features)

    kmeans_model = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    cluster_assignments = kmeans_model.fit_predict(normalized_features)

    cluster_means = []
    for cluster_id in range(num_clusters):
        cluster_indices = [i for i, label in enumerate(cluster_assignments) if label == cluster_id]
        cluster_customer_counts = [customer_data["customer_counts"][i] for i in cluster_indices]
        cluster_means.append(np.mean(cluster_customer_counts))

    sorted_cluster_indices = np.argsort(cluster_means)

    return cluster_assignments, sorted_cluster_indices


def create_clustering_visualization(customer_data):
    """Creates K-means clustering visualization"""

    cluster_assignments, sorted_cluster_indices = perform_kmeans_clustering(customer_data)
    num_clusters = 5

    segment_display_names = {}
    for i, cluster_id in enumerate(sorted_cluster_indices):
        segment_indices = [j for j, assignment in enumerate(cluster_assignments) if assignment == cluster_id]
        if segment_indices:
            segment_idx = segment_indices[0]
            if segment_idx < len(customer_data["segment_names"]):
                segment_display_names[cluster_id] = customer_data["segment_names"][segment_idx]
            else:
                segment_display_names[cluster_id] = f"Segment {i + 1}"
        else:
            segment_display_names[cluster_id] = f"Segment {i + 1}"

    plt.figure(figsize=(12, 8))

    for display_position, cluster_id in enumerate(sorted_cluster_indices):
        cluster_customer_counts = [customer_data["customer_counts"][i] for i in range(len(customer_data["customer_counts"])) if cluster_assignments[i] == cluster_id]

        if cluster_customer_counts:
            avg_customers_in_cluster = np.mean(cluster_customer_counts)
            color = plt.cm.viridis(display_position / num_clusters)

            plt.barh(display_position, avg_customers_in_cluster, color=color, alpha=0.7)

            segment_name = segment_display_names.get(cluster_id, f"Cluster {cluster_id}")
            plt.text(avg_customers_in_cluster + 50, display_position, segment_name)

    plt.ylabel("Customer Clusters (sorted by size)")
    plt.xlabel("Average Number of Customers")
    plt.title("K-means Clustering of Customer Segments")
    plt.yticks(range(num_clusters), [f"Cluster {i + 1}" for i in range(num_clusters)])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def create_scatter_visualization(customer_data):
    segment_names = customer_data["segment_names"]
    customer_counts = customer_data["customer_counts"]
    months_purchased = customer_data["avg_months_purchased"]
    purchase_frequency = customer_data["avg_purchase_frequency"]

    max_customers = max(customer_counts)
    normalized_bubble_sizes = [count / max_customers * 1200 for count in customer_counts]

    colors = plt.cm.tab20(np.linspace(0, 1, len(segment_names)))

    plt.figure(figsize=(12, 8))

    scatter_plots = []
    for i, segment in enumerate(segment_names):
        scatter = plt.scatter(months_purchased[i], purchase_frequency[i], 
                            s=normalized_bubble_sizes[i], c=[colors[i]], 
                            alpha=0.7, edgecolors="black", linewidth=1,
                            label=f"{segment} ({customer_counts[i]} customers)")
        scatter_plots.append(scatter)

    plt.xlabel("Customer Loyalty (Average Months with Purchases)")
    plt.ylabel("Purchase Activity (Average Purchase Frequency)")
    plt.title("Customer Segment Analysis - Bubble Chart")
    plt.grid(True, alpha=0.3)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

    plt.xlim(left=0)
    plt.ylim(bottom=0)

    plt.tight_layout()
    plt.show()

def main():
    """Main function that executes the complete analysis"""

    customer_data = fetch_customer_data()
    if not customer_data:
        return

    create_clustering_visualization(customer_data)
    create_scatter_visualization(customer_data)


if __name__ == "__main__":
    main()
