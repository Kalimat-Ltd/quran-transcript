from dataclasses import dataclass

from .conv_base_operation import ConversionOperation
from ..alphabet import uthmani as uth
from ..alphabet import phonetics as ph


@dataclass
class RemoveKasheeda:
    name: str = "RemoveKasheeda"


@dataclass
class RemoveAlifMaksoraFromIsmMaksorNakira(ConversionOperation):
    name: str = "RemoveAlifMaksoraFromIsmMaksorNakira"
    arabic_name: str = "حذف الألف المفصوبة من الاسم المقصور النكرة"
    input_regs: str = (
        f"({uth.tanween_fath_mothhar}|{uth.tanween_fath_modgham}){uth.alif_maksora}"
    )
    output_regs: str = r"\1"

@dataclass
class RemoveAlifMa
