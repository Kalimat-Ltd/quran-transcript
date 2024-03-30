import streamlit as st
from typing import Any
from pathlib import Path
import json
import app.api_utils as api
from app.quran_utils import AyaFormat


DEFAULT_AYA_SAVE = 'APP_AYA_IDS.json'
QURAN_MAP_PATH = 'quran-script/quran-uthmani-imlaey-map.json'


def app_main():
    aya_format = get_selected_aya()

    left_col, right_col = st.columns(2)
    with left_col:
        st.button('امش', on_click=walk)
    with right_col:
        st.button('حفظ', on_click=save_quran_dict)

    # st.write(aya_format)

    edit_rasm_map_wedgit(aya_format)


def save_quran_dict():
    """
    Saving Rasm map in Quran-Map file
    """
    api.save_quran_dict()


def walk():
    aya_format = api.get_first_aya_to_annotate()
    st.session_state.aya_selector = aya_format.aya_idx
    st.session_state.sura_selector = aya_format.sura_idx


def edit_rasm_map_wedgit(aya_format: AyaFormat):
    if 'edit_uthmani' not in st.session_state.keys():
        st.session_state.edit_uthmani = False
    if 'edit_imlaey' not in st.session_state.keys():
        st.session_state.edit_imlaey = False
    if 'last_ayaformat' not in st.session_state.keys():
        st.session_state.last_ayaformat = hash_ayaformat(aya_format)

    if st.session_state.last_ayaformat != hash_ayaformat(aya_format):
        st.session_state.edit_imlaey = False
        st.session_state.edit_uthmani = False

    uthmani_words: list[list[str]] = (
        [[word] for word in aya_format.uthmani.split(' ')])
    imlaey_words: list[list[str]] = (
        [[word] for word in aya_format.imlaey.split(' ')])
    if aya_format.rasm_map is not None:
        uthmani_words = aya_format.get_formatted_rasm_map().uthmani
        imlaey_words = aya_format.get_formatted_rasm_map().imlaey

    raws = [None] * 2
    raws[0] = st.columns(2)
    raws[1] = st.columns(2)
    raws[0][1].subheader('الرسم الإملائي')
    raws[0][0].subheader('الرسم العثماني')
    with raws[0][1]:
        imlaey_placeholder = st.empty()
    with raws[0][0]:
        uthmani_placeholder = st.empty()

    new_rasm_map_flag = True

    if len(uthmani_words) > len(imlaey_words) or st.session_state.edit_uthmani:
        with imlaey_placeholder.container():
            display_rasm(imlaey_words)
        with uthmani_placeholder.container():
            uthmani_words = get_new_rasm_map(uthmani_words, len(imlaey_words))
    elif len(uthmani_words) < len(imlaey_words) or st.session_state.edit_imlaey:
        with imlaey_placeholder.container():
            imlaey_words = get_new_rasm_map(imlaey_words, len(uthmani_words))
        with uthmani_placeholder.container():
            display_rasm(uthmani_words)
    else:
        new_rasm_map_flag = False
        with imlaey_placeholder.container():
            display_rasm(imlaey_words)
        with uthmani_placeholder.container():
            display_rasm(uthmani_words)

    # Imlaey Edit
    with raws[1][1]:
        st.button('تعديل الإملائي', on_click=edit_rasm_on_click,
                  kwargs={'imlaey': True})

    with raws[1][0]:
        st.button('تعديل العثماني', on_click=edit_rasm_on_click,
                  kwargs={'uthmani': True})

    if new_rasm_map_flag:
        st.button(
            'حفظ رسم الآية',
            on_click=save_rasm_map_click,
            kwargs={'aya_format': aya_format,
                    'uthmani_words': uthmani_words,
                    'imlaey_words': imlaey_words})

    st.session_state.last_ayaformat = hash_ayaformat(aya_format)


def hash_ayaformat(ayaformat: AyaFormat):
    return f'{ayaformat.sura_idx}_{ayaformat.aya_idx}'


def edit_rasm_on_click(uthmani=False, imlaey=False):
    st.session_state.edit_imlaey = imlaey
    st.session_state.edit_uthmani = uthmani


def display_rasm(rasm: list[list[str]], suffix=' '):
    for words in rasm:
        st.write(suffix.join(words))
        st.write('---------')


