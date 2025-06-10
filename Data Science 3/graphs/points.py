import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    try:
        df = pd.read_csv("../data/Test_knight.csv")
        return df
    except FileNotFoundError:
        return None
    except Exception:
        return None


def load_train_data():
    try:
        df = pd.read_csv("../data/Train_knight.csv")
        return df
    except FileNotFoundError:
        return None
    except Exception:
        return None


def create_scatter_plot(ax, df, x_col, y_col, title, has_knight_col=False):
    if has_knight_col and "knight" in df.columns:
        jedi_data = df[df["knight"] == "Jedi"]
        sith_data = df[df["knight"] == "Sith"]
        ax.scatter(jedi_data[x_col], jedi_data[y_col], color="blue", alpha=0.6, s=20, label="Jedi")
        ax.scatter(sith_data[x_col], sith_data[y_col], color="red", alpha=0.6, s=20, label="Sith")
    else:
        ax.scatter(df[x_col], df[y_col], color="green", alpha=0.6, s=20, label="Knight")

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)


def create_four_plots():
    df_train = load_train_data()
    df_test = load_data()

    if df_train is None or df_test is None:
        print("Erreur: impossible de charger les données")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    plots_config = [
        (axes[0, 0], df_train, "Empowered", "Prescience", "Train - Empowered vs Prescience", True),
        (axes[0, 1], df_train, "Deflection", "Survival", "Train - Deflection vs Survival", True),
        (axes[1, 0], df_test, "Empowered", "Prescience", "Test - Empowered vs Prescience", False),
        (axes[1, 1], df_test, "Deflection", "Survival", "Test - Deflection vs Survival", False),
    ]

    for ax, df, x_col, y_col, title, has_knight in plots_config:
        create_scatter_plot(ax, df, x_col, y_col, title, has_knight)

    plt.tight_layout()
    return fig


def main():
    create_four_plots()
    plt.show()


if __name__ == "__main__":
    main()
