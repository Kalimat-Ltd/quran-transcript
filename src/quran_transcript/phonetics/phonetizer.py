import re
from dataclasses import dataclass

from .operations import OPERATION_ORDER
from .moshaf_attributes import MoshafAttributes
from .sifa import process_sifat, SifaaOuput
from .. import alphabet as alph


@dataclass
class QuranPhoneticScriptOutput:
    phonemes: str
    sifat: list[SifaaOuput]


def quran_phonetizer(
    uhtmani_text: str, moshaf: MoshafAttributes, remove_sapce=False
) -> QuranPhoneticScriptOutput:
    text = uhtmani_text
    for op in OPERATION_ORDER:
        text = op.apply(text, moshaf)

    sifat = process_sifat(
        uthmani_script=uhtmani_text,
        phonetic_script=text,
        moshaf=moshaf,
    )

    if remove_sapce:
        text = re.sub(alph.uthmani.space, r"", text)

    return QuranPhoneticScriptOutput(phonemes=text, sifat=sifat)
