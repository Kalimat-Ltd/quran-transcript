import pytest
import re

from quran_transcript.phonetics.moshaf_attributes import MoshafAttributes
from quran_transcript.phonetics.operations import (
    DisassembleHrofMoqatta,
    SpecialCases,
    ConvertAlifMaksora,
    NormalizeHmazat,
    IthbatYaaYohie,
    RemoveKasheeda,
    RemoveHmzatWaslMiddle,
    RemoveSkoonMostadeer,
    SkoonMostateel,
    MaddAlewad,
    WawAlsalah,
    EnlargeSmallLetters,
    CleanEnd,
    NormalizeTaa,
)
from quran_transcript import Aya
from quran_transcript import alphabet as alph


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "ذَٰلِكَ ٱلْكِتَـٰبُ لَا رَيْبَ فِيهِ هُدًۭى لِّلْمُتَّقِينَ",
            "ذَٰلِكَ ٱلْكِتَـٰبُ لَا رَيْبَ فِيهِ هُدًۭ لِّلْمُتَّقِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # alif khnjaria
        (
            "أُو۟لَـٰٓئِكَ ٱلَّذِينَ ٱشْتَرَوُا۟ ٱلضَّلَـٰلَةَ بِٱلْهُدَىٰ فَمَا رَبِحَت تِّجَـٰرَتُهُمْ وَمَا كَانُوا۟ مُهْتَدِينَ",
            "أُو۟لَـٰٓئِكَ ٱلَّذِينَ ٱشْتَرَوُا۟ ٱلضَّلَـٰلَةَ بِٱلْهُدَا فَمَا رَبِحَت تِّجَـٰرَتُهُمْ وَمَا كَانُوا۟ مُهْتَدِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # alif middle
        (
            "إِذْ هَمَّت طَّآئِفَتَانِ مِنكُمْ أَن تَفْشَلَا وَٱللَّهُ وَلِيُّهُمَا وَعَلَى ٱللَّهِ فَلْيَتَوَكَّلِ ٱلْمُؤْمِنُونَ",
            "إِذْ هَمَّت طَّآئِفَتَانِ مِنكُمْ أَن تَفْشَلَا وَٱللَّهُ وَلِيُّهُمَا وَعَلَا ٱللَّهِ فَلْيَتَوَكَّلِ ٱلْمُؤْمِنُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # alif end
        (
            "إِذْ هَمَّت طَّآئِفَتَانِ مِنكُمْ أَن تَفْشَلَا وَٱللَّهُ وَلِيُّهُمَا وَعَلَى",
            "إِذْ هَمَّت طَّآئِفَتَانِ مِنكُمْ أَن تَفْشَلَا وَٱللَّهُ وَلِيُّهُمَا وَعَلَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa (kasra before)
        (
            "أَوْ كَصَيِّبٍۢ مِّنَ ٱلسَّمَآءِ فِيهِ ظُلُمَـٰتٌۭ وَرَعْدٌۭ وَبَرْقٌۭ يَجْعَلُونَ أَصَـٰبِعَهُمْ فِىٓ ءَاذَانِهِم مِّنَ ٱلصَّوَٰعِقِ حَذَرَ ٱلْمَوْتِ وَٱللَّهُ مُحِيطٌۢ بِٱلْكَـٰفِرِينَ",
            "أَوْ كَصَيِّبٍۢ مِّنَ ٱلسَّمَآءِ فِيهِ ظُلُمَـٰتٌۭ وَرَعْدٌۭ وَبَرْقٌۭ يَجْعَلُونَ أَصَـٰبِعَهُمْ فِيٓ ءَاذَانِهِم مِّنَ ٱلصَّوَٰعِقِ حَذَرَ ٱلْمَوْتِ وَٱللَّهُ مُحِيطٌۢ بِٱلْكَـٰفِرِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa multiples
        (
            "وَلَمَّا جَهَّزَهُم بِجَهَازِهِمْ قَالَ ٱئْتُونِى بِأَخٍۢ لَّكُم مِّنْ أَبِيكُمْ أَلَا تَرَوْنَ أَنِّىٓ أُوفِى ٱلْكَيْلَ وَأَنَا۠ خَيْرُ ٱلْمُنزِلِينَ",
            "وَلَمَّا جَهَّزَهُم بِجَهَازِهِمْ قَالَ ٱئْتُونِي بِأَخٍۢ لَّكُم مِّنْ أَبِيكُمْ أَلَا تَرَوْنَ أَنِّيٓ أُوفِي ٱلْكَيْلَ وَأَنَا۠ خَيْرُ ٱلْمُنزِلِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + kasra
        (
            "وَقَالَ ٱللَّهُ لَا تَتَّخِذُوٓا۟ إِلَـٰهَيْنِ ٱثْنَيْنِ إِنَّمَا هُوَ إِلَـٰهٌۭ وَٰحِدٌۭ فَإِيَّـٰىَ فَٱرْهَبُونِ",
            "وَقَالَ ٱللَّهُ لَا تَتَّخِذُوٓا۟ إِلَـٰهَيْنِ ٱثْنَيْنِ إِنَّمَا هُوَ إِلَـٰهٌۭ وَٰحِدٌۭ فَإِيَّـٰيَ فَٱرْهَبُونِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + tanween dam
        (
            "صُمٌّۢ بُكْمٌ عُمْىٌۭ فَهُمْ لَا يَرْجِعُونَ",
            "صُمٌّۢ بُكْمٌ عُمْيٌۭ فَهُمْ لَا يَرْجِعُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + damma
        (
            "أَلَمْ يَعْلَمُوٓا۟ أَنَّهُۥ مَن يُحَادِدِ ٱللَّهَ وَرَسُولَهُۥ فَأَنَّ لَهُۥ نَارَ جَهَنَّمَ خَـٰلِدًۭا فِيهَا ذَٰلِكَ ٱلْخِزْىُ ٱلْعَظِيمُ",
            "أَلَمْ يَعْلَمُوٓا۟ أَنَّهُۥ مَن يُحَادِدِ ٱللَّهَ وَرَسُولَهُۥ فَأَنَّ لَهُۥ نَارَ جَهَنَّمَ خَـٰلِدًۭا فِيهَا ذَٰلِكَ ٱلْخِزْيُ ٱلْعَظِيمُ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + ksara
        (
            "قُلْ إِنَّمَآ أُنذِرُكُم بِٱلْوَحْىِ وَلَا يَسْمَعُ ٱلصُّمُّ ٱلدُّعَآءَ إِذَا مَا يُنذَرُونَ",
            "قُلْ إِنَّمَآ أُنذِرُكُم بِٱلْوَحْيِ وَلَا يَسْمَعُ ٱلصُّمُّ ٱلدُّعَآءَ إِذَا مَا يُنذَرُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + raas_haa
        (
            "وَءَاتُوا۟ ٱلنِّسَآءَ صَدُقَـٰتِهِنَّ نِحْلَةًۭ فَإِن طِبْنَ لَكُمْ عَن شَىْءٍۢ مِّنْهُ نَفْسًۭا فَكُلُوهُ هَنِيٓـًۭٔا مَّرِيٓـًۭٔا",
            "وَءَاتُوا۟ ٱلنِّسَآءَ صَدُقَـٰتِهِنَّ نِحْلَةًۭ فَإِن طِبْنَ لَكُمْ عَن شَيْءٍۢ مِّنْهُ نَفْسًۭا فَكُلُوهُ هَنِيٓـًۭٔا مَّرِيٓـًۭٔا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + shadda
        (
            "بِأَىِّ ذَنۢبٍۢ قُتِلَتْ",
            "بِأَيِّ ذَنۢبٍۢ قُتِلَتْ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        # yaa + madd
        (
            "وَأَشْرَقَتِ ٱلْأَرْضُ بِنُورِ رَبِّهَا وَوُضِعَ ٱلْكِتَـٰبُ وَجِا۟ىٓءَ بِٱلنَّبِيِّـۧنَ وَٱلشُّهَدَآءِ وَقُضِىَ بَيْنَهُم بِٱلْحَقِّ وَهُمْ لَا يُظْلَمُونَ",
            "وَأَشْرَقَتِ ٱلْأَرْضُ بِنُورِ رَبِّهَا وَوُضِعَ ٱلْكِتَـٰبُ وَجِا۟يٓءَ بِٱلنَّبِيِّـۧنَ وَٱلشُّهَدَآءِ وَقُضِيَ بَيْنَهُم بِٱلْحَقِّ وَهُمْ لَا يُظْلَمُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_convert_alif_maksora(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = ConvertAlifMaksora()
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


def test_convert_alif_maksora_stress_test():
    start_aya = Aya()
    op = ConvertAlifMaksora()
    moshaf = MoshafAttributes(
        rewaya="hafs",
        madd_monfasel_len=4,
        madd_mottasel_len=4,
        madd_mottasel_waqf=4,
        madd_aared_len=4,
    )

    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
        out_text = op.apply(txt, moshaf, mode="test")
        if alph.uthmani.alif_maksora in out_text:
            print(aya)
            print(out_text)
            raise ValueError()


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "وَمَن يَرْغَبُ عَن مِّلَّةِ إِبْرَٰهِـۧمَ إِلَّا مَن سَفِهَ نَفْسَهُۥ وَلَقَدِ ٱصْطَفَيْنَـٰهُ فِى ٱلدُّنْيَا وَإِنَّهُۥ فِى ٱلْـَٔاخِرَةِ لَمِنَ ٱلصَّـٰلِحِينَ",
            "وَمَن يَرْغَبُ عَن مِّلَّةِ ءِبْرَٰهِـۧمَ ءِلَّا مَن سَفِهَ نَفْسَهُۥ وَلَقَدِ ٱصْطَفَيْنَـٰهُ فِى ٱلدُّنْيَا وَءِنَّهُۥ فِى ٱلْـءَاخِرَةِ لَمِنَ ٱلصَّـٰلِحِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_normalize_hamazat(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = NormalizeHmazat()
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


def test_normalize_hamazat_stress_test():
    start_aya = Aya()
    op = NormalizeHmazat()
    moshaf = MoshafAttributes(
        rewaya="hafs",
        madd_monfasel_len=4,
        madd_mottasel_len=4,
        madd_mottasel_waqf=4,
        madd_aared_len=4,
    )

    hamazat = re.sub(alph.uthmani.hamza, "", alph.uthmani.hamazat_group)
    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
        out_text = op.apply(txt, moshaf, mode="test")
        if re.search(f"[{hamazat}]", out_text):
            print(aya)
            print(out_text)
            raise ValueError()


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "أَلَمْ تَرَ إِلَى ٱلَّذِى حَآجَّ إِبْرَٰهِـۧمَ فِى رَبِّهِۦٓ أَنْ ءَاتَىٰهُ ٱللَّهُ ٱلْمُلْكَ إِذْ قَالَ إِبْرَٰهِـۧمُ رَبِّىَ ٱلَّذِى يُحْىِۦ وَيُمِيتُ قَالَ أَنَا۠ أُحْىِۦ وَأُمِيتُ قَالَ إِبْرَٰهِـۧمُ فَإِنَّ ٱللَّهَ يَأْتِى بِٱلشَّمْسِ مِنَ ٱلْمَشْرِقِ فَأْتِ بِهَا مِنَ ٱلْمَغْرِبِ فَبُهِتَ ٱلَّذِى كَفَرَ وَٱللَّهُ لَا يَهْدِى ٱلْقَوْمَ ٱلظَّـٰلِمِينَ",
            "أَلَمْ تَرَ إِلَى ٱلَّذِى حَآجَّ إِبْرَٰهِـۧمَ فِى رَبِّهِۦٓ أَنْ ءَاتَىٰهُ ٱللَّهُ ٱلْمُلْكَ إِذْ قَالَ إِبْرَٰهِـۧمُ رَبِّىَ ٱلَّذِى يُحْىِۦ وَيُمِيتُ قَالَ أَنَا۠ أُحْىِۦ وَأُمِيتُ قَالَ إِبْرَٰهِـۧمُ فَإِنَّ ٱللَّهَ يَأْتِى بِٱلشَّمْسِ مِنَ ٱلْمَشْرِقِ فَأْتِ بِهَا مِنَ ٱلْمَغْرِبِ فَبُهِتَ ٱلَّذِى كَفَرَ وَٱللَّهُ لَا يَهْدِى ٱلْقَوْمَ ٱلظَّـٰلِمِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَإِذْ قَالَ إِبْرَٰهِـۧمُ رَبِّ أَرِنِى كَيْفَ تُحْىِ ٱلْمَوْتَىٰ قَالَ أَوَلَمْ تُؤْمِن قَالَ بَلَىٰ وَلَـٰكِن لِّيَطْمَئِنَّ قَلْبِى قَالَ فَخُذْ أَرْبَعَةًۭ مِّنَ ٱلطَّيْرِ فَصُرْهُنَّ إِلَيْكَ ثُمَّ ٱجْعَلْ عَلَىٰ كُلِّ جَبَلٍۢ مِّنْهُنَّ جُزْءًۭا ثُمَّ ٱدْعُهُنَّ يَأْتِينَكَ سَعْيًۭا وَٱعْلَمْ أَنَّ ٱللَّهَ عَزِيزٌ حَكِيمٌۭ",
            "وَإِذْ قَالَ إِبْرَٰهِـۧمُ رَبِّ أَرِنِى كَيْفَ تُحْيِي ٱلْمَوْتَىٰ قَالَ أَوَلَمْ تُؤْمِن قَالَ بَلَىٰ وَلَـٰكِن لِّيَطْمَئِنَّ قَلْبِى قَالَ فَخُذْ أَرْبَعَةًۭ مِّنَ ٱلطَّيْرِ فَصُرْهُنَّ إِلَيْكَ ثُمَّ ٱجْعَلْ عَلَىٰ كُلِّ جَبَلٍۢ مِّنْهُنَّ جُزْءًۭا ثُمَّ ٱدْعُهُنَّ يَأْتِينَكَ سَعْيًۭا وَٱعْلَمْ أَنَّ ٱللَّهَ عَزِيزٌ حَكِيمٌۭ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_ithbat_yaa_yohie(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = IthbatYaaYohie()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "وَٱلَّذِينَ يُؤْمِنُونَ بِمَآ أُنزِلَ إِلَيْكَ وَمَآ أُنزِلَ مِن قَبْلِكَ وَبِٱلْـَٔاخِرَةِ هُمْ يُوقِنُونَ",
            "وَٱلَّذِينَ يُؤْمِنُونَ بِمَآ أُنزِلَ إِلَيْكَ وَمَآ أُنزِلَ مِن قَبْلِكَ وَبِٱلَْٔاخِرَةِ هُمْ يُوقِنُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_remove_kasheeda(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = RemoveKasheeda()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "ٱسْتِكْبَارًۭا فِى ٱلْأَرْضِ وَمَكْرَ ٱلسَّيِّئِ وَلَا يَحِيقُ ٱلْمَكْرُ ٱلسَّيِّئُ إِلَّا بِأَهْلِهِۦ فَهَلْ يَنظُرُونَ إِلَّا سُنَّتَ ٱلْأَوَّلِينَ فَلَن تَجِدَ لِسُنَّتِ ٱللَّهِ تَبْدِيلًۭا وَلَن تَجِدَ لِسُنَّتِ ٱللَّهِ تَحْوِيلًا",
            "ٱسْتِكْبَارًۭا فِى لْأَرْضِ وَمَكْرَ لسَّيِّئِ وَلَا يَحِيقُ لْمَكْرُ لسَّيِّئُ إِلَّا بِأَهْلِهِۦ فَهَلْ يَنظُرُونَ إِلَّا سُنَّتَ لْأَوَّلِينَ فَلَن تَجِدَ لِسُنَّتِ للَّهِ تَبْدِيلًۭا وَلَن تَجِدَ لِسُنَّتِ للَّهِ تَحْوِيلًا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_remove_kasheeda(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = RemoveHmzatWaslMiddle()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "وَجِا۟ىٓءَ يَوْمَئِذٍۭ بِجَهَنَّمَ يَوْمَئِذٍۢ يَتَذَكَّرُ ٱلْإِنسَـٰنُ وَأَنَّىٰ لَهُ ٱلذِّكْرَىٰ",
            "وَجِىٓءَ يَوْمَئِذٍۭ بِجَهَنَّمَ يَوْمَئِذٍۢ يَتَذَكَّرُ ٱلْإِنسَـٰنُ وَأَنَّىٰ لَهُ ٱلذِّكْرَىٰ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَٱنطَلَقَ ٱلْمَلَأُ مِنْهُمْ أَنِ ٱمْشُوا۟ وَٱصْبِرُوا۟ عَلَىٰٓ ءَالِهَتِكُمْ إِنَّ هَـٰذَا لَشَىْءٌۭ يُرَادُ",
            "وَٱنطَلَقَ ٱلْمَلَأُ مِنْهُمْ أَنِ ٱمْشُو وَٱصْبِرُو عَلَىٰٓ ءَالِهَتِكُمْ إِنَّ هَـٰذَا لَشَىْءٌۭ يُرَادُ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_remove_skoon_mostadeer(
    in_text: str, target_text: str, moshaf: MoshafAttributes
):
    op = RemoveSkoonMostadeer()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "فَقَالَ أَنَا۠ رَبُّكُمُ ٱلْأَعْلَىٰ",
            "فَقَالَ أَنَ رَبُّكُمُ ٱلْأَعْلَىٰ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَيُطَافُ عَلَيْهِم بِـَٔانِيَةٍۢ مِّن فِضَّةٍۢ وَأَكْوَابٍۢ كَانَتْ قَوَارِيرَا۠",
            "وَيُطَافُ عَلَيْهِم بِـَٔانِيَةٍۢ مِّن فِضَّةٍۢ وَأَكْوَابٍۢ كَانَتْ قَوَارِيرَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_skoon_mostateel(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = SkoonMostateel()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


def test_skoon_mostateel_stree_test():
    start_aya = Aya()
    op = SkoonMostateel()
    moshaf = MoshafAttributes(
        rewaya="hafs",
        madd_monfasel_len=4,
        madd_mottasel_len=4,
        madd_mottasel_waqf=4,
        madd_aared_len=4,
    )

    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
        out_text = op.apply(txt, moshaf, mode="test")
        if alph.uthmani.skoon_mostateel in out_text:
            print(aya)
            print(out_text)
            raise ValueError()


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "وَإِن مِّن قَرْيَةٍ إِلَّا نَحْنُ مُهْلِكُوهَا قَبْلَ يَوْمِ ٱلْقِيَـٰمَةِ أَوْ مُعَذِّبُوهَا عَذَابًۭا شَدِيدًۭا كَانَ ذَٰلِكَ فِى ٱلْكِتَـٰبِ مَسْطُورًۭا",
            "وَإِن مِّن قَرْيَةٍ إِلَّا نَحْنُ مُهْلِكُوهَا قَبْلَ يَوْمِ ٱلْقِيَـٰمَةِ أَوْ مُعَذِّبُوهَا عَذَابًۭ شَدِيدًۭ كَانَ ذَٰلِكَ فِى ٱلْكِتَـٰبِ مَسْطُورَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "ٱلَّذِى جَعَلَ لَكُمُ ٱلْأَرْضَ فِرَٰشًۭا وَٱلسَّمَآءَ بِنَآءًۭ وَأَنزَلَ مِنَ ٱلسَّمَآءِ مَآءًۭ فَأَخْرَجَ بِهِۦ مِنَ ٱلثَّمَرَٰتِ رِزْقًۭا لَّكُمْ فَلَا تَجْعَلُوا۟ لِلَّهِ أَندَادًۭا وَأَنتُمْ تَعْلَمُونَ",
            "ٱلَّذِى جَعَلَ لَكُمُ ٱلْأَرْضَ فِرَٰشًۭ وَٱلسَّمَآءَ بِنَآءًۭ وَأَنزَلَ مِنَ ٱلسَّمَآءِ مَآءًۭ فَأَخْرَجَ بِهِۦ مِنَ ٱلثَّمَرَٰتِ رِزْقًۭ لَّكُمْ فَلَا تَجْعَلُوا۟ لِلَّهِ أَندَادًۭ وَأَنتُمْ تَعْلَمُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "ٱلَّذِى جَعَلَ لَكُمُ ٱلْأَرْضَ فِرَٰشًۭا وَٱلسَّمَآءَ بِنَآءًۭ وَأَنزَلَ مِنَ ٱلسَّمَآءِ مَآءًۭ",
            "ٱلَّذِى جَعَلَ لَكُمُ ٱلْأَرْضَ فِرَٰشًۭ وَٱلسَّمَآءَ بِنَآءًۭ وَأَنزَلَ مِنَ ٱلسَّمَآءِ مَآءَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَٱلسَّارِقُ وَٱلسَّارِقَةُ فَٱقْطَعُوٓا۟ أَيْدِيَهُمَا جَزَآءًۢ بِمَا كَسَبَا نَكَـٰلًۭا مِّنَ ٱللَّهِ وَٱللَّهُ عَزِيزٌ حَكِيمٌۭ",
            "وَٱلسَّارِقُ وَٱلسَّارِقَةُ فَٱقْطَعُوٓا۟ أَيْدِيَهُمَا جَزَآءًۢ بِمَا كَسَبَا نَكَـٰلًۭ مِّنَ ٱللَّهِ وَٱللَّهُ عَزِيزٌ حَكِيمٌۭ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَٱلسَّارِقُ وَٱلسَّارِقَةُ فَٱقْطَعُوٓا۟ أَيْدِيَهُمَا جَزَآءًۢ",
            "وَٱلسَّارِقُ وَٱلسَّارِقَةُ فَٱقْطَعُوٓا۟ أَيْدِيَهُمَا جَزَآءَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_madd_alewad(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = MaddAlewad()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "إِنَّمَا يَعْمُرُ مَسَـٰجِدَ ٱللَّهِ مَنْ ءَامَنَ بِٱللَّهِ وَٱلْيَوْمِ ٱلْـَٔاخِرِ وَأَقَامَ ٱلصَّلَوٰةَ وَءَاتَى ٱلزَّكَوٰةَ وَلَمْ يَخْشَ إِلَّا ٱللَّهَ فَعَسَىٰٓ أُو۟لَـٰٓئِكَ أَن يَكُونُوا۟ مِنَ ٱلْمُهْتَدِينَ",
            "إِنَّمَا يَعْمُرُ مَسَـٰجِدَ ٱللَّهِ مَنْ ءَامَنَ بِٱللَّهِ وَٱلْيَوْمِ ٱلْـَٔاخِرِ وَأَقَامَ ٱلصَّلَاةَ وَءَاتَى ٱلزَّكَاةَ وَلَمْ يَخْشَ إِلَّا ٱللَّهَ فَعَسَىٰٓ أُو۟لَـٰٓئِكَ أَن يَكُونُوا۟ مِنَ ٱلْمُهْتَدِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "ٱلَّذِينَ يَأْكُلُونَ ٱلرِّبَوٰا۟ لَا يَقُومُونَ إِلَّا كَمَا يَقُومُ ٱلَّذِى يَتَخَبَّطُهُ ٱلشَّيْطَـٰنُ مِنَ ٱلْمَسِّ ذَٰلِكَ بِأَنَّهُمْ قَالُوٓا۟ إِنَّمَا ٱلْبَيْعُ مِثْلُ ٱلرِّبَوٰا۟ وَأَحَلَّ ٱللَّهُ ٱلْبَيْعَ وَحَرَّمَ ٱلرِّبَوٰا۟ فَمَن جَآءَهُۥ مَوْعِظَةٌۭ مِّن رَّبِّهِۦ فَٱنتَهَىٰ فَلَهُۥ مَا سَلَفَ وَأَمْرُهُۥٓ إِلَى ٱللَّهِ وَمَنْ عَادَ فَأُو۟لَـٰٓئِكَ أَصْحَـٰبُ ٱلنَّارِ هُمْ فِيهَا خَـٰلِدُونَ",
            "ٱلَّذِينَ يَأْكُلُونَ ٱلرِّبَاا۟ لَا يَقُومُونَ إِلَّا كَمَا يَقُومُ ٱلَّذِى يَتَخَبَّطُهُ ٱلشَّيْطَـٰنُ مِنَ ٱلْمَسِّ ذَٰلِكَ بِأَنَّهُمْ قَالُوٓا۟ إِنَّمَا ٱلْبَيْعُ مِثْلُ ٱلرِّبَاا۟ وَأَحَلَّ ٱللَّهُ ٱلْبَيْعَ وَحَرَّمَ ٱلرِّبَاا۟ فَمَن جَآءَهُۥ مَوْعِظَةٌۭ مِّن رَّبِّهِۦ فَٱنتَهَىٰ فَلَهُۥ مَا سَلَفَ وَأَمْرُهُۥٓ إِلَى ٱللَّهِ وَمَنْ عَادَ فَأُو۟لَـٰٓئِكَ أَصْحَـٰبُ ٱلنَّارِ هُمْ فِيهَا خَـٰلِدُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "",
            "",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_waw_alslah(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = WawAlsalah()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "ذَٰلِكَ ٱلْكِتَـٰبُ لَا رَيْبَ فِيهِ هُدًۭى لِّلْمُتَّقِينَ",
            "ذَالِكَ ٱلْكِتَـابُ لَا رَيْبَ فِيهِ هُدًۭى لِّلْمُتَّقِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "فَٱسْتَجَبْنَا لَهُۥ وَنَجَّيْنَـٰهُ مِنَ ٱلْغَمِّ وَكَذَٰلِكَ نُـۨجِى ٱلْمُؤْمِنِينَ",
            "فَٱسْتَجَبْنَا لَهُو وَنَجَّيْنَـاهُ مِنَ ٱلْغَمِّ وَكَذَالِكَ نُـنجِى ٱلْمُؤْمِنِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَيَخْلُدْ فِيهِۦ",
            "وَيَخْلُدْ فِيهِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "يَحْسَبُ أَنَّ مَالَهُۥٓ",
            "يَحْسَبُ أَنَّ مَالَهُ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "فَلْيَنظُرِ ٱلْإِنسَـٰنُ إِلَىٰ طَعَامِهِۦٓ",
            "فَلْيَنظُرِ ٱلْإِنسَـانُ إِلَىا طَعَامِهِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_enlarge_small_letters(
    in_text: str, target_text: str, moshaf: MoshafAttributes
):
    op = EnlargeSmallLetters()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "ذَٰلِكَ ٱلْكِتَـٰبُ لَا رَيْبَ فِيهِ هُدًۭى لِّلْمُتَّقِينَ",
            "ذَٰلِكَ ٱلْكِتَـٰبُ لَا رَيْبَ فِيهِ هُدًۭى لِّلْمُتَّقِين",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "لَّهُۥ مَا فِى ٱلسَّمَـٰوَٰتِ وَمَا فِى ٱلْأَرْضِ وَإِنَّ ٱللَّهَ لَهُوَ ٱلْغَنِىُّ ٱلْحَمِيدُ",
            "لَّهُۥ مَا فِى ٱلسَّمَـٰوَٰتِ وَمَا فِى ٱلْأَرْضِ وَإِنَّ ٱللَّهَ لَهُوَ ٱلْغَنِىُّ ٱلْحَمِيد",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "لَّهُۥ مَا فِى ٱلسَّمَـٰوَٰتِ وَمَا فِى ٱلْأَرْضِ وَإِنَّ ٱللَّهَ لَهُوَ ٱلْغَنِىُّ",
            "لَّهُۥ مَا فِى ٱلسَّمَـٰوَٰتِ وَمَا فِى ٱلْأَرْضِ وَإِنَّ ٱللَّهَ لَهُوَ ٱلْغَنِىّ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَٱلَّذِينَ يُؤْمِنُونَ بِمَآ أُنزِلَ إِلَيْكَ وَمَآ",
            "وَٱلَّذِينَ يُؤْمِنُونَ بِمَآ أُنزِلَ إِلَيْكَ وَمَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "لِيُوَفِّيَهُمْ أُجُورَهُمْ وَيَزِيدَهُم مِّن فَضْلِهِۦٓ إِنَّهُۥ غَفُورٌۭ شَكُورٌۭ",
            "لِيُوَفِّيَهُمْ أُجُورَهُمْ وَيَزِيدَهُم مِّن فَضْلِهِۦٓ إِنَّهُۥ غَفُورٌۭ شَكُور",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "إِنَّ ٱلَّذِينَ كَفَرُوا۟ سَوَآءٌ",
            "إِنَّ ٱلَّذِينَ كَفَرُوا۟ سَوَآء",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "يَمْحَقُ ٱللَّهُ ٱلرِّبَوٰا۟ وَيُرْبِى ٱلصَّدَقَـٰتِ وَٱللَّهُ لَا يُحِبُّ كُلَّ كَفَّارٍ",
            "يَمْحَقُ ٱللَّهُ ٱلرِّبَوٰا۟ وَيُرْبِى ٱلصَّدَقَـٰتِ وَٱللَّهُ لَا يُحِبُّ كُلَّ كَفَّار",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "فَتَوَلَّ عَنْهُمْ يَوْمَ يَدْعُ ٱلدَّاعِ إِلَىٰ شَىْءٍۢ نُّكُرٍ",
            "فَتَوَلَّ عَنْهُمْ يَوْمَ يَدْعُ ٱلدَّاعِ إِلَىٰ شَىْءٍۢ نُّكُر",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ",
            "وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَد",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_clean_end(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = CleanEnd()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


def test_clean_end_stree_test():
    start_aya = Aya()
    op = CleanEnd()
    moshaf = MoshafAttributes(
        rewaya="hafs",
        madd_monfasel_len=4,
        madd_mottasel_len=4,
        madd_mottasel_waqf=4,
        madd_aared_len=4,
    )

    is_error = False
    for aya in start_aya.get_ayat_after(114):
        txt = aya.get().uthmani
        out_text = op.apply(txt, moshaf, mode="test")
        if out_text[-1] not in (
            alph.uthmani.letters_group + alph.uthmani.ras_haaa + alph.uthmani.shadda
        ):
            is_error = True
            print(aya)
            print(out_text)
            print("\n" * 2)
    if is_error:
        raise ValueError()


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "لَّا مَقْطُوعَةٍۢ وَلَا مَمْنُوعَةٍۢ",
            "لَّا مَقْطُوعَتٍۢ وَلَا مَمْنُوعَه",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_normalize_taa(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = NormalizeTaa()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ الٓمٓ ٱللَّهُ لَآ إِلَـٰهَ",
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ أَلِفْ لَآم مِّيٓمَ ٱللَّهُ لَآ إِلَـٰهَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "الٓمٓ",
            "أَلِفْ لَآم مِّيٓمْ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "الٓمٓ ذَٰلِكَ ٱلْكِتَـٰبُ لَا",
            "أَلِفْ لَآم مِّيٓمْ ذَٰلِكَ ٱلْكِتَـٰبُ لَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ الٓمٓ ذَٰلِكَ ٱلْكِتَـٰبُ لَا",
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ أَلِفْ لَآم مِّيٓمْ ذَٰلِكَ ٱلْكِتَـٰبُ لَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "وَبَشِّرِ ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّـٰلِحَـٰتِ أَنَّ لَهُمْ جَنَّـٰتٍۢ تَجْرِى مِن تَحْتِهَا ٱلْأَنْهَـٰرُ كُلَّمَا رُزِقُوا۟ مِنْهَا مِن ثَمَرَةٍۢ رِّزْقًۭا قَالُوا۟ هَـٰذَا ٱلَّذِى رُزِقْنَا مِن قَبْلُ وَأُتُوا۟ بِهِۦ مُتَشَـٰبِهًۭا وَلَهُمْ فِيهَآ أَزْوَٰجٌۭ مُّطَهَّرَةٌۭ وَهُمْ فِيهَا خَـٰلِدُونَ",
            "وَبَشِّرِ ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّـٰلِحَـٰتِ أَنَّ لَهُمْ جَنَّـٰتٍۢ تَجْرِى مِن تَحْتِهَا ٱلْأَنْهَـٰرُ كُلَّمَا رُزِقُوا۟ مِنْهَا مِن ثَمَرَةٍۢ رِّزْقًۭا قَالُوا۟ هَـٰذَا ٱلَّذِى رُزِقْنَا مِن قَبْلُ وَأُتُوا۟ بِهِۦ مُتَشَـٰبِهًۭا وَلَهُمْ فِيهَآ أَزْوَٰجٌۭ مُّطَهَّرَةٌۭ وَهُمْ فِيهَا خَـٰلِدُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
        (
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ حمٓ عٓسٓقٓ كَذَٰلِكَ يُوحِىٓ",
            "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ حَا مِيٓمْ عَيٓن سِيٓن قَآفْ كَذَٰلِكَ يُوحِىٓ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
            ),
        ),
    ],
)
def test_disassemble_hrof_moqatta(
    in_text: str, target_text: str, moshaf: MoshafAttributes
):
    op = DisassembleHrofMoqatta()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text


@pytest.mark.parametrize(
    "in_text, target_text, moshaf",
    [
        (
            "ٱلْحَمْدُ لِلَّهِ ٱلَّذِىٓ أَنزَلَ عَلَىٰ عَبْدِهِ ٱلْكِتَـٰبَ وَلَمْ يَجْعَل لَّهُۥ عِوَجَا قَيِّمًۭا لِّيُنذِرَ بَأْسًۭا شَدِيدًۭا",
            "ٱلْحَمْدُ لِلَّهِ ٱلَّذِىٓ أَنزَلَ عَلَىٰ عَبْدِهِ ٱلْكِتَـٰبَ وَلَمْ يَجْعَل لَّهُۥ عِوَجَاۜ قَيِّمًۭا لِّيُنذِرَ بَأْسًۭا شَدِيدًۭا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_iwaja="sakt",
            ),
        ),
        (
            "ٱلْحَمْدُ لِلَّهِ ٱلَّذِىٓ أَنزَلَ عَلَىٰ عَبْدِهِ ٱلْكِتَـٰبَ وَلَمْ يَجْعَل لَّهُۥ عِوَجَا قَيِّمًۭا لِّيُنذِرَ بَأْسًۭا شَدِيدًۭا",
            "ٱلْحَمْدُ لِلَّهِ ٱلَّذِىٓ أَنزَلَ عَلَىٰ عَبْدِهِ ٱلْكِتَـٰبَ وَلَمْ يَجْعَل لَّهُۥ عِوَجًۭا قَيِّمًۭا لِّيُنذِرَ بَأْسًۭا شَدِيدًۭا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_iwaja="idraj",
            ),
        ),
        (
            "قَالُوا۟ يَـٰوَيْلَنَا مَنۢ بَعَثَنَا مِن مَّرْقَدِنَا هَـٰذَا مَا وَعَدَ ٱلرَّحْمَـٰنُ وَصَدَقَ ٱلْمُرْسَلُونَ",
            "قَالُوا۟ يَـٰوَيْلَنَا مَنۢ بَعَثَنَا مِن مَّرْقَدِنَاۜ هَـٰذَا مَا وَعَدَ ٱلرَّحْمَـٰنُ وَصَدَقَ ٱلْمُرْسَلُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_marqdena="sakt",
            ),
        ),
        (
            "قَالُوا۟ يَـٰوَيْلَنَا مَنۢ بَعَثَنَا مِن مَّرْقَدِنَا هَـٰذَا مَا وَعَدَ ٱلرَّحْمَـٰنُ وَصَدَقَ ٱلْمُرْسَلُونَ",
            "قَالُوا۟ يَـٰوَيْلَنَا مَنۢ بَعَثَنَا مِن مَّرْقَدِنَا هَـٰذَا مَا وَعَدَ ٱلرَّحْمَـٰنُ وَصَدَقَ ٱلْمُرْسَلُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_marqdena="idraj",
            ),
        ),
        (
            "وَقِيلَ مَنْ رَاقٍۢ",
            "وَقِيلَ مَنْۜ رَاقٍۢ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_man_raq="sakt",
            ),
        ),
        (
            "وَقِيلَ مَنْ رَاقٍۢ",
            "وَقِيلَ مَن رَّاقٍۢ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_man_raq="idraj",
            ),
        ),
        (
            "كَلَّا بَلْ رَانَ عَلَىٰ قُلُوبِهِم",
            "كَلَّا بَلْۜ رَانَ عَلَىٰ قُلُوبِهِم",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_bal_ran="sakt",
            ),
        ),
        (
            "كَلَّا بَلْ رَانَ عَلَىٰ قُلُوبِهِم",
            "كَلَّا بَل رَّانَ عَلَىٰ قُلُوبِهِم",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_bal_ran="idraj",
            ),
        ),
        (
            "مَآ أَغْنَىٰ عَنِّى مَالِيَهْ هَلَكَ عَنِّى سُلْطَـٰنِيَهْ",
            "مَآ أَغْنَىٰ عَنِّى مَالِيَهْۜ هَلَكَ عَنِّى سُلْطَـٰنِيَهْ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_maleeyah="sakt",
            ),
        ),
        (
            "مَآ أَغْنَىٰ عَنِّى مَالِيَهْ هَلَكَ عَنِّى سُلْطَـٰنِيَهْ",
            "مَآ أَغْنَىٰ عَنِّى مَالِيَه هَّلَكَ عَنِّى سُلْطَـٰنِيَهْ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                sakt_maleeyah="idgham",
            ),
        ),
        (
            "إِنَّ ٱللَّهَ بِكُلِّ شَىْءٍ عَلِيمٌۢ بَرَآءَةٌۭ مِّنَ ٱللَّهِ وَرَسُولِهِۦٓ",
            "إِنَّ ٱللَّهَ بِكُلِّ شَىْءٍ عَلِيمۜ بَرَآءَةٌۭ مِّنَ ٱللَّهِ وَرَسُولِهِۦٓ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                between_anfal_and_tawba="sakt",
            ),
        ),
        (
            "إِنَّ ٱللَّهَ بِكُلِّ شَىْءٍ عَلِيمٌۢ بَرَآءَةٌۭ مِّنَ ٱللَّهِ وَرَسُولِهِۦٓ",
            "إِنَّ ٱللَّهَ بِكُلِّ شَىْءٍ عَلِيمٌۢ بَرَآءَةٌۭ مِّنَ ٱللَّهِ وَرَسُولِهِۦٓ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                between_anfal_and_tawba="wasl",
            ),
        ),
        (
            "يسٓ",
            "يسٓ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_and_yaseen="izhar",
            ),
        ),
        (
            "يسٓ وَٱلْقُرْءَانِ ٱلْحَكِيمِ",
            "يَا سِيٓنْ وَٱلْقُرْءَانِ ٱلْحَكِيمِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_and_yaseen="izhar",
            ),
        ),
        (
            "يسٓ وَٱلْقُرْءَانِ ٱلْحَكِيمِ",
            "يَا سِيٓن وَٱلْقُرْءَانِ ٱلْحَكِيمِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_and_yaseen="idgham",
            ),
        ),
        (
            "نٓ وَٱلْقَلَمِ",
            "نُوٓنْ وَٱلْقَلَمِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_and_yaseen="izhar",
            ),
        ),
        (
            "نٓ وَٱلْقَلَمِ",
            "نُوٓن وَٱلْقَلَمِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_and_yaseen="idgham",
            ),
        ),
        (
            "فَلَمَّا جَآءَ سُلَيْمَـٰنَ قَالَ أَتُمِدُّونَنِ بِمَالٍۢ فَمَآ ءَاتَىٰنِۦَ ٱللَّهُ خَيْرٌۭ مِّمَّآ ءَاتَىٰكُم بَلْ أَنتُم بِهَدِيَّتِكُمْ تَفْرَحُونَ",
            "فَلَمَّا جَآءَ سُلَيْمَـٰنَ قَالَ أَتُمِدُّونَنِ بِمَالٍۢ فَمَآ ءَاتَىٰنِۦَ ٱللَّهُ خَيْرٌۭ مِّمَّآ ءَاتَىٰكُم بَلْ أَنتُم بِهَدِيَّتِكُمْ تَفْرَحُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yaa_ataan="wasl",
            ),
        ),
        (
            "فَلَمَّا جَآءَ سُلَيْمَـٰنَ قَالَ أَتُمِدُّونَنِ بِمَالٍۢ فَمَآ ءَاتَىٰنِۦَ",
            "فَلَمَّا جَآءَ سُلَيْمَـٰنَ قَالَ أَتُمِدُّونَنِ بِمَالٍۢ فَمَآ ءَاتَىٰنِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yaa_ataan="hadhf",
            ),
        ),
        (
            "فَلَمَّا جَآءَ سُلَيْمَـٰنَ قَالَ أَتُمِدُّونَنِ بِمَالٍۢ فَمَآ ءَاتَىٰنِۦَ",
            "فَلَمَّا جَآءَ سُلَيْمَـٰنَ قَالَ أَتُمِدُّونَنِ بِمَالٍۢ فَمَآ ءَاتَىٰنِي",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yaa_ataan="ithbat",
            ),
        ),
        (
            "يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ لَا يَسْخَرْ قَوْمٌۭ مِّن قَوْمٍ عَسَىٰٓ أَن يَكُونُوا۟ خَيْرًۭا مِّنْهُمْ وَلَا نِسَآءٌۭ مِّن نِّسَآءٍ عَسَىٰٓ أَن يَكُنَّ خَيْرًۭا مِّنْهُنَّ وَلَا تَلْمِزُوٓا۟ أَنفُسَكُمْ وَلَا تَنَابَزُوا۟ بِٱلْأَلْقَـٰبِ بِئْسَ ٱلِٱسْمُ ٱلْفُسُوقُ بَعْدَ ٱلْإِيمَـٰنِ وَمَن لَّمْ يَتُبْ فَأُو۟لَـٰٓئِكَ هُمُ ٱلظَّـٰلِمُونَ",
            "يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ لَا يَسْخَرْ قَوْمٌۭ مِّن قَوْمٍ عَسَىٰٓ أَن يَكُونُوا۟ خَيْرًۭا مِّنْهُمْ وَلَا نِسَآءٌۭ مِّن نِّسَآءٍ عَسَىٰٓ أَن يَكُنَّ خَيْرًۭا مِّنْهُنَّ وَلَا تَلْمِزُوٓا۟ أَنفُسَكُمْ وَلَا تَنَابَزُوا۟ بِٱلْأَلْقَـٰبِ بِئْسَ ٱلِٱسْمُ ٱلْفُسُوقُ بَعْدَ ٱلْإِيمَـٰنِ وَمَن لَّمْ يَتُبْ فَأُو۟لَـٰٓئِكَ هُمُ ٱلظَّـٰلِمُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                start_with_ism="wasl",
            ),
        ),
        (
            "ٱلِٱسْمُ ٱلْفُسُوقُ بَعْدَ ٱلْإِيمَـٰنِ وَمَن لَّمْ يَتُبْ فَأُو۟لَـٰٓئِكَ",
            "لِسْمُ ٱلْفُسُوقُ بَعْدَ ٱلْإِيمَـٰنِ وَمَن لَّمْ يَتُبْ فَأُو۟لَـٰٓئِكَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                start_with_ism="lism",
            ),
        ),
        (
            "ٱلِٱسْمُ ٱلْفُسُوقُ بَعْدَ ٱلْإِيمَـٰنِ وَمَن لَّمْ يَتُبْ فَأُو۟لَـٰٓئِكَ",
            "أَلِسْمُ ٱلْفُسُوقُ بَعْدَ ٱلْإِيمَـٰنِ وَمَن لَّمْ يَتُبْ فَأُو۟لَـٰٓئِكَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                start_with_ism="alism",
            ),
        ),
        (
            "مَّن ذَا ٱلَّذِى يُقْرِضُ ٱللَّهَ قَرْضًا حَسَنًۭا فَيُضَـٰعِفَهُۥ لَهُۥٓ أَضْعَافًۭا كَثِيرَةًۭ وَٱللَّهُ يَقْبِضُ وَيَبْصُۜطُ وَإِلَيْهِ تُرْجَعُونَ",
            "مَّن ذَا ٱلَّذِى يُقْرِضُ ٱللَّهَ قَرْضًا حَسَنًۭا فَيُضَـٰعِفَهُۥ لَهُۥٓ أَضْعَافًۭا كَثِيرَةًۭ وَٱللَّهُ يَقْبِضُ وَيَبْسُطُ وَإِلَيْهِ تُرْجَعُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yabsut="seen",
            ),
        ),
        (
            "مَّن ذَا ٱلَّذِى يُقْرِضُ ٱللَّهَ قَرْضًا حَسَنًۭا فَيُضَـٰعِفَهُۥ لَهُۥٓ أَضْعَافًۭا كَثِيرَةًۭ وَٱللَّهُ يَقْبِضُ وَيَبْصُۜطُ وَإِلَيْهِ تُرْجَعُونَ",
            "مَّن ذَا ٱلَّذِى يُقْرِضُ ٱللَّهَ قَرْضًا حَسَنًۭا فَيُضَـٰعِفَهُۥ لَهُۥٓ أَضْعَافًۭا كَثِيرَةًۭ وَٱللَّهُ يَقْبِضُ وَيَبْصُطُ وَإِلَيْهِ تُرْجَعُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yabsut="saad",
            ),
        ),
        (
            "أَوَعَجِبْتُمْ أَن جَآءَكُمْ ذِكْرٌۭ مِّن رَّبِّكُمْ عَلَىٰ رَجُلٍۢ مِّنكُمْ لِيُنذِرَكُمْ وَٱذْكُرُوٓا۟ إِذْ جَعَلَكُمْ خُلَفَآءَ مِنۢ بَعْدِ قَوْمِ نُوحٍۢ وَزَادَكُمْ فِى ٱلْخَلْقِ بَصْۜطَةًۭ فَٱذْكُرُوٓا۟ ءَالَآءَ ٱللَّهِ لَعَلَّكُمْ تُفْلِحُونَ",
            "أَوَعَجِبْتُمْ أَن جَآءَكُمْ ذِكْرٌۭ مِّن رَّبِّكُمْ عَلَىٰ رَجُلٍۢ مِّنكُمْ لِيُنذِرَكُمْ وَٱذْكُرُوٓا۟ إِذْ جَعَلَكُمْ خُلَفَآءَ مِنۢ بَعْدِ قَوْمِ نُوحٍۢ وَزَادَكُمْ فِى ٱلْخَلْقِ بَسْطَةًۭ فَٱذْكُرُوٓا۟ ءَالَآءَ ٱللَّهِ لَعَلَّكُمْ تُفْلِحُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                bastah="seen",
            ),
        ),
        (
            "أَوَعَجِبْتُمْ أَن جَآءَكُمْ ذِكْرٌۭ مِّن رَّبِّكُمْ عَلَىٰ رَجُلٍۢ مِّنكُمْ لِيُنذِرَكُمْ وَٱذْكُرُوٓا۟ إِذْ جَعَلَكُمْ خُلَفَآءَ مِنۢ بَعْدِ قَوْمِ نُوحٍۢ وَزَادَكُمْ فِى ٱلْخَلْقِ بَصْۜطَةًۭ فَٱذْكُرُوٓا۟ ءَالَآءَ ٱللَّهِ لَعَلَّكُمْ تُفْلِحُونَ",
            "أَوَعَجِبْتُمْ أَن جَآءَكُمْ ذِكْرٌۭ مِّن رَّبِّكُمْ عَلَىٰ رَجُلٍۢ مِّنكُمْ لِيُنذِرَكُمْ وَٱذْكُرُوٓا۟ إِذْ جَعَلَكُمْ خُلَفَآءَ مِنۢ بَعْدِ قَوْمِ نُوحٍۢ وَزَادَكُمْ فِى ٱلْخَلْقِ بَصْطَةًۭ فَٱذْكُرُوٓا۟ ءَالَآءَ ٱللَّهِ لَعَلَّكُمْ تُفْلِحُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                bastah="saad",
            ),
        ),
        (
            "أَمْ عِندَهُمْ خَزَآئِنُ رَبِّكَ أَمْ هُمُ ٱلْمُصَۣيْطِرُونَ",
            "أَمْ عِندَهُمْ خَزَآئِنُ رَبِّكَ أَمْ هُمُ ٱلْمُسَيْطِرُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                almusaytirun="seen",
            ),
        ),
        (
            "أَمْ عِندَهُمْ خَزَآئِنُ رَبِّكَ أَمْ هُمُ ٱلْمُصَۣيْطِرُونَ",
            "أَمْ عِندَهُمْ خَزَآئِنُ رَبِّكَ أَمْ هُمُ ٱلْمُصَيْطِرُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                almusaytirun="saad",
            ),
        ),
        (
            "لَّسْتَ عَلَيْهِم بِمُصَيْطِرٍ",
            "لَّسْتَ عَلَيْهِم بِمُسَيْطِرٍ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                bimusaytir="seen",
            ),
        ),
        (
            "لَّسْتَ عَلَيْهِم بِمُصَيْطِرٍ",
            "لَّسْتَ عَلَيْهِم بِمُصَيْطِرٍ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                bimusaytir="saad",
            ),
        ),
        (
            "يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ لَا تُحِلُّوا۟ شَعَـٰٓئِرَ ٱللَّهِ وَلَا ٱلشَّهْرَ ٱلْحَرَامَ وَلَا ٱلْهَدْىَ وَلَا ٱلْقَلَـٰٓئِدَ وَلَآ ءَآمِّينَ ٱلْبَيْتَ ٱلْحَرَامَ يَبْتَغُونَ فَضْلًۭا مِّن رَّبِّهِمْ وَرِضْوَٰنًۭا وَإِذَا حَلَلْتُمْ فَٱصْطَادُوا۟ وَلَا يَجْرِمَنَّكُمْ شَنَـَٔانُ قَوْمٍ أَن صَدُّوكُمْ عَنِ ٱلْمَسْجِدِ ٱلْحَرَامِ أَن تَعْتَدُوا۟ وَتَعَاوَنُوا۟ عَلَى ٱلْبِرِّ وَٱلتَّقْوَىٰ وَلَا تَعَاوَنُوا۟ عَلَى ٱلْإِثْمِ وَٱلْعُدْوَٰنِ وَٱتَّقُوا۟ ٱللَّهَ إِنَّ ٱللَّهَ شَدِيدُ ٱلْعِقَابِ",
            "يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ لَا تُحِلُّوا۟ شَعَـٰٓئِرَ ٱللَّهِ وَلَا ٱلشَّهْرَ ٱلْحَرَامَ وَلَا ٱلْهَدْىَ وَلَا ٱلْقَلَـٰٓئِدَ وَلَآ ءَآمِّينَ ٱلْبَيْتَ ٱلْحَرَامَ يَبْتَغُونَ فَضْلًۭا مِّن رَّبِّهِمْ وَرِضْوَٰنًۭا وَإِذَا حَلَلْتُمْ فَٱصْطَادُوا۟ وَلَا يَجْرِمَنَّكُمْ شَنَـَٔانُ قَوْمٍ أَن صَدُّوكُمْ عَنِ ٱلْمَسْجِدِ ٱلْحَرَامِ أَن تَعْتَدُوا۟ وَتَعَاوَنُوا۟ عَلَى ٱلْبِرِّ وَٱلتَّقْوَىٰ وَلَا تَعَاوَنُوا۟ عَلَى ٱلْإِثْمِ وَٱلْعُدْوَٰنِ وَٱتَّقُوا۟ ٱللَّهَ إِنَّ ٱللَّهَ شَدِيدُ ٱلْعِقَابِ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                tasheel_or_madd="tasheel",
            ),
        ),
        (
            "ثَمَـٰنِيَةَ أَزْوَٰجٍۢ مِّنَ ٱلضَّأْنِ ٱثْنَيْنِ وَمِنَ ٱلْمَعْزِ ٱثْنَيْنِ قُلْ ءَآلذَّكَرَيْنِ حَرَّمَ أَمِ ٱلْأُنثَيَيْنِ أَمَّا ٱشْتَمَلَتْ عَلَيْهِ أَرْحَامُ ٱلْأُنثَيَيْنِ نَبِّـُٔونِى بِعِلْمٍ إِن كُنتُمْ صَـٰدِقِينَ",
            "ثَمَـٰنِيَةَ أَزْوَٰجٍۢ مِّنَ ٱلضَّأْنِ ٱثْنَيْنِ وَمِنَ ٱلْمَعْزِ ٱثْنَيْنِ قُلْ ءَا۬لذَّكَرَيْنِ حَرَّمَ أَمِ ٱلْأُنثَيَيْنِ أَمَّا ٱشْتَمَلَتْ عَلَيْهِ أَرْحَامُ ٱلْأُنثَيَيْنِ نَبِّـُٔونِى بِعِلْمٍ إِن كُنتُمْ صَـٰدِقِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                tasheel_or_madd="tasheel",
            ),
        ),
        (
            "ثَمَـٰنِيَةَ أَزْوَٰجٍۢ مِّنَ ٱلضَّأْنِ ٱثْنَيْنِ وَمِنَ ٱلْمَعْزِ ٱثْنَيْنِ قُلْ ءَآلذَّكَرَيْنِ حَرَّمَ أَمِ ٱلْأُنثَيَيْنِ أَمَّا ٱشْتَمَلَتْ عَلَيْهِ أَرْحَامُ ٱلْأُنثَيَيْنِ نَبِّـُٔونِى بِعِلْمٍ إِن كُنتُمْ صَـٰدِقِينَ",
            "ثَمَـٰنِيَةَ أَزْوَٰجٍۢ مِّنَ ٱلضَّأْنِ ٱثْنَيْنِ وَمِنَ ٱلْمَعْزِ ٱثْنَيْنِ قُلْ ءَآلذَّكَرَيْنِ حَرَّمَ أَمِ ٱلْأُنثَيَيْنِ أَمَّا ٱشْتَمَلَتْ عَلَيْهِ أَرْحَامُ ٱلْأُنثَيَيْنِ نَبِّـُٔونِى بِعِلْمٍ إِن كُنتُمْ صَـٰدِقِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                tasheel_or_madd="madd",
            ),
        ),
        (
            "قُلِ ٱلْحَمْدُ لِلَّهِ وَسَلَـٰمٌ عَلَىٰ عِبَادِهِ ٱلَّذِينَ ٱصْطَفَىٰٓ ءَآللَّهُ خَيْرٌ أَمَّا يُشْرِكُونَ",
            "قُلِ ٱلْحَمْدُ لِلَّهِ وَسَلَـٰمٌ عَلَىٰ عِبَادِهِ ٱلَّذِينَ ٱصْطَفَىٰٓ ءَا۬للَّهُ خَيْرٌ أَمَّا يُشْرِكُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                tasheel_or_madd="tasheel",
            ),
        ),
        (
            "قُلِ ٱلْحَمْدُ لِلَّهِ وَسَلَـٰمٌ عَلَىٰ عِبَادِهِ ٱلَّذِينَ ٱصْطَفَىٰٓ ءَآللَّهُ خَيْرٌ أَمَّا يُشْرِكُونَ",
            "قُلِ ٱلْحَمْدُ لِلَّهِ وَسَلَـٰمٌ عَلَىٰ عِبَادِهِ ٱلَّذِينَ ٱصْطَفَىٰٓ ءَآللَّهُ خَيْرٌ أَمَّا يُشْرِكُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                tasheel_or_madd="madd",
            ),
        ),
        (
            "ءَآلْـَٔـٰنَ وَقَدْ عَصَيْتَ قَبْلُ وَكُنتَ مِنَ ٱلْمُفْسِدِينَ",
            "ءَا۬لْـَٔـٰنَ وَقَدْ عَصَيْتَ قَبْلُ وَكُنتَ مِنَ ٱلْمُفْسِدِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                tasheel_or_madd="tasheel",
            ),
        ),
        (
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث ذَّٰلِكَ مَثَلُ ٱلْقَوْمِ ٱلَّذِينَ كَذَّبُوا۟ بِـَٔايَـٰتِنَا فَٱقْصُصِ ٱلْقَصَصَ لَعَلَّهُمْ يَتَفَكَّرُونَ",
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَثْ ذَٰلِكَ مَثَلُ ٱلْقَوْمِ ٱلَّذِينَ كَذَّبُوا۟ بِـَٔايَـٰتِنَا فَٱقْصُصِ ٱلْقَصَصَ لَعَلَّهُمْ يَتَفَكَّرُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yalhath_dhalik="izhar",
            ),
        ),
        (
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث",
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yalhath_dhalik="izhar",
            ),
        ),
        (
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث",
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yalhath_dhalik="waqf",
            ),
        ),
        (
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث ذَّٰلِكَ مَثَلُ ٱلْقَوْمِ ٱلَّذِينَ كَذَّبُوا۟ بِـَٔايَـٰتِنَا فَٱقْصُصِ ٱلْقَصَصَ لَعَلَّهُمْ يَتَفَكَّرُونَ",
            "وَلَوْ شِئْنَا لَرَفَعْنَـٰهُ بِهَا وَلَـٰكِنَّهُۥٓ أَخْلَدَ إِلَى ٱلْأَرْضِ وَٱتَّبَعَ هَوَىٰهُ فَمَثَلُهُۥ كَمَثَلِ ٱلْكَلْبِ إِن تَحْمِلْ عَلَيْهِ يَلْهَثْ أَوْ تَتْرُكْهُ يَلْهَث ذَّٰلِكَ مَثَلُ ٱلْقَوْمِ ٱلَّذِينَ كَذَّبُوا۟ بِـَٔايَـٰتِنَا فَٱقْصُصِ ٱلْقَصَصَ لَعَلَّهُمْ يَتَفَكَّرُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                yalhath_dhalik="idgham",
            ),
        ),
        (
            "وَهِىَ تَجْرِى بِهِمْ فِى مَوْجٍۢ كَٱلْجِبَالِ وَنَادَىٰ نُوحٌ ٱبْنَهُۥ وَكَانَ فِى مَعْزِلٍۢ يَـٰبُنَىَّ ٱرْكَب مَّعَنَا وَلَا تَكُن مَّعَ ٱلْكَـٰفِرِينَ",
            "وَهِىَ تَجْرِى بِهِمْ فِى مَوْجٍۢ كَٱلْجِبَالِ وَنَادَىٰ نُوحٌ ٱبْنَهُۥ وَكَانَ فِى مَعْزِلٍۢ يَـٰبُنَىَّ ٱرْكَبْ مَعَنَا وَلَا تَكُن مَّعَ ٱلْكَـٰفِرِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                irkab_maana="izhar",
            ),
        ),
        (
            "وَهِىَ تَجْرِى بِهِمْ فِى مَوْجٍۢ كَٱلْجِبَالِ وَنَادَىٰ نُوحٌ ٱبْنَهُۥ وَكَانَ فِى مَعْزِلٍۢ يَـٰبُنَىَّ ٱرْكَب مَّعَنَا وَلَا تَكُن مَّعَ ٱلْكَـٰفِرِينَ",
            "وَهِىَ تَجْرِى بِهِمْ فِى مَوْجٍۢ كَٱلْجِبَالِ وَنَادَىٰ نُوحٌ ٱبْنَهُۥ وَكَانَ فِى مَعْزِلٍۢ يَـٰبُنَىَّ ٱرْكَب مَّعَنَا وَلَا تَكُن مَّعَ ٱلْكَـٰفِرِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                irkab_maana="idgham",
            ),
        ),
        (
            "قَالُوا۟ يَـٰٓأَبَانَا مَا لَكَ لَا تَأْمَ۫نَّا عَلَىٰ يُوسُفَ وَإِنَّا لَهُۥ لَنَـٰصِحُونَ",
            "قَالُوا۟ يَـٰٓأَبَانَا مَا لَكَ لَا تَأْمَنَّا عَلَىٰ يُوسُفَ وَإِنَّا لَهُۥ لَنَـٰصِحُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_tamnna="ishmam",
            ),
        ),
        (
            "قَالُوا۟ يَـٰٓأَبَانَا مَا لَكَ لَا تَأْمَ۫نَّا عَلَىٰ يُوسُفَ وَإِنَّا لَهُۥ لَنَـٰصِحُونَ",
            "قَالُوا۟ يَـٰٓأَبَانَا مَا لَكَ لَا تَأْمَنؙنَا عَلَىٰ يُوسُفَ وَإِنَّا لَهُۥ لَنَـٰصِحُونَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                noon_tamnna="rawm",
            ),
        ),
        (
            "ٱلْـَٔـٰنَ خَفَّفَ ٱللَّهُ عَنكُمْ وَعَلِمَ أَنَّ فِيكُمْ ضَعْفًۭا فَإِن يَكُن مِّنكُم مِّا۟ئَةٌۭ صَابِرَةٌۭ يَغْلِبُوا۟ مِا۟ئَتَيْنِ وَإِن يَكُن مِّنكُمْ أَلْفٌۭ يَغْلِبُوٓا۟ أَلْفَيْنِ بِإِذْنِ ٱللَّهِ وَٱللَّهُ مَعَ ٱلصَّـٰبِرِينَ",
            "ٱلْـَٔـٰنَ خَفَّفَ ٱللَّهُ عَنكُمْ وَعَلِمَ أَنَّ فِيكُمْ ضَعْفًۭا فَإِن يَكُن مِّنكُم مِّا۟ئَةٌۭ صَابِرَةٌۭ يَغْلِبُوا۟ مِا۟ئَتَيْنِ وَإِن يَكُن مِّنكُمْ أَلْفٌۭ يَغْلِبُوٓا۟ أَلْفَيْنِ بِإِذْنِ ٱللَّهِ وَٱللَّهُ مَعَ ٱلصَّـٰبِرِينَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                harakat_daaf="dam",
            ),
        ),
        (
            "ٱللَّهُ ٱلَّذِى خَلَقَكُم مِّن ضَعْفٍۢ ثُمَّ جَعَلَ مِنۢ بَعْدِ ضَعْفٍۢ قُوَّةًۭ ثُمَّ جَعَلَ مِنۢ بَعْدِ قُوَّةٍۢ ضَعْفًۭا وَشَيْبَةًۭ يَخْلُقُ مَا يَشَآءُ وَهُوَ ٱلْعَلِيمُ ٱلْقَدِيرُ",
            "ٱللَّهُ ٱلَّذِى خَلَقَكُم مِّن ضُعْفٍۢ ثُمَّ جَعَلَ مِنۢ بَعْدِ ضُعْفٍۢ قُوَّةًۭ ثُمَّ جَعَلَ مِنۢ بَعْدِ قُوَّةٍۢ ضُعْفًۭا وَشَيْبَةًۭ يَخْلُقُ مَا يَشَآءُ وَهُوَ ٱلْعَلِيمُ ٱلْقَدِيرُ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                harakat_daaf="dam",
            ),
        ),
        (
            "ٱللَّهُ ٱلَّذِى خَلَقَكُم مِّن ضَعْفٍۢ ثُمَّ جَعَلَ مِنۢ بَعْدِ ضَعْفٍۢ قُوَّةًۭ ثُمَّ جَعَلَ مِنۢ بَعْدِ قُوَّةٍۢ ضَعْفًۭا وَشَيْبَةًۭ يَخْلُقُ مَا يَشَآءُ وَهُوَ ٱلْعَلِيمُ ٱلْقَدِيرُ",
            "ٱللَّهُ ٱلَّذِى خَلَقَكُم مِّن ضَعْفٍۢ ثُمَّ جَعَلَ مِنۢ بَعْدِ ضَعْفٍۢ قُوَّةًۭ ثُمَّ جَعَلَ مِنۢ بَعْدِ قُوَّةٍۢ ضَعْفًۭا وَشَيْبَةًۭ يَخْلُقُ مَا يَشَآءُ وَهُوَ ٱلْعَلِيمُ ٱلْقَدِيرُ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                harakat_daaf="fath",
            ),
        ),
        (
            "إِنَّآ أَعْتَدْنَا لِلْكَـٰفِرِينَ سَلَـٰسِلَا۟ وَأَغْلَـٰلًۭا وَسَعِيرًا",
            "إِنَّآ أَعْتَدْنَا لِلْكَـٰفِرِينَ سَلَـٰسِلَا۟ وَأَغْلَـٰلًۭا وَسَعِيرًا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                alif_salasila="ithbat",
            ),
        ),
        (
            "إِنَّآ أَعْتَدْنَا لِلْكَـٰفِرِينَ سَلَـٰسِلَا۟",
            "إِنَّآ أَعْتَدْنَا لِلْكَـٰفِرِينَ سَلَـٰسِلَا",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                alif_salasila="ithbat",
            ),
        ),
        (
            "إِنَّآ أَعْتَدْنَا لِلْكَـٰفِرِينَ سَلَـٰسِلَا۟",
            "إِنَّآ أَعْتَدْنَا لِلْكَـٰفِرِينَ سَلَـٰسِلَ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                alif_salasila="hadhf",
            ),
        ),
        (
            "أَلَمْ نَخْلُقكُّم مِّن مَّآءٍۢ مَّهِينٍۢ",
            "أَلَمْ نَخْلُقكُّم مِّن مَّآءٍۢ مَّهِينٍۢ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                idgham_nakhluqkum="idgham_kamil",
            ),
        ),
        (
            "أَلَمْ نَخْلُقكُّم مِّن مَّآءٍۢ مَّهِينٍۢ",
            "أَلَمْ نَخْلُقكُم مِّن مَّآءٍۢ مَّهِينٍۢ",
            MoshafAttributes(
                rewaya="hafs",
                madd_monfasel_len=4,
                madd_mottasel_len=4,
                madd_mottasel_waqf=4,
                madd_aared_len=4,
                idgham_nakhluqkum="idgham_naqis",
            ),
        ),
    ],
)
def test_special_cases(in_text: str, target_text: str, moshaf: MoshafAttributes):
    op = SpecialCases()
    for b_op in op.ops_before:
        target_text = b_op.apply(target_text, moshaf)
    out_text = op.apply(in_text, moshaf, mode="test")
    print(out_text)
    assert out_text == target_text
