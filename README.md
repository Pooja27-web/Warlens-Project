# Warlens-Project

WarLens is an NLP-powered news analysis and dataset dashboard built with
Streamlit, Python, and SQLite. It includes news CRUD controls and text
vectorization models.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Select this repository and the `main` branch.
4. Set the main file path to `WARLENS/streamlit_app.py`.
5. Click **Deploy**.

Streamlit Cloud installs dependencies from `WARLENS/requirements.txt`.
The application initializes the SQLite database and seeds the bundled dataset
on its first run.

## Run locally

```text
cd WARLENS
pip install -r requirements.txt
streamlit run streamlit_app.py
```
