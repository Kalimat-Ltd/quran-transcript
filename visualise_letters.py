import re

from quran_transcript import Aya
import quran_transcript.alphabet as alph


def get_occurance(char: str):
    start_aya = Aya()
    for aya in start_aya.get_ayat_after(114):
        outs = re.finditer(char, aya.get().uthmani)
        first = True
        for out in outs:
            if first:
                print(aya)
                first = False
            print(out)
            print(aya.get().uthmani[: out.start()])

            print("-" * 30)
            print()
            print()


def get_missing_cases(char: str, regs: list[str]):
    start_aya = Aya()
    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
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
            f"{alph.uthmani.alif_maksora}[{alph.uthmani.harakat_group}{alph.uthmani.madd}{alph.uthmani.ras_haaa}{alph.uthmani.shadda}{alph.uthmani.tanween_dam}]",
            f"({alph.uthmani.tanween_fath_mothhar}|{alph.uthmani.tanween_fath_modgham}){alph.uthmani.alif_maksora}",
        ],
    )
