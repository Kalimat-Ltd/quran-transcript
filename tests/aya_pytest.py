import pytest

from quran_transcript import Aya, WordSpan


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
