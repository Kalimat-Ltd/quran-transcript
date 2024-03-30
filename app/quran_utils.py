from functools import reduce
import operator
from pathlib import Path
import json
import xmltodict
from dataclasses import dataclass


def get_from_dict(data_dict: dict, keys: list[str]):
    """
    src: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
    get a value from dict using sequence of keys
    Example:
        d = {'a': {'b': {'c': 3}}}
       get_from_dict(d, ['a', 'b', 'c'])
       >> 3
    """
    return reduce(operator.getitem, keys, data_dict)


@dataclass
class RasmFormat:
    uthmani: list[list[str]]
    imlaey: list[list[str]]


@dataclass
class AyaFormat:
    sura_idx: int
    aya_idx: int
    sura_name: str
    num_ayat_in_sura: int
    uthmani: str
    imlaey: str
    rasm_map: dict[str, list[str]] = None
    bismillah_uthmani: str = None
    bismillah_imlaey: str = None
    bismillah_map: dict[str, list[str]] = None

    def get_formatted_rasm_map(self,
                               join_prefix=' ',
                               uthmani_key='@uthmani',
                               imlaey_key='@imlaey',
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
            raise ValueError('Rasmp map is None')

        uthmani_words: list[list[str]] = []
        imlaey_words: list[list[str]] = []
        for item in self.rasm_map:
            uthmani_words.append(item[uthmani_key].split(join_prefix))
            imlaey_words.append(item[imlaey_key].split(join_prefix))
        return RasmFormat(
            uthmani=uthmani_words,
            imlaey=imlaey_words)


class Aya(object):
    def __init__(self, quran_path: str | Path,
                 sura_idx=1,
                 aya_idx=1,
                 quran_dict: dict = None,
                 prefix='@',
                 map_key='rasm_map',
                 bismillah_map_key='bismillah_map',
                 bismillah_key='bismillah',
                 uthmani_key='uthmani',
                 imlaey_key='imlaey',
                 sura_name_key='name',
                 join_prefix=' ',
                 ):
        """
        quran_path (str | Path) path to the quran json script with
            emlaey uthmani scripts
        sura_idx: the index of the Sura in the Quran starting with 1 to 114
        aya_idx: the index of the aya starting form 1
        """
        self.quran_path = Path(quran_path)
        if quran_dict is None:
            with open(self.quran_path, 'r', encoding='utf8') as f:
                self.quran_dict = json.load(f)
        else:
            self.quran_dict = quran_dict

        self._check_indices(sura_idx - 1, aya_idx - 1)
        self.sura_idx = sura_idx - 1
        self.aya_idx = aya_idx - 1

        self.map_key = map_key
        self.bismillah_map_key = bismillah_map_key
        self.uthmani_key = prefix + uthmani_key
        self.imlaey_key = prefix + imlaey_key
        self.sura_name_key = prefix + sura_name_key
        self.bismillah_uthmani_key = f'{prefix}{bismillah_key}_{uthmani_key}'
        self.bismillah_imlaey_key = f'{prefix}{bismillah_key}_{imlaey_key}'
        self.join_prefix = join_prefix

    def _get_sura(self, sura_idx):
        assert sura_idx >= 0 and sura_idx <= 113, (
            f'Wrong Sura index {sura_idx + 1}')
        return self.quran_dict['quran']['sura'][sura_idx]['aya']

    def _get_sura_object(self, sura_idx):
        assert sura_idx >= 0 and sura_idx <= 113, (
            f'Wrong Sura index {sura_idx + 1}')
        return self.quran_dict['quran']['sura'][sura_idx]

    def _get_aya(self, sura_idx, aya_idx):
        assert aya_idx >= 0 and aya_idx < len(self._get_sura(sura_idx)), (
            f'Sura index out of range sura_index={sura_idx + 1} ' +
            f'and len of sura={len(self._get_sura(sura_idx))}')
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
        assert sura_idx >= 0 and sura_idx <= 113, (
            f'Wrong Sura index {sura_idx + 1}')

        assert aya_idx >= 0 and aya_idx < len(self._get_sura(sura_idx)), (
            f'Aya index out of range (sura_index={sura_idx + 1} ' +
            f'aya_index={aya_idx + 1}) ' +
            f'and length of sura={len(self._get_sura(sura_idx))}')

    def _set_ids(self, sura_idx, aya_idx):
        self.sura_idx = sura_idx
        self.aya_idx = aya_idx

    def set(self, sura_idx, aya_idx) -> None:
        """
        Set the aya
        Args:
        sura_idx: the index of the Sura in the Quran starting with 1 to 114
        aya_idx: the index of the aya starting form 1
        """
        self._check_indices(sura_idx - 1, aya_idx - 1)
        self._set_ids(sura_idx=sura_idx - 1, aya_idx=aya_idx - 1)

    def set_new(self, sura_idx, aya_idx):
        """
        Return new aya with sura, and aya indices
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
                if (aya_relative_idx < num_ayat):
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
                if (aya_relative_idx >= 0):
                    break

        return Aya(
            quran_path=self.quran_path,
            sura_idx=sura_idx + 1,
            aya_idx=aya_relative_idx + 1,
            quran_dict=self.quran_dict,
        )

    def get_ayat_after(self):
        """
        iterator looping over Quran ayayt (verses) starting from the
        current aya to the end of the Holy Quran
        """
        aya_start_idx = self.aya_idx
        for sura_loop_idx in range(self.sura_idx, 114):
            for aya_loop_idx in range(
                    aya_start_idx, len(self._get_sura(sura_loop_idx))):
                yield Aya(
                    quran_path=self.quran_path,
                    sura_idx=sura_loop_idx + 1,
                    aya_idx=aya_loop_idx + 1,
                    quran_dict=self.quran_dict,
                )
            aya_start_idx = 0

    def _get_map_dict(self,
                      uthmani_list: list[str],
                      imlaey_list: list[str]
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
                })
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
            f'Lenght mismatch: len(uthmani)={len(uthmani_list)} ' +
            f'and len(imlaey)={len(imlaey_list)}'
        )

        # assert missing script
        # (Uthmani)
        assert self._get_str_from_lists(uthmani_list) == self.get().uthmani, (
            f'Missing Uthmani script words! input_uthmani_list={uthmani_list}' +
            f'\nAnd the original uthmani Aya={self.get().uthmani}')
        # (Imlaey)
        assert self._get_str_from_lists(imlaey_list) == self.get().imlaey, (
            f'Missing Imlaey script words! input_imlaey_list={imlaey_list}' +
            f'\nAnd the original imlaey Aya={self.get().imlaey}')

        # check first aya (set bismillah map)
        bismillah_map = None
        if (self.get().bismillah_uthmani is not None and
                self.get().bismillah_map is None):
            bismillah_uthmani = self.get().bismillah_uthmani.split(self.join_prefix)
            bismillah_uthmani = [[word] for word in bismillah_uthmani]
            bismillah_imlaey = self.get().bismillah_imlaey.split(self.join_prefix)
            bismillah_imlaey = [[word] for word in bismillah_imlaey]

            bismillah_map = self._get_map_dict(
                uthmani_list=bismillah_uthmani,
                imlaey_list=bismillah_imlaey)

        # get rasm map
        rasm_map = self._get_map_dict(
            uthmani_list=uthmani_list,
            imlaey_list=imlaey_list)

        # save quran script file
        self.quran_dict['quran']['sura'][self.sura_idx]['aya'][self.aya_idx][
            self.map_key] = rasm_map
        if bismillah_map is not None:
            self.quran_dict['quran']['sura'][self.sura_idx]['aya'][self.aya_idx][
                self.bismillah_map_key] = bismillah_map

        # save the file
        with open(self.quran_path, 'w+', encoding='utf8') as f:
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
            raise ValueError('Rasmp map is None')

        uthmani_words: list[list[str]] = []
        imlaey_words: list[list[str]] = []
        for item in self.get().rasm_map:
            uthmani_words.append(item[self.uthmani_key].split(self.join_prefix))
            imlaey_words.append(item[self.imlaey_key].split(self.join_prefix))
        return RasmFormat(
            uthmani=uthmani_words,
            imlaey=imlaey_words)
