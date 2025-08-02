from dataclasses import dataclass, field
import re

from .conv_base_operation import ConversionOperation
from .moshaf_attributes import MoshafAttributes
from ..alphabet import uthmani as uth
from ..alphabet import phonetics as ph


@dataclass
class DisassembleHrofMoqatta(ConversionOperation):
    arabic_name: str = "فك الحروف المقطعة"
    regs: tuple[str, str] = ("", "")

    def forward(self, text, moshaf):
        for word, rep in uth.hrof_moqtaa_disassemble.items():
            text = re.sub(f"(^|{uth.space}){word}({uth.space}|$)", f"\\1{rep}\\2", text)
        return text


@dataclass
class SpecialCases(ConversionOperation):
    arabic_name: str = "فك الحالات الخاصة"
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [DisassembleHrofMoqatta()]
    )
    regs: tuple[str, str] = ("", "")

    def forward(self, text, moshaf: MoshafAttributes):
        for case in uth.special_patterns:
            pattern = case.pattern
            if case.pos == "start":
                pattern = r"^" + pattern
            elif case.pos == "end":
                pattern = pattern + r"$"

            if case.attr_name is not None:
                moshaf_attr = getattr(moshaf, case.attr_name)
                if moshaf_attr in case.opts:
                    rep_pattern = case.opts[moshaf_attr]
                else:
                    rep_pattern = pattern
            elif case.target_pattern is not None:
                rep_pattern = case.target_pattern

            text = re.sub(pattern, rep_pattern, text)

        return text


@dataclass
class SpecialWays(ConversionOperation):
    arabic_name: str = "الأوجه الخاصة لحفص"
    regs: tuple[str, str] = ("", "")

    def forward(self, text, moshaf):
        for word, rep in uth.hrof_moqtaa_disassemble.items():
            text = re.sub(f"(^|{uth.space}){word}({uth.space}|$)", f"\\1{rep}\\2", text)
        return text


@dataclass
class ConvertAlifMaksora(ConversionOperation):
    arabic_name: str = "تحويل الأف المقصورة إله: حضف أو ألف أو ياء"
    regs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            # حذف الأف المقصورة من الاسم المقصور النكرة
            (
                f"({uth.tanween_fath_modgham}|{uth.tanween_fath_iqlab}|{uth.tanween_fath_mothhar}){uth.alif_maksora}",
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
        f"(?!^){uth.hamzat_wasl}",
        r"",
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
                f"({uth.tanween_fath_modgham}|{uth.tanween_fath_iqlab}|{uth.tanween_fath_mothhar}){uth.alif}({uth.space}|$)",
                r"\1\2",
            ),
            # convert to alif at the end
            (
                f"({uth.tanween_fath_modgham}|{uth.tanween_fath_iqlab}|{uth.tanween_fath_mothhar})$",
                f"{uth.fatha}{uth.alif}",
            ),
        ]
    )


@dataclass
class WawAlsalah(ConversionOperation):
    arabic_name: str = "إبدال واو الصلاة ومثيلاتها ألفا"
    regs: tuple[str, str] = (
        f"{uth.waw}{uth.alif_khnjaria}",
        f"{uth.alif}",
    )


@dataclass
class EnlargeSmallLetters(ConversionOperation):
    arabic_name: str = (
        "تكبير الألف والياء والاو والنون الصغار مع حذف مد الصلة عند الوقف"
    )
    regs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            # small alif
            (
                uth.alif_khnjaria,
                uth.alif,
            ),
            # small noon
            (
                uth.small_noon,
                uth.noon,
            ),
            # small waw
            (
                f"{uth.haa}{uth.dama}{uth.small_waw}{uth.madd}?$",
                f"{uth.haa}{uth.dama}",
            ),
            (
                uth.small_waw,
                uth.waw,
            ),
            # Small yaa
            (
                uth.small_yaa,
                uth.small_yaa_sila,
            ),
            (
                f"{uth.haa}{uth.kasra}{uth.small_yaa_sila}{uth.madd}?$",
                f"{uth.haa}{uth.kasra}",
            ),
            (
                uth.small_yaa_sila,
                uth.yaa,
            ),
        ]
    )


