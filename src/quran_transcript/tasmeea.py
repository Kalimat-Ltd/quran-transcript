from dataclasses import dataclass
import math

import Levenshtein as lv


from .utils import normalize_aya, Aya, SegmentScripts


# def match_text(input_text: str, ref_text: str) -> float:
#     """returns the ratio donates how the input text is matching the `ref_text` the higher the better"""
#     ...
#
#
# def tasmeea_part(
#     input_text: str,
#     ref_words: list[str],
#     start_words=3,
#     overlap: int = 4,
#     window=10,
#     acceptance_ratio=0.3,
# ) -> str:
#     """
#     returns the best matching text or `None` if no matches
#     """
#     start = max(0, start_words - overlap)
#     num_of_windows = 3  # TODO:
#     best_ratio: float = None
#     best_text: str = None
#     for _ in num_of_windows:
#         # looping over all available winodws
#         for loop_window_len in range(window):
#             ref_text = "".join(ref_words[start : start + loop_window_len])
#             ratio = match_text(input_text, ref_text)
#             if ratio >= acceptance_ratio:
#                 if best_ratio is not None:
#                     if ratio > best_ratio:
#                         best_ratio = ratio
#                         best_text = ref_text
#                 else:
#                     best_ratio = ratio
#                     best_text = ref_text
#         start += 1
#
#     if best_ratio is not None:
#         return best_text
#     else:
#         return None


def estimate_window_len(text: str, winodw_words: int) -> tuple[int, int]:
    return (max(1, int(len(text) / 6)), math.ceil(len(text) / 3))


# TODO: add this
def estimate_overlap(text: str, prev_text: str | None, max_overlap: int) -> int: ...


def tasmeea_sura(
    text_segments: list[str],
    sura_idx: int,
    overlap_words: int = 6,
    window_words=30,
    acceptance_ratio: float = 0.5,
    include_istiaatha=True,
    include_bismillah=True,
    include_sadak=True,
    **kwargs,
) -> list[tuple[SegmentScripts | None], float]:
    """Returns the best matching quracic script for every text part"""

    assert overlap_words >= 0

    kwargs["remove_spaces"] = True
    aya = Aya(
        sura_idx=sura_idx,
        include_istiaatha_in_by_words_mode=include_istiaatha,
        include_bismillah_in_by_words_mode=include_bismillah,
        include_sdak_in_by_words_mode=include_sadak,
    )
    outputs = []
    prev_norm_text = None
    for text_seg in text_segments:
        norm_text = normalize_aya(text_seg, **kwargs)
        min_winodw_len, max_windwo_len = estimate_window_len(norm_text, window_words)
        overlap_len = estimate_overlap(norm_text, prev_norm_text, overlap_words)
        best_segment_scripts: SegmentScripts | None = None
        best_ratio: float = 0.0

        # initializing step words with min_window_len if not acceptable match
        step_words = min_winodw_len

        for start_words in range(-overlap_len, window_words - overlap_words):
            # looping over all available windows
            for loop_window_len in range(min_winodw_len, max_windwo_len + 1):
                segment_scripts = aya.get_by_imlaey_words(
                    start=start_words,
                    window=loop_window_len,
                )
                aya_imalaey_str = normalize_aya(segment_scripts.imalaey, **kwargs)
                match_ratio = lv.ratio(norm_text, aya_imalaey_str)
                if (match_ratio >= acceptance_ratio) and (match_ratio > best_ratio):
                    step_words = loop_window_len
                    best_segment_scripts = segment_scripts
                    best_ratio = match_ratio

        # move aya
        outputs.append((best_segment_scripts, best_ratio))
        aya = aya.step_by_imlaey_words(step_words)
        prev_norm_text = norm_text

    return outputs
