from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import altair as alt
import pandas as pd
from services.queries import (
    most_rented_films,
    rentals_per_month,
    revenue_by_category,
    get_film_lengths,
)
from utils.api_client import send_question

st.set_page_config(layout="wide")

st.title("🎬 Pagila database")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "processing_request" not in st.session_state:
    st.session_state["processing_request"] = False

df_revenue = revenue_by_category()
df_rentals = rentals_per_month()
df_rentals["month"] = df_rentals["month"].dt.strftime("%Y-%m")

df_lengths = get_film_lengths()
num_bins = 10
bins = pd.cut(df_lengths["length"], bins=num_bins)
df_lengths["length_bin"] = bins.astype(str)
df_hist = df_lengths["length_bin"].value_counts().sort_index().reset_index()
df_hist.columns = ["length_bin", "count"]

df_top_films = most_rented_films(10)

plot_col, chat_col = st.columns([0.6, 0.4])

with plot_col:
    st.subheader("📊 Data visualization")
    subcol_1, subcol_2 = st.columns(2)

    with subcol_1:
        st.markdown("📈 Revenue by Category")
        revenue_chart = (
            alt.Chart(df_revenue)
            .mark_bar()
            .encode(x="revenue", y=alt.Y("category", sort="-x"))
        )
        st.altair_chart(revenue_chart, use_container_width=True)

        st.markdown("📈 Film Length Distribution")
        hist_len_chart = (
            alt.Chart(df_hist)
            .mark_bar(color="skyblue")
            .encode(
                x=alt.X("length_bin", title="Film Length (minutes)"),
                y=alt.Y("count", title="Number of Films"),
                tooltip=["length_bin", "count"],
            )
        )
        st.altair_chart(hist_len_chart, use_container_width=True)

    with subcol_2:
        st.markdown("📈 Rentals per Month")
        st.bar_chart(df_rentals, x="month", y="rentals")

        st.markdown("📈 Top 10 Most Rented Films")
        top_rented_chart = (
            alt.Chart(df_top_films)
            .mark_bar()
            .encode(x="rental_count", y=alt.Y("film", sort="-x"))
        )
        st.altair_chart(top_rented_chart, use_container_width=True)


with chat_col:
    st.subheader("🗒️ Text to SQL")

    chat_html = ""
    for msg in reversed(st.session_state["messages"]):
        role_color = "#1a1c23" if msg["role"] == "user" else "transparent"
        chat_html += f"""
        <div style="
            background-color:{role_color};
            color: #fff;
            padding:12px 16px;
            margin:4px 0;
            border-radius:8px;
            width: 100%;
        ">
            <b>{msg['role'].upper()}:</b> {msg['content']}
        </div>
        """

    st.markdown(
        f"""
        <div style="
            height:400px;
            overflow-y:auto;
            display:flex;
            flex-direction:column-reverse;
            border:0;
            padding:10px;
            background-color:transparent;
        ">
            {chat_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if prompt := st.chat_input(
        "Ask a question...", disabled=st.session_state["processing_request"]
    ):
        st.session_state["processing_request"] = True

        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.rerun()

    if (
        st.session_state["processing_request"]
        and st.session_state["messages"][-1]["role"] == "user"
    ):
        prompt = st.session_state["messages"][-1]["content"]
        response = send_question(prompt)
        st.session_state["messages"].append(
            {"role": "assistant", "content": response["answer"]}
        )

        st.session_state["processing_request"] = False
        st.rerun()
