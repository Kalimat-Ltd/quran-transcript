import pytest

from quran_transcript import Aya, WordSpan
from quran_transcript.utils import SegmentScripts, QuranWordIndex
from quran_transcript.tasmeea import check_sura_missing_parts


@pytest.mark.parametrize(
    "aya, start, end, istiaatha, bismillah, sadaka, exp_uth_text",
    [
        (
            Aya(1, 1),
            0,
            None,
            False,
            False,
            False,
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
        ),
        (
            Aya(1, 1),
            0,
            None,
            True,
            False,
            False,
            "أَعُوذُ بِٱللَّهِ مِنَ ٱلشَّيْطَانِ ٱلرَّجِيمِ" + " " + "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
        ),
        (
            Aya(1, 7),
            0,
            None,
            False,
            False,
            True,
            "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ"
            + " "
            + "صَدَقَ ٱللَّهُ ٱلْعَظِيمُ",
        ),
        (
            Aya(1, 7),
            3,
            8,
            False,
            False,
            True,
            "عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا",
        ),
        (
            Aya(1, 7),
            8,
            10,
            False,
            False,
            True,
            "ٱلضَّآلِّينَ" + " " + "صَدَقَ",
        ),
        (
            Aya(2, 21),
            0,
            None,
            False,
            False,
            False,
            "يَـٰٓأَيُّهَا ٱلنَّاسُ ٱعْبُدُوا۟ رَبَّكُمُ ٱلَّذِى خَلَقَكُمْ وَٱلَّذِينَ مِن قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ",
        ),
        (
            Aya(2, 21),
            0,
            None,
            True,
            True,
            False,
            "يَـٰٓأَيُّهَا ٱلنَّاسُ ٱعْبُدُوا۟ رَبَّكُمُ ٱلَّذِى خَلَقَكُمْ وَٱلَّذِينَ مِن قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ",
        ),
        (
            Aya(20, 94),
            0,
            None,
            False,
            False,
            False,
            "قَالَ يَبْنَؤُمَّ لَا تَأْخُذْ بِلِحْيَتِى وَلَا بِرَأْسِىٓ إِنِّى خَشِيتُ أَن تَقُولَ فَرَّقْتَ بَيْنَ بَنِىٓ إِسْرَٰٓءِيلَ وَلَمْ تَرْقُبْ قَوْلِى",
        ),
        (
            Aya(20, 94),
            0,
            5,
            False,
            False,
            False,
            "قَالَ يَبْنَؤُمَّ لَا",
        ),
        (
            Aya(22, 56),
            0,
            None,
            False,
            False,
            False,
            "ٱلْمُلْكُ يَوْمَئِذٍۢ لِّلَّهِ يَحْكُمُ بَيْنَهُمْ فَٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّـٰلِحَـٰتِ فِى جَنَّـٰتِ ٱلنَّعِيمِ",
        ),
        (
            Aya(22, 56),
            3,
            7,
            False,
            False,
            False,
            "يَحْكُمُ بَيْنَهُمْ فَٱلَّذِينَ ءَامَنُوا۟",
        ),
        (
            Aya(2, 31),
            0,
            None,
            False,
            False,
            False,
            "وَعَلَّمَ ءَادَمَ ٱلْأَسْمَآءَ كُلَّهَا ثُمَّ عَرَضَهُمْ عَلَى ٱلْمَلَـٰٓئِكَةِ فَقَالَ أَنۢبِـُٔونِى بِأَسْمَآءِ هَـٰٓؤُلَآءِ إِن كُنتُمْ صَـٰدِقِينَ",
        ),
        (
            Aya(2, 31),
            9,
            None,
            False,
            False,
            False,
            "أَنۢبِـُٔونِى بِأَسْمَآءِ هَـٰٓؤُلَآءِ إِن كُنتُمْ صَـٰدِقِينَ",
        ),
        (
            Aya(47, 38),
            0,
            None,
            False,
            False,
            False,
            "هَـٰٓأَنتُمْ هَـٰٓؤُلَآءِ تُدْعَوْنَ لِتُنفِقُوا۟ فِى سَبِيلِ ٱللَّهِ فَمِنكُم مَّن يَبْخَلُ وَمَن يَبْخَلْ فَإِنَّمَا يَبْخَلُ عَن نَّفْسِهِۦ وَٱللَّهُ ٱلْغَنِىُّ وَأَنتُمُ ٱلْفُقَرَآءُ وَإِن تَتَوَلَّوْا۟ يَسْتَبْدِلْ قَوْمًا غَيْرَكُمْ ثُمَّ لَا يَكُونُوٓا۟ أَمْثَـٰلَكُم",
        ),
        (
            Aya(47, 38),
            0,
            5,
            False,
            False,
            False,
            "هَـٰٓأَنتُمْ هَـٰٓؤُلَآءِ تُدْعَوْنَ لِتُنفِقُوا۟",
        ),
        (
            Aya(72, 16),
            0,
            None,
            False,
            False,
            False,
            "وَأَلَّوِ ٱسْتَقَـٰمُوا۟ عَلَى ٱلطَّرِيقَةِ لَأَسْقَيْنَـٰهُم مَّآءً غَدَقًۭا",
        ),
        (
            Aya(72, 16),
            0,
            4,
            False,
            False,
            False,
            "وَأَلَّوِ ٱسْتَقَـٰمُوا۟ عَلَى",
        ),
    ],
)
def test_imlaey_to_uthmani(
    aya: Aya,
    start: int,
    end: int | None,
    istiaatha: bool,
    bismillah: bool,
    sadaka: bool,
    exp_uth_text: str,
):
    wordspan = WordSpan(start=start, end=end)
    out_uth_str = aya.imlaey_to_uthmani(
        wordspan,
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    print(out_uth_str)
    assert out_uth_str == exp_uth_text


def test_imlaey_to_uthmai_with_caching():
    aya = Aya(72, 16)
    start = 0
    end = None
    istiaatha = False
    bismillah = False
    sadaka = False
    expected_uthmani = "وَأَلَّوِ ٱسْتَقَـٰمُوا۟ عَلَى ٱلطَّرِيقَةِ لَأَسْقَيْنَـٰهُم مَّآءً غَدَقًۭا"

    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani

    start = 0
    end = 3
    istiaatha = False
    bismillah = False
    sadaka = False
    expected_uthmani = "وَأَلَّوِ ٱسْتَقَـٰمُوا۟"
    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani

    start = 0
    end = 3
    istiaatha = True
    bismillah = False
    sadaka = False
    expected_uthmani = "وَأَلَّوِ ٱسْتَقَـٰمُوا۟"
    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani


def test_imlaey_to_uthmai_with_caching_istiaahta():
    aya = Aya(1, 1)
    start = 0
    end = None
    istiaatha = False
    bismillah = False
    sadaka = False
    expected_uthmani = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"

    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani

    istiaatha = True
    bismillah = False
    sadaka = False
    expected_uthmani = "أَعُوذُ بِٱللَّهِ مِنَ ٱلشَّيْطَانِ ٱلرَّجِيمِ" + " " + "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani


def test_imlaey_to_uthmai_with_caching_sadaka():
    aya = Aya(1, 7)
    start = 0
    end = None
    istiaatha = False
    bismillah = False
    sadaka = False
    expected_uthmani = "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ"

    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani

    istiaatha = False
    bismillah = False
    sadaka = True
    expected_uthmani = (
        "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ" + " " + "صَدَقَ ٱللَّهُ ٱلْعَظِيمُ"
    )
    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani


def test_imlaey_to_uthmai_with_caching_bismlillah():
    aya = Aya(2, 1)
    start = 0
    end = None
    istiaatha = False
    bismillah = False
    sadaka = False
    expected_uthmani = "الٓمٓ"

    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani

    istiaatha = False
    bismillah = True
    sadaka = True
    expected_uthmani = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ" + " " + "الٓمٓ"
    out_uthmni = aya.imlaey_to_uthmani(
        WordSpan(start, end),
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_uthmni == expected_uthmani


@pytest.mark.parametrize(
    "aya, start, window, istiaatha, bismillah, sadaka, ex_segment_scripts",
    [
        # sadaka with no quran
        (
            Aya(112, 4),
            6,
            2,
            False,
            False,
            True,
            SegmentScripts(
                imalaey="اللَّهُ الْعَظِيمُ",
                uthmani="ٱللَّهُ ٱلْعَظِيمُ",
                start_span=None,
                end_span=None,
                has_quran=False,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=True,
            ),
        ),
        # istiaatha with no quran
        (
            Aya(50, 1),
            0,
            5,
            True,
            True,
            False,
            SegmentScripts(
                imalaey="أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ",
                uthmani="أَعُوذُ بِٱللَّهِ مِنَ ٱلشَّيْطَانِ ٱلرَّجِيمِ",
                start_span=None,
                end_span=None,
                has_quran=False,
                has_istiaatha=True,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        # bimillah with no quran
        (
            Aya(20, 1),
            0,
            4,
            False,
            True,
            False,
            SegmentScripts(
                imalaey="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                uthmani="بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                start_span=None,
                end_span=None,
                has_quran=False,
                has_istiaatha=False,
                has_bismillah=True,
                has_sadaka=False,
            ),
        ),
        # Adding istiaatha
        (
            Aya(1, 1),
            5,
            4,
            True,
            False,
            False,
            SegmentScripts(
                imalaey="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                uthmani="بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                start_span=(1, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(1, 1, QuranWordIndex(imlaey=4, uthmani=4)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        # Adding istiaatha
        (
            Aya(1, 1),
            0,
            7,
            True,
            False,
            False,
            SegmentScripts(
                imalaey="أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ" + " " + "بِسْمِ اللَّهِ",
                uthmani="أَعُوذُ بِٱللَّهِ مِنَ ٱلشَّيْطَانِ ٱلرَّجِيمِ" + " " + "بِسْمِ ٱللَّهِ",
                start_span=(1, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(1, 1, QuranWordIndex(imlaey=2, uthmani=2)),
                has_quran=True,
                has_istiaatha=True,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        # Adding bismillah
        (
            Aya(2, 1),
            2,
            4,
            False,
            True,
            False,
            SegmentScripts(
                imalaey="الرَّحْمَٰنِ الرَّحِيمِ" + " الم" + " " + "ذَٰلِكَ",
                uthmani="ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ" + " " + "الٓمٓ" + " " + "ذَٰلِكَ",
                start_span=(2, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(2, 2, QuranWordIndex(imlaey=1, uthmani=1)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=True,
                has_sadaka=False,
            ),
        ),
        # Adding istiaatha + bismillah
        (
            Aya(2, 1),
            0,
            11,
            True,
            True,
            False,
            SegmentScripts(
                imalaey="أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ"
                + " "
                + "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
                + " "
                + "الم"
                + " "
                + "ذَٰلِكَ",
                uthmani="أَعُوذُ بِٱللَّهِ مِنَ ٱلشَّيْطَانِ ٱلرَّجِيمِ"
                + " "
                + "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
                + " "
                + "الٓمٓ"
                + " "
                + "ذَٰلِكَ",
                start_span=(2, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(2, 2, QuranWordIndex(imlaey=1, uthmani=1)),
                has_quran=True,
                has_istiaatha=True,
                has_bismillah=True,
                has_sadaka=False,
            ),
        ),
        # Adding sadaka
        (
            Aya(114, 6),
            0,
            5,
            False,
            False,
            True,
            SegmentScripts(
                imalaey="مِنَ الْجِنَّةِ وَالنَّاسِ" + " " + "صَدَقَ اللَّهُ",
                uthmani="مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ" + " " + "صَدَقَ ٱللَّهُ",
                start_span=(114, 6, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(114, 6, QuranWordIndex(imlaey=3, uthmani=3)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=True,
            ),
        ),
        (
            Aya(1, 1),
            0,
            4,
            False,
            False,
            False,
            SegmentScripts(
                imalaey="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                uthmani="بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                start_span=(1, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(1, 1, QuranWordIndex(imlaey=4, uthmani=4)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        (
            Aya(1, 1),
            -2,
            6,
            False,
            False,
            False,
            SegmentScripts(
                imalaey="الْجِنَّةِ وَالنَّاسِ" + " " + "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                uthmani="ٱلْجِنَّةِ وَٱلنَّاسِ" + " " + "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                start_span=(114, 6, QuranWordIndex(imlaey=1, uthmani=1)),
                end_span=(1, 1, QuranWordIndex(imlaey=4, uthmani=4)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        (
            Aya(1, 1),
            -10,
            12,
            False,
            False,
            False,
            SegmentScripts(
                imalaey="الْوَسْوَاسِ الْخَنَّاسِ"
                + " "
                + "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ"
                + " "
                + "مِنَ الْجِنَّةِ وَالنَّاسِ"
                + " "
                + "بِسْمِ اللَّهِ",
                uthmani="ٱلْوَسْوَاسِ ٱلْخَنَّاسِ"
                + " "
                + "ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ"
                + " "
                + "مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ"
                + " "
                + "بِسْمِ ٱللَّهِ",
                start_span=(114, 4, QuranWordIndex(imlaey=2, uthmani=2)),
                end_span=(1, 1, QuranWordIndex(imlaey=2, uthmani=2)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        (
            Aya(1, 1),
            -10,
            20,
            False,
            False,
            False,
            SegmentScripts(
                imalaey="الْوَسْوَاسِ الْخَنَّاسِ"
                + " "
                + "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ"
                + " "
                + "مِنَ الْجِنَّةِ وَالنَّاسِ"
                + " "
                + "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
                + " "
                + "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"
                + " "
                + "الرَّحْمَٰنِ الرَّحِيمِ",
                uthmani="ٱلْوَسْوَاسِ ٱلْخَنَّاسِ"
                + " "
                + "ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ"
                + " "
                + "مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ"
                + " "
                + "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
                + " "
                + "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَـٰلَمِينَ"
                + " "
                + "ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                start_span=(114, 4, QuranWordIndex(imlaey=2, uthmani=2)),
                end_span=(1, 3, QuranWordIndex(imlaey=2, uthmani=2)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        # +ve only
        (
            Aya(112, 4),
            4,
            20,
            False,
            False,
            False,
            SegmentScripts(
                imalaey=" ".join(
                    [
                        "أَحَدٌ",
                        "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ",
                        "مِن شَرِّ مَا خَلَقَ",
                        "وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ",
                        "وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ",
                        "وَمِن",
                    ]
                ),
                uthmani=" ".join(
                    [
                        "أَحَدٌۢ",
                        "قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ",
                        "مِن شَرِّ مَا خَلَقَ",
                        "وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ",
                        "وَمِن شَرِّ ٱلنَّفَّـٰثَـٰتِ فِى ٱلْعُقَدِ",
                        "وَمِن",
                    ]
                ),
                start_span=(112, 4, QuranWordIndex(imlaey=4, uthmani=4)),
                end_span=(113, 5, QuranWordIndex(imlaey=1, uthmani=1)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        (
            Aya(2, 21),
            0,
            5,
            False,
            False,
            False,
            SegmentScripts(
                imalaey="يَا أَيُّهَا النَّاسُ اعْبُدُوا رَبَّكُمُ",
                uthmani="يَـٰٓأَيُّهَا ٱلنَّاسُ ٱعْبُدُوا۟ رَبَّكُمُ",
                start_span=(2, 21, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(2, 21, QuranWordIndex(imlaey=5, uthmani=4)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
        # Failed Case
        (
            Aya(114, 1, start_imlaey_word_idx=4),
            4,
            2,
            False,
            True,
            False,
            SegmentScripts(
                imalaey="مَلِكِ النَّاسِ",
                uthmani="مَلِكِ ٱلنَّاسِ",
                start_span=(114, 2, QuranWordIndex(imlaey=0, uthmani=0)),
                end_span=(114, 2, QuranWordIndex(imlaey=2, uthmani=2)),
                has_quran=True,
                has_istiaatha=False,
                has_bismillah=False,
                has_sadaka=False,
            ),
        ),
    ],
)
def test_get_by_imlaey_words(
    aya: Aya,
    start,
    window,
    istiaatha,
    bismillah,
    sadaka,
    ex_segment_scripts: SegmentScripts,
):
    out_seg_scripts = aya.get_by_imlaey_words(
        start=start,
        window=window,
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    print(out_seg_scripts)
    assert out_seg_scripts == ex_segment_scripts


@pytest.mark.parametrize(
    "aya, start, window, istiaatha, bismillah, sadaka, ex_aya",
    [
        (
            Aya(1, 1),
            0,
            4,
            False,
            False,
            False,
            Aya(
                sura_idx=1,
                aya_idx=2,
                start_imlaey_word_idx=0,
            ),
        ),
        (
            Aya(1, 1),
            -2,
            6,
            False,
            False,
            False,
            Aya(
                sura_idx=1,
                aya_idx=2,
                start_imlaey_word_idx=0,
            ),
        ),
        (
            Aya(1, 1),
            -10,
            12,
            False,
            False,
            False,
            Aya(
                sura_idx=1,
                aya_idx=1,
                start_imlaey_word_idx=2,
            ),
        ),
        (
            Aya(1, 1),
            -10,
            20,
            False,
            False,
            False,
            Aya(
                sura_idx=1,
                aya_idx=4,
                start_imlaey_word_idx=0,
            ),
        ),
    ],
)
def test_step_by_imlaey_words(
    aya: Aya,
    start,
    window,
    istiaatha,
    bismillah,
    sadaka,
    ex_aya: Aya,
):
    out_aya = aya.step_by_imlaey_words(
        start=start,
        window=window,
        include_istiaatha=istiaatha,
        include_bismillah=bismillah,
        include_sadaka=sadaka,
    )
    assert out_aya.sura_idx == ex_aya.sura_idx
    assert out_aya.aya_idx == ex_aya.aya_idx
    assert out_aya.start_imlaey_word_idx == ex_aya.start_imlaey_word_idx


@pytest.mark.parametrize(
    "sura_idx, fixed_segments, ex_missings",
    [
        (
            114,
            [
                SegmentScripts(
                    imalaey="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                    uthmani="بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                    has_istiaatha=False,
                    has_bismillah=True,
                    has_sadaka=False,
                    has_quran=False,
                    start_span=None,
                    end_span=None,
                ),
                SegmentScripts(
                    imalaey="قُلْ أَعُوذُ بِرَبِّ النَّاسِ",
                    uthmani="قُلْ أَعُوذُ بِرَبِّ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 1, QuranWordIndex(imlaey=4, uthmani=4)),
                ),
                None,
                None,
                None,
                SegmentScripts(
                    imalaey="الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ",
                    uthmani="ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 5, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 5, QuranWordIndex(imlaey=5, uthmani=5)),
                ),
                SegmentScripts(
                    imalaey="مِنَ الْجِنَّةِ وَالنَّاسِ",
                    uthmani="مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 6, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 6, QuranWordIndex(imlaey=3, uthmani=3)),
                ),
                SegmentScripts(
                    imalaey="صَدَقَ اللَّهُ الْعَظِيمُ",
                    uthmani="صَدَقَ ٱللَّهُ ٱلْعَظِيمُ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=True,
                    has_quran=False,
                    start_span=None,
                    end_span=None,
                ),
            ],
            [
                SegmentScripts(
                    imalaey="مَلِكِ النَّاسِ",
                    uthmani="مَلِكِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 2, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 2, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                SegmentScripts(
                    imalaey="إِلَٰهِ النَّاسِ",
                    uthmani="إِلَـٰهِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 3, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 3, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                SegmentScripts(
                    imalaey="مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ",
                    uthmani="مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 4, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 4, QuranWordIndex(imlaey=4, uthmani=4)),
                ),
            ],
        ),
        # Missing word
        (
            114,
            [
                SegmentScripts(
                    imalaey="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                    uthmani="بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                    has_istiaatha=False,
                    has_bismillah=True,
                    has_sadaka=False,
                    has_quran=False,
                    start_span=None,
                    end_span=None,
                ),
                SegmentScripts(
                    imalaey="قُلْ أَعُوذُ بِرَبِّ النَّاسِ",
                    uthmani="قُلْ أَعُوذُ بِرَبِّ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 1, QuranWordIndex(imlaey=4, uthmani=4)),
                ),
                None,
                None,
                None,
                SegmentScripts(
                    imalaey="الَّذِي يُوَسْوِسُ فِي صُدُورِ",
                    uthmani="ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 5, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 5, QuranWordIndex(imlaey=4, uthmani=4)),
                ),
                SegmentScripts(
                    imalaey="مِنَ الْجِنَّةِ وَالنَّاسِ",
                    uthmani="مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 6, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 6, QuranWordIndex(imlaey=3, uthmani=3)),
                ),
                SegmentScripts(
                    imalaey="صَدَقَ اللَّهُ الْعَظِيمُ",
                    uthmani="صَدَقَ ٱللَّهُ ٱلْعَظِيمُ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=True,
                    has_quran=False,
                    start_span=None,
                    end_span=None,
                ),
            ],
            [
                SegmentScripts(
                    imalaey="مَلِكِ النَّاسِ",
                    uthmani="مَلِكِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 2, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 2, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                SegmentScripts(
                    imalaey="إِلَٰهِ النَّاسِ",
                    uthmani="إِلَـٰهِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 3, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 3, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                SegmentScripts(
                    imalaey="مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ",
                    uthmani="مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 4, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 4, QuranWordIndex(imlaey=4, uthmani=4)),
                ),
                SegmentScripts(
                    imalaey="النَّاسِ",
                    uthmani="ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 5, QuranWordIndex(imlaey=4, uthmani=4)),
                    end_span=(114, 5, QuranWordIndex(imlaey=5, uthmani=5)),
                ),
            ],
        ),
        (
            114,
            [
                SegmentScripts(
                    imalaey="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ قُلْ أَعُوذُ",
                    uthmani="بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ قُلْ أَعُوذُ",
                    has_istiaatha=False,
                    has_bismillah=True,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 1, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 1, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                None,
                SegmentScripts(
                    imalaey="مَلِكِ النَّاسِ",
                    uthmani="مَلِكِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 2, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 2, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                SegmentScripts(
                    imalaey="إِلَٰهِ النَّاسِ",
                    uthmani="إِلَـٰهِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 3, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 3, QuranWordIndex(imlaey=2, uthmani=2)),
                ),
                SegmentScripts(
                    imalaey="مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ",
                    uthmani="مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 4, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 4, QuranWordIndex(imlaey=4, uthmani=4)),
                ),
                SegmentScripts(
                    imalaey="الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ",
                    uthmani="ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 5, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 5, QuranWordIndex(imlaey=5, uthmani=5)),
                ),
                SegmentScripts(
                    imalaey="مِنَ الْجِنَّةِ وَالنَّاسِ",
                    uthmani="مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 6, QuranWordIndex(imlaey=0, uthmani=0)),
                    end_span=(114, 6, QuranWordIndex(imlaey=3, uthmani=3)),
                ),
                SegmentScripts(
                    imalaey="صَدَقَ اللَّهُ الْعَظِيمُ",
                    uthmani="صَدَقَ ٱللَّهُ ٱلْعَظِيمُ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=True,
                    has_quran=False,
                    start_span=None,
                    end_span=None,
                ),
            ],
            [
                SegmentScripts(
                    imalaey="بِرَبِّ النَّاسِ",
                    uthmani="بِرَبِّ ٱلنَّاسِ",
                    has_istiaatha=False,
                    has_bismillah=False,
                    has_sadaka=False,
                    has_quran=True,
                    start_span=(114, 1, QuranWordIndex(imlaey=2, uthmani=2)),
                    end_span=(114, 1, QuranWordIndex(imlaey=4, uthmani=4)),
                )
            ],
        ),
    ],
)
def test_check_sura_missing_parts(sura_idx, fixed_segments, ex_missings):
    missings = check_sura_missing_parts(
        sura_idx=sura_idx, fixed_segments=fixed_segments
    )
    assert len(missings) == len(ex_missings)
    assert missings == ex_missings
