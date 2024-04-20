from app.quran_utils import Aya
from app.alphabet import ImlaeyAlphabet, UniqueRasmMap
from pathlib import Path
from collections import defaultdict
import json


def get_rasm_map_more_than_words(quran_map_path: str | Path,
                                 suffix=' ',
                                 ) -> set[tuple[str, str]]:
    """
    return: set((uthamni_script, imlaey_script))
    """
    unique_words = set()
    start_aya = Aya(quran_map_path, 1, 1)
    for aya in start_aya.get_ayat_after():
        imlaey_words = aya.get_formatted_rasm_map().imlaey
        uthmani_words = aya.get_formatted_rasm_map().uthmani
        for imlaey_word, uthmani_word in zip(imlaey_words, uthmani_words):
            if len(imlaey_word) > 2:
                unique_words |= {
                    (suffix.join(uthmani_word), suffix.join(imlaey_word))}
    return unique_words


def get_unique_imlaey_start_word(quran_map_path: str | Path) -> set[str]:
    """
    return dict{unique_words: frequency_of_this_word_in_the_holly_Quran}
    """
    unique_starts = defaultdict(lambda: 0)
    start_aya = Aya(quran_map_path, 1, 1)
    for aya in start_aya.get_ayat_after():
        imlaey_words = aya.get_formatted_rasm_map().imlaey
        for words in imlaey_words:
            if len(words) > 1:
                unique_starts[words[0]] += 1
    return unique_starts


def save_unique_rasm_map(alphabet_path,
                         unique_rasm_map_set: set,
                         unique_start_imlaey_words: dict[str, int]):
    alphabet_dict = {}
    if Path(alphabet_path).is_file():
        with open(alphabet_path, 'r', encoding='utf8') as f:
            alphabet_dict = json.load(f)

    unique_rasm_map_list = []
    for uthmani_word, imlaey_word in unique_rasm_map_set:
        unique_rasm_map_list.append(
            {
                "uthmani": uthmani_word,
                "imlaey": imlaey_word,
            }
        )
    unique_rasm_map_list.append(
        {
            "uthmani": "وَأَلَّوِ",
            "imlaey": "وَأَن لَّوِ",
        }
    )

    unique_imlaey_starts = list(
        set(unique_start_imlaey_words.keys()) - {"وَأَن"})

    unique_rasm = UniqueRasmMap(
        rasm_map=unique_rasm_map_list,
        imlaey_starts=unique_imlaey_starts
    )
    alphabet_dict['unique_rasm_map'] = unique_rasm.__dict__
    with open(alphabet_path, 'w+', encoding='utf8') as f:
        json.dump(alphabet_dict, f, indent=2, ensure_ascii=False)


def get_alphabet(quran_map_path: str | Path, rasm_type: str) -> set[str]:
    assert rasm_type in ['uthmani', 'imlaey'], (
        f'only valid rasm_types are: {["uthmani", "imlaey"]}')
    alphabet = set()
    start_aya = Aya(quran_map_path, 1, 1)
    for aya in start_aya.get_ayat_after():
        alphabet |= set(getattr(aya.get(), rasm_type))
    alphabet -= {' '}
    alphabet = sorted(list(alphabet))
    return alphabet


def save_imlaey_alphabet(alphabet_path, alphabet: list[str]):
    alphabet_dict = {}
    if Path(alphabet_path).is_file():
        with open(alphabet_path, 'r', encoding='utf8') as f:
            alphabet_dict = json.load(f)

    imlaey_alphabet = ImlaeyAlphabet(
        alphabet="".join(alphabet),
        hamazat="".join(alphabet[0: 6]),
        hamza=alphabet[0],
        alef=alphabet[6],
        alef_maksoora=alphabet[34],
        taa_mabsoota=alphabet[9],
        taa_marboota=alphabet[8],
        haa=alphabet[32],
        small_alef="".join(alphabet[44]),
        tashkeel="".join(alphabet[36: 44]),
        skoon=alphabet[43],
    )
    alphabet_dict['imlaey'] = imlaey_alphabet.__dict__
    with open(alphabet_path, 'w+', encoding='utf8') as f:
        json.dump(alphabet_dict, f, indent=2, ensure_ascii=False)
    return imlaey_alphabet


if __name__ == "__main__":
    quran_map_path = 'quran-script/quran-uthmani-imlaey-map.json'
    quran_alphabet_path = 'quran-script/quran-alphabet.json'

    imlaey_alphabet = get_alphabet(quran_map_path, 'imlaey')
    print('Imlaey Script Alphabet')
    print(f'Len of alphabet={len(imlaey_alphabet)}')
    for idx, char in enumerate(imlaey_alphabet):
        print(f"{idx}-> '{char}'")
    print()

    print('Saving Imlaey Alphabet ....')
    imlaey_alphabet_obj = save_imlaey_alphabet(quran_alphabet_path, imlaey_alphabet)
    for key, val in imlaey_alphabet_obj.__dict__.items():
        print(f'{key} -> {" ".join(list(val))}')

    print('Saving Unique RasmMap .........')
    unique_rasm_set = get_rasm_map_more_than_words(quran_map_path)
    unique_imlaey_start_words = get_unique_imlaey_start_word(quran_map_path)
    save_unique_rasm_map(
        alphabet_path=quran_alphabet_path,
        unique_rasm_map_set=unique_rasm_set,
        unique_start_imlaey_words=unique_imlaey_start_words
    )
