#!/usr/bin/env python3
import pandas as pd
import sys
from sklearn.model_selection import train_test_split


def split_dataset(input_file, train_ratio=0.8, random_state=42):
    """
    Divise un dataset en Training et Validation sets
    
    Args:
        input_file: Chemin vers le fichier CSV à diviser
        train_ratio: Proportion pour le training set (0.8 = 80%)
        random_state: Seed pour la reproductibilité
    """
    try:
        # Charger les données
        df = pd.read_csv(input_file)
        print(f"📊 Dataset original : {len(df)} lignes")
        
        # Diviser le dataset
        train_df, validation_df = train_test_split(
            df, 
            test_size=1-train_ratio,  # 1-0.8 = 0.2 (20% validation)
            random_state=random_state,
            stratify=df['knight'] if 'knight' in df.columns else None  # Garde les mêmes proportions Jedi/Sith
        )