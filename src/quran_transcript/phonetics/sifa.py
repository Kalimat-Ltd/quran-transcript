from typing import Literal
from pydantic import BaseModel
import re

from .moshaf_attributes import MoshafAttributes
from ..alphabet import phonetics as ph
from ..alphabet import uthmani as uth
from ..alphabet import phonetic_groups as phg


class SifaaOuput(BaseModel):
    phonemes: str
    hams_or_jahr: Literal["hams", "jahr"]
    shidda_or_rakhawa: Literal["shadeed", "between", "rikhw"]
    tafkheem_or_taqeeq: Literal["mofakham", "moraqaq"]
    itbaq: Literal["monfateh", "motbaq"]
    safeer: Literal["safeer", "no_safeer"]
    qalqla: Literal["moqalqal", "not_moqalqal"]
    tikraar: Literal["mokarar", "not_mokarar"]
    tafashie: Literal["motafashie", "not_motafashie"]
    istitala: Literal["mostateel", "not_mostateel"]
    ghonna: Literal["maghnoon", "not_maghnoon"]


def chunck_phonemes(phonetic_script: str) -> list[str]:
    core_group = "|".join([f"{c}+" for c in phg.core])
    return re.findall(f"((?:{core_group})[{phg.residuals}]?)", phonetic_script)


def parse_tafkheem_sifa(
    phonemes: list[str], idx: int
) -> Literal["mofakham", "moraqaq"]:
    p_group = phonemes[idx]

    # ghonna for noon
    if p_group[0] == ph.noon_mokhfah:
        if idx == 0:
            raise ValueError(f"Noon Mokhfaa comes in the middle not at the start")
        elif idx == len(phonemes) - 1:
            raise ValueError(f"Noon Mokhfaa comes in the middle not at the end")
        elif phonemes[idx + 1][0] in phg.tafkheem:
            return "mofakham"
        else:
            return "moraqaq"

    # alif
    if p_group[0] == ph.alif:
        if idx == 0:
            raise ValueError(
                f"For Letter alif: `{ph.alif}` can not start  a phoneme script"
            )
        elif phonemes[idx - 1][0] in phg.tafkheem:
            return "mofakham"
        else:
            return "moraqaq"

    # اسم الله
    # letter raa
    return "mofakham" if phonemes[idx][0] in phg.tafkheem else "moraqaq"


def lam_tafkheem_tarqeeq_finder(
    phonetic_script_with_space: str,
) -> list[Literal["mofakham", "moraqaq"]]:
    """findes lam in script and returns tafkheem or tarqeeq for
    every lam

    This specially created to handel lam of the name of Allah
    """
    phoneme_with_laam_Allh_reg = f"(?<!{ph.jeem})(?<!{ph.daal})(?<!{ph.taa}{ph.fatha}{ph.waw})(.{uth.space}?{ph.lam}{{2}}){ph.fatha}{ph.alif}{{2,6}}{ph.haa}(?!{ph.dama}{ph.meem}(?!{ph.meem}))"
    laam_reg = f"({ph.lam}+)[{phg.residuals}]?"

    lam_poses = []
    for match in re.finditer(laam_reg, phonetic_script_with_space):
        lam_poses.append(match.start(1))

    pos_to_phoneme_before_lam_Allah = {}
    for match in re.finditer(phoneme_with_laam_Allh_reg, phonetic_script_with_space):
        pos = match.end(1) - 2
        pos_to_phoneme_before_lam_Allah[pos] = match.group(1)[0]

    outputs = []
    for lam_pos in lam_poses:
        if lam_pos in pos_to_phoneme_before_lam_Allah:
            if pos_to_phoneme_before_lam_Allah[lam_pos] == ph.kasra:
                outputs.append("moraqaq")
            else:
                outputs.append("mofakham")
        else:
            outputs.append("moraqaq")
    return outputs

    # ph_or_lam_list = re.findall(
    #     "|".join([phoneme_before_laam_Allh_reg, laam_reg]), phonetic_script_with_space
    # )
    # print(ph_or_lam_list)
    #
    # outputs = []
    # for phoneme, lam in ph_or_lam_list:
    #     if phoneme:
    #         if phoneme == ph.kasra:
    #             outputs.append("moraqaq")
    #         else:
    #             outputs.append("mofakham")
    #     elif lam:
    #         outputs.append("moraqaq")
    #
    # return outputs


