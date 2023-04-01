import streamlit as st
import pandas as pd
import numpy as np
import files_access
import db_access


# Configuring the Main Stage
st.set_page_config(page_title="Music Selection", layout='wide')
st.title("Feature Selection based Music Selection")
col1, col2 = st.columns([3, 7])  # 2 vertical Sections [30%, 70%]


@st.cache_data  # storing the file_names for select box
def music_options():
    return pd.DataFrame(db_access.read_db("SELECT name FROM `audio-data`"))['name'].tolist()


# Starting Components
with col1:
    option = st.selectbox(
        'Select Music',
        ['-----Select Option-----'] + music_options())

    if option != '-----Select Option-----':
        with st.container():
            st.markdown(f"Your Selection: **{option}**")
            spec = files_access.return_spectrogram(option)
            audio = files_access.return_audio(option)
            st.image(spec, width=500)
            st.audio(audio)

        with col2:
            with st.container():
                st.write("This is inside the container")

                # You can call any Streamlit command, including custom components:
                st.bar_chart(np.random.randn(50, 3))

            st.write("This is outside the container")
