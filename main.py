import streamlit as st
import pandas as pd
import numpy as np
import time
import files_access
import db_access
import similarity

# Startup Config
st.set_page_config(page_title="Music Selection", layout='wide')


@st.cache_data(show_spinner=False)  # storing the file_names for select box
def audio_names_from_db():
    return pd.DataFrame(db_access.read_db(f"SELECT name FROM `{db_access.TABLE_PATH}`"))


@st.cache_data(show_spinner=False)
def similarity_calculation():
    enc_files = pd.DataFrame(
        db_access.read_db(f"SELECT encoding_name FROM `{db_access.TABLE_PATH}`")
    )['encoding_name'].values.tolist()
    encodings = np.array([np.load(files_access.return_np_encoding(f)) for f in enc_files])
    sim_vector = similarity.ts_ss(encodings)

    return sim_vector.detach().cpu().numpy().copy()


@st.cache_resource(show_spinner=False)
def initializer():
    """
    To initialize page at start
    """
    with st.spinner("Initializing. Please Wait......"):
        similarity_calculation()
        audio_names_from_db()
        alert = st.success("Ready", icon="✅")
    time.sleep(1.5)
    alert.empty()

    st.markdown("""<style>div.block-container{padding-top:0rem;}</style>""", unsafe_allow_html=True)
    # with open("assets/image.png", "rb") as f:
    #     data = base64.b64encode(f.read()).decode("utf-8")
    # st.markdown(f"""<img src="data:image/png;base64,{data}" width="100%" height="100">""", unsafe_allow_html=True)
    st.title("Feature Selection based Music Recommendation")


def main_stage():
    """
    main app
    """
    col1, col2 = st.columns([3, 7])  # 2 vertical Sections [30%, 70%]
    with col1:
        options_list = audio_names_from_db()['name'].values.tolist()
        option = st.selectbox('Select Music', ['-----Select Option-----'] + options_list)

        if option != '-----Select Option-----':
            with st.container():
                st.markdown(f"Your Selection: **{option}**")
                selection = pd.DataFrame(
                    db_access.read_db(f"SELECT genre, spec_name, audio_name FROM `{db_access.TABLE_PATH}` WHERE name = '{option}'"))

                spec = files_access.return_spectrogram(selection['spec_name'].values[0])
                audio_path = selection['genre'].values[0] + "/" + selection['audio_name'].values[0]
                audio = files_access.return_audio(audio_path)

                st.image(spec)
                st.audio(audio)

            with col2:
                ind = options_list.index(option)
                top_ind = np.argsort(similarity_calculation()[ind])[:5]  #
                top_audio = [options_list[i] for i in top_ind]
                if option in top_audio:
                    top_audio.remove(option)

                sim_query = pd.DataFrame(
                    db_access.read_db(
                        f"""SELECT spec_name, audio_name, genre FROM `{db_access.TABLE_PATH}` WHERE name IN("{top_audio[0]}", "{top_audio[1]}", "{top_audio[2]}")""")
                )
                spec_names = sim_query['spec_name'].values.tolist()
                audio_names = sim_query['audio_name'].values.tolist()
                genres_names = sim_query['genre'].values.tolist()
                top1 = files_access.return_spectrogram(spec_names[0])
                top1_audio = files_access.return_audio(genres_names[0] + "/" + audio_names[0])
                top2 = files_access.return_spectrogram(spec_names[1])
                top2_audio = files_access.return_audio(genres_names[1] + "/" + audio_names[1])
                top3 = files_access.return_spectrogram(spec_names[2])
                top3_audio = files_access.return_audio(genres_names[2] + "/" + audio_names[2])

                st.write("""<p>
                                <div style='text-align:center; font-size:28px;'> 
                                    <i>Top Selection of Similar Music</i> 
                                </div> 
                            </p>""",
                         unsafe_allow_html=True)

                sec1, sec2, sec3 = st.columns([1, 1, 1])
                with sec1:
                    st.write(top_audio[0])
                    st.image(top1)
                    st.audio(top1_audio)
                with sec2:
                    st.write(top_audio[1])
                    st.image(top2)
                    st.audio(top2_audio)
                with sec3:
                    st.write(top_audio[2])
                    st.image(top3)
                    st.audio(top3_audio)


initializer()
main_stage()
