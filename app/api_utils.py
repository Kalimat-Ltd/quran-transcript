from requests import get, post
from app.quran_utils import AyaFormat


URL = 'http://127.0.0.1:9000'


def get_aya(sura_idx: int, aya_idx: int) -> AyaFormat:
    response = get(
        f'{URL}/get/', params={'sura_idx': sura_idx, 'aya_idx': aya_idx})
    return AyaFormat(**response.json())


def get_suar_names() -> list[int]:
    """
    Return list of (114) suar names
    """
    response = get(f'{URL}/get_suar_names/')
    return response.json()


def step_ayat(ayaformat: AyaFormat, step: int) -> AyaFormat:
    """
    Return: Aya after or before the input "ayaformt"
    """
    response = get(
        f'{URL}/step_ayat/',
        params={'sura_idx': ayaformat.sura_idx,
                'aya_idx': ayaformat.aya_idx,
                'step': step})
    return AyaFormat(**response.json())
