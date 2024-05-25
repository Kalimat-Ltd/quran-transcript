from pathlib import Path
import json
import xmltodict
from dataclasses import dataclass
import re
from app import alphabet as alpha


class PartOfUthmaniWord(Exception):
    pass


@dataclass
class RasmFormat:
    uthmani: list[list[str]]
    imlaey: list[list[str]]


@dataclass
class Vertex:
    aya_idx: int
    word_idx: int


@dataclass
class WordSpan:
    start: int
    end: int


@dataclass
class AyaFormat:
    sura_idx: int
    aya_idx: int
    sura_name: str
    num_ayat_in_sura: int
    uthmani: str
    imlaey: str
    istiaatha_uthmani: str
    istiaatha_imlaey: str
    rasm_map: dict[str, list[str]] = None
    bismillah_uthmani: str = None
    bismillah_imlaey: str = None
    bismillah_map: dict[str, list[str]] = None

    def get_formatted_rasm_map(
        self,
        join_prefix=" ",
        uthmani_key="@uthmani",
        imlaey_key="@imlaey",
    ) -> RasmFormat:
        """
        return rasm map in fromt like:
            [
                {'@uthmani: str, '@imlaey: str},
                {'@uthmani: str, '@imlaey: str},
            ]
            to
            RasmFormat.uthmani: list[list[str]]
            RasmFormat.imlaey: list[list[str]]
        """
        if self.rasm_map is None:
            raise ValueError("Rasmp map is None")

        uthmani_words: list[list[str]] = []
        imlaey_words: list[list[str]] = []
        for item in self.rasm_map:
            uthmani_words.append(item[uthmani_key].split(join_prefix))
            imlaey_words.append(item[imlaey_key].split(join_prefix))
        return RasmFormat(uthmani=uthmani_words, imlaey=imlaey_words)


