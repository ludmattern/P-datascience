import pandas as pd
import numpy as np


def calculate_correlations():
    """
    Calculate correlation factors between the target column 'knight' and all other features.
    Returns correlations sorted by absolute value in descending order.
    """
    df = pd.read_csv("../data/Train_knight.csv")

    df["knight"] = df["knight"].map({"Jedi": 1, "Sith": 0})
    
    correlations = df.corr()["knight"]
    correlations_sorted = correlations.sort_values(ascending=False)

    return correlations_sorted


def print_correlations():
    """
    Print correlation factors in the required format.
    """
    correlations = calculate_correlations()

    for feature, correlation in correlations.items():
        print(f"{feature} {correlation:.6f}")


if __name__ == "__main__":
    print_correlations()
