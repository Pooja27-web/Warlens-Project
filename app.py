# ============================================================
# app.py — Flask Backend Server
# Project: 2026 Iran War NLP News Dataset
# ============================================================
# This file is the main server file.
# It handles all API routes (CRUD + NLP).
# Run this file to start the web server.
# ============================================================

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import init_db, get_all_news, add_news, update_news, delete_news, get_news_by_id, seed_data
from nlp_engine import run_bow, run_tfidf, run_word2vec

# Create the Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend
# ============================================================
# ROUTE: Home Page
# ============================================================
@app.route("/")
def home():
    # Serve the main HTML page
    return render_template("index.html")
# ============================================================
# CRUD ROUTES
# ============================================================

# READ — Get all news events
@app.route("/api/news", methods=["GET"])
def get_news():
    news = get_all_news()
    return jsonify({ "success": True, "data": news, "count": len(news) })


# READ ONE — Get a single news event by ID
@app.route("/api/news/<int:news_id>", methods=["GET"])
def get_one(news_id):
    news = get_news_by_id(news_id)
    if news:
        return jsonify({ "success": True, "data": news })
    return jsonify({ "success": False, "message": "News not found" }), 404


# CREATE — Add a new news event
@app.route("/api/news", methods=["POST"])
def create_news():
    body = request.get_json()

    # Validate required fields
    required = ["date", "headline", "news_text", "source", "location", "event_type"]
    for field in required:
        if not body.get(field):
            return jsonify({ "success": False, "message": f"Field '{field}' is required" }), 400

    new_id = add_news(
        date               = body["date"],
        headline           = body["headline"],
        news_text          = body["news_text"],
        source             = body["source"],
        location           = body["location"],
        casualties_reported= body.get("casualties_reported", "Unknown"),
        event_type         = body["event_type"],
        sentiment          = body.get("sentiment", "Negative")
    )

    return jsonify({ "success": True, "message": "News added successfully", "id": new_id }), 201


# UPDATE — Edit an existing news event
@app.route("/api/news/<int:news_id>", methods=["PUT"])
def edit_news(news_id):
    body = request.get_json()

    existing = get_news_by_id(news_id)
    if not existing:
        return jsonify({ "success": False, "message": "News not found" }), 404

    update_news(
        news_id            = news_id,
        date               = body.get("date",                existing["date"]),
        headline           = body.get("headline",            existing["headline"]),
        news_text          = body.get("news_text",           existing["news_text"]),
        source             = body.get("source",              existing["source"]),
        location           = body.get("location",            existing["location"]),
        casualties_reported= body.get("casualties_reported", existing["casualties_reported"]),
        event_type         = body.get("event_type",          existing["event_type"]),
        sentiment          = body.get("sentiment",           existing["sentiment"])
    )

    return jsonify({ "success": True, "message": "News updated successfully" })


# DELETE — Remove a news event
@app.route("/api/news/<int:news_id>", methods=["DELETE"])
def remove_news(news_id):
    existing = get_news_by_id(news_id)
    if not existing:
        return jsonify({ "success": False, "message": "News not found" }), 404

    delete_news(news_id)
    return jsonify({ "success": True, "message": "News deleted successfully" })


# ============================================================
# NLP ROUTES
# ============================================================

# Bag of Words analysis
@app.route("/api/nlp/bow", methods=["GET"])
def bow_analysis():
    news_list = get_all_news()
    texts = [n["news_text"] for n in news_list]
    result = run_bow(texts)
    return jsonify({ "success": True, "analysis": "Bag of Words", "data": result })


# TF-IDF analysis
@app.route("/api/nlp/tfidf", methods=["GET"])
def tfidf_analysis():
    news_list = get_all_news()
    texts = [n["news_text"] for n in news_list]
    result = run_tfidf(texts)
    return jsonify({ "success": True, "analysis": "TF-IDF", "data": result })


# Word2Vec analysis
@app.route("/api/nlp/word2vec", methods=["GET"])
def word2vec_analysis():
    news_list = get_all_news()
    texts = [n["news_text"] for n in news_list]
    result = run_word2vec(texts)
    return jsonify({ "success": True, "analysis": "Word2Vec", "data": result })


# ============================================================
# START THE SERVER
# ============================================================
if __name__ == "__main__":
    # Step 1: Initialize the database (create tables)
    init_db()

    # Step 2: Seed initial data if database is empty
    seed_data()

    # Step 3: Start the server
    # debug=True means auto-reload when you change code
    print("\n✅ Server running at: http://localhost:5000\n")
    app.run(debug=True, port=5000)
