import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
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

    scaled_df = pd.DataFrame(scaled_data, columns=numeric_data.columns)

    return scaled_df


def calculate_vif(data):
    """Calculate VIF for each feature"""
    vif_data = pd.DataFrame()
    vif_data["Feature"] = data.columns
    vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
    vif_data["Tolerance"] = 1 / vif_data["VIF"]

    return vif_data


def remove_high_vif_features(data, threshold=5):
    """Remove features with VIF > threshold iteratively"""
    current_data = data.copy()
    removed_features = []
    iteration = 0

    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")

        vif_df = calculate_vif(current_data)
        vif_df = vif_df.sort_values("VIF", ascending=False)

        print(f"Current features: {len(current_data.columns)}")
        print("VIF values:")
        print(vif_df.to_string(index=False))

        max_vif = vif_df["VIF"].max()
        if max_vif <= threshold:
            print(f"\nAll VIF values are <= {threshold}. Feature selection complete!")
            break

        feature_to_remove = vif_df.iloc[0]["Feature"]
        removed_features.append(feature_to_remove)
        current_data = current_data.drop(columns=[feature_to_remove])

        print(f"Removed feature: {feature_to_remove} (VIF: {vif_df.iloc[0]['VIF']:.6f})")

        if len(current_data.columns) <= 1:
            print("Warning: Only one feature remaining!")
            break

    return current_data, removed_features, vif_df


def display_final_results(final_data, removed_features, final_vif):
    """Display the final results"""
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    print(f"\nRemoved features ({len(removed_features)}):")
    for i, feature in enumerate(removed_features, 1):
        print(f"{i:2d}. {feature}")

    print(f"\nKept features ({len(final_data.columns)}):")
    for i, feature in enumerate(final_data.columns, 1):
        print(f"{i:2d}. {feature}")

    print(f"\nFinal VIF values (all <= 5):")
    print(final_vif.to_string(index=False))


def main():
    """Main function to execute the feature selection"""
    data = load_data("../data/Train_knight.csv")
    if data is None:
        return

    print("Original dataset shape:", data.shape)
    print("Original features:", list(data.columns))

    prepared_data = prepare_data(data)
    print(f"\nNumeric features: {len(prepared_data.columns)}")

    print("\n" + "=" * 60)
    print("INITIAL VIF CALCULATION")
    print("=" * 60)

    initial_vif = calculate_vif(prepared_data)
    initial_vif = initial_vif.sort_values("VIF", ascending=False)
    print(initial_vif.to_string(index=False))

    print("\n" + "=" * 60)
    print("FEATURE SELECTION PROCESS")
    print("=" * 60)

    final_data, removed_features, final_vif = remove_high_vif_features(prepared_data, threshold=5)

    display_final_results(final_data, removed_features, final_vif)


if __name__ == "__main__":
    main()
