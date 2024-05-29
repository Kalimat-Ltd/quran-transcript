from requests import get, post
from quran_transcript import AyaFormat


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


def get_first_aya_to_annotate() -> AyaFormat:
    """
    get first aya to annotate "len(uthmani_words) != len(imlaey_words)"
    """
    response = get(f'{URL}/get_first_aya_to_annotate/')
    return AyaFormat(**response.json())


def save_rasm_map(
    sura_idx: int,
    aya_idx: int,
    uthmani_words: list[list[str]],
    imlaey_words: list[list[str]]
):
    to_send = {
        'sura_idx': sura_idx,
        'aya_idx': aya_idx,
        'uthmani_words': uthmani_words,
        'imlaey_words': imlaey_words
    }
    response = post(f'{URL}/save_rasm_map', json=to_send)
    if response.status_code == 406:
        raise ValueError(
            f'Rasm Map not acceptable of (sura_idx={sura_idx}, aya_idx={aya_idx})')
    return response.status_code


def save_quran_dict() -> None:
    """
    Saving changes in quran-map file
    """
    response = get(f'{URL}/save_quran_dict/')
    return response.status_code