@dataclass
class CleanEnd(ConversionOperation):
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [
            ConvertAlifMaksora(),
            NormalizeHmazat(),
            IthbatYaaYohie(),
            RemoveKasheeda(),
            RemoveSkoonMostadeer(),
            SkoonMostateel(),
            MaddAlewad(),
            WawAlsalah(),
            EnlargeSmallLetters(),
        ]
    )
    arabic_name: str = "تسكين حرف الوقف"
    regs: tuple[str, str] = (
        f"({'|'.join([uth.fatha, uth.dama, uth.kasra, uth.tanween_dam_modgham, uth.tanween_dam_iqlab, uth.tanween_dam_mothhar, uth.tanween_kasr_modgham, uth.tanween_kasr_iqlab, uth.tanween_kasr_mothhar, uth.madd])})$",
        r"",
    )


@dataclass
class NormalizeTaa(ConversionOperation):
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [
            CleanEnd(),
        ]
    )
    arabic_name: str = "تحويب التاء المربطة في الوسط لتاء وفي الآخر لهاء"
    regs: tuple[str, str] = field(
        default_factory=lambda: [
            (f"{uth.taa_marboota}$", f"{uth.haa}"),
            (f"{uth.taa_marboota}", f"{uth.taa_mabsoota}"),
        ]
    )


@dataclass
class AddAlifIsmAllah(ConversionOperation):
    arabic_name: str = "إضافة ألف مد الطبيعي في اسم الله عز وجل"
    regs: tuple[str, str] = (
        f"{uth.lam}({uth.kasra})?{uth.lam}{uth.shadda}{uth.fatha}{uth.haa}",
        f"{uth.lam}\\1{uth.lam}{uth.shadda}{uth.fatha}{uth.alif}{uth.haa}",
    )


@dataclass
class PrepareGhonnaIdghamIqlab(ConversionOperation):
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [
            SpecialCases(),
            RemoveHmzatWaslMiddle(),
            CleanEnd(),
            NormalizeTaa(),
            AddAlifIsmAllah(),
        ]
    )
    arabic_name: str = "فك الإقلاب والعغنة الإدغام"
    regs: tuple[str, str] = field(
        default_factory=lambda: [
            # النون المقلبة ميمام
            (
                f"{uth.noon}{uth.meem_iqlab}",
                f"{uth.meem}",
            ),
            # تنوين الفتح المقبل ميمام
            (
                # f"{uth.tanween_fath_iqlab}",
                # f"{uth.fatha}{uth.meem}",
                f"{uth.tanween_fath}.({uth.space}{uth.baa})",
                f"{uth.fatha}{uth.meem}\\1",
            ),
            #  فك تنوين الضم المقلب
            (
                # f"{uth.tanween_dam_iqlab}",
                # f"{uth.dama}{uth.meem}",
                f"{uth.tanween_dam}.({uth.space}{uth.baa})",
                f"{uth.dama}{uth.meem}\\1",
            ),
            #  فك تنوين الكسر المقلب ميما
            (
                # f"{uth.tanween_kasr_iqlab}",
                # f"{uth.kasra}{uth.meem}",
                f"{uth.tanween_kasr}.({uth.space}{uth.baa})",
                f"{uth.kasra}{uth.meem}\\1",
            ),
            # فك التنوين المدغم
            (
                # f"{uth.tanween_fath_modgham}",
                # f"{uth.fatha}{uth.noon}",
                f"{uth.tanween_fath}.({uth.space}[{uth.noon_ikhfaa_group}{uth.noon_idgham_group}])",
                f"{uth.fatha}{uth.noon}\\1",
            ),
            (
                # f"{uth.tanween_dam_modgham}",
                # f"{uth.dama}{uth.noon}",
                f"{uth.tanween_dam}.({uth.space}[{uth.noon_ikhfaa_group}{uth.noon_idgham_group}])",
                f"{uth.dama}{uth.noon}\\1",
            ),
            (
                # f"{uth.tanween_kasr_modgham}",
                # f"{uth.kasra}{uth.noon}",
                f"{uth.tanween_kasr}.({uth.space}[{uth.noon_ikhfaa_group}{uth.noon_idgham_group}])",
                f"{uth.kasra}{uth.noon}\\1",
            ),
            # فك التنوين المظهر
            (
                f"{uth.tanween_fath_mothhar}",
                f"{uth.fatha}{uth.noon}{uth.ras_haaa}",
            ),
            (
                f"{uth.tanween_dam_mothhar}",
                f"{uth.dama}{uth.noon}{uth.ras_haaa}",
            ),
            (
                f"{uth.tanween_kasr_mothhar}",
                f"{uth.kasra}{uth.noon}{uth.ras_haaa}",
            ),
            # حذف الحرف الأول من الحفران المدغمان
            (
                f"([{uth.fatha}{uth.dama}]{uth.yaa}|[{uth.fatha}{uth.kasra}]{uth.waw}|[{uth.pure_letters_without_yaa_and_waw_group}]){uth.space}?([{uth.pure_letters_group}]{uth.shadda})",
                r"\2",
            ),
        ]
    )


