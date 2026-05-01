import streamlit as st
import pandas as pd

from src import tools
from src.llm import get_intent, parse_intent

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🤖 Echabot (EDA Chatbot)")

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# ======================
# TAMPILKAN CHAT HISTORY
# ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ======================
# INPUT AREA (CHAT + UPLOAD)
# ======================
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Ngobrol atau analisis data...")

with col2:
    uploaded_file = st.file_uploader(
        "",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

# ======================
# HANDLE FILE UPLOAD
# ======================
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # cleaning khusus walmart
    df.rename(columns={
        "Date": "date",
        "Weekly_Sales": "sales",
        "Store": "store"
    }, inplace=True)

    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    st.session_state.df = df

    st.success("File berhasil diupload!")

# indikator dataset aktif
if st.session_state.df is not None:
    st.caption("Dataset aktif siap digunakan")

# ======================
# HANDLE CHAT
# ======================
if user_input:
    # tampilkan user
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # LLM processing
    llm_response = get_intent(user_input)
    intent = parse_intent(llm_response)

    df = st.session_state.df

    # ======================
    # DATA ANALYSIS MODE
    # ======================
    if intent and df is not None:

        if intent == "plot_per_year":
            path = tools.plot_per_year(df)

            with st.chat_message("assistant"):
                st.write("Ini grafik penjualan per tahun:")
                st.image(path)

        elif intent == "plot_per_month":
            path = tools.plot_per_month(df)

            with st.chat_message("assistant"):
                st.write("Ini grafik penjualan per bulan:")
                st.image(path)

        elif intent == "plot_per_store":
            path = tools.plot_per_store(df)

            with st.chat_message("assistant"):
                st.write("Ini grafik penjualan per store:")
                st.image(path)

        st.session_state.messages.append({
            "role": "assistant",
            "content": "Menampilkan hasil analisis"
        })

    # ======================
    # MINTA DATA TAPI BELUM UPLOAD
    # ======================
    elif intent and df is None:
        response = "Upload dulu datasetnya baru gue bisa analisis koplok"

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # ======================
    # CHAT BIASA
    # ======================
    else:
        with st.chat_message("assistant"):
            st.write(llm_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": llm_response
        })