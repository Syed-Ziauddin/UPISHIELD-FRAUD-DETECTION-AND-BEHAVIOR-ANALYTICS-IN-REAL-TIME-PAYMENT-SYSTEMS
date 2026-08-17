# =====================================================
# app.py — Flask Integration for Multi-Aspect Fraud Detection + Login System
# =====================================================
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
import re
import joblib
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from scipy.special import expit
from urllib.parse import urlparse
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from db_connection import get_db_connection  #  import MySQL connector

# =====================================================
# Flask Setup
# =====================================================
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs("model", exist_ok=True)

# =====================================================
# Globals
# =====================================================
fraud_labels = ["Normal", "Fraud"]
transaction_type_labels = ["Bill Payment", "P2M", "P2P", "Recharge"]
label_encoders = {}
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# =====================================================
# Preprocessing
# =====================================================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def preprocess_data(df=None, mode='train'):
    if df is None:
        raise ValueError("A valid DataFrame must be provided.")
    df = df.fillna({
        col: 0 if pd.api.types.is_numeric_dtype(df[col]) else 'unknown'
        for col in df.columns
    })

    age_cols = ['sender_age_group', 'receiver_age_group']
    for col in age_cols:
        if col in df.columns:
            df[f'{col}_min'] = df[col].apply(lambda x: int(x.split('-')[0]) if '-' in str(x) else 0)
            df[f'{col}_max'] = df[col].apply(lambda x: int(x.split('-')[1]) if '-' in str(x) else 0)
    df.drop(columns=[col for col in age_cols if col in df.columns], inplace=True)

    text_columns = df.select_dtypes(include='object').columns.tolist()
    targets = ['transaction_type', 'fraud_flag']
    text_columns = [col for col in text_columns if col not in targets]

    for col in text_columns:
        df[col] = df[col].apply(clean_text)

    df['combined_text'] = df[text_columns].agg(' '.join, axis=1)
    numeric_data = df.select_dtypes(include=[np.number])
    X = pd.concat([df[['combined_text']], numeric_data], axis=1)
    X = X.drop(columns=[col for col in targets if col in X.columns], errors='ignore')

    if mode == 'train':
        Y_dict = {}
        for target in targets:
            if target in df.columns:
                le = LabelEncoder()
                Y_dict[target] = le.fit_transform(df[target].astype(str))
                label_encoders[target] = le
        return X, Y_dict.get('transaction_type'), Y_dict.get('fraud_flag')
    elif mode == 'test':
        return X

# =====================================================
# SBERT Feature Extraction
# =====================================================
def sbert_feature_extraction(texts, model_name='sentence-transformers/all-MiniLM-L6-v2', batch_size=32):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    all_embeddings = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Extracting SBERT embeddings"):
        batch_texts = texts[i:i + batch_size]
        encoded_input = tokenizer(batch_texts, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**encoded_input)
        token_embeddings = model_output.last_hidden_state
        attention_mask = encoded_input['attention_mask']
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
        sum_mask = input_mask_expanded.sum(dim=1)
        embeddings = sum_embeddings / sum_mask
        all_embeddings.append(embeddings.cpu().numpy())
    X = np.vstack(all_embeddings)
    return X

def feature_extraction(X_df, model_dir='model', is_train=True):
    x_file = os.path.join(model_dir, f'X_Numerical_SBERT.pkl')
    text_data = X_df['combined_text'].tolist()
    model_name = 'sentence-transformers/all-mpnet-base-v2'

    if is_train:
        if os.path.exists(x_file):
            X = joblib.load(x_file)
        else:
            X = sbert_feature_extraction(text_data, model_name=model_name)
            joblib.dump(X, x_file)
    else:
        X = sbert_feature_extraction(text_data, model_name=model_name)

    return X

# =====================================================
# Routes: Authentication
# =====================================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, address, email, password) VALUES (%s, %s, %s, %s)",
            (username, address, email, password)
        )
        conn.commit()
        conn.close()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()  #   allows dict-like access for user['username']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user['username']
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('predict_page'))
        else:
            flash("Invalid credentials!", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

# =====================================================
# Routes: Prediction
# =====================================================
@app.route('/predict_page')
def predict_page():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('prediction.html', user=session['user'])

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded!"

    file = request.files['file']
    if file.filename == '':
        return "No file selected!"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    df = pd.read_csv(file_path)
    X_test = preprocess_data(df, mode='test')
    features_test = feature_extraction(X_test, is_train=False)

    histgb_models = {
        'fraud_flag': joblib.load('model/Numerical BERT_fraud_flag_histgb_model.pkl'),
        'transaction_type': joblib.load('model/Numerical BERT_transaction_type_histgb_model.pkl')
    }

    df_result = df.copy()
    for target in ['transaction_type', 'fraud_flag']:
        y_pred = histgb_models[target].predict(features_test)
        if target == 'transaction_type':
            label_encoders[target] = LabelEncoder()
            label_encoders[target].classes_ = np.array(transaction_type_labels)
        else:
            label_encoders[target] = LabelEncoder()
            label_encoders[target].classes_ = np.array(fraud_labels)
        mapped_labels = label_encoders[target].inverse_transform(y_pred)
        df_result[f'Predicted_{target}'] = mapped_labels

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'predicted_output.csv')
    df_result.to_csv(output_path, index=False)

    return render_template(
        'results.html',
        table=df_result.head(10).to_html(classes='data', index=False),
        filename=output_path
    )

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

# =====================================================
# Run App
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
