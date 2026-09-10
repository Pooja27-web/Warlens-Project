"""Streamlit interface for the WarLens news and NLP dashboard."""

from collections import Counter

import pandas as pd
import streamlit as st

from database import (
    add_news,
    delete_news,
    get_all_news,
    get_news_by_id,
    init_db,
    seed_data,
    update_news,
)
from nlp_engine import run_bow, run_tfidf, run_word2vec


st.set_page_config(
    page_title="WarLens NLP Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def initialize_database():
    init_db()
    seed_data()
    return True


def load_news():
    return get_all_news()


def news_frame(news):
    return pd.DataFrame(news) if news else pd.DataFrame(
        columns=[
            "id", "date", "headline", "news_text", "source", "location",
            "casualties_reported", "event_type", "sentiment",
        ]
    )


def run_analysis(name, texts):
    if not texts:
        return None
    try:
        if name == "Bag of Words":
            return run_bow(texts)
        if name == "TF-IDF":
            return run_tfidf(texts)
        return run_word2vec(texts)
    except ValueError:
        return None


def add_news_form():
    with st.form("add_news_form", clear_on_submit=True):
        st.subheader("Add a news event")
        first, second = st.columns(2)
        date = first.text_input("Date", placeholder="2026-03-24")
        headline = second.text_input("Headline")
        news_text = st.text_area("News text")
        first, second, third = st.columns(3)
        source = first.text_input("Source")
        location = second.text_input("Location")
        event_type = third.text_input("Event type")
        first, second = st.columns(2)
        casualties = first.text_input("Casualties reported", value="Unknown")
        sentiment = second.selectbox("Sentiment", ["Negative", "Neutral", "Positive"])
        submitted = st.form_submit_button("Add news", type="primary")

    if submitted:
        required = {
            "Date": date, "Headline": headline, "News text": news_text,
            "Source": source, "Location": location, "Event type": event_type,
        }
        missing = [label for label, value in required.items() if not value.strip()]
        if missing:
            st.error("Complete these fields: " + ", ".join(missing))
        else:
            add_news(
                date, headline, news_text, source, location, casualties,
                event_type, sentiment,
            )
            st.success("News event added.")
            st.rerun()


def edit_news_form(news):
    if not news:
        st.info("No news events are available to edit.")
        return

    by_id = {item["id"]: item for item in news}
    selected_id = st.selectbox(
        "Select an event",
        list(by_id),
        format_func=lambda item_id: f"{item_id}: {by_id[item_id]['headline']}",
    )
    selected = by_id[selected_id]

    with st.form("edit_news_form"):
        first, second = st.columns(2)
        date = first.text_input("Date", value=selected["date"])
        headline = second.text_input("Headline", value=selected["headline"])
        news_text = st.text_area("News text", value=selected["news_text"])
        first, second, third = st.columns(3)
        source = first.text_input("Source", value=selected["source"])
        location = second.text_input("Location", value=selected["location"])
        event_type = third.text_input("Event type", value=selected["event_type"])
        first, second = st.columns(2)
        casualties = first.text_input(
            "Casualties reported", value=selected["casualties_reported"]
        )
        sentiment = second.selectbox(
            "Sentiment",
            ["Negative", "Neutral", "Positive"],
            index=["Negative", "Neutral", "Positive"].index(selected["sentiment"])
            if selected["sentiment"] in ["Negative", "Neutral", "Positive"] else 0,
        )
        submitted = st.form_submit_button("Save changes", type="primary")

    if submitted:
        values = [date, headline, news_text, source, location, event_type]
        if any(not value.strip() for value in values):
            st.error("Date, headline, news text, source, location, and event type are required.")
        else:
            update_news(
                selected_id, date, headline, news_text, source, location,
                casualties, event_type, sentiment,
            )
            st.success("News event updated.")
            st.rerun()


def delete_news_form(news):
    if not news:
        return
    by_id = {item["id"]: item for item in news}
    selected_id = st.selectbox(
        "Select an event to delete",
        list(by_id),
        format_func=lambda item_id: f"{item_id}: {by_id[item_id]['headline']}",
        key="delete_id",
    )
    if st.button("Delete selected event", type="secondary"):
        delete_news(selected_id)
        st.success("News event deleted.")
        st.rerun()


initialize_database()
news = load_news()
frame = news_frame(news)

st.title("WarLens")
st.caption("NLP-powered news analysis and dataset dashboard")

with st.sidebar:
    st.header("Filters")
    search = st.text_input("Search headline or article")
    locations = sorted(frame["location"].dropna().unique().tolist())
    event_types = sorted(frame["event_type"].dropna().unique().tolist())
    location_filter = st.multiselect("Location", locations)
    event_filter = st.multiselect("Event type", event_types)

filtered = frame.copy()
if search:
    mask = (
        filtered["headline"].str.contains(search, case=False, na=False)
        | filtered["news_text"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if location_filter:
    filtered = filtered[filtered["location"].isin(location_filter)]
if event_filter:
    filtered = filtered[filtered["event_type"].isin(event_filter)]

metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("News events", len(filtered))
metric_two.metric("Locations", filtered["location"].nunique())
metric_three.metric("Event types", filtered["event_type"].nunique())
metric_four.metric("Sources", filtered["source"].nunique())

tab_dashboard, tab_nlp, tab_manage = st.tabs(
    ["Dashboard", "NLP analysis", "Manage news"]
)

with tab_dashboard:
    st.subheader("News events")
    if filtered.empty:
        st.info("No events match the selected filters.")
    else:
        display_columns = [
            "id", "date", "headline", "source", "location",
            "event_type", "sentiment", "casualties_reported",
        ]
        st.dataframe(
            filtered[display_columns],
            use_container_width=True,
            hide_index=True,
        )
        left, right = st.columns(2)
        with left:
            st.subheader("Events by type")
            st.bar_chart(filtered["event_type"].value_counts())
        with right:
            st.subheader("Events by location")
            st.bar_chart(filtered["location"].value_counts())

        st.subheader("Article details")
        selected_id = st.selectbox(
            "Select an event to read",
            filtered["id"].tolist(),
            format_func=lambda item_id: filtered.loc[
                filtered["id"] == item_id, "headline"
            ].iloc[0],
        )
        selected = get_news_by_id(selected_id)
        if selected:
            st.markdown(f"**{selected['headline']}**")
            st.write(selected["news_text"])
            st.caption(
                f"{selected['date']} · {selected['source']} · "
                f"{selected['location']} · {selected['event_type']}"
            )

with tab_nlp:
    st.subheader("Natural language processing")
    technique = st.selectbox("Technique", ["Bag of Words", "TF-IDF", "Word2Vec"])
    analysis = run_analysis(technique, filtered["news_text"].tolist())
    if analysis is None:
        st.warning("There is not enough text to run this analysis.")
    else:
        st.write(analysis["description"])
        first, second = st.columns(2)
        first.metric("Documents", analysis["total_documents"])
        second.metric("Vocabulary size", analysis["vocabulary_size"])
        if technique in ["Bag of Words", "TF-IDF"]:
            values = analysis["top_words"]
            value_column = "count" if technique == "Bag of Words" else "tfidf_score"
            st.bar_chart(pd.DataFrame(values).set_index("word")[value_column])
            st.dataframe(pd.DataFrame(values), use_container_width=True, hide_index=True)
        else:
            for word, similar in analysis["similar_words"].items():
                if similar:
                    st.write(f"**{word}**")
                    st.dataframe(pd.DataFrame(similar), hide_index=True)

with tab_manage:
    add_news_form()
    st.divider()
    st.subheader("Edit a news event")
    edit_news_form(news)
    st.divider()
    st.subheader("Delete a news event")
    delete_news_form(news)
