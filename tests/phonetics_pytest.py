import pytest

from quran_transcript.phonetics.moshaf_attributes import MoshafAttributes
from quran_transcript.phonetics.operations import ConvertAlifMaksora
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