# TODO: Add quran_dict as default
class Aya(object):
    def __init__(
        self,
        sura_idx=1,
        aya_idx=1,
        quran_path: str | Path = 'quran-script/quran-uthmani-imlaey.json',
        quran_dict: dict = None,
        prefix="@",
        map_key="rasm_map",
        bismillah_map_key="bismillah_map",
        bismillah_key="bismillah",
        uthmani_key="uthmani",
        imlaey_key="imlaey",
        sura_name_key="name",
        join_prefix=" ",
    ):
        """
        quran_path (str | Path) path to the quran json script with
            emlaey uthmani scripts
        sura_idx: the index of the Sura in the Quran starting with 1 to 114
        aya_idx: the index of the aya starting form 1
        """
        self.quran_path = Path(quran_path)
        if quran_dict is None:
            with open(self.quran_path, "r", encoding="utf8") as f:
                self.quran_dict = json.load(f)
        else:
            self.quran_dict = quran_dict

        # Loading Istiaath
        self.istiaatha_imlaey = alpha.istiaatha.imlaey
        self.istiaatha_uthmani = alpha.istiaatha.uthmani

        self._check_indices(sura_idx - 1, aya_idx - 1)
        self.sura_idx = sura_idx - 1
        self.aya_idx = aya_idx - 1

        self.map_key = map_key
        self.bismillah_map_key = bismillah_map_key
        self.uthmani_key = prefix + uthmani_key
        self.imlaey_key = prefix + imlaey_key
        self.sura_name_key = prefix + sura_name_key
        self.bismillah_uthmani_key = f"{prefix}{bismillah_key}_{uthmani_key}"
        self.bismillah_imlaey_key = f"{prefix}{bismillah_key}_{imlaey_key}"
        self.join_prefix = join_prefix

    def _get_sura(self, sura_idx):
        assert sura_idx >= 0 and sura_idx <= 113, f"Wrong Sura index {sura_idx + 1}"
        return self.quran_dict["quran"]["sura"][sura_idx]["aya"]

    def _get_sura_object(self, sura_idx):
        assert sura_idx >= 0 and sura_idx <= 113, f"Wrong Sura index {sura_idx + 1}"
        return self.quran_dict["quran"]["sura"][sura_idx]

    def _get_aya(self, sura_idx, aya_idx):
        assert aya_idx >= 0 and aya_idx < len(self._get_sura(sura_idx)), (
            f"Sura index out of range sura_index={sura_idx + 1} "
            + f"and len of sura={len(self._get_sura(sura_idx))}"
        )
        return self._get_sura(sura_idx)[aya_idx]

    def _get(self, sura_idx, aya_idx) -> AyaFormat:
        """
        get an aya from quran script
        Args:
            sura_idx (int): from 0 to 113
            aya_idx (int): form 0 to len(sura) - 1
        Example to get the first aya of sura Alfateha quran_scirt[1, 1]
        Return:
            AyaFormt:
                sura_idx (int): the absoulte index of the sura
                aya_idx (int): the absoulte index of the aya
                sura_name (str): the name of the sura
                num_aya_in_sura (int): number of ayat in the sura
                uthmani (str): the uthmani script of the aya
                imlaey (str): the imlaey script of the aya

                rasm_map (list[dict[str, str]]): maping from imaley to uthmani
                    scritps (word of uthmani to word or words of imlaey) and the
                    opesite. Example:
                    rasm_map=[
                        {'@uthmani': 'مِنَ', '@imlaey': 'مِنَ'},
                        {'@uthmani': 'ٱلْجِنَّةِ', '@imlaey': 'الْجِنَّةِ'},
                        {'@uthmani': 'وَٱلنَّاسِ', '@imlaey': 'وَالنَّاسِ'}]
                    Every item in the item is a dict with "@uthmain" and
                    if None: the rasem map is not set yet

                bismillah_uthmani (str): bismillah in uthmani script if the
                    aya index == 1 and the sura has bismillah or bismillah is
                    not aya like sura Alfateha and else (None)

                bismillah_imlaey (str): bismillah in uthmani script if the
                    aya index == 1 and the sura has bismillah or bismillah is
                    not aya like sura Alfateha and else (None)

                bismillah_map (list[dict[str, str]]): maping from imaley to uthmani
                    scritps (word of uthmani to word or words of imlaey) and
                    the opesite. Example:
                    bismillah_map=[
                        {'@uthmani': 'بِسْمِ', '@imlaey': 'بِسْمِ'},
                        {'@uthmani': 'ٱللَّهِ', '@imlaey': 'اللَّهِ'},
                        {'@uthmani': 'ٱلرَّحْمَـٰنِ', '@imlaey': 'الرَّحْمَٰنِ'},
                        {'@uthmani': 'ٱلرَّحِيمِ', '@imlaey': 'الرَّحِيمِ'}]
                        Every item in the item is a dict with "@uthmain" and
                    if None: the aya is not the first aya of the sura
                    (Note: bismillah maping is set automaticllay no by the user)
        """
        bismillah = {self.bismillah_uthmani_key: None,
                     self.bismillah_imlaey_key: None}
        for key in bismillah.keys():
            if key in self._get_aya(sura_idx, aya_idx).keys():
                bismillah[key] = self._get_aya(sura_idx, aya_idx)[key]

        bismillah_map = None
        if self.bismillah_map_key in self._get_aya(sura_idx, aya_idx).keys():
            bismillah_map = self._get_aya(sura_idx, aya_idx)[
                self.bismillah_map_key]

        rasm_map = None
        if self.map_key in self._get_aya(sura_idx, aya_idx).keys():
            rasm_map = self._get_aya(sura_idx, aya_idx)[self.map_key]

        return AyaFormat(
            sura_idx=sura_idx + 1,
            aya_idx=aya_idx + 1,
            sura_name=self._get_sura_object(sura_idx)[self.sura_name_key],
            num_ayat_in_sura=len(self._get_sura(sura_idx)),
            uthmani=self._get_aya(sura_idx, aya_idx)[self.uthmani_key],
            imlaey=self._get_aya(sura_idx, aya_idx)[self.imlaey_key],
            rasm_map=rasm_map,
            bismillah_uthmani=bismillah[self.bismillah_uthmani_key],
            bismillah_imlaey=bismillah[self.bismillah_imlaey_key],
            bismillah_map=bismillah_map,
            istiaatha_uthmani=self.istiaatha_uthmani,
            istiaatha_imlaey=self.istiaatha_imlaey,
        )

    def get(self) -> AyaFormat:
        """
        get an aya from quran script
        Return:
            AyaFormt:
                sura_idx (int): the absoulte index of the sura
                aya_idx (int): the absoulte index of the aya
                sura_name (str): the name of the sura
                uthmani (str): the uthmani script of the aya
                imlaey (str): the imlaey script of the aya

                bismillah_uthmani (str): bismillah in uthmani script if the
                    aya index == 1 and the sura has bismillah or bismillah is
                    not aya like sura Alfateha and else (None)

                bismillah_imlaey (str): bismillah in uthmani script if the
                    aya index == 1 and the sura has bismillah or bismillah is
                    not aya like sura Alfateha and else (None)
        """

        return self._get(self.sura_idx, self.aya_idx)

    def __str__(self):
        return str(self.get())

    def _check_indices(self, sura_idx: int, aya_idx: int):
        """
        check sura ds compatibility
        """
        assert sura_idx >= 0 and sura_idx <= 113, f"Wrong Sura index {sura_idx + 1}"

        assert aya_idx >= 0 and aya_idx < len(self._get_sura(sura_idx)), (
            f"Aya index out of range (sura_index={sura_idx + 1} "
            + f"aya_index={aya_idx + 1}) "
            + f"and length of sura={len(self._get_sura(sura_idx))}"
        )

    def _set_ids(self, sura_idx, aya_idx):
        self.sura_idx = sura_idx
        self.aya_idx = aya_idx

    def set(self, sura_idx, aya_idx) -> None:
        """Set the aya
        Args:
        sura_idx: the index of the Sura in the Quran starting with 1 to 114
        aya_idx: the index of the aya starting form 1
        """
        self._check_indices(sura_idx - 1, aya_idx - 1)
        self._set_ids(sura_idx=sura_idx - 1, aya_idx=aya_idx - 1)

    def set_new(self, sura_idx, aya_idx):
        """Return new aya with sura, and aya indices
        Args:
        sura_idx: the index of the Sura in the Quran starting with 1 to 114
        aya_idx: the index of the aya starting form 1
        """
        return Aya(
            quran_path=self.quran_path,
            sura_idx=sura_idx,
            aya_idx=aya_idx,
            quran_dict=self.quran_dict,
        )

    def step(self, step_len: int):
        """
        Return new Aya object with "step_len" aya after of before
        """
        aya_relative_idx = step_len + self.aya_idx

        # +VE or zero aya idx
        if aya_relative_idx >= 0:
            sura_idx = self.sura_idx
            while True:
                num_ayat = self._get(
                    sura_idx=sura_idx, aya_idx=0).num_ayat_in_sura
                if aya_relative_idx < num_ayat:
                    break
                aya_relative_idx -= num_ayat
                sura_idx = (sura_idx + 1) % 114

        # -VE aya idx
        else:
            sura_idx = (self.sura_idx - 1) % 114
            while True:
                num_ayat = self._get(
                    sura_idx=sura_idx, aya_idx=0).num_ayat_in_sura
                aya_relative_idx += num_ayat
                if aya_relative_idx >= 0:
                    break

        return Aya(
            quran_path=self.quran_path,
            sura_idx=sura_idx + 1,
            aya_idx=aya_relative_idx + 1,
            quran_dict=self.quran_dict,
        )

    # TODO: Add vertix
    def get_ayat_after(self, end_vertix=(114, 6), num_ayat=None):
        """
        iterator looping over Quran ayayt (verses) starting from the
        current aya to the end of the Holy Quran
        Args:
            num_aya: loop for ayat until reaching aya + num_ayat - 1
        """
        if num_ayat is not None:
            aya = self
            for _ in range(num_ayat):
                yield aya
                aya = aya.step(1)
            return

        aya_start_idx = self.aya_idx
        for sura_loop_idx in range(self.sura_idx, 114):
            for aya_loop_idx in range(
                aya_start_idx, len(self._get_sura(sura_loop_idx))
            ):
                yield Aya(
                    quran_path=self.quran_path,
                    sura_idx=sura_loop_idx + 1,
                    aya_idx=aya_loop_idx + 1,
                    quran_dict=self.quran_dict,
                )
            aya_start_idx = 0

    def _get_map_dict(
        self, uthmani_list: list[str], imlaey_list: list[str]
    ) -> dict[str, list[dict[str, str]]]:
        """
        Return:
            [
                {'@uthmani: str, '@imlaey: str},
                {'@uthmani: str, '@imlaey: str},
            ]
        """
        map_list: list[str] = []
        for uthmani_words, imlaey_words in zip(uthmani_list, imlaey_list):
            map_list.append(
                {
                    self.uthmani_key: self.join_prefix.join(uthmani_words),
                    self.imlaey_key: self.join_prefix.join(imlaey_words),
                }
            )
        return map_list

    def _get_str_from_lists(self, L: list[list[str]]) -> str:
        """
        join a list of lists of str with (self.join_prefix)
        Example: :
            L = [
                    ['a', 'b'],
                    ['c', 'd', 'e']
                ]
            self.join_prefic = ' '
            Ouput: 'a b c d e'
        """
        return self.join_prefix.join([self.join_prefix.join(x) for x in L])

    def set_rasm_map(
        self,
        uthmani_list: list[list[str]],
        imlaey_list: list[list[str]],
    ):
        # Assert len
        assert len(uthmani_list) == len(imlaey_list), (
            f"Lenght mismatch: len(uthmani)={len(uthmani_list)} "
            + f"and len(imlaey)={len(imlaey_list)}"
        )

        # assert missing script
        # (Uthmani)
        assert self._get_str_from_lists(uthmani_list) == self.get().uthmani, (
            f"Missing Uthmani script words! input_uthmani_list={uthmani_list}"
            + f"\nAnd the original uthmani Aya={self.get().uthmani}"
        )
        # (Imlaey)
        assert self._get_str_from_lists(imlaey_list) == self.get().imlaey, (
            f"Missing Imlaey script words! input_imlaey_list={imlaey_list}"
            + f"\nAnd the original imlaey Aya={self.get().imlaey}"
        )

        # check first aya (set bismillah map)
        bismillah_map = None
        if (
            self.get().bismillah_uthmani is not None
            and self.get().bismillah_map is None
        ):
            bismillah_uthmani = self.get().bismillah_uthmani.split(self.join_prefix)
            bismillah_uthmani = [[word] for word in bismillah_uthmani]
            bismillah_imlaey = self.get().bismillah_imlaey.split(self.join_prefix)
            bismillah_imlaey = [[word] for word in bismillah_imlaey]

            bismillah_map = self._get_map_dict(
                uthmani_list=bismillah_uthmani, imlaey_list=bismillah_imlaey
            )

        # get rasm map
        rasm_map = self._get_map_dict(
            uthmani_list=uthmani_list, imlaey_list=imlaey_list
        )

        # save quran script file
        self.quran_dict["quran"]["sura"][self.sura_idx]["aya"][self.aya_idx][
            self.map_key
        ] = rasm_map
        if bismillah_map is not None:
            self.quran_dict["quran"]["sura"][self.sura_idx]["aya"][self.aya_idx][
                self.bismillah_map_key
            ] = bismillah_map

    def save_quran_dict(self):
        # save the file
        with open(self.quran_path, "w+", encoding="utf8") as f:
            json.dump(self.quran_dict, f, ensure_ascii=False, indent=2)

        # # TODO for debuging
        # with open(self.quran_path.parent / 'text.xml', 'w+', encoding='utf8') as f:
        #     new_file = xmltodict.unparse(self.quran_dict, pretty=True)
        #     f.write(new_file)

    def get_formatted_rasm_map(self) -> RasmFormat:
        """
        return rasm map in fromt like:
            [
                {'@uthmani: str, '@imlaey: str},
                {'@uthmani: str, '@imlaey: str},
            ]
            to
            RasmFormat.uthmani: list[list[str]]
            RasmFormat.imlaey: list[list[str]]
        """
        if self.get().rasm_map is None:
            raise ValueError("Rasmp map is None")

        uthmani_words: list[list[str]] = []
        imlaey_words: list[list[str]] = []
        for item in self.get().rasm_map:
            uthmani_words.append(
                item[self.uthmani_key].split(self.join_prefix))
            imlaey_words.append(item[self.imlaey_key].split(self.join_prefix))
        return RasmFormat(uthmani=uthmani_words, imlaey=imlaey_words)

    def imlaey_to_uthmani(
        self,
        imlaey_word_span: WordSpan,
        include_bismillah=False,
    ) -> str:
        """return the uthmai script of the given imlaey script word indices

        Args:
            imlaey_word_span (WordSpan): the input imlay word ids in the Aya.
            Wordspan.start: the start word index, WordSpan.end: the end word index

            include_bimillah (bool): include Bismillah as a part of the Aya while
            calculating uthmani str

        Return:
            the uthmain script
        """
        imlaey2uthmani: dict[int, int] = self._encode_imlaey_to_uthmani(
            include_bismillah=include_bismillah
        )
        uthmani_script = self._decode_uthmani(
            imlaey2uthmani=imlaey2uthmani,
            imlaey_wordspan=imlaey_word_span,
            include_bismillah=include_bismillah,
        )
        return uthmani_script

    def _encode_imlaey_to_uthmani(
        self,
        include_bismillah=False,
    ) -> dict[int, int]:
        """
        Args:
            inlcude_bismillah (bool): if True it will include bismillah in the
                encoded dictionary as a part of the first aya
        """
        uthmani_words = []
        imlaey_words = []
        if include_bismillah and (self.get().bismillah_uthmani is not None):
            uthmani_words += self.get().bismillah_uthmani.split(self.join_prefix)
            imlaey_words += self.get().bismillah_imlaey.split(self.join_prefix)

        uthmani_words += self.get().uthmani.split(self.join_prefix)
        imlaey_words += self.get().imlaey.split(self.join_prefix)

        if len(uthmani_words) == len(imlaey_words):
            return {idx: idx for idx in range(len(uthmani_words))}

        # len mismatch
        iml_idx = 0
        imlaey2uthmani = {}
        for uth_idx in range(len(uthmani_words)):
            # special words of Uthmani Rasm
            span = self._get_unique_rasm_map_span(iml_idx, imlaey_words)
            if span is not None:
                for idx in range(iml_idx, iml_idx + span):
                    imlaey2uthmani[idx] = uth_idx
                iml_idx += span

            elif imlaey_words[iml_idx] in alpha.unique_rasm.imlaey_starts:
                imlaey2uthmani[iml_idx] = uth_idx
                imlaey2uthmani[iml_idx + 1] = uth_idx
                iml_idx += 2

            else:
                imlaey2uthmani[iml_idx] = uth_idx
                iml_idx += 1

        assert sorted(imlaey2uthmani.keys())[-1] == len(imlaey_words) - 1
        #
        assert sorted(imlaey2uthmani.values())[-1] == len(uthmani_words) - 1

        return imlaey2uthmani

    def _get_unique_rasm_map_span(self, idx: int, words: list[int]) -> int:
        """
        check that words starting of idx is in alphabet.unique_rasm.rasm_map
        if that applies, it will return the number of imlaey words in
        alphabet.unique_rasm.rasm_map
        Else: None
        """
        for unique_rasm in alpha.unique_rasm.rasm_map:
            span = len(unique_rasm["imlaey"].split(self.join_prefix))
            if self.join_prefix.join(words[idx: idx + span]) == unique_rasm["imlaey"]:
                return span
        return None

    def _decode_uthmani(
        self,
        imlaey2uthmani: dict[int, int],
        imlaey_wordspan: WordSpan,
        include_bismillah=False,
    ) -> str:
        """
        Args:
            Imlaey_wordspan: (start, end):
                start: the start word idx in imlaey script of the aya
                end: the (end + 1) word idx in imlaey script of the aya if end
                    is None then means to the last word idx of the imlaey aya
            inlcude_bismillah (bool): if True it will include bismillah in the
                decoding process
        return the uthmani script of the given imlaey_word_span in
        Imlaey script Aya
        """
        start = imlaey_wordspan.start
        end = imlaey_wordspan.end
        if imlaey_wordspan.end is None:
            end = len(imlaey2uthmani)

        if end in imlaey2uthmani.keys():
            if imlaey2uthmani[end - 1] == imlaey2uthmani[end]:
                raise PartOfUthmaniWord(
                    "The Imlay Word is part of uthmani word")

        # Preparing Uthamni Words
        uthmani_words = []
        if include_bismillah and (self.get().bismillah_uthmani is not None):
            uthmani_words += self.get().bismillah_uthmani.split(self.join_prefix)

        uthmani_words += self.get().uthmani.split(self.join_prefix)

        out_script = ""
        prev_uth_idx = -1
        for idx in range(start, end):
            if prev_uth_idx != imlaey2uthmani[idx]:
                out_script += uthmani_words[imlaey2uthmani[idx]]

                # Adding space Except for end idx
                if idx != end - 1:
                    out_script += self.join_prefix
            prev_uth_idx = imlaey2uthmani[idx]
        return out_script


