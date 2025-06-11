import sys
import numpy as np
import matplotlib.pyplot as plt


def load_data(predictions_file, truth_file):
    """Load predictions and truth data from files"""
    try:
        with open(predictions_file, "r") as f:
            predictions = [line.strip() for line in f if line.strip()]

        with open(truth_file, "r") as f:
            truth = [line.strip() for line in f if line.strip()]

        if len(predictions) != len(truth):
            raise ValueError("Predictions and truth files must have the same number of lines")

        return predictions, truth

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def calculate_confusion_matrix(predictions, truth):
    """Calculate confusion matrix manually"""
    classes = sorted(list(set(predictions + truth)))
    n_classes = len(classes)

    confusion_matrix = [[0 for _ in range(n_classes)] for _ in range(n_classes)]

    for pred, true in zip(predictions, truth):
        true_idx = classes.index(true)
        pred_idx = classes.index(pred)
        confusion_matrix[true_idx][pred_idx] += 1

    return confusion_matrix, classes


def calculate_metrics(confusion_matrix, classes):
    """Calculate precision, recall, f1-score for each class and accuracy"""
    n_classes = len(classes)
    metrics = {}

    total_samples = sum(sum(row) for row in confusion_matrix)
    correct_predictions = sum(confusion_matrix[i][i] for i in range(n_classes))
    accuracy = correct_predictions / total_samples

    for i, class_name in enumerate(classes):
        tp = confusion_matrix[i][i]

        fp = sum(confusion_matrix[j][i] for j in range(n_classes)) - tp
        fn = sum(confusion_matrix[i][j] for j in range(n_classes)) - tp

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        class_total = sum(confusion_matrix[i][j] for j in range(n_classes))

        metrics[class_name] = {"precision": precision, "recall": recall, "f1_score": f1_score, "total": class_total}

    return metrics, accuracy


def display_results(metrics, accuracy, confusion_matrix, classes):
    """Display results in the required format"""
    total_samples = sum(sum(row) for row in confusion_matrix)

    print(f"{'':12} | {'precision':>9} | {'recall':>9} | {'f1-score':>9} | {'total':>9}")
    print("-" * 13 + "+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 11)

    for class_name in classes:
        m = metrics[class_name]
        print(f"{class_name:12} | {m['precision']:9.2f} | {m['recall']:9.2f} | {m['f1_score']:9.2f} | {m['total']:9}")

    print("-" * 13 + "+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 11)

    print(f"{'accuracy':12} | {'':<9} | {'':<9} | {accuracy:9.2f} | {total_samples:9}")

    print()
    print("Confusion Matrix:")
    print(f"{confusion_matrix[0]}\n{confusion_matrix[1]}")


def plot_confusion_matrix(confusion_matrix, classes):
    """
    Plot confusion matrix using matplotlib
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(confusion_matrix, interpolation="nearest", cmap="plasma")
    plt.title("Confusion Matrix")
    plt.colorbar()

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    for row in range(len(classes)):
        for col in range(len(classes)):
            value = confusion_matrix[row][col]
            if row == col:
                label = f"{value} : True Positive"
            else:
                if row == 0 and col == 1:
                    label = f"{value} : False Negative"
                else:
                    label = f"{value} : False Positive"

            max_value = max(max(row) for row in confusion_matrix)
            text_color = "black" if value > max_value * 0.9 else "white"

            plt.text(col, row, label, horizontalalignment="center", verticalalignment="center", color=text_color, fontsize=14)

    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 3:
        print("Usage: python Confusion_Matrix.py predictions.txt truth.txt")
        sys.exit(1)

    predictions_file = sys.argv[1]
    truth_file = sys.argv[2]

    predictions, truth = load_data(predictions_file, truth_file)

    confusion_matrix, classes = calculate_confusion_matrix(predictions, truth)

    metrics, accuracy = calculate_metrics(confusion_matrix, classes)

    display_results(metrics, accuracy, confusion_matrix, classes)

    plot_confusion_matrix(confusion_matrix, classes)


if __name__ == "__main__":
    main()
