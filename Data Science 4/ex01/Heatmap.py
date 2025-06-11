import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


def plot_heatmap(data):
    """Plot correlation heatmap"""
    
    correlation_matrix = data.corr(numeric_only=True)
    plt.figure(figsize=(20, 16))
    
    sns.heatmap(correlation_matrix, square=True,
        xticklabels=True, yticklabels=True)
    
    plt.title('Correlation Heatmap - Knight Dataset', fontsize=16, fontweight='bold')
    plt.tight_layout(pad=5.0)
    plt.show()


def main():
    """Main function to execute the heatmap generation"""
    data = load_data("../data/Train_knight.csv")
    if data is None:
        return
    plot_heatmap(data)


if __name__ == "__main__":
    main()