@dataclass
class SearchItem:
    start_aya: Aya
    num_ayat: int
    imlaey_word_span: WordSpan
    uthmani_script: int
    has_bismillah: bool = False
    has_istiaatha: bool = False
    """
    start_aya (Aya): the start aya of the first search

    num_aya: (int): number of ayat that is included in the search item

    has_bismillah (bool): True if the search item has bismliilah
        (not the Aya in El-Fatiha of in the Alnaml)

    has_istiaatha (bool): True if the search item has istiaatha

    imlaey_word_span (WordSpan):
        start: the start word idx of the imlaey scriptin thestart_aya
        end: the end imlaey_idx of the imlaey (start_aya + num_ayat - 1)

    uthmani_script (str) the equvilent uthmani script of the given imlaey script
    if istiaatha is only will return:
        start_aya=None, num_ayat=None, imlaey_word_span=None, has_bismillah=None
    """

    def __str__(self):
        out_str = ""
        if self.start_aya:
            out_str += f"start_aya(sura_idx={self.start_aya.get().sura_idx}, aya_idx={self.start_aya.get().aya_idx})"
        else:
            out_str += f"start_aya(sura_idx={None}, aya_idx={None})"
        out_str += f", num_ayat={self.num_ayat}"
        out_str += f", uthmnai_script={self.uthmani_script}"
        out_str += f", has_istiaatha={self.has_istiaatha}"
        out_str += f", has_bismillah={self.has_bismillah}"
        out_str += f", imlaey_word_span={self.imlaey_word_span}"

        return out_str