@dataclass
class IltiqaaAlsaknan(ConversionOperation):
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [
            PrepareGhonnaIdghamIqlab(),
        ]
    )
    arabic_name: str = "التقاء الساكنان وكسر التنوين"
    regs: list[tuple[str, str]] = field(
        default_factory=lambda: [
            # كسر التنوين
            (
                f"({uth.noon}){uth.ras_haaa}({uth.space}.[{uth.ras_haaa}{uth.shadda}])",
                f"\\1{uth.kasra}\\2",
            ),
            # حذف حرف المد الأول لاتقاء الساعكنان
            # alif
            (
                f"{uth.madd_alif}({uth.space}.[{uth.ras_haaa}{uth.shadda}])",
                f"{uth.fatha}\\1",
            ),
            # waw
            (
                f"{uth.madd_waw}({uth.space}.[{uth.ras_haaa}{uth.shadda}])",
                f"{uth.dama}\\1",
            ),
            # yaa
            (
                f"{uth.madd_yaa}({uth.space}.[{uth.ras_haaa}{uth.shadda}])",
                f"{uth.kasra}\\1",
            ),
        ]
    )


@dataclass
class Ghonna(ConversionOperation):
    ops_before: list[ConversionOperation] = field(
        default_factory=lambda: [
            IltiqaaAlsaknan(),
        ]
    )
    arabic_name: str = "وضع الغنة في النون الميم"
    regs: tuple[str, str] = ("", "")
    ghonna_len: int = 3
    idgham_yaa_waw_len: int = 2

    def forward(self, text, moshaf: MoshafAttributes) -> str:
        # الميم المخفار
        if moshaf.meem_mokhfah == "meem":
            meem_mokhfah = ph.meem
        elif moshaf.meem_mokhfah == "ikhfaa":
            meem_mokhfah = ph.meem_mokhfah
        else:
            raise ValueError()
        text = re.sub(
            f"{uth.meem}{uth.space}?{uth.baa}",
            f"{meem_mokhfah * self.ghonna_len}{uth.baa}",
            text,
        )

        # إدغام النون في الياء و الواو
        text = re.sub(
            f"{uth.noon}{uth.space}([{uth.yaa}{uth.waw}])",
            r"\1" * (self.idgham_yaa_waw_len + 1),
            text,
        )

        # إخفاء النون
        text = re.sub(
            f"{uth.noon}{uth.space}?([{uth.noon_ikhfaa_group}])",
            f"{ph.noon_mokhfah * self.ghonna_len}\\1",
            text,
        )

        # النون والميم المشددتين
        text = re.sub(
            f"([{uth.meem}{uth.noon}]){uth.shadda}",
            r"\1" * (self.ghonna_len + 1),
            text,
        )

        return text


OPERATION_ORDER = [
    DisassembleHrofMoqatta(),
    SpecialCases(),
    ConvertAlifMaksora(),
    NormalizeHmazat(),
    IthbatYaaYohie(),
    RemoveKasheeda(),
    RemoveHmzatWaslMiddle(),
    RemoveSkoonMostadeer(),
    SkoonMostateel(),
    MaddAlewad(),
    WawAlsalah(),
    EnlargeSmallLetters(),
    CleanEnd(),
    NormalizeTaa(),
    AddAlifIsmAllah(),
    PrepareGhonnaIdghamIqlab(),
    IltiqaaAlsaknan(),
    Ghonna(),
]
