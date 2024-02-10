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
    buttons_names = ['Edit', 'Fill', 'Clear']
    buttons = {}
    for col, button in zip(st.columns(len(buttons_names)), buttons_names):
        with col:
            buttons[button] = st.button(button)


def flatten(L: list):
    flattened_list = []
    for outer in L:
        for inner in outer:
            flattened_list.append(inner)
    return flattened_list


def convert_ids_to_options(ids: list[int],
                           options: list[Any]) -> list[Any]:
    return_options = []
    for idx in ids:
        return_options.append(options[idx])
    return return_options


def multiselect_callback(m_select_idx: int,
                         multiselect_save: list[dict],
                         multiselect='multiselect',
                         ):
    max_len = len(multiselect_save)
    # we assuem to deselct or select only one box at a time
    if not st.session_state[f'{multiselect}_{m_select_idx}']:
        # move the box to the multiselct box above
        box_idx = multiselect_save[m_select_idx]['value']
        for key in ['value', 'options']:
            multiselect_save[m_select_idx - 1][key] += box_idx
            multiselect_save[m_select_idx - 1][key].sort()

        # ----------------------------------------------------------------
        # move all boxes down up one box starting of the selected box
        # ----------------------------------------------------------------
        for m_idx in range(m_select_idx, max_len - 2, 1):
            for key in ['value', 'options']:
                multiselect_save[m_idx][key] = multiselect_save[m_idx + 1][key]

        # box(max_len) - 2
        for key in ['value', 'options']:
            multiselect_save[max_len - 2][key] =\
                multiselect_save[max_len - 1]['value']

        # last box(max_len) - 1
        multiselect_save[max_len - 1]['options'] = \
            sorted(
                set(multiselect_save[max_len - 1]['options']) - \
                set(multiselect_save[max_len - 1]['value'])
                )

        multiselect_save[max_len - 1]['value'] = \
            multiselect_save[max_len - 1]['options'][:1]

    # st.session_state['multiselect_save'] = multiselect_save
    for idx, d in enumerate(st.session_state['multiselect_save']):
        print(idx)
        for k, v in d.items():
            print(f'{k}={v}')
        print('-' * 10)


def multiselect_list(options: list,
                     max_len: int):

    multiselect_save_name = 'multiselect_save'
    multiselect = 'multiselect'

    # initialize sessoin state
    if multiselect_save_name not in st.session_state:
        st.session_state[multiselect_save_name] = []
        for m_idx in range(max_len - 1):
            st.session_state[multiselect_save_name].append({
                'value': [m_idx],
                'options': [m_idx]
            })
            # value os the mulitselect box itself
            st.session_state[f'{multiselect}_{m_idx}'] = convert_ids_to_options(
                [m_idx], options)

    # last multiselct cell (filled with the rest of the cells)
    st.session_state[multiselect_save_name].append({
            'value': [max_len - 1],
            'options': list(range(max_len - 1, len(options), 1))
        })
    # value os the mulitselect box itself
    st.session_state[f'{multiselect}_{max_len - 1}'] = convert_ids_to_options(
        [max_len - 1], options)

    # main code
    print('#' * 30)
    print('MultiSelect')
    for m_idx in range(max_len):
        print(m_idx)
        print(convert_ids_to_options(st.session_state[multiselect_save_name][m_idx]['value'], options))
        print(convert_ids_to_options(st.session_state[multiselect_save_name][m_idx]['options'], options))
        st.multiselect(
            options=convert_ids_to_options(
                st.session_state[multiselect_save_name][m_idx]['options'], options),
            default=convert_ids_to_options(
                st.session_state[multiselect_save_name][m_idx]['value'], options),
            label='Select',
            label_visibility='hidden',
            on_change=multiselect_callback,
            args=(m_idx, st.session_state[multiselect_save_name]),
            key=f'{multiselect}_{m_idx}')

    # clean session_state

# def mulitselect_list(options: list,
#                      max_len: int) -> list:
#     pool = set(options[max_len:])
#     selected_options = [[]] * max_len
#     for idx in range(max_len):
#         selected_options[idx] = [options[idx]]
#
#     idx = 0
#     while idx < max_len:
#         curr_selected = st.multiselect(
#             options=selected_options[idx] + list(pool),
#             default=selected_options[idx] if selected_options[idx] else None,
#             label='Select',
#             label_visibility='hidden',
#             key=f'multiselect_{idx}')
#
#         if curr_selected == selected_options[idx]:
#             idx += 1
#         else:
#             idx = 0
#             pool = set(options) - set(flatten(selected_options))
#
#     return selected_options


# def mulitselect_list(options: list,
#                      max_len: int) -> list:
#     selected_idx = 0
#     selected_options = [[]] * max_len
#     for idx in range(max_len):
#         selected_options[idx] = st.multiselect(
#             options=options[selected_idx:],
#             default=options[selected_idx],
#             label='Select',
#             label_visibility='hidden',
#             key=f'mulitselect_{idx}'
#         )
#         selected_idx += len(selected_options[-1])
#
#     return selected_options
