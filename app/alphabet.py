from dataclasses import dataclass
import json


@dataclass
class ImlaeyAlphabet:
    alphabet: str
    hamazat: str
    hamza: str
    alef: str
    alef_maksoora: str
    taa_marboota: str
    taa_mabsoota: str
    haa: str
    small_alef: str
    tashkeel: str  # including skoon
    skoon: str


@dataclass
class UthmaniAlphabet:
    pass


alphabet_path = 'quran-script/quran-alphabet.json'
with open(alphabet_path, 'r', encoding='utf8') as f:
    alphabet_dict = json.load(f)
    imlaey = ImlaeyAlphabet(**alphabet_dict['imlaey'])
    uthmani = UthmaniAlphabet(**alphabet_dict['uthmani'])
