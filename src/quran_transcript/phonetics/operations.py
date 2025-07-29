from dataclasses import dataclass, field

from .conv_base_operation import ConversionOperation
from ..alphabet import uthmani as uth
from ..alphabet import phonetics as ph


@dataclass
class ConvertAlifMaksora(ConversionOperation):
    arabic_name: str = "تحويل الأف المقصورة إله: حضف أو ألف أو ياء"
    regs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            # حذف الأف المقصورة من الاسم المقصور النكرة
            (
                f"({uth.tanween_fath_mothhar}|{uth.tanween_fath_modgham}){uth.alif_maksora}",
                r"\1",
            ),
            # تحويلا الألف المقصورة المحضوفة وصلا إلى ألف
            (
                f"({uth.fatha}){uth.alif_maksora}({uth.space}|$)",
                f"\\1{uth.alif}\\2",
            ),
            # تحويل الألف الخنرجية في السم المقصور لألف
            (
                f"{uth.alif_maksora}{uth.alif_khnjaria}",
                f"{uth.alif}",
            ),
            # تحويلا الألف المقصورة المسبوقة بكسرة إلي ياء
            (
                f"{uth.kasra}{uth.alif_maksora}",
                f"{uth.kasra}{uth.yaa}",
            ),
            # ياء
            (
                f"{uth.alif_maksora}([{uth.harakat_group}{uth.ras_haaa}{uth.shadda}{uth.tanween_dam}{uth.madd}])",
                f"{uth.yaa}\\1",
            ),
        ]
    )


@dataclass
class NormalizeHmazat(ConversionOperation):
    arabic_name: str = "توحيد الهمزات"
    regs: tuple[str, str] = (
        f"[{uth.hamazat_group}]",
        f"{uth.hamza}",
    )


@dataclass
class IthbatYaaYohie(ConversionOperation):
    arabic_name: str = "إثبات الياء في أفعال المضارعة: نحي"
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [ConvertAlifMaksora(), NormalizeHmazat()]
    )
    regs: tuple[str, str] = (
        f"([{uth.hamza}{uth.noon}{uth.yaa}{uth.taa_mabsoota}]{uth.dama}{uth.haa_mohmala}{uth.ras_haaa}{uth.yaa}{uth.kasra})({uth.space}|$)",
        f"\\1{uth.yaa}\\2",
    )


@dataclass
class RemoveKasheeda(ConversionOperation):
    arabic_name: str = "حذف الكشيدة"
    regs: tuple[str, str] = (
        f"{uth.kasheeda}",
        "",
    )


@dataclass
class RemoveHmzatWaslMiddle(ConversionOperation):
    arabic_name: str = "حذف همزة الوصل وصلا"
    regs: tuple[str, str] = (
        f"({uth.space}){uth.hamzat_wasl}",
        r"\1",
    )


@dataclass
class RemoveSkoonMostadeer(ConversionOperation):
    arabic_name: str = "حذف الحرف أعلاه سكون مستدير"
    regs: tuple[str, str] = (
        f"(.){uth.skoon_mostadeer}",
        r"",
    )


@dataclass
class SkoonMostateel(ConversionOperation):
    arabic_name: str = "ضبط السكون المستطيل"
    regs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            # remove from the middle
            (
                f"{uth.alif}{uth.skoon_mostateel}{uth.space}",
                f"{uth.space}",
            ),
            # convert to alif at the end
            (
                f"{uth.alif}{uth.skoon_mostateel}$",
                f"{uth.alif}",
            ),
        ]
    )


@dataclass
class MaddAlewad(ConversionOperation):
    arabic_name: str = "ضبط مد العوض وسطا ووقفا"
    regs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            # remove from the middle
            (
                f"({uth.tanween_fath_modgham}|{uth.tanween_fath_mothhar}){uth.alif}({uth.space}|$)",
                r"\1\2",
            ),
            # convert to alif at the end
            (
                f"({uth.tanween_fath_modgham}|{uth.tanween_fath_mothhar})$",
                f"{uth.fatha}{uth.alif}",
            ),
        ]
    )


OPERATION_ORDER = [
    ConvertAlifMaksora(),
    NormalizeHmazat(),
    IthbatYaaYohie(),
    RemoveKasheeda(),
    RemoveHmzatWaslMiddle(),
    RemoveSkoonMostadeer(),
    SkoonMostateel(),
    MaddAlewad(),
]
