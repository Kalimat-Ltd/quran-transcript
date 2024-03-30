import streamlit as st
from pathlib import Path
import shutil
from app.utils import app_main


@st.cache_data
def move_fonts_files(fonts_dir: str | Path):
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


@st.cache_data
def load_css(css_path: str | Path):
    with open(Path(css_path)) as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


if __name__ == "__main__":
    move_fonts_files('app/fonts')

    load_css("style.css")

    app_main()
