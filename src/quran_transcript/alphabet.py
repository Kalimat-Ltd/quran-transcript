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


@dataclass
class UniqueRasmMap:
    rasm_map: list[dict[str, str]]
    imlaey_starts: list[str]


@dataclass
class Istiaatha:
    imlaey: str
    uthmani: str


"""
rasm_map=
[
    {
        "uthmani": str
        "imlaey": str
    },
]

imlaey_starts: ["يا", "ويا", "ها"]
"""


alphabet_path = 'quran-script/quran-alphabet.json'
with open(alphabet_path, 'r', encoding='utf8') as f:
    alphabet_dict = json.load(f)
    imlaey = ImlaeyAlphabet(**alphabet_dict['imlaey'])
    uthmani = UthmaniAlphabet(**alphabet_dict['uthmani'])
    unique_rasm = UniqueRasmMap(**alphabet_dict['unique_rasm_map'])
    istiaatha = Istiaatha(**alphabet_dict['istiaatha'])
