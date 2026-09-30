# ============================================================
# nlp_engine.py — NLP Analysis Functions
# Project: 2026 Iran War NLP News Dataset
# ============================================================
# This file contains three NLP techniques:
# 1. Bag of Words (BoW)
# 2. TF-IDF (Term Frequency - Inverse Document Frequency)
# 3. Word2Vec (Word Embeddings)
# ============================================================

import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec


# ============================================================
# HELPER — Clean text before analysis
# ============================================================
def clean_text(text):
    """
    Cleans raw text:
    - Converts to lowercase
    - Removes punctuation and numbers
    - Removes extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.strip()
    return text


# ============================================================
# TECHNIQUE 1 — BAG OF WORDS
# ============================================================
def run_bow(texts):
    """
    Bag of Words counts how many times each word appears.
    Returns top words and their total frequency counts.
    """
    # Clean all texts first
    cleaned = [clean_text(t) for t in texts]

    # Create BoW model — use top 20 words, ignore english stopwords
    bow_model = CountVectorizer(max_features=20, stop_words="english")
    bow_matrix = bow_model.fit_transform(cleaned)

    # Get word names
    words = bow_model.get_feature_names_out().tolist()

    # Sum frequency of each word across all documents
    freq_array = bow_matrix.toarray().sum(axis=0)
    frequencies = freq_array.tolist()

    # Combine words and frequencies into a list
    result = []
    for i in range(len(words)):
        result.append({
            "word": words[i],
            "count": int(frequencies[i])
        })

    # Sort by count descending
    result.sort(key=lambda x: x["count"], reverse=True)

    return {
        "technique": "Bag of Words",
        "description": "Counts how many times each word appears across all documents.",
        "total_documents": len(texts),
        "vocabulary_size": len(words),
        "top_words": result
    }


# ============================================================
# TECHNIQUE 2 — TF-IDF
# ============================================================
def run_tfidf(texts):
    """
    TF-IDF gives each word an importance score.
    Common words get low scores. Rare important words get high scores.
    """
    cleaned = [clean_text(t) for t in texts]

    # Create TF-IDF model
    tfidf_model = TfidfVectorizer(max_features=20, stop_words="english")
    tfidf_matrix = tfidf_model.fit_transform(cleaned)

    # Get word names
    words = tfidf_model.get_feature_names_out().tolist()

    # Average TF-IDF score of each word across all documents
    avg_scores = tfidf_matrix.toarray().mean(axis=0)

    # Combine into list
    result = []
    for i in range(len(words)):
        result.append({
            "word": words[i],
            "tfidf_score": round(float(avg_scores[i]), 4)
        })

    # Sort by score descending
    result.sort(key=lambda x: x["tfidf_score"], reverse=True)

    return {
        "technique": "TF-IDF",
        "description": "Scores words by importance. High score = rare but important word.",
        "total_documents": len(texts),
        "vocabulary_size": len(words),
        "top_words": result
    }


# ============================================================
# TECHNIQUE 3 — WORD2VEC
# ============================================================
def run_word2vec(texts):
    """
    Word2Vec learns word relationships.
    Similar words get similar vector representations.
    Returns similar words for key war-related terms.
    """
    cleaned = [clean_text(t) for t in texts]

    # Convert each text into a list of words (tokens)
    sentences = [text.split() for text in cleaned]

    # Train Word2Vec model
    model = Word2Vec(
        sentences=sentences,
        vector_size=100,   # each word becomes a 100-number vector
        window=5,          # look at 5 words around each word
        min_count=1,       # include words that appear at least once
        workers=2,
        epochs=50
    )

    # Find similar words for key terms
    key_words = ["strikes", "missiles", "iran", "oil", "war", "attack", "killed", "nuclear"]
    similar_words = {}

    for word in key_words:
        try:
            similar = model.wv.most_similar(word, topn=5)
            similar_words[word] = [
                { "word": w, "similarity": round(float(s), 4) }
                for w, s in similar
            ]
        except KeyError:
            similar_words[word] = []

    # Vocabulary size
    vocab_size = len(model.wv)

    return {
        "technique": "Word2Vec",
        "description": "Learns word relationships. Similar words have similar vector representations.",
        "total_documents": len(texts),
        "vocabulary_size": vocab_size,
        "vector_size": 100,
        "similar_words": similar_words
    }
