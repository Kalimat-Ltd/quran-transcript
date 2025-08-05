from typing import Literal
from pydantic import BaseModel
import re

from .moshaf_attributes import MoshafAttributes
from ..alphabet import phonetics as ph
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


# TODO:
def parse_tafkheem_sifa(
    phonemes: list[str], idx: int
) -> Literal["mofakham", "moraqaq"]:
    return "mofakham" if phonemes[idx][0] in phg.tafkheem else "moraqaq"


# TODO: add state for letter raaa
def process_sifat(phonetic_script: str, moshaf: MoshafAttributes) -> list[SifaaOuput]:
    phonenemes_groups = chunck_phonemes(phonetic_script)
    outputs = []
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
