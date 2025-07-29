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
    taa_mofakhama: str
    zaa_mofakhama: str
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

    # تنوين مظهر وتنوين مدغم
    tanween_fath_mothhar: str = ""
    tanween_dam_mothhar: str = ""
    tanween_kasr_mothhar: str = ""
    tanween_fath_modgham: str = ""
    tanween_dam_modgham: str = ""
    tanween_kasr_modgham: str = ""

    # letters groups
    noon_ikhfaa_group: str = ""
    harakat_group: str = ""  # حركات
    hamazat_group: str = ""

    def __post_init__(self):
        # Groups
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
            + self.taa_mofakhama
            + self.zay
            + self.faa
            + self.taa_marboota
            + self.daad
            + self.taa_mofakhama
        )
        self.harakat_group = self.fatha + self.dama + self.kasra
        self.hamazat_group = (
            self.hamza
            + self.hamza_above_alif
            + self.hamza_below_alif
            + self.hamza_above_waw
            + self.hamza_above_yaa
            + self.hamza_mamdoda
        )

        # تنوين مظهر وتنوين مدغم
        self.tanween_fath_mothhar = self.tanween_fath
        self.tanween_dam_mothhar = self.tanween_dam
        self.tanween_kasr_mothhar = self.tanween_kasr

        self.tanween_fath_modgham = self.tanween_fath + self.tanween_idhaam_dterminer
        self.tanween_dam_modgham = self.tanween_dam + self.tanween_idhaam_dterminer
        self.tanween_kasr_modgham = self.tanween_kasr + self.tanween_idhaam_dterminer


@dataclass
class QuranPhoneticScriptAlphabet:
    hamza: str
    baa: str
    taa: str
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
    taa_mofakhama: str
    zaa_mofakhama: str
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

    # Madd group
    alif: str
    yaa_madd: str
    waw_madd: str

    # Harakat
    fatha: str
    dama: str
    kasra: str

    # special charcters
    fatha_momala: str
    alif_momala: str
    hamza_mosahala: str
    qlqla: str
    noon_mokhfa: str
    meem_mokhfa: str
    sakt: str


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
    phonetics = QuranPhoneticScriptAlphabet(
        hamza=uthmani.hamza,
        baa=uthmani.baa,
        taa=uthmani.taa_mabsoota,
        thaa=uthmani.thaa,
        jeem=uthmani.jeem,
        haa_mohmala=uthmani.haa_mohmala,
        khaa=uthmani.khaa,
        daal=uthmani.daal,
        thaal=uthmani.thaal,
        raa=uthmani.raa,
        zay=uthmani.zay,
        seen=uthmani.seen,
        sheen=uthmani.sheen,
        saad=uthmani.saad,
        daad=uthmani.daad,
        taa_mofakhama=uthmani.taa_mofakhama,
        zaa_mofakhama=uthmani.zaa_mofakhama,
        ayn=uthmani.ayn,
        ghyn=uthmani.ghyn,
        faa=uthmani.faa,
        qaf=uthmani.qaf,
        kaf=uthmani.kaf,
        lam=uthmani.lam,
        meem=uthmani.meem,
        noon=uthmani.noon,
        haa=uthmani.haa,
        waw=uthmani.waw,
        yaa=uthmani.yaa,
        alif=uthmani.alif,
        yaa_madd=uthmani.small_yaa_sila,
        waw_madd=uthmani.small_waw,
        fatha=uthmani.fatha,
        dama=uthmani.dama,
        kasra=uthmani.kasra,
        fatha_momala=uthmani.imala_sign,
        alif_momala=uthmani.kasheeda,
        hamza_mosahala=uthmani.tasheel_sign,
        qlqla="\u066f",  # dotless qaf "ٯ"
        noon_mokhfa=uthmani.small_noon,
        meem_mokhfa=uthmani.meem_iqlab,
        sakt=uthmani.small_seen_above,
    )
