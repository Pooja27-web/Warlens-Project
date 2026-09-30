# WarLens — 2026 Iran War NLP Analysis
## Full Stack Web Application

---

## Project Overview

WarLens is a full-stack web application built as an NLP (Natural Language Processing) project for BCA Semester IV. It collects, manages, and analyzes news events from the 2026 Iran-US-Israel war using three NLP techniques: Bag of Words, TF-IDF, and Word2Vec.

---

## Tech Stack

| Layer      | Technology         |
|------------|--------------------|
| Frontend   | HTML, CSS, JavaScript |
| Backend    | Python Flask       |
| Database   | SQLite             |
| NLP        | Scikit-learn, Gensim |
| Deployment | Render.com (free)  |

---

## Project Structure

```
war-news-app/
├── app.py              ← Main Flask server (API routes)
├── database.py         ← SQLite database operations (CRUD)
├── nlp_engine.py       ← NLP analysis (BoW, TF-IDF, Word2Vec)
├── requirements.txt    ← Python package list
├── README.md           ← This file
└── templates/
    └── index.html      ← Frontend (HTML + CSS + JavaScript)
```

---

## How to Run Locally

### Step 1: Install Python
Download from https://python.org (version 3.10 or higher)

### Step 2: Install Required Packages
Open terminal/command prompt and run:
```
pip install -r requirements.txt
```

### Step 3: Run the Server
```
python app.py
```

### Step 4: Open the Website
Open your browser and go to:
```
http://localhost:5000
```

---

## API Endpoints (CRUD)

| Method | URL                    | What it does              |
|--------|------------------------|---------------------------|
| GET    | /api/news              | Get all news events       |
| GET    | /api/news/&lt;id&gt;   | Get one news by ID        |
| POST   | /api/news              | Add new news event        |
| PUT    | /api/news/&lt;id&gt;   | Update existing news      |
| DELETE | /api/news/&lt;id&gt;   | Delete a news event       |
| GET    | /api/nlp/bow           | Run Bag of Words analysis |
| GET    | /api/nlp/tfidf         | Run TF-IDF analysis       |
| GET    | /api/nlp/word2vec      | Run Word2Vec analysis     |

---

## How to Deploy on Render.com (Free)

### Step 1: Push code to GitHub
- Create a GitHub account at github.com
- Create a new repository
- Upload all project files

### Step 2: Sign up on Render.com
- Go to https://render.com
- Sign up with your GitHub account

### Step 3: Create a New Web Service
- Click "New" → "Web Service"
- Connect your GitHub repository
- Set:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app`
  - Environment: Python 3

### Step 4: Deploy
- Click "Create Web Service"
- Wait 2-3 minutes
- Your website goes live at: `https://your-app-name.onrender.com`

---

## Features

- View all 51 war news events from database
- Add new news events (Create)
- Edit existing news events (Update)
- Delete news events (Delete)
- Search and filter news by type/location
- Run NLP analysis: Bag of Words, TF-IDF, Word2Vec
- Visual bar charts for event distribution
- Word frequency cloud
- Timeline view
- Click any news card for full details popup

---

## NLP Techniques Used

### 1. Bag of Words
Converts text into word count numbers.
Each word = one feature column.
Each document = one row showing word frequencies.

### 2. TF-IDF (Term Frequency - Inverse Document Frequency)
Gives importance scores to words.
Common words across all documents get low scores.
Rare but important words get high scores.

### 3. Word2Vec
Learns word relationships from context.
Similar words get similar vector representations.
Shows which words appear in similar contexts.

---

## Dataset

- 51 news events from the 2026 Iran-US-Israel war
- Date range: February 28 to March 23, 2026
- Sources: Al Jazeera, CNN, Reuters, BBC, Wikipedia, UNICEF
- Columns: date, headline, news_text, source, location, casualties_reported, event_type, sentiment

---

## Students

BCA Semester IV
Alliance University — School of Advanced Computing
Subject: Natural Language Processing