def get_new_rasm_map(
        rasm_words: list[list[str]],
        max_len: int = None) -> list[str]:
    if max_len is None:
        max_len = len(join_lists(rasm_words))
    new_words_ids: list[list[int]] = multiselect_list(rasm_words, max_len)
    new_words_map: list[list[str]] = []
    raw_rasm_words = join_lists(rasm_words)

    for ids_list in new_words_ids:
        words_list = []
        for idx in ids_list:
            words_list.append(raw_rasm_words[idx])
        new_words_map.append(words_list)

    return new_words_map


def save_rasm_map_click(
    aya_format: AyaFormat,
    uthmani_words: list[list[str]],
    imlaey_words: list[list[str]]
        ):

    st.session_state.edit_imlaey = False
    st.session_state.edit_uthmani = False
    api.save_rasm_map(
        sura_idx=aya_format.sura_idx,
        aya_idx=aya_format.aya_idx,
        uthmani_words=uthmani_words,
        imlaey_words=imlaey_words)

# --------------------------------------------------------------------------
# Function to handel get_aya()
# --------------------------------------------------------------------------


@st.cache_data
def get_suar_list() -> list[int]:
    return api.get_suar_names()


def get_selected_aya() -> AyaFormat:
    # # get last aya we were working on
    if 'on_start' not in st.session_state.keys():
        last_sura_idx, last_aya_idx = get_last_aya(DEFAULT_AYA_SAVE)
        st.session_state['last_sura_idx'] = last_sura_idx
        st.session_state['last_aya_idx'] = last_aya_idx
        st.session_state['on_start'] = True

    raws = [None] * 2
    raws[0] = st.columns(2)
    raws[1] = st.columns(2)

    # -----------------------
    # Absolute Selection
    # -----------------------
    with raws[0][1]:
        sura_idx = st.selectbox(
            label='Sura',
            options=list(range(1, 115, 1)),
            format_func=lambda sura_idx: get_suar_list()[sura_idx - 1],
            index=st.session_state['last_sura_idx'] - 1,
            key='sura_selector',
        )

    aya_format: AyaFormat = api.get_aya(sura_idx=sura_idx, aya_idx=1)
    default_aya = st.session_state['last_aya_idx']
    if sura_idx != st.session_state['last_sura_idx']:
        default_aya = 1

    with raws[0][0]:
        aya_idx = st.number_input(
            label='Aya',
            min_value=1,
            max_value=aya_format.num_ayat_in_sura,
            value=default_aya,
            key='aya_selector',
        )
    aya_format = api.get_aya(sura_idx=sura_idx, aya_idx=aya_idx)

    # -----------------------
    # Next, previos
    # -----------------------
    with raws[1][1]:
        st.button(
            'الآية التالية',
            on_click=next_prev_aya, args=(aya_format,), kwargs={'step': 1})

    with raws[1][0]:
        st.button(
            'الآية السابقة',
            on_click=next_prev_aya, args=(aya_format,), kwargs={'step': -1})

    # save last Aya we were working on
    save_last_aya(
        sura_idx=aya_format.sura_idx,
        aya_idx=aya_format.aya_idx,
        last_aya_save_file=DEFAULT_AYA_SAVE,
        )
    return aya_format


def next_prev_aya(ayaformat: AyaFormat, step=1):
    new_ayaformat = api.step_ayat(ayaformat, step)
    st.session_state.aya_selector = new_ayaformat.aya_idx
    st.session_state.sura_selector = new_ayaformat.sura_idx


def get_last_aya(
    last_aya_save_file: str | Path = Path('aya_ids.json')
        ) -> tuple[int, int]:
    """
    get last aya of indeices from last work
    Return:
        tuple[sura_index, aya_index]
        sura_index (int): starting from 1
        aya_index (int): starting from 1
    """
    try:
        with open(last_aya_save_file, 'r') as f:
            ids_dict = json.load(f)
            return ids_dict['sura_idx'], ids_dict['aya_idx']

    except FileNotFoundError:
        with open(last_aya_save_file, 'w+') as f:
            ids_dict = json.dump({'sura_idx': 1, 'aya_idx': 1}, f)
            return 1, 1


def save_last_aya(
    sura_idx: int,
    aya_idx: int,
    last_aya_save_file: str | Path = Path('aya_ids.json'),
        ):
    """
    set last aya of indices to be loaded one the beginning of the app
    Return:
        tuple[sura_index, aya_index]
        sura_index (int): starting from 1
        aya_index (int): starting from 1
    """
    with open(last_aya_save_file, 'w+') as f:
        json.dump({'sura_idx': sura_idx, 'aya_idx': aya_idx}, f)

