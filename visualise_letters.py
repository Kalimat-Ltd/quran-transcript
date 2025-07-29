import re

from quran_transcript import Aya
import quran_transcript.alphabet as alph
from quran_transcript.phonetics.operations import (
    ConvertAlifMaksora,
    ConversionOperation,
    NormalizeHmazat,
)
from quran_transcript.phonetics.moshaf_attributes import MoshafAttributes


def get_occurance(char: str, operations: list[ConversionOperation] = [], context=4):
    moshaf = MoshafAttributes(
        rewaya="hafs",
        madd_monfasel_len=4,
        madd_mottasel_len=4,
        madd_mottasel_waqf=4,
        madd_aared_len=4,
    )

    start_aya = Aya()
    counter = 0
    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
        for op in operations:
            txt = op.apply(txt, moshaf)
        outs = re.finditer(char, txt)
        first = True
        for out in outs:
            if first:
                print(aya)
                first = False
            counter += 1
            print(f"Case: `{counter}`")
            print(out)
            print(aya.get().uthmani[: out.start() + context])

            print("-" * 30)
            print()
            print()


def get_missing_cases(
    char: str, regs: list[str], operations: list[ConversionOperation] = []
):
    moshaf = MoshafAttributes(
        rewaya="hafs",
        madd_monfasel_len=4,
        madd_mottasel_len=4,
        madd_mottasel_waqf=4,
        madd_aared_len=4,
    )

    start_aya = Aya()
    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
        for op in operations:
            txt = op.apply(txt, moshaf)
        if char in txt:
            main_outs = re.finditer(char, txt)
            found = False
            for main_out in main_outs:
                txt_part = txt[: main_out.start() + len(char) + 5]
                for reg in regs:
                    re_out = re.search(reg, txt_part)
                    if re_out:
                        found = True
                        break
                if not found:
                    print(aya)
                    print(txt_part)
                    print("-" * 30)
                    print()
                    print()


if __name__ == "__main__":
    # get_occurance(alph.uthmani.alif_maksora)
    get_missing_cases(
        alph.uthmani.alif_maksora,
        [
            f"{alph.uthmani.fatha}{alph.uthmani.alif_maksora}({alph.uthmani.space}|$)",
            f"{alph.uthmani.alif_maksora}{alph.uthmani.alif_khnjaria}",
            f"{alph.uthmani.kasra}{alph.uthmani.alif_maksora}",
            f"{alph.uthmani.alif_maksora}([{alph.uthmani.harakat_group}{alph.uthmani.ras_haaa}{alph.uthmani.shadda}{alph.uthmani.tanween_dam}{alph.uthmani.madd}])",
            f"({alph.uthmani.tanween_fath_mothhar}|{alph.uthmani.tanween_fath_modgham}){alph.uthmani.alif_maksora}",
        ],
    )

    # # yass + kasra at the end of the word
    # get_occurance(
    #     alph.uthmani.yaa + alph.uthmani.kasra + "(\s|$)",
    #     operations=[ConvertAlifMaksora()],
    #     context=10,
    # )

    # يحي
    get_occurance(
        f"[{alph.uthmani.hamza}{alph.uthmani.noon}{alph.uthmani.yaa}{alph.uthmani.taa_mabsoota}]{alph.uthmani.dama}{alph.uthmani.haa_mohmala}{alph.uthmani.ras_haaa}{alph.uthmani.yaa}{alph.uthmani.kasra}({alph.uthmani.space}|$)",
        operations=[ConvertAlifMaksora(), NormalizeHmazat()],
        context=10,
    )
