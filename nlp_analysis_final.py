# ============================================================
# NLP PROJECT - 2026 IRAN WAR NEWS ANALYSIS
# Dataset: war_news_dataset_updated.csv
# Student: BCA Semester IV
# Techniques: Bag of Words, TF-IDF, Word2Vec, Logistic Regression
# ============================================================

# STEP 1: IMPORT LIBRARIES
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from gensim.models import Word2Vec
import warnings
warnings.filterwarnings("ignore")

print("=" * 60)
print("  2026 IRAN WAR - NLP ANALYSIS")
print("=" * 60)


# ============================================================
# STEP 2: LOAD THE DATASET
# ============================================================

df = pd.read_csv("war_news_dataset_updated.csv")

print("\n✅ Dataset Loaded Successfully!")
print("Total Rows (News Events):", len(df))
print("Total Columns:", len(df.columns))
print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 3 Rows of Dataset:")
print(df.head(3))


# ============================================================
# STEP 3: TEXT PREPROCESSING
# ============================================================
# We clean the text before applying NLP techniques.
# Cleaning means:
# 1. Convert to lowercase
# 2. Remove punctuation and numbers
# 3. Remove extra spaces

def clean_text(text):
    # Step 1: Lowercase all words
    text = text.lower()

    # Step 2: Remove punctuation and numbers (keep only letters)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Step 3: Remove extra whitespace
    text = text.strip()

    return text


# Apply cleaning to the news_text column
df["cleaned_text"] = df["news_text"].apply(clean_text)

print("\n" + "=" * 60)
print("STEP 3: TEXT PREPROCESSING")
print("=" * 60)
print("\nOriginal Text (Row 1):")
print(df["news_text"][0])
print("\nCleaned Text (Row 1):")
print(df["cleaned_text"][0])


# ============================================================
# STEP 4: BAG OF WORDS (BoW)
# ============================================================
# Bag of Words converts text into word count numbers.
# Each word becomes a column (feature).
# Each row shows how many times that word appears.

print("\n" + "=" * 60)
print("STEP 4: BAG OF WORDS (BoW)")
print("=" * 60)

# Create the Bag of Words model
bow_model = CountVectorizer(max_features=15, stop_words="english")

# Fit and transform the cleaned text
bow_matrix = bow_model.fit_transform(df["cleaned_text"])

# Get the feature/word names
bow_words = bow_model.get_feature_names_out()

# Convert to a readable DataFrame
bow_df = pd.DataFrame(bow_matrix.toarray(), columns=bow_words)

print("\nTop 15 Words selected by Bag of Words:")
print(bow_words.tolist())

print("\nBoW Matrix (first 5 rows x 15 words):")
print(bow_df.head(5))

print("\nBoW Matrix Shape (rows x columns):", bow_matrix.shape)

# Word frequency count
print("\nTotal word frequency (sum of each word across all documents):")
word_freq = bow_df.sum().sort_values(ascending=False)
print(word_freq)


# ============================================================
# STEP 5: TF-IDF
# ============================================================
# TF-IDF = Term Frequency x Inverse Document Frequency
#
# TF  = How often a word appears in ONE document
# IDF = How rare a word is across ALL documents
#
# High TF-IDF = Very important word for that document
# Low TF-IDF  = Common word not very useful

print("\n" + "=" * 60)
print("STEP 5: TF-IDF")
print("=" * 60)

# Create the TF-IDF model
tfidf_model = TfidfVectorizer(max_features=15, stop_words="english")

# Fit and transform the cleaned text
tfidf_matrix = tfidf_model.fit_transform(df["cleaned_text"])

# Get the feature/word names
tfidf_words = tfidf_model.get_feature_names_out()

# Convert to a readable DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_words)

print("\nTop 15 Words selected by TF-IDF:")
print(tfidf_words.tolist())

print("\nTF-IDF Matrix (first 5 rows x 15 words):")
print(tfidf_df.head(5).round(3))

print("\nTF-IDF Matrix Shape (rows x columns):", tfidf_matrix.shape)

# Average importance of each word
print("\nAverage TF-IDF score per word (higher = more important):")
avg_tfidf = tfidf_df.mean().sort_values(ascending=False)
print(avg_tfidf.round(4))