def alif_tafkheem_tarqeeq_finder(
    phonetic_script_with_space: str,
) -> list[Literal["mofakham", "moraqaq"] | None]:
    """findes lam in script and returns tafkheem or tarqeeq for
    every madd alif

    This specially created to handel alif after lam اسم الله
    """
    phoneme_with_laam_Allh_reg = f"(?<!{ph.jeem})(?<!{ph.daal})(?<!{ph.taa}{ph.fatha}{ph.waw})(.){uth.space}?{ph.lam}{{2}}{ph.fatha}({ph.alif}{{2,6}}){ph.haa}(?!{ph.dama}{ph.meem}(?!{ph.meem}))"
    alif_reg = f"{ph.fatha}({ph.alif}{{2,6}})"

    alif_poses = []
    for match in re.finditer(alif_reg, phonetic_script_with_space):
        alif_poses.append(match.start(1))

    pos_to_phoneme_before_lam_Allah = {}
    for match in re.finditer(phoneme_with_laam_Allh_reg, phonetic_script_with_space):
        pos = match.start(2)
        pos_to_phoneme_before_lam_Allah[pos] = match.group(1)

    outputs = []
    for alif_pos in alif_poses:
        if alif_pos in pos_to_phoneme_before_lam_Allah:
            if pos_to_phoneme_before_lam_Allah[alif_pos] == ph.kasra:
                outputs.append("moraqaq")
            else:
                outputs.append("mofakham")
        else:
            outputs.append(None)
    return outputs


# TODO: add state for letter raaa
def process_sifat(phonetic_script: str, moshaf: MoshafAttributes) -> list[SifaaOuput]:
    phonenemes_groups = chunck_phonemes(phonetic_script)
    outputs = []
    lam_tafkheem_and_tarqeeq = lam_tafkheem_tarqeeq_finder(phonetic_script)
    alif_tafkheem_and_tarqeeq = alif_tafkheem_tarqeeq_finder(phonetic_script)
    lam_idx = 0
    alif_idx = 0
    for idx in range(len(phonenemes_groups)):
        p = phonenemes_groups[idx][0]
        hams = "hams" if p in phg.hams else "jahr"
        shidda = (
            "shadeed"
            if p in phg.shidda
            else "between"
            if p in phg.between_shidda_rakhawa
            else "rikhw"
        )

        tafkheem = parse_tafkheem_sifa(phonenemes_groups, idx)
        if phonenemes_groups[idx][0] == ph.lam:
            tafkheem = lam_tafkheem_and_tarqeeq[lam_idx]
            lam_idx += 1
        if phonenemes_groups[idx][0] == ph.alif:
            alif_state = alif_tafkheem_and_tarqeeq[alif_idx]
            if alif_state is not None:
                tafkheem = alif_state
            alif_idx += 1

        itbaq = "motbaq" if p in phg.itbaaq else "monfateh"
        safeer = "safeer" if p in phg.safeer else "no_safeer"
        qalqa = (
            "moqalqal"
            if phonenemes_groups[idx][-1] not in phg.harakat and p in phg.qalqal
            else "not_moqalqal"
        )
        tikrar = "mokarar" if p in phg.tikrar else "not_mokarar"
        tafashie = "motafashie" if p in phg.tafashie else "not_motafashie"
        istitala = "mostateel" if p in phg.istitala else "not_mostateel"
        ghonna = "maghnoon" if p in phg.ghonna else "not_maghnoon"
        outputs.append(
            SifaaOuput(
                phonemes=phonenemes_groups[idx],
                hams_or_jahr=hams,
                shidda_or_rakhawa=shidda,
                tafkheem_or_taqeeq=tafkheem,
                itbaq=itbaq,
                safeer=safeer,
                qalqla=qalqa,
                tikraar=tikrar,
                tafashie=tafashie,
                istitala=istitala,
                ghonna=ghonna,
            )
        )

    return outputs
