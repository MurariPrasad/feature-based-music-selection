import streamlit as st
import pandas as pd
import numpy as np
import time
import files_access
import db_access
import similarity


# Configuring the Main Stage
st.set_page_config(page_title="Music Selection", layout='wide')


@st.cache_data(show_spinner=False)  # storing the file_names for select box
def audio_names_from_db():
    return pd.DataFrame(db_access.read_db("SELECT name FROM `audio-data`"))


@st.cache_data(show_spinner=False)
def similarity_calculation():
    enc_files = pd.DataFrame(db_access.read_db("SELECT encoding_name FROM `audio-data`"))['encoding_name'].values.tolist()
    encodings = [np.load(files_access.return_np_encoding(f)) for f in enc_files]
    sim_vector = similarity.ts_ss(encodings)

    return sim_vector.detach().cpu().numpy().copy()


@st.cache_data(show_spinner=False)
def initializer():
    # To initialze our caches at start
    with st.spinner("Initializing. Please Wait......"):
        similarity_calculation()
        audio_names_from_db()
        alert = st.success("Ready", icon="✅")
    time.sleep(1.5)
    alert.empty()


initializer()
st.title("Feature Selection based Music Selection")
col1, col2 = st.columns([3, 7])  # 2 vertical Sections [30%, 70%]

# Starting Components
with col1:
    options_list = audio_names_from_db()['name'].values.tolist()
    option = st.selectbox('Select Music', ['-----Select Option-----'] + options_list)

    if option != '-----Select Option-----':
        with st.container():
            st.markdown(f"Your Selection: **{option}**")
            selection = pd.DataFrame(db_access.read_db(f"SELECT genre, spec_name, audio_name FROM `audio-data` WHERE name = '{option}'"))

            spec = files_access.return_spectrogram(selection['spec_name'].values[0])
            audio_path = selection['genre'].values[0]+"/"+selection['audio_name'].values[0]
            audio = files_access.return_audio(audio_path)

            st.image(spec)
            st.audio(audio)

        with col2:

            ind = options_list.index(option)  # -1 because of stock option at ind 0
            top_ind = np.argsort(similarity_calculation()[ind])[1:4]  #
            top_audio = [options_list[i] for i in top_ind]
            top_sim = [similarity_calculation()[ind][i] for i in top_ind]

            spec_names = pd.DataFrame(
                db_access.read_db(f"""SELECT spec_name FROM `audio-data` WHERE name IN("{top_audio[0]}", "{top_audio[1]}", "{top_audio[2]}")""")
            )['spec_name'].values.tolist()
            top1 = files_access.return_spectrogram(spec_names[0])
            top2 = files_access.return_spectrogram(spec_names[1])
            top3 = files_access.return_spectrogram(spec_names[2])

            sec1, sec2, sec3 = st.columns([1, 1, 1])  # 2 vertical Sections [30%, 70%]
            with sec1:
                st.write(top_audio[0])
                st.image(top1)
            with sec2:
                st.write(top_audio[1])
                st.image(top2)
            with sec3:
                st.write(top_audio[2])
                st.image(top3)
