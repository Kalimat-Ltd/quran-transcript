import pytest
import re

from quran_transcript.phonetics.moshaf_attributes import MoshafAttributes
from quran_transcript.phonetics.operations import (
    ConvertAlifMaksora,
    NormalizeHmazat,
    IthbatYaaYohie,
    RemoveKasheeda,
    RemoveHmzatWaslMiddle,
    RemoveSkoonMostadeer,
    SkoonMostateel,
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
