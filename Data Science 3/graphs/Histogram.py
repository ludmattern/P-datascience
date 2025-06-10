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


def create_histograms(df):
    if df is None:
        return

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    n_cols = len(numeric_columns)

    if n_cols == 0:
        return

    cols_per_row = 5
    n_rows = (n_cols + cols_per_row - 1) // cols_per_row

    fig, axes = plt.subplots(n_rows, cols_per_row, figsize=(15, 4 * n_rows))

    if n_rows == 1:
        axes = axes.reshape(1, -1) if n_cols > 1 else [axes]

    axes_flat = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]

    for i, column in enumerate(numeric_columns):
        ax = axes_flat[i]
        data = df[column].dropna()

        ax.hist(data, color="green", bins=40, alpha=0.5, label="Knight")
        ax.set_title(column, fontsize=8)
        ax.legend(fontsize=8)
        ax.tick_params(axis="both", which="major", labelsize=8)

    for i in range(n_cols, len(axes_flat)):
        axes_flat[i].set_visible(False)

    plt.tight_layout(pad=5.0)
    return fig


def create_diff_histograms(df):
    if df is None:
        return

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    n_cols = len(numeric_columns)

    if n_cols == 0:
        return

    cols_per_row = 5
    n_rows = (n_cols + cols_per_row - 1) // cols_per_row

    fig, axes = plt.subplots(n_rows, cols_per_row, figsize=(15, 4 * n_rows))

    if n_rows == 1:
        axes = axes.reshape(1, -1) if n_cols > 1 else [axes]

    axes_flat = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]

    jedi_data = df[df["knight"] == "Jedi"]
    sith_data = df[df["knight"] == "Sith"]

    for i, column in enumerate(numeric_columns):
        ax = axes_flat[i]

        jedi_values = jedi_data[column].dropna()
        sith_values = sith_data[column].dropna()

        ax.hist(jedi_values, color="blue", bins=40, alpha=0.5, label="Jedi")
        ax.hist(sith_values, color="red", bins=40, alpha=0.5, label="Sith")
        ax.set_title(column, fontsize=8)
        ax.legend(fontsize=8)
        ax.tick_params(axis="both", which="major", labelsize=8)

    for i in range(n_cols, len(axes_flat)):
        axes_flat[i].set_visible(False)

    plt.tight_layout(pad=5.0)
    return fig


def main():
    df = load_data()
    if df is None:
        return

    create_histograms(df)
    plt.show()

    df_train = load_train_data()
    if df_train is None:
        return

    create_diff_histograms(df_train)
    plt.show()


if __name__ == "__main__":
    main()
