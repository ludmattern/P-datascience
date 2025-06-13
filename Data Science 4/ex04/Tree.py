#!/usr/bin/env python3

import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt


def main():
    if len(sys.argv) != 3:
        print("Usage: python Tree.py Train_knight.csv Test_knight.csv")
        sys.exit(1)

    train_data = pd.read_csv(sys.argv[1])
    test_data = pd.read_csv(sys.argv[2])

    X = train_data.drop("knight", axis=1)
    y = train_data["knight"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)

    y_pred_val = model.predict(X_val)
    f1 = f1_score(y_val, y_pred_val, pos_label="Jedi")
    print(f"F1 score: {f1:.4f}")

    X_test = test_data
    predictions = model.predict(X_test)

    with open("Tree.txt", "w") as f:
        for pred in predictions:
            f.write(f"{pred}\n")

    plt.figure(figsize=(20, 12))
    plot_tree(model.estimators_[0],
              feature_names=X.columns,
              class_names=["Jedi", "Sith"],
              filled=True,
              rounded=True,
              fontsize=8,
              max_depth=30)
    plt.title("Random Forest - First Tree")
    plt.show()


if __name__ == "__main__":
    main()
