import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def main():
    """Normalise les données Train et affiche le scatter plot Empowered vs Prescience"""
    try:
        df = pd.read_csv("../data/Train_knight.csv")
    except FileNotFoundError:
        return

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    df_std = df.copy()

    normalizer = MinMaxScaler()
    df_std[numeric_columns] = normalizer.fit_transform(df[numeric_columns])

    print(df[numeric_columns].head())
    print(df_std[numeric_columns].head())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    if "knight" in df.columns:
        jedi_data = df_std[df_std["knight"] == "Jedi"]
        sith_data = df_std[df_std["knight"] == "Sith"]

        axes[0].scatter(jedi_data["Empowered"], jedi_data["Prescience"], color="blue", alpha=0.6, s=20, label="Jedi")
        axes[0].scatter(sith_data["Empowered"], sith_data["Prescience"], color="red", alpha=0.6, s=20, label="Sith")
        axes[0].set_xlabel("Empowered (normalized)")
        axes[0].set_ylabel("Prescience (normalized)")
        axes[0].set_title("Train - Empowered vs Prescience (normalized)")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].scatter(jedi_data["Deflection"], jedi_data["Survival"], color="blue", alpha=0.6, s=20, label="Jedi")
        axes[1].scatter(sith_data["Deflection"], sith_data["Survival"], color="red", alpha=0.6, s=20, label="Sith")
        axes[1].set_xlabel("Deflection (normalized)")
        axes[1].set_ylabel("Survival (normalized)")
        axes[1].set_title("Train - Deflection vs Survival (normalized)")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    else:
        axes[0].scatter(df_std["Empowered"], df_std["Prescience"], color="green", alpha=0.6, s=20, label="Knights")
        axes[0].set_xlabel("Empowered (normalized)")
        axes[0].set_ylabel("Prescience (normalized)")
        axes[0].set_title("Test - Empowered vs Prescience (normalized)")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].scatter(df_std["Deflection"], df_std["Survival"], color="green", alpha=0.6, s=20, label="Knights")
        axes[1].set_xlabel("Deflection (normalized)")
        axes[1].set_ylabel("Survival (normalized)")
        axes[1].set_title("Test - Deflection vs Survival (normalized)")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
