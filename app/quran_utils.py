from functools import reduce
import operator
from pathlib import Path
import json
import xmltodict
from dataclasses import dataclass
import copy


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
class AyaForamt:
    sura_idx: int
    aya_idx: int
    sura_name: str
    uthmani: str
    imlaey: str
    bismillah_uthmani: str = None
    bismillah_imlaey: str = None


class Aya(object):
    def __init__(self, quran_path: str | Path,
                 sura_idx=1,
                 aya_idx=1,
                 prefix='@',
                 map_key='rasm_map',
                 bismillah_key='bismillah',
                 uthmani_key='uthmani',
                 imlaey_key='imlaey',
                 sura_name_key='name'):
        """
        quran_path (str | Path) path to the quran json script with
            emlaey uthmani scripts
        sura_idx: the index of the Sura in the Quran starting with 1 to 114
        aya_idx: the index of the aya starting form 1
        """
        self.quran_path = Path(quran_path)
        with open(self.quran_path, 'r', encoding='utf8') as f:
            self.quran_dict = json.load(f)

        self._check_indices(sura_idx - 1, aya_idx - 1)
        self.sura_idx = sura_idx - 1
        self.aya_idx = aya_idx - 1

        self.map_key = prefix + map_key
        self.uthmani_key = prefix + uthmani_key
        self.imlaey_key = prefix + imlaey_key
        self.sura_name_key = prefix + sura_name_key
        self.bismillah_uthmani_key = f'{prefix}{bismillah_key}_{uthmani_key}'
        self.bismillah_imlaey_key = f'{prefix}{bismillah_key}_{imlaey_key}'

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

    def _get(self, sura_idx, aya_idx) -> AyaForamt:
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
                uthmani (str): the uthmani script of the aya
                imlaey (str): the imlaey script of the aya

                bismillah_uthmani (str): bismillah in uthmani script if the
                    aya index == 1 and the sura has bismillah or bismillah is
                    not aya like sura Alfateha and else (None)

                bismillah_imlaey (str): bismillah in uthmani script if the
                    aya index == 1 and the sura has bismillah or bismillah is
                    not aya like sura Alfateha and else (None)
        """
        bismillah = {self.bismillah_uthmani_key: None,
                     self.bismillah_imlaey_key: None}
        for key in bismillah.keys():
            if key in self._get_aya(sura_idx, aya_idx):
                bismillah[key] = self._get_aya(sura_idx, aya_idx)[key]
        return AyaForamt(
            sura_idx=sura_idx + 1,
            aya_idx=aya_idx + 1,
            sura_name=self._get_sura_object(sura_idx)[self.sura_name_key],
            uthmani=self._get_aya(sura_idx, aya_idx)[self.uthmani_key],
            imlaey=self._get_aya(sura_idx, aya_idx)[self.uthmani_key],
            bismillah_uthmani=bismillah[self.bismillah_uthmani_key],
            bismillah_imlaey=bismillah[self.bismillah_imlaey_key],
            )

    def get(self) -> AyaForamt:
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

    def get_ayat_after(self):
        """
        iterator looping over Quran ayayt (verses) starting from the
        current aya to the end of the Holy Quran
        """
        aya_start_idx = self.aya_idx
        for sura_loop_idx in range(self.sura_idx, 114):
            for aya_loop_idx in range(
                    aya_start_idx, len(self._get_sura(sura_loop_idx))):
                self._set_ids(sura_loop_idx, aya_loop_idx)
                yield self
            aya_start_idx = 0

# --------------------------------------------
# Testing
# --------------------------------------------
# if __name__ == "__main__":
#     start_aya = Aya('quran-script/quran-uthmani-imlaey.json', 1, 1)
#     start_aya.set(114, 9)
#     print(start_aya.get())
#     for idx, aya in enumerate(start_aya.get_ayat_after()):
#         print(aya.get())
#     print('idx', idx)
