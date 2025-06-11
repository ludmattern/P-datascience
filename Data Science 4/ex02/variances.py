import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def load_data(file_path):
    """Load data from CSV file"""
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def prepare_data(data):
    """Prepare data by removing non-numeric columns and standardizing"""
    numeric_data = data.select_dtypes(include=[np.number])

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)

    return scaled_data, numeric_data.columns


def calculate_variances(data):
    """Calculate variance explained by each principal component"""
    pca = PCA()
    pca.fit(data)

    variances = pca.explained_variance_ratio_ * 100

    cumulative_variances = np.cumsum(variances)

    return variances, cumulative_variances


def find_components_for_threshold(cumulative_variances, threshold=90):
    """Find number of components needed to reach the threshold"""
    components_needed = np.where(cumulative_variances >= threshold)[0]
    if len(components_needed) > 0:
        return components_needed[0] + 1
    else:
        return len(cumulative_variances)


def plot_variances(variances, cumulative_variances, components_90):
    """Plot the variance analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.bar(range(1, len(variances) + 1), variances, alpha=0.7, color="skyblue")
    ax1.set_xlabel("Principal Component")
    ax1.set_ylabel("Variance Explained (%)")
    ax1.set_title("Individual Variance Explained by Each Component")
    ax1.grid(True, alpha=0.3)

    ax2.plot(range(1, len(cumulative_variances) + 1), cumulative_variances, "o-", color="orange", linewidth=2, markersize=4)
    ax2.axhline(y=90, color="red", linestyle="--", alpha=0.7, label="90% threshold")
    ax2.axvline(x=components_90, color="red", linestyle="--", alpha=0.7, label=f"{components_90} components")
    ax2.set_xlabel("Number of Components")
    ax2.set_ylabel("Cumulative Variance Explained (%)")
    ax2.set_title("Cumulative Variance Explained")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.show()


def main():
    """Main function to execute the variance analysis"""
    data = load_data("../data/Train_knight.csv")
    if data is None:
        return

    scaled_data, feature_names = prepare_data(data)

    variances, cumulative_variances = calculate_variances(scaled_data)

    components_90 = find_components_for_threshold(cumulative_variances, 90)

    print("Variances (Percentage):")
    print(variances)
    print("\nCumulative Variances (Percentage):")
    print(cumulative_variances)
    print(f"\n{components_90}")

    plot_variances(variances, cumulative_variances, components_90)


if __name__ == "__main__":
    main()
