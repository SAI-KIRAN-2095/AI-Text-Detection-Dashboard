import os
import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.ensemble import VotingClassifier
import joblib

def main():
    print("=== Training Machine Learning Models for LLM Text Detection ===")
    
    base_dir = r"c:\Users\DELL\Desktop\ai\LLM-Text-Detection"
    actual_dir = os.path.join(base_dir, "Actual-Datasets")
    extra_dir = os.path.join(base_dir, "Extra-Datasets-Used")
    output_dir = r"c:\Users\DELL\Desktop\ai\backend\models"
    os.makedirs(output_dir, exist_ok=True)
    
    dfs = []
    
    # 1. Actual Train Dataset
    train_actual_path = os.path.join(actual_dir, "train_essays.csv")
    if os.path.exists(train_actual_path):
        df_actual = pd.read_csv(train_actual_path)[['text', 'generated']].rename(columns={'generated': 'label'})
        dfs.append(df_actual)
        print(f"Loaded train_essays.csv: {len(df_actual)} samples")

    # 2. Extra Datasets
    extra_files = ['train_drcat_01.csv', 'LLM_generated_essay_PaLM.csv', 'falcon_180b_v1.csv', 'llama_70b_v1.csv']
    for fn in extra_files:
        fp = os.path.join(extra_dir, fn)
        if os.path.exists(fp):
            df = pd.read_csv(fp)
            if 'generated_text' in df.columns:
                df = df.rename(columns={'generated_text': 'text'})
            if 'generated' in df.columns:
                df = df.rename(columns={'generated': 'label'})
            if 'label' not in df.columns:
                df['label'] = 1
            dfs.append(df[['text', 'label']])
            print(f"Loaded {fn}: {len(df)} samples")

    if not dfs:
        raise RuntimeError("No training datasets found!")

    df_combined = pd.concat(dfs, ignore_index=True).dropna(subset=['text', 'label'])
    df_combined['label'] = df_combined['label'].astype(int)
    df_combined = df_combined.drop_duplicates(subset=['text'])

    print(f"\nTotal Dataset Size: {len(df_combined)} samples")
    print(f"Human (0): {(df_combined['label']==0).sum()}, AI (1): {(df_combined['label']==1).sum()}")

    # Subsample if dataset is very large to speed up training while retaining high accuracy
    if len(df_combined) > 40000:
        print("Sampling 40,000 balanced instances for efficient training...")
        df_human = df_combined[df_combined['label'] == 0]
        df_ai = df_combined[df_combined['label'] == 1].sample(min(20000, len(df_combined[df_combined['label'] == 1])), random_state=42)
        df_combined = pd.concat([df_human, df_ai]).sample(frac=1.0, random_state=42).reset_index(drop=True)

    texts = df_combined['text'].astype(str).values
    labels = df_combined['label'].values

    # --- Train Model 2: Voting Classifier (LogisticRegression + SGD) ---
    print("\n--- Training Model 2: Logistic Regression + SGD Voting Classifier ---")
    m2_vec = TfidfVectorizer(ngram_range=(1, 2), max_features=40000, sublinear_tf=True, strip_accents='unicode')
    X_m2 = m2_vec.fit_transform(texts)
    
    lr = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    sgd = SGDClassifier(loss='modified_huber', max_iter=2000, tol=1e-4, random_state=42)
    m2_ensemble = VotingClassifier(estimators=[('lr', lr), ('sgd', sgd)], voting='soft', weights=[0.2, 0.8])
    m2_ensemble.fit(X_m2, labels)

    joblib.dump(m2_vec, os.path.join(output_dir, "model2_vectorizer.joblib"))
    joblib.dump(m2_ensemble, os.path.join(output_dir, "model2_ensemble.joblib"))
    print("Model 2 saved successfully!")

    # --- Train Model 3: Hybrid Stacking Ensemble (MNB + SGD + Dual TF-IDF) ---
    print("\n--- Training Model 3: Hybrid Stacking Ensemble (MNB + SGD + Dual Word/Char TF-IDF) ---")
    m3_word_vec = TfidfVectorizer(ngram_range=(1, 3), max_features=40000, sublinear_tf=True, strip_accents='unicode')
    m3_char_vec = TfidfVectorizer(ngram_range=(3, 5), analyzer='char_wb', max_features=40000, sublinear_tf=True)

    X_m3_word = m3_word_vec.fit_transform(texts)
    X_m3_char = m3_char_vec.fit_transform(texts)
    X_m3 = hstack([X_m3_word, X_m3_char]).tocsr()

    mnb = MultinomialNB(alpha=0.02)
    sgd_m3 = SGDClassifier(loss='modified_huber', max_iter=2000, tol=1e-4, random_state=42)
    m3_ensemble = VotingClassifier(estimators=[('mnb', mnb), ('sgd', sgd_m3)], voting='soft', weights=[0.3, 0.7])
    m3_ensemble.fit(X_m3, labels)

    joblib.dump(m3_word_vec, os.path.join(output_dir, "model3_word_vec.joblib"))
    joblib.dump(m3_char_vec, os.path.join(output_dir, "model3_char_vec.joblib"))
    joblib.dump(m3_ensemble, os.path.join(output_dir, "model3_ensemble.joblib"))
    print("Model 3 saved successfully!")

    print("\n=== All Models Trained and Saved Successfully! ===")

if __name__ == "__main__":
    main()
