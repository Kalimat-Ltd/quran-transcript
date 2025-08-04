import re

from .operations import OPERATION_ORDER
from .moshaf_attributes import MoshafAttributes
from .. import alphabet as alph


def quran_phonetizer(
    uhtmani_text: str, moshaf: MoshafAttributes, remove_sapce=False
) -> str:
    text = uhtmani_text
    for op in OPERATION_ORDER:
        text = op.apply(text, moshaf)

    if remove_sapce:
        text = re.sub(alph.uthmani.space, r"", text)

    return text
