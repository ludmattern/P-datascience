#!/usr/bin/env python3

import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler


def main():
    if len(sys.argv) != 3:
        print("Usage: python democracy.py Train_knight.csv Test_knight.csv")
        sys.exit(1)

    train_data = pd.read_csv(sys.argv[1])
    test_data = pd.read_csv(sys.argv[2])

    X = train_data.drop("knight", axis=1)
    y = train_data["knight"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(test_data)

    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10)

    knn_model = KNeighborsClassifier(n_neighbors=11)

    lr_model = LogisticRegression(max_iter=1000)

    rf_model.fit(X_train, y_train)
    rf_pred_val = rf_model.predict(X_val)
    rf_f1 = f1_score(y_val, rf_pred_val, pos_label="Jedi")
    print(f"Random Forest F1 score: {rf_f1:.4f}")

    knn_model.fit(X_train_scaled, y_train)
    knn_pred_val = knn_model.predict(X_val_scaled)
    knn_f1 = f1_score(y_val, knn_pred_val, pos_label="Jedi")
    print(f"KNN F1 score: {knn_f1:.4f}")

    lr_model.fit(X_train_scaled, y_train)
    lr_pred_val = lr_model.predict(X_val_scaled)
    lr_f1 = f1_score(y_val, lr_pred_val, pos_label="Jedi")
    print(f"Logistic Regression F1 score: {lr_f1:.4f}")

    rf_pred_test = rf_model.predict(test_data)
    knn_pred_test = knn_model.predict(X_test_scaled)
    lr_pred_test = lr_model.predict(X_test_scaled)

    final_predictions = []
    for i in range(len(test_data)):
        votes = [rf_pred_test[i], knn_pred_test[i], lr_pred_test[i]]

        jedi_votes = votes.count("Jedi")
        sith_votes = votes.count("Sith")

        if jedi_votes > sith_votes:
            final_predictions.append("Jedi")
        else:
            final_predictions.append("Sith")

    voting_pred_val = []
    for i in range(len(X_val)):
        votes = [rf_pred_val[i], knn_pred_val[i], lr_pred_val[i]]

        votes = [rf_pred_val[i], knn_pred_val[i], knn_pred_val[i], lr_pred_val[i]]

        jedi_votes = votes.count("Jedi")
        sith_votes = votes.count("Sith")

        if jedi_votes > sith_votes:
            voting_pred_val.append("Jedi")
        else:
            voting_pred_val.append("Sith")

    voting_f1 = f1_score(y_val, voting_pred_val, pos_label="Jedi")
    print(f"Voting Classifier F1 score: {voting_f1:.4f}")

    with open("Voting.txt", "w") as f:
        for pred in final_predictions:
            f.write(f"{pred}\n")

    print(f"Final Voting F1 score: {voting_f1:.4f}")
    if voting_f1 < 0.94:
        print("Warning: F1 score is below 94% requirement")
    else:
        print("✅ F1 score requirement (94%) met!")


if __name__ == "__main__":
    main()
