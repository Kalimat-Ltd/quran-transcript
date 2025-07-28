from pathlib import Path
import json
from dataclasses import asdict

from quran_transcript.alphabet import UthmaniAlphabet
from quran_transcript import Aya


def get_uthmani_alpabet() -> list[str]:
    aya = Aya(1, 1)
    alphabet = set()
    for aya in aya.get_ayat_after(114):
        alphabet |= set(aya.get().uthmani)
    return sorted(alphabet)


if __name__ == "__main__":
    alphabet_path = "./quran-script/quran-alphabet.json"
    uth_alph = get_uthmani_alpabet()

    uthmani_alphabet = UthmaniAlphabet(
        space=uth_alph[0],
        hamza=uth_alph[1],
        hamza_above_alif=uth_alph[2],
        hamza_above_waw=uth_alph[3],
        hamza_below_alif=uth_alph[4],
        hamza_above_yaa=uth_alph[5],
        alif=uth_alph[6],
        baa=uth_alph[7],
        taa_marboota=uth_alph[8],
        taa_mabsoota=uth_alph[9],
        thaa=uth_alph[10],
        jeem=uth_alph[11],
        haa_mohmala=uth_alph[12],
        khaa=uth_alph[13],
        daal=uth_alph[14],
        thaal=uth_alph[15],
        raa=uth_alph[16],
        zay=uth_alph[17],
        seen=uth_alph[18],
        sheen=uth_alph[19],
        saad=uth_alph[20],
        daad=uth_alph[21],
        taa_mofkhama=uth_alph[22],
        zaa_mofkhama=uth_alph[23],
        ayn=uth_alph[24],
        ghyn=uth_alph[25],
        kasheeda=uth_alph[26],
        faa=uth_alph[27],
        qaf=uth_alph[28],
        kaf=uth_alph[29],
        lam=uth_alph[30],
        meem=uth_alph[31],
        noon=uth_alph[32],
        haa=uth_alph[33],
        waw=uth_alph[34],
        alif_maksora=uth_alph[35],
        yaa=uth_alph[36],
        tanween_fath=uth_alph[37],
        tanween_dam=uth_alph[38],
        tanween_kasr=uth_alph[39],
        fatha=uth_alph[40],
        dama=uth_alph[41],
        kasra=uth_alph[42],
        shadda=uth_alph[43],
        ras_haaa=uth_alph[44],
        madd=uth_alph[45],
        hamza_mamdoda=uth_alph[46],
        alif_khnjaria=uth_alph[47],
        hamzat_wasl=uth_alph[48],
        small_seen_above=uth_alph[49],
        skoon_mostadeer=uth_alph[50],
        skoon_mostateel=uth_alph[51],
        meem_iqlab=uth_alph[52],
        small_seen_below=uth_alph[53],
        small_waw=uth_alph[54],
        small_yaa_sila=uth_alph[55],
        small_yaa=uth_alph[56],
        small_noon=uth_alph[57],
        imala_sign=uth_alph[58],
        ishmam_sign=uth_alph[59],
        tasheel_sign=uth_alph[60],
        tanween_idhaam_dterminer=uth_alph[61],
    )

    assert set(uth_alph) == set(asdict(uthmani_alphabet).values())

    with open(alphabet_path, "r", encoding="utf-8") as f:
        alphabet = json.load(f)
    alphabet["uthmani"] = asdict(uthmani_alphabet)
    with open(alphabet_path, "w+", encoding="utf-8") as f:
        alphabet = json.dump(alphabet, f, indent=2, ensure_ascii=False)
