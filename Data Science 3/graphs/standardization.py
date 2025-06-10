import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def main():
    """Standardise les données Train et affiche le scatter plot Empowered vs Prescience"""
    try:
        df = pd.read_csv("../data/Test_knight.csv")
    except FileNotFoundError:
        return

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    df_std = df.copy()

    scaler = StandardScaler()
    df_std[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    print(df[numeric_columns].head())
    print(df_std[numeric_columns].head())

    fig, ax = plt.subplots(figsize=(8, 6))

    if "knight" in df.columns:
        jedi_data = df_std[df_std["knight"] == "Jedi"]
        sith_data = df_std[df_std["knight"] == "Sith"]
        ax.scatter(jedi_data["Empowered"], jedi_data["Prescience"], color="blue", alpha=0.6, s=20, label="Jedi")
        ax.scatter(sith_data["Empowered"], sith_data["Prescience"], color="red", alpha=0.6, s=20, label="Sith")
    else:
        ax.scatter(df_std["Empowered"], df_std["Prescience"], color="green", alpha=0.6, s=20, label="Knights")

    ax.set_xlabel("Empowered (standardized)")
    ax.set_ylabel("Prescience (standardized)")
    title = "Train - Empowered vs Prescience" if "knight" in df.columns else "Test - Empowered vs Prescience"
    ax.set_title(f"{title} (Standardized)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