# --------------------------------------------------------------------------
# Function to handel edit reasm map
# --------------------------------------------------------------------------


class MultiSelectSave(object):
    def __init__(self,
                 dict_obj: dict,
                 key_name: str,
                 max_len: int,
                 max_options: int,
                 options_key='options'):
        self.key_name = key_name
        self.dict_obj = dict_obj
        self.max_len = max_len
        self.max_options = max_options
        self.options_key = options_key

    def __len__(self):
        return self.max_len

    def __getitem__(self, idx):
        key = f'{self.key_name}_{idx}'
        assert idx <= self.max_len, \
            f'Index out of range: max_len={self.max_len} you give: {idx}'

        assert key in self.dict_obj.keys(), \
            f'the key({key}) not in the dict_obj'
        return self.dict_obj[key]

    def __setitem__(self, idx, val):
        key = f'{self.key_name}_{idx}'
        assert idx <= self.max_len, \
            f'Index out of range: max_len={self.max_len} you give: {idx}'

        assert key in self.dict_obj.keys(), \
            f'the key({key}) not in the dict_obj'
        self.dict_obj[key] = val

    def __str__(self):
        print_str = ""
        for idx in range(self.max_len):
            print_str += f'obj[{idx}] = {self.__getitem__(idx)}\n'
        return print_str

    def get_max_options(self):
        return self.max_options

    def validate_duplicate_ids(self):
        ids = []
        for idx in range(self.max_len):
            if isinstance(self.__getitem__(idx), dict):
                for key in self.__getitem__(idx):
                    obj_id = id(self.__getitem__(idx)[key])
                    assert obj_id not in ids, \
                        'Duplicate Object ids'
                    if obj_id not in ids:
                        ids.append(obj_id)

    def check_options(self):
        # check than optins are valid
        options = []
        for idx in range(self.max_len):
            options += self.__getitem__(idx)[self.options_key]

        assert options == list(range(self.max_options)), \
            f'Options not consistent, current oject: \n:{self}'

    def get_effective_len(self):
        max_len = self.max_len
        for idx in range(self.max_len - 1, -1, -1):
            if self.__getitem__(idx)[self.options_key]:
                return max_len
            else:
                max_len -= 1

    # # for looping
    # def __iter__(self):
    #     return self
    # and
    # def __next__(self):
    # src: https://www.programiz.com/python-programming/iterator

    def __iter__(self):
        for idx in range(self.max_len):
            yield self.__getitem__(idx).copy()


def select_ids(ids: list[int],
               options: list[Any],
               rtl=True) -> list[Any]:
    """
    Emulate numpy like: arr[ids] i.e(arr[1, 2, 3])
    Args:
        rtl: (bool) return ids in descending order (right to left)
    """
    return_options = []
    for idx in ids:
        return_options.append(options[idx])
    return sorted(return_options, reverse=rtl)


def deselct_single_box(m_select_idx: int,
                       m_save_obj: MultiSelectSave):
    # *************************************************************
    # Deslect the only left box ("B")
    # Before:
    # --------
    # |A     |
    # |B     |  <-- (deselct "B")
    # |C, D  |
    # --------
    #  E    ("E" not selected yet)
    #
    # After: (Merge "B" with the box above & move the boxes below one block up)
    # --------
    # |A, B  |
    # |C, D  |
    # |E     |
    # --------
    # *************************************************************
    """
    Args:
        m_select_idx: (int) the id of the multiseclt raw
        m_save_obj: (MultiSelectSave) an object which we store st.seesion_state
    """

    # we assuem to deselct or select only one box at a time
    N = m_save_obj.get_effective_len()

    # move the box to the multiselct box above
    # force selcting the least options
    box = sorted(m_save_obj[m_select_idx]['options'])[:1]
    m_save_obj[m_select_idx]['value'] = box.copy()
    for key in ['value', 'options']:
        m_save_obj[m_select_idx - 1][key] += box
        m_save_obj[m_select_idx - 1][key].sort()

        m_save_obj[m_select_idx][key] = sorted(
            set(m_save_obj[m_select_idx][key]) - set(box))

    # move all boxes down up one box starting of the selected box
    for idx in range(m_select_idx, N - 2, 1):
        for key in ['value', 'options']:
            m_save_obj[idx][key] = m_save_obj[idx + 1][key]

    # box(N) - 2
    if m_select_idx != N - 1:
        for key in ['value', 'options']:
            m_save_obj[N - 2][key] = sorted(m_save_obj[N - 1]['value'])

    # last box(N) - 1
    m_save_obj[N - 1]['options'] = sorted(
        set(m_save_obj[N - 1]['options']) - set(m_save_obj[N - 2]['value']))
    m_save_obj[N - 1]['value'] = m_save_obj[N - 1]['options'][:1]


