import streamlit as st
from pathlib import Path
import json
import shutil
from app.utils import multiselect_list, app_main


def move_font_files(fonts_dir: str | Path):
    """
    copying font files into stramlit path to be rendered correctly
    """
    STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / "static"
    CSS_PATH = STREAMLIT_STATIC_PATH
    for dir in ['assets', 'fonts']:
        CSS_PATH = CSS_PATH / dir
        if not CSS_PATH.is_dir():
            CSS_PATH.mkdir()

    font_files = Path(fonts_dir).glob('*')
    for font_file in font_files:
        shutil.copy(font_file, CSS_PATH)


def handle_change():
    st.session_state.level_1 = st.session_state.level_1_slider


def set_slider_max():
    st.session_state.slider_max = int(st.session_state.number_input)


if __name__ == "__main__":
    # move_font_files('app/fonts')
    #
    # with open("style.css") as css:
    #     st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    #
    # edit_ayah_page([], [])
    # L = ['A', 'B', 'C', 'D']
    # st.write(mulitselect_list(L, 3))
    #
    #
    # moshaf_path = Path('/home/abdullah/Downloads/kfgqpc_hafs_smart_4/kfgqpc_hafs_smart_data/hafs_smart_v8.json')
    #
    # with open(moshaf_path, 'r', encoding='utf8') as f:
    #     moshaf = json.load(f)
    #
    # ayah = moshaf[8]['aya_text']
    # st.write(ayah)
    # st.write('------------')
    # for idx, char in enumerate(ayah):
    #     st.write(f'{(idx)}  -> {char}')
    # st.write(len(ayah))
    # st.write(ayah[5] == ayah[12])
    #
    # # s = "أحمد جاء من هنا"
    # # st.write(s)

    # src: https://github.com/streamlit/streamlit/issues/3925#issuecomment-946148239
    # if 'level_1' not in st.session_state:
    #     # Initialize to the saved value in session state if it's available
    #     if 'level_1_slider' in st.session_state:
    #         st.session_state.level_1 = st.session_state.level_1_slider
    #     else:
    #         st.session_state.level_1 = 1
    #         st.session_state.level_1_slider = 1
    #
    # if 'slider_max' not in st.session_state:
    #     # Initialize to the saved value in session state if it's available
    #     # if 'number_input' in st.session_state:
    #     #     st.session_state.slider_max = int(st.session_state.number_input)
    #     # else:
    #     st.session_state['number_input'] = 10
    #     st.session_state['slider_max'] = 10
    #
    # st.number_input('Enter max value', on_change=set_slider_max, key='number_input')
    # st.slider('level1', min_value=0, max_value=st.session_state.slider_max, value=st.session_state.level_1, on_change=handle_change, key="level_1_slider")
    #
    # st.write('level_1 = ', st.session_state.level_1)

    # st.write(multiselect_list(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 5))
    # st.write(multiselect_list(['A', 'B', 'C', 'D'], 4))

    app_main()
