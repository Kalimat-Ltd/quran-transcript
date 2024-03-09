import streamlit as st
from typing import Any


def edit_ayah_page(uthmani_words: list[str],
                   emlaey_words: list[str],
                   emlaey_to_uthmani: dict[str, str] = None) -> dict[str, str]:
    """
    the display function that maps emlaey script words to uthmani script words
    Args:
        uthmani_words: list[str] list of the uthmani words of the ayah
        emaley_words: list[str] list of the emlaey words of the ayah
        emaley_to_uthmani: dict[str, str] dict with
            keys (emaley words or words) and value of (uthmani word or words)
    Return:
        emaley_to_uthmani: dict[str, str] dict with
            keys (emaley words or words) and value of (uthmani word or words)
            after uditing using the User Interface
    """
    pass


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

    # initialize sessoin state
    for m_idx in range(max_len - 1):
        if (f'{multiselect_save}_{m_idx}' not in st.session_state) or hard:
            st.session_state[f'{multiselect_save}_{m_idx}'] = {
                'value': [m_idx],
                'options': [m_idx]
            }
            # value os the mulitselect box itself
            st.session_state[f'{multiselect}_{m_idx}'] = select_ids(
                [m_idx], options_ids, rtl=rtl)

    # last multiselct cell (filled with the rest of the cells)
    if (f'{multiselect_save}_{max_len - 1}' not in st.session_state) or hard:
        st.session_state[f'{multiselect_save}_{max_len - 1}'] = {
            'value': [max_len - 1],
            'options': list(range(max_len - 1, len(options_ids), 1))
        }
        # value os the mulitselect box itself
        st.session_state[f'{multiselect}_{max_len - 1}'] = select_ids(
            [max_len - 1], options_ids, rtl=rtl)


def multiselect_list(options: list,
                     max_len: int,
                     rtl=True) -> list[list[int]]:
    """
    src for dynamicly change wedgit default values:
    https://github.com/streamlit/streamlit/issues/3925#issuecomment-946148239

    Args:
        rtl: (bool) display boxes in descending order (right to left)
    Return:
        seleteced_ids of the options (2D list)
    """

    multiselect_save = 'multiselect_save'
    multiselect = 'multiselect'
    m_save_obj = MultiSelectSave(
        dict_obj=st.session_state,
        key_name=multiselect_save,
        max_len=max_len,
        max_options=len(options),
    )

    # reset session_state
    reset_multiselcts(
        max_len=max_len,
        max_options=len(options),
        multiselect=multiselect,
        multiselect_save=multiselect_save,
        rtl=rtl)

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
            key=f'{multiselect}_{m_idx}')
        selected_options_ids.append(selected_ids)

    return selected_options_ids