# TODO: Add Examples
def search(
    text: str,
    start_aya: Aya = Aya(1, 1),
    window: int = 2,
    suffix=" ",
    **kwargs,
) -> list[SearchItem]:
    """searches the Holy Quran of Imlaey script to match the given text

    searches the Holy quran for a given Imlaey text of specifc window arround
    the `start_aya` applying some filters of the search string

    Example:
        >> results = search('الحمد لله',
            start_aya=Aya(1, 1), window=4, ignore_tashkeel=True)
        >> results
    Args:
        text (str): the text to search with (expected with imlaey script)

        start_aya (Aya): The Pivot Aya to set Search with.

        winodw (int): the search winodw:
        [start_aya - winowd //2, start_aya + winodw //2]

        suffix (str): the suffix that sperate the quran words either imlaey or uthmani
        the rest of **kwargs are from normalize_aya function below
    Returns:
        list[SearchItem]: Every SearchItem is:
        * start_aya (Aya): the start aya of the first search

        * num_aya: (int): number of ayat that is included in the search item

        * has_bismillah (bool): True if the search item has bismliilah
        (not the Aya in El-Fatiha of in the Alnaml)

        * has_istiaatha (bool): True if the search item has istiaatha

        * imlaey_word_span (WordSpan):
        start: the start word idx of the imlaey scriptin thestart_aya
        end: the end imlaey_idx of the imlaey (start_aya + num_ayat - 1)

        * uthmani_script (str) the equvilent uthmani script of the given imlaey script
        NOTE: if istiaatha is only will return:
        start_aya=None, num_ayat=None, imlaey_word_span=None, has_bismillah=None
    """
    normalized_text: str = normalize_aya(text, remove_spaces=True, **kwargs)
    if normalized_text == "":
        return []

    # Prepare ayat within [-window/2, window/2]
    loop_aya = start_aya.step(-window // 2)

    # ----------------------------------
    # Checking for Itiaatha
    # ----------------------------------
    # NOTE: Assuming Istiaatha is at the first only
    has_istiaatha = False
    istiaatha_imlaey_words = normalize_aya(
        start_aya.get().istiaatha_imlaey,
        remove_spaces=False,
        **kwargs,
    ).split(suffix)
    istiaatha_imlaey_str = "".join(istiaatha_imlaey_words)
    re_span = re.search(istiaatha_imlaey_str, normalized_text)
    if re_span:
        normalized_text = normalized_text[re_span.span()[1]:]
        has_istiaatha = True
        if normalized_text == "":
            # return istiaatha only
            return [
                SearchItem(
                    start_aya=None,
                    num_ayat=None,
                    imlaey_word_span=None,
                    has_bismillah=None,
                    has_istiaatha=has_istiaatha,
                    uthmani_script=start_aya.get().istiaatha_uthmani,
                )
            ]

    found = []
    for bismillah_flag in [False, True]:
        aya_imlaey_words, aya_imlaey_str = _get_imlaey_words_and_str(
            start_aya=loop_aya,
            window=window,
            suffix=suffix,
            include_bismillah=bismillah_flag,
            **kwargs,
        )

        for re_search in re.finditer(normalized_text, aya_imlaey_str):
            if re_search is not None:
                span = _get_words_span(
                    start=re_search.span()[0],
                    end=re_search.span()[1],
                    words_list=aya_imlaey_words,
                )
                if span is not None:
                    start_vertex, end_vertex = span
                    found.append(
                        SearchItem(
                            start_aya=loop_aya.step(start_vertex.aya_idx),
                            num_ayat=end_vertex.aya_idx - start_vertex.aya_idx + 1,
                            imlaey_word_span=WordSpan(
                                start=start_vertex.word_idx, end=end_vertex.word_idx
                            ),
                            has_bismillah=bismillah_flag,
                            has_istiaatha=has_istiaatha,
                            uthmani_script="",
                        )
                    )
                    found[-1].uthmani_script = _get_uthmani_of_result_item(
                        found[-1], suffix=suffix
                    )
        if found != []:
            # add istiaatah uthamni script
            if has_istiaatha:
                for item in found:
                    item.uthmani_script = (
                        start_aya.get().istiaatha_uthmani + suffix + item.uthmani_script
                    )
            return found

    return found


def normalize_aya(
    text: str,
    remove_spaces=True,
    ignore_hamazat=False,
    ignore_alef_maksoora=True,
    ignore_taa_marboota=False,
    normalize_taat=False,
    remove_small_alef=True,
    remove_tashkeel=False,
) -> str:
    """Apply filters to match input Kwargs on **Imlaey** text

    Args:
        remove_spaces (bool): remove spaces for text

        ignore_hamazat (bool): making all hamazat equal (أ, آ, إ ء, ئ, ؤ) = (ء)
        alphabet.imlaey.hmazat -> alphabet.imlaey.

        ignore_alef_maksoora (bool): (ى) -> (ا).
        alphabet.imlaey.alef_maksoora = alphabet.imlaey.alef

        ignore_taa_marboota (bool): (ة) -> (ه).
        alphabet.imlaey.taa_motaterfa -> alphabet.imlaey.haa

        normalize_taat (bool): (ة) -> (ت).
        alphabet.imlaey.taa_marboota = alphabet.taa_mabsoota

        NOTE: We can not use `ignore_taaa_marboota` and `normalize_taaat` at
        the same time

        remove_small_alef (bool): remove small alef "ٰ" in
        alphabet.imlaey.small_alef (alef khingarai)

        remove_tashkeel (bool): remove tashkeel: "ًٌٍَُِّْ" in alphabet.imlaey.tashkeel

        Return:
            str: the normalied imlaey text
    """
    assert not (ignore_taa_marboota and normalize_taat), (
        'You can not `ignore_taa_marboota` and `normaize_taat` at the same time')

    norm_text = text

    # TODO: Ingonre alef as hamza

    if remove_spaces:
        norm_text = re.sub(r"\s+", "", norm_text)

    if ignore_alef_maksoora:
        norm_text = re.sub(alpha.imlaey.alef_maksoora,
                           alpha.imlaey.alef, norm_text)

    if ignore_hamazat:
        norm_text = re.sub(f"[{alpha.imlaey.hamazat}]",
                           alpha.imlaey.hamza, norm_text)

    if ignore_taa_marboota:
        norm_text = re.sub(
            f"[{alpha.imlaey.taa_marboota}]",
            alpha.imlaey.haa,
            norm_text,
        )

    if normalize_taat:
        norm_text = re.sub(
            f"[{alpha.imlaey.taa_marboota}]",
            alpha.imlaey.taa_mabsoota,
            norm_text,
        )

    if remove_small_alef:
        norm_text = re.sub(alpha.imlaey.small_alef, "", norm_text)

    if remove_tashkeel:
        norm_text = re.sub(f"[{alpha.imlaey.tashkeel}]", "", norm_text)

    return norm_text


def _get_words_span(
    start: int, end: int, words_list=list[list[str]]
) -> tuple[Vertex, Vertex]:
    """
    return the word indices at every word boundary only not inside the word:
    which means:
    * start character is at the beginning of the word
    * end character is at the end of the word + 1
    EX: start = 0, end = 8, words_list=[['aaa', 'bbb',], ['cc', 'ddd']]
                                          ^                 ^
                                          0               8 - 1
    return (start, end)
    (start.aya_idx=0, start.word_idx=0, end. aya_idx=1, end.word_idx=0 + 1)

    return None if:
        * start not at the beginning of the word.
        * end is not at (end + 1) of the word.
        * start >= end

    Args:
        start (int): the start char idx
        end (int): the end char idx + 1
        words_list (list[list[str]]): given words

    return: WordSpan:
        start: the start idx of the word in "words"
        end: (end_idx + 1) of the word in "words"
        if valid boundary else None
    """

    def _get_start_span(start_char: int) -> tuple[int, int]:
        chars_count = 0
        for aya_idx in range(len(words_list)):
            for word_idx in range(len(words_list[aya_idx])):
                if start_char == chars_count:
                    return aya_idx, word_idx
                chars_count += len(words_list[aya_idx][word_idx])
            aya_idx += 1
        return None

    def _get_end_span(
        end_char: int, chars_count=0, start_aya_idx=0, start_word_idx=0
    ) -> tuple[int, int]:
        for aya_idx in range(start_aya_idx, len(words_list)):
            for word_idx in range(start_word_idx, len(words_list[aya_idx])):
                chars_count += len(words_list[aya_idx][word_idx])
                if end_char == chars_count:
                    return aya_idx, word_idx + 1
            start_word_idx = 0
        return None

    # print('start=', start, ', end=', end)
    span = _get_start_span(start)
    # print(f'start=({span})')
    if span is None:
        return None
    start_aya_idx, start_word_idx = span

    span = _get_end_span(
        end,
        chars_count=start,
        start_aya_idx=start_aya_idx,
        start_word_idx=start_word_idx,
    )
    # print(f'end=({span})')
    if span is None:
        return None
    end_aya_idx, end_word_idx = span
    return (
        Vertex(aya_idx=start_aya_idx, word_idx=start_word_idx),
        Vertex(aya_idx=end_aya_idx, word_idx=end_word_idx),
    )


def _get_uthmani_of_result_item(search_item: SearchItem, suffix=" ") -> str:
    """
    add uthmani script of the imlaey script found in the SearchItem
    """
    # parsing spans
    wordspans = [WordSpan(0, None) for _ in range(search_item.num_ayat)]
    wordspans[0].start = search_item.imlaey_word_span.start
    wordspans[-1].end = search_item.imlaey_word_span.end

    uthmani_str = ""
    for idx, aya in enumerate(
        search_item.start_aya.get_ayat_after(num_ayat=search_item.num_ayat)
    ):
        uthmani_str += aya.imlaey_to_uthmani(
            wordspans[idx],
            include_bismillah=search_item.has_bismillah,
        )
        uthmani_str += suffix
    # removing last suffix from the end
    uthmani_str = uthmani_str[: -len(suffix)]

    return uthmani_str


def _get_imlaey_words_and_str(
    start_aya: Aya,
    window: int,
    include_bismillah=False,
    suffix=" ",
    **kwargs,
) -> tuple[list[list[str]], str]:
    """
    return (words, scipt): The imlaey script either of multiple ayat
        words: 2D list dimention(0) is of length of number of ayat, dimention(1)
            is the aya words
        script: the joined script of ayat without spaces
    """
    aya_imlaey_words: list[list[str]] = []
    aya_imlaey_str = ""
    for aya in start_aya.get_ayat_after(num_ayat=window + 1):
        aya_words = []

        # Including Bismillah at The start of sura except for:
        # Alfatiha [is an Aya] and Al tuoba
        if include_bismillah and (aya.get().bismillah_imlaey is not None):
            aya_words += normalize_aya(
                aya.get().bismillah_imlaey,
                remove_spaces=False,
                **kwargs,
            ).split(suffix)

        # Aya Words
        aya_words += normalize_aya(
            aya.get().imlaey,
            remove_spaces=False,
            **kwargs,
        ).split(suffix)
        aya_imlaey_words.append(aya_words)

        # imlaey String With spaces removed
        aya_imlaey_str += re.sub(r"\s+", "", "".join(aya_words))
    return aya_imlaey_words, aya_imlaey_str