def deselect_left_most_box_idx(m_select_idx: int,
                               m_save_obj: MultiSelectSave,
                               del_box: list[int],
                               del_box_idx: int):
    # *************************************************************
    # Deslect the left most box with raw filled with at least 2 boxes
    # Before:
    # ---------
    # |A      |
    # |B, C, D|  <-- (deselct "B")
    # |E, F   |
    # |G      |
    # ---------
    #  H    ("H" not selected yet)
    #
    # After: ("B" will be the only box in the row & the rest of raws will
    #         move downwards)
    # ---------
    # |A      |
    # |B      |
    # |C, D   |
    # |E, F   |
    # ---------
    #  G    ("G", "H" moved to options of last raw)
    #  H
    # *************************************************************
    """
    Args:
        m_select_idx: (int) the id of the multiseclt raw
        m_save_obj: (MultiSelectSave) an object which we store st.seesion_state
        del_box: (list[int]) the box which is deleselected
        de_box_idx: (int) the id of the del box in m_save_obj[m_selecd_idx]['value']
    """


    N = len(m_save_obj)
    if m_select_idx == N - 1:
        # move select it & the reset of boxes to options
        m_save_obj[N - 1]['value'] = del_box
    else:
        # remove the deleted box form the current selectbox
        for key in ['value', 'options']:
            del m_save_obj[m_select_idx][key][del_box_idx]

        # last box
        m_save_obj[N - 1]['options'] += m_save_obj[N - 2]['options'].copy()
        m_save_obj[N - 1]['options'].sort()
        m_save_obj[N - 1]['value'] = m_save_obj[N - 2]['value'].copy()

        for idx in range(N - 2, m_select_idx, -1):
            for key in ['value', 'options']:
                m_save_obj[idx][key] = m_save_obj[idx - 1][key]

        # Set current box
        for key in ['value', 'options']:
            m_save_obj[m_select_idx][key] = del_box.copy()


def deselect_right_most_box_idx(m_select_idx: int,
                                m_save_obj: MultiSelectSave,
                                del_box: list[int],
                                del_box_idx: int):
    # *************************************************************
    # Deslect the righ most box raw filled with at least 2 boxes
    # Before:
    # ---------
    # |A      |
    # |B, C, D|  <-- (deselct "D")
    # |E, F   |
    # |G      |
    # ---------
    #  H    ("H" not selected yet)
    #
    # After: ("D" will be the only box in the row & the rest of raws will
    #         move downwards)
    # ---------
    # |A      |
    # |B, C   |
    # |D      |
    # |E, F   |
    # ---------
    #  G    ("G", "H" moved to options of last raw)
    #  H
    # *************************************************************
    """
    Args:
        m_select_idx: (int) the id of the multiseclt raw
        m_save_obj: (MultiSelectSave) an object which we store st.seesion_state
        del_box: (list[int]) the box which is deleselected
        de_box_idx: (int) the id of the del box in m_save_obj[m_selecd_idx]['value']
    """
    N = len(m_save_obj)
    # remove the deleted box form the current selectbox
    for key in ['value', 'options']:
        del m_save_obj[m_select_idx][key][del_box_idx]

    if m_select_idx == N - 2:
        m_save_obj[N - 1]['options'] += del_box.copy()
        m_save_obj[N - 1]['options'].sort()
        m_save_obj[N - 1]['value'] = del_box.copy()
    else:
        # last box
        m_save_obj[N - 1]['options'] += m_save_obj[N - 2]['options'].copy()
        m_save_obj[N - 1]['options'].sort()
        m_save_obj[N - 1]['value'] = m_save_obj[N - 2]['value'].copy()

        # move boxes one raw below
        for idx in range(N - 2, m_select_idx + 1, -1):
            for key in ['value', 'options']:
                m_save_obj[idx][key] = m_save_obj[idx - 1][key]

        # Set current box
        for key in ['value', 'options']:
            m_save_obj[m_select_idx + 1][key] = del_box.copy()


