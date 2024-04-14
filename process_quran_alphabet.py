from app.quran_utils import Aya
from app.alphabet import ImlaeyAlphabet
from pathlib import Path
import json


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
