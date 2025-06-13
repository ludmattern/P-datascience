#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def main():
    if len(sys.argv) != 3:
        print("Usage: python KNN.py Train_knight.csv Test_knight.csv")
        sys.exit(1)
    
    train_data = pd.read_csv(sys.argv[1])
    test_data = pd.read_csv(sys.argv[2])
    
    X = train_data.drop('knight', axis=1)
    y = train_data['knight']
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(test_data)
    
    k_values = range(1, 21)
    precisions = []
    f1_scores = []
    accuracies = []
    
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        
        y_pred_val = knn.predict(X_val_scaled)
        precision = precision_score(y_val, y_pred_val, pos_label='Jedi')
        f1 = f1_score(y_val, y_pred_val, pos_label='Jedi')
        accuracy = accuracy_score(y_val, y_pred_val)
        
        precisions.append(precision * 100)
        f1_scores.append(f1)
        accuracies.append(accuracy * 100)
    
    best_k_idx = np.argmax(f1_scores)
    best_k = k_values[best_k_idx]
    best_f1 = f1_scores[best_k_idx]
    
    print(f"\nBest k={best_k} with F1 score: {best_f1:.4f}")
    
    final_knn = KNeighborsClassifier(n_neighbors=best_k)
    final_knn.fit(X_train_scaled, y_train)
    
    predictions = final_knn.predict(X_test_scaled)
    
    with open('KNN.txt', 'w') as f:
        for pred in predictions:
            f.write(f"{pred}\n")
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(k_values, accuracies, 'g-o', markersize=6, linewidth=2)
    plt.title('KNN Accuracy vs K-value')
    plt.xlabel('K-value')
    plt.ylabel('Accuracy (%)')
    plt.grid(True, alpha=0.3)
    plt.xticks(k_values)
    
    min_acc = min(accuracies)
    max_acc = max(accuracies)
    margin = (max_acc - min_acc) * 0.1
    plt.ylim(min_acc - margin, max_acc + margin)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Final F1 score: {best_f1:.4f}")
    if best_f1 < 0.92:
        print("Warning: F1 score is below 92% requirement")


if __name__ == "__main__":
    main()