def multiselect_callback(m_select_idx: int,
                         m_save_obj: MultiSelectSave,
                         multiselect='multiselect',
                         debug=False,
                         ):
    # *************************************************************
    # Deslect the only left box ("B")
    # Before:
    # --------
    # |A     |
    # |B     |  <-- (deselct "B")
    # |C, D  |
    # --------
    #  E    ("E" not selected yet)
    #
    # After: (Merge "B" with the box above & move the boxes below one block up)
    # --------
    # |A, B  |
    # |C, D  |
    # |E     |
    # --------
    # *************************************************************
    # we assuem to deselct or select only one box at a time
    if (st.session_state[f'{multiselect}_{m_select_idx}'] == [] and
            m_select_idx != 0):
        deselct_single_box(m_select_idx, m_save_obj)

    elif (st.session_state[f'{multiselect}_{m_select_idx}'] == []
            and m_select_idx == 0):
        st.session_state[f'{multiselect}_{m_select_idx}'] = \
            m_save_obj[0]['value']

    else:
        N = len(m_save_obj)
        del_box = list(
            set(m_save_obj[m_select_idx]['value']) -
            set(st.session_state[f'{multiselect}_{m_select_idx}']))
        del_box_idx = None
        if del_box:
            del_box_idx = m_save_obj[m_select_idx]['value'].index(del_box[0])

        # *************************************************************
        # Deslect the left most box with raw filled with at least 2 boxes
        # Before:
        # ---------
        # |A      |
        # |B, C, D|  <-- (deselct "B")
        # |E, F   |
        # |G      |
        # ---------
        #  H    ("H" not selected yet)
        #
        # After: ("B" will be the only box in the row & the rest of raws will
        #         move downwards)
        # ---------
        # |A      |
        # |B      |
        # |C, D   |
        # |E, F   |
        # ---------
        #  G    ("G", "H" moved to options of last raw)
        #  H
        # *************************************************************
        # we assuem every element of ['value'] or ['options'] is a sorted list
        # if the box is at the left (move rest of boxed down)
        if del_box_idx == 0:
            deselect_left_most_box_idx(
                m_select_idx=m_select_idx,
                m_save_obj=m_save_obj,
                del_box=del_box,
                del_box_idx=del_box_idx)

        # *************************************************************
        # Deslect the righ most box raw filled with at least 2 boxes
        # Before:
        # ---------
        # |A      |
        # |B, C, D|  <-- (deselct "D")
        # |E, F   |
        # |G      |
        # ---------
        #  H    ("H" not selected yet)
        #
        # After: ("D" will be the only box in the row & the rest of raws will
        #         move downwards)
        # ---------
        # |A      |
        # |B, C   |
        # |D      |
        # |E, F   |
        # ---------
        #  G    ("G", "H" moved to options of last raw)
        #  H
        # *************************************************************
        elif ((del_box_idx == len(m_save_obj[m_select_idx]['value']) - 1) and
                (m_select_idx != N - 1)):
            deselect_right_most_box_idx(
                    m_select_idx=m_select_idx,
                    m_save_obj=m_save_obj,
                    del_box=del_box,
                    del_box_idx=del_box_idx)

        else:
            m_save_obj[m_select_idx]['value'] = sorted(
                st.session_state[f'{multiselect}_{m_select_idx}'])

    if debug:
        print(f'm_idx: {m_select_idx}')
        print(m_save_obj)
    m_save_obj.validate_duplicate_ids()

    # assetion if the selected options are not following each other
    if st.session_state[f'{multiselect}_{m_select_idx}']:
        sorted_values = sorted(st.session_state[f'{multiselect}_{m_select_idx}'])
        low = sorted_values[0]
        high = sorted_values[-1]
        if sorted_values != list(range(low, high + 1, 1)):
            reset_multiselcts(
                max_len=len(m_save_obj),
                max_options=m_save_obj.get_max_options(),
                multiselect=multiselect,
                hard=True)

    # check for options are the same as the input (sorted)
    m_save_obj.check_options()