# ============================================================
# STEP 6: WORD2VEC
# ============================================================
# Word2Vec converts words into vectors (numbers).
# Similar words get similar vectors.

print("\n" + "=" * 60)
print("STEP 6: WORD2VEC")
print("=" * 60)

# Word2Vec needs a list of sentences
sentences = []
for text in df["cleaned_text"]:
    words = text.split()
    sentences.append(words)

print("\nSample sentence (first row as list of words):")
print(sentences[0][:10], "...")

# Train the Word2Vec model
w2v_model = Word2Vec(
    sentences=sentences,
    vector_size=100,
    window=5,
    min_count=1,
    workers=2,
    epochs=50
)

print("\n✅ Word2Vec Model Trained!")
print("Vocabulary Size (unique words learned):", len(w2v_model.wv))

# Show vector for a word
print("\nWord Vector for 'missiles' (first 10 numbers):")
try:
    print(w2v_model.wv["missiles"][:10])
except:
    print("Word 'missiles' not in vocabulary")

# Find similar words
print("\nWords most similar to 'strikes':")
try:
    similar = w2v_model.wv.most_similar("strikes", topn=5)
    for word, score in similar:
        print(f"  {word}  ->  similarity score: {round(score, 4)}")
except:
    print("Word not found")

print("\nWords most similar to 'oil':")
try:
    similar2 = w2v_model.wv.most_similar("oil", topn=5)
    for word, score in similar2:
        print(f"  {word}  ->  similarity score: {round(score, 4)}")
except:
    print("Word not found")

print("\nWords most similar to 'iran':")
try:
    similar3 = w2v_model.wv.most_similar("iran", topn=5)
    for word, score in similar3:
        print(f"  {word}  ->  similarity score: {round(score, 4)}")
except:
    print("Word not found")

print("\nSimilarity score between 'attack' and 'strike':")
try:
    sim = w2v_model.wv.similarity("attack", "strike")
    print(f"  {round(sim, 4)} (closer to 1.0 = more similar)")
except:
    print("One of the words not in vocabulary")


# ============================================================
# STEP 7: ML MODEL — LOGISTIC REGRESSION
# ============================================================
# We use Logistic Regression to classify news events
# into their event types (Airstrike, Economic, Political, etc.)
#
# Input  (X) = TF-IDF vectors of news_text
# Output (Y) = event_type column (the label/class)
#
# This is a multi-class text classification problem.

print("\n" + "=" * 60)
print("STEP 7: ML MODEL — LOGISTIC REGRESSION")
print("=" * 60)

# ── PREPARE DATA ──

# X = features (TF-IDF vectors of cleaned text)
# We use more features here for better classification
tfidf_for_model = TfidfVectorizer(max_features=50, stop_words="english")
X = tfidf_for_model.fit_transform(df["cleaned_text"])

# Y = labels (event_type column)
# We group rare categories to ensure enough samples per class
def group_event_type(event):
    event = event.lower()
    if "airstrike" in event:
        return "Airstrike"
    elif "missile" in event or "rocket" in event or "drone" in event:
        return "Missile/Drone Attack"
    elif "economic" in event:
        return "Economic"
    elif "political" in event:
        return "Political"
    elif "humanitarian" in event:
        return "Humanitarian"
    elif "diplomatic" in event:
        return "Diplomatic"
    else:
        return "Other"

df["grouped_event"] = df["event_type"].apply(group_event_type)
Y = df["grouped_event"]

print("\nLabel Distribution (event type counts):")
print(Y.value_counts())
print(f"\nTotal classes: {Y.nunique()}")
print(f"Classes: {Y.unique().tolist()}")

# ── SPLIT DATA ──
# 80% training data, 20% testing data
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,      # 20% for testing
    random_state=42,    # fixed seed for reproducibility
    stratify=Y          # keep class balance in split
)

print(f"\nTraining set size: {X_train.shape[0]} samples")
print(f"Testing set size:  {X_test.shape[0]} samples")

# ── TRAIN THE MODEL ──
print("\n🔄 Training Logistic Regression model...")

lr_model = LogisticRegression(
    max_iter=1000,       # maximum iterations to converge
    random_state=42,     # fixed seed
    solver="lbfgs",      # optimization algorithm
    multi_class="auto"   # handles multiple classes automatically
)

