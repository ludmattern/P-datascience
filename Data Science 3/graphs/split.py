#!/usr/bin/env python3
import pandas as pd
import sys
from sklearn.model_selection import train_test_split


def main():
    if len(sys.argv) != 2:
        print("Usage: ./split.py Train_knight.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        df = pd.read_csv(input_file)
        
        train_df, validation_df = train_test_split(
            df, 
            test_size=0.2,
            random_state=42,
            stratify=df['knight'] if 'knight' in df.columns else None
        )
        
        train_df.to_csv("Training_knight.csv", index=False)
        validation_df.to_csv("Validation_knight.csv", index=False)
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()