def reset_multiselcts(max_len: int,
                      max_options: int,
                      multiselect='multiselect',
                      multiselect_save='multiselect_save',
                      default_options: list[list[Any]] = None,
                      hard=False,
                      rtl=True):
    """
    Rest the multiselcts
    max_len: (int): max number of multiselct boxes
    max_optins: (int): max number of optins
    multiselect: (str) the name of multiselct base key in the st.session_state
        to be used as (f'{multiselect}_{m_idx}')
    multiselect_save: (str) the name of multiselct_save base key in
        the st.session_state to be used as
        st.seesion_state[f'{multiselect_save}_{m_idx}'] = \
            {'options': list[int], value: list[int]}
        where 'options': the the list of optins for the multisect with id=m_idx
        and 'value': is the default value associated with the box
    hard: (bool) force to reset the multiselect to the initial state
    rtl: (bool) display boxes in descending order (right to left)
    """
    options_ids = list(range(max_options))
    default_options_ids = [[idx] for idx in options_ids]
    if default_options is not None:
        if len(default_options) >= max_len:
            default_options_ids = get_boxes_ids(default_options)

    # Initialize sessoin state
    for m_idx in range(max_len - 1):
        if (f'{multiselect_save}_{m_idx}' not in st.session_state) or hard:
            st.session_state[f'{multiselect_save}_{m_idx}'] = {
                'value': default_options_ids[m_idx],
                'options': default_options_ids[m_idx].copy(),
            }
            # value os the mulitselect box itself
            st.session_state[f'{multiselect}_{m_idx}'] = select_ids(
                default_options_ids[m_idx], options_ids, rtl=rtl)

    # Last multiselct cell (filled with the rest of the cells)
    if (f'{multiselect_save}_{max_len - 1}' not in st.session_state) or hard:
        st.session_state[f'{multiselect_save}_{max_len - 1}'] = {
            'value': default_options_ids[max_len - 1],
            'options': join_lists(default_options_ids[max_len - 1:].copy())
        }
        # value os the mulitselect box itself
        st.session_state[f'{multiselect}_{max_len - 1}'] = select_ids(
            default_options_ids[max_len - 1], options_ids, rtl=rtl)


def join_lists(L: list[list[Any]]) -> list[Any]:
    out_L = []
    for item in L:
        out_L += item
    return out_L


def get_boxes_ids(default_optins: list[list[Any]]) -> list[list[int]]:
    """
    Return: Ids of of options staring from 0
    ex: [['A', 'B'], ['C', 'D'] ['E']] -> [[0, 1], [2, 3], [4]]
    """
    idx = 0
    default_optins_ids: list[list[int]] = []
    for inner_opt in default_optins:
        inner_ids = list(range(idx, idx + len(inner_opt), 1))
        default_optins_ids.append(inner_ids)
        idx += len(inner_opt)
    return default_optins_ids


def hash_options(options: list[list[Any]], max_len):
    return f'{options}_{max_len}'


def multiselect_list(default_options: list[list[Any]],
                     max_len: int,
                     rtl=True,
                     debug=False) -> list[list[int]]:
    """
    src for dynamicly change wedgit default values:
    https://github.com/streamlit/streamlit/issues/3925#issuecomment-946148239

    Args:
        default_optoins (2D list): of options
        rtl: (bool) display boxes in descending order (right to left)
    Return:
        seleteced_ids of the options (2D list)
    """
    options = join_lists(default_options)

    multiselect_save = 'multiselect_save'
    multiselect = 'multiselect'
    m_save_obj = MultiSelectSave(
        dict_obj=st.session_state,
        key_name=multiselect_save,
        max_len=max_len,
        max_options=len(options),
    )

    # Reset session_state
    # if stored default_options != new_default_options -> reset hard
    reset_hard = False
    if 'last_default_options' not in st.session_state:
        st.session_state.last_default_options = (
            hash_options(default_options, max_len))
    if (hash_options(default_options, max_len) !=
            st.session_state.last_default_options):
        reset_hard = True
        st.session_state.last_default_options = (
            hash_options(default_options, max_len))
    reset_multiselcts(
        max_len=max_len,
        max_options=len(options),
        multiselect=multiselect,
        multiselect_save=multiselect_save,
        default_options=default_options,
        rtl=rtl,
        hard=reset_hard,
    )

    options_ids = list(range(len(options)))

    # main code
    selected_options_ids = []
    for m_idx in range(max_len):
        # foram-fun: https://discuss.streamlit.io/t/format-func-function-examples-please/11295/2
        selected_ids = st.multiselect(
            options=select_ids(
                m_save_obj[m_idx]['options'], options_ids, rtl=False),
            default=select_ids(
                m_save_obj[m_idx]['value'], options_ids, rtl=rtl),
            label='Select',
            label_visibility='hidden',
            format_func=lambda x: options[x],
            on_change=multiselect_callback,
            args=(m_idx, m_save_obj),
            kwargs={'debug': debug},
            key=f'{multiselect}_{m_idx}')
        st.write('----------------')
        selected_options_ids.append(sorted(selected_ids))

    return selected_options_ids
