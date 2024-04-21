from app.quran_utils import Aya
from pathlib import Path
from collections import defaultdict


def get_rasm_map_more_than_words(quran_map_path: str | Path,
                                 suffix=' ',
                                 ) -> set[tuple[str, str]]:
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
    unique_starts = defaultdict(lambda: 0)
    start_aya = Aya(quran_map_path, 1, 1)
    for aya in start_aya.get_ayat_after():
        imlaey_words = aya.get_formatted_rasm_map().imlaey
        for words in imlaey_words:
            if len(words) > 1:
                unique_starts[words[0]] += 1
    return unique_starts


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


if __name__ == "__main__":
    quran_map_path = 'quran-script/quran-uthmani-imlaey-map.json'

    # Imlaey words > 2
    unique_words = get_rasm_map_more_than_words(quran_map_path)
    print('Uthmani Word that map to Imlaey Words > 2')
    print(unique_words)
    print()

    unique_imlaey_starts = get_unique_imlaey_start_word(quran_map_path)
    print('Imaley First word of uthmni words map to imleey words > 1')
    print(unique_imlaey_starts)
    print()

    imlaey_alphabet = get_alphabet(quran_map_path, 'imlaey')
    print('Imlaey Script Alphabet')
    print(f'Len of alphabet={len(imlaey_alphabet)}')

    for idx, char in enumerate(imlaey_alphabet):
        print(f"{idx}-> '{char}'")
    print()

    uthmani_alphabet = get_alphabet(quran_map_path, 'uthmani')
    print('Uthmani Script Alphabet')
    print(f'Len of alphabet={len(uthmani_alphabet)}')
    for idx, char in enumerate(uthmani_alphabet):
        print(f"{idx}-> '{char}'")
    print()
