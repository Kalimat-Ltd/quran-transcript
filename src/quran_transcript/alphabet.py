from dataclasses import dataclass
import json
from pathlib import Path


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
    alif: str
    alif_maksora: str
    baa: str
    taa_mabsoota: str
    taa_marboota: str
    thaa: str
    jeem: str
    haa_mohmala: str
    khaa: str
    daal: str
    thaal: str
    raa: str
    zay: str
    seen: str
    sheen: str
    saad: str
    daad: str
    taa_mofkhama: str
    zaa_mofkhama: str
    ayn: str
    ghyn: str
    faa: str
    qaf: str
    kaf: str
    lam: str
    meem: str
    noon: str
    haa: str
    waw: str
    yaa: str

    # hmazat
    hamza: str
    hamza_above_alif: str
    hamza_below_alif: str
    hamza_above_waw: str
    hamza_above_yaa: str
    hamza_mamdoda: str  # 46

    # harakat
    tanween_fath: str
    tanween_dam: str
    tanween_kasr: str
    fatha: str
    dama: str
    kasra: str

    shadda: str  # 43
    ras_haaa: str  # 44
    madd: str  # 45

    hamzat_wasl: str  # 48

    # small letters
    alif_khnjaria: str  # 47
    small_seen_above: str  # 49
    small_seen_below: str  # 53
    small_waw: str  # 54
    small_yaa_sila: str  # 55
    small_yaa: str  # 56
    small_noon: str  # 57

    # dabt letters
    skoon_mostadeer: str  # 50
    skoon_mostateel: str  # 51
    meem_iqlab: str  # 52
    imala_sign: str  # 58
    ishmam_sign: str  # 59
    tasheel_sign: str  # 60

    # special letters
    tanween_idhaam_dterminer: str  # 61
    kasheeda: str  # 26
    space: str

    # letters groups
    noon_ikhfaa_group: str = ""

    def __post_init__(self):
        self.noon_ikhfaa_group = (
            self.saad
            + self.thaal
            + self.thaa
            + self.kaf
            + self.jeem
            + self.sheen
            + self.qaf
            + self.seen
            + self.daal
            + self.taa_mofkhama
            + self.zay
            + self.faa
            + self.taa_marboota
            + self.daad
            + self.taa_mofkhama
        )


@dataclass
class UniqueRasmMap:
    rasm_map: list[dict[str, str]]
    imlaey_starts: list[str]


@dataclass
class Istiaatha:
    imlaey: str
    uthmani: str


@dataclass
class Sadaka:
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

BASE_PATH = Path(__file__).parent
alphabet_path = BASE_PATH / "quran-script/quran-alphabet.json"
with open(alphabet_path, "r", encoding="utf8") as f:
    alphabet_dict = json.load(f)
    imlaey = ImlaeyAlphabet(**alphabet_dict["imlaey"])
    uthmani = UthmaniAlphabet(**alphabet_dict["uthmani"])
    unique_rasm = UniqueRasmMap(**alphabet_dict["unique_rasm_map"])
    istiaatha = Istiaatha(**alphabet_dict["istiaatha"])
    sadaka = Sadaka(**alphabet_dict["sadaka"])