# Train (fit) the model on training data
lr_model.fit(X_train, Y_train)

print("✅ Logistic Regression Model Trained!")

# ── MAKE PREDICTIONS ──
Y_pred = lr_model.predict(X_test)

print("\nActual labels  (Y_test):", list(Y_test))
print("Predicted labels (Y_pred):", list(Y_pred))

# ── EVALUATE THE MODEL ──

print("\n" + "=" * 60)
print("STEP 8: MODEL EVALUATION")
print("=" * 60)

# Accuracy
accuracy = accuracy_score(Y_test, Y_pred)
print(f"\nAccuracy  : {round(accuracy * 100, 2)}%")
print("  (How many predictions were correct overall)")

# Precision
precision = precision_score(Y_test, Y_pred, average="weighted", zero_division=0)
print(f"\nPrecision : {round(precision * 100, 2)}%")
print("  (Of all predicted positives, how many were actually correct)")

# Recall
recall = recall_score(Y_test, Y_pred, average="weighted", zero_division=0)
print(f"\nRecall    : {round(recall * 100, 2)}%")
print("  (Of all actual positives, how many did model find)")

# F1 Score
f1 = f1_score(Y_test, Y_pred, average="weighted", zero_division=0)
print(f"\nF1 Score  : {round(f1 * 100, 2)}%")
print("  (Balanced score combining precision and recall)")

# Full Classification Report
print("\nFull Classification Report:")
print(classification_report(Y_test, Y_pred, zero_division=0))

# Confusion Matrix
print("Confusion Matrix:")
cm = confusion_matrix(Y_test, Y_pred, labels=lr_model.classes_)
cm_df = pd.DataFrame(cm, index=lr_model.classes_, columns=lr_model.classes_)
print(cm_df)


# ── SAMPLE PREDICTIONS ──

print("\n" + "=" * 60)
print("STEP 9: SAMPLE PREDICTIONS")
print("=" * 60)

# Test with 5 sample news texts
sample_texts = [
    "Israel launched airstrikes on Tehran killing military commanders",
    "Oil prices surged to 114 dollars per barrel as Strait of Hormuz closed",
    "Iran fired ballistic missiles at US military bases in Kuwait",
    "United Nations warned three million Iranians displaced by attacks",
    "Trump threatened to obliterate Iran power plants within 48 hours"
]

print("\nPredicting event type for new sample news texts:")
for i, text in enumerate(sample_texts):
    cleaned = clean_text(text)
    vec = tfidf_for_model.transform([cleaned])
    prediction = lr_model.predict(vec)[0]
    confidence = lr_model.predict_proba(vec).max()
    print(f"\n  Sample {i+1}: \"{text[:60]}...\"")
    print(f"  Predicted Type: {prediction}")
    print(f"  Confidence    : {round(confidence * 100, 2)}%")


# ============================================================
# STEP 10: FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

print(f"\nDataset:          2026 Iran-US-Israel War News")
print(f"Total Events:     {len(df)}")
print(f"Columns:          {list(df.columns)}")

print(f"\nBag of Words:")
print(f"  Matrix Shape:   {bow_matrix.shape}")
print(f"  Top 5 Words:    {bow_words[:5].tolist()}")

print(f"\nTF-IDF:")
print(f"  Matrix Shape:   {tfidf_matrix.shape}")
print(f"  Top 5 Words:    {tfidf_words[:5].tolist()}")

print(f"\nWord2Vec:")
print(f"  Vocab Size:     {len(w2v_model.wv)}")
print(f"  Vector Size:    100 dimensions per word")

print(f"\nLogistic Regression:")
print(f"  Task:           Multi-class Text Classification")
print(f"  Features:       TF-IDF (50 features)")
print(f"  Train/Test:     80% / 20%")
print(f"  Accuracy:       {round(accuracy * 100, 2)}%")
print(f"  Precision:      {round(precision * 100, 2)}%")
print(f"  Recall:         {round(recall * 100, 2)}%")
print(f"  F1 Score:       {round(f1 * 100, 2)}%")

print(f"\nEvent Types in Dataset:")
print(df["event_type"].value_counts())

print(f"\nSources in Dataset:")
print(df["source"].value_counts())

print("\n" + "=" * 60)
print("✅ NLP ANALYSIS COMPLETE!")
print("=" * 60)
