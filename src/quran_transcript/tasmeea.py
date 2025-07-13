from dataclasses import dataclass
import math

import Levenshtein as lv

from .utils import normalize_aya, Aya, SegmentScripts, QuranWordIndex


def estimate_window_len(text: str, winodw_words: int) -> tuple[int, int]:
    return (max(1, int(len(text) / 5)), math.ceil(len(text) / 3))


def estimate_overlap(text: str, prev_text: str | None, max_overlap: int) -> int:
    if prev_text is None:
        return 0

    # suppose that the word has 5 characters
    return min(int(len(prev_text) / 10), max_overlap)


@dataclass
class BestSegment:
    start: int
    window: int
    segment_scripts: SegmentScripts | None = None
    ratio: float = 0.0
    bisimillah: bool = False


def tasmeea_sura(
    text_segments: list[str],
    sura_idx: int,
    overlap_words: int = 6,
    window_words=30,
    acceptance_ratio: float = 0.5,
    include_istiaatha=True,
    include_bismillah=True,
    include_sadaka=True,
    **kwargs,
) -> list[tuple[SegmentScripts | None, float]]:
    """Returns the best matching quracic script for every text part"""

    def _check_segment(
        _best: BestSegment,
        _aya,
        _start,
        _window,
        _istiaatha=False,
        _bismillah=False,
        _sadaka=False,
    ) -> BestSegment | None:
        segment_scripts = _aya.get_by_imlaey_words(
            start=_start,
            window=_window,
            include_istiaatha=_istiaatha,
            include_bismillah=_bismillah,
            include_sadaka=_sadaka,
        )
        aya_imalaey_str = normalize_aya(segment_scripts.imalaey, **kwargs)
        match_ratio = lv.ratio(norm_text, aya_imalaey_str)
        if (match_ratio >= acceptance_ratio) and (match_ratio > _best.ratio):
            _best.segment_scripts = segment_scripts
            _best.ratio = match_ratio
            _best.bisimillah = _bismillah
            if _istiaatha or _sadaka:
                _best.window = 0
                _best.start = 0
            else:
                _best.window = _window
                _best.start = _start
            return _best
        else:
            return None

    assert overlap_words >= 0

    kwargs["remove_spaces"] = True
    kwargs["remove_tashkeel"] = True
    aya = Aya(
        sura_idx=sura_idx,
    )
    last_aya = aya.step(aya.get().num_ayat_in_sura - 1)
    outputs = []
    prev_norm_text = None
    window_penalty = 0
    overlap_penalty = 0
    for idx, text_seg in enumerate(text_segments):
        norm_text = normalize_aya(text_seg, **kwargs)
        min_winodw_len, max_windwo_len = estimate_window_len(norm_text, window_words)
        overlap_len = estimate_overlap(norm_text, prev_norm_text, overlap_words)
        best = BestSegment(
            segment_scripts=None,
            ratio=0.0,
            start=overlap_len,
            window=min_winodw_len,
            bisimillah=False,
        )
        # istiaatha at the first
        if idx == 0 and include_istiaatha:
            out = _check_segment(
                _best=best,
                _aya=aya,
                _start=0,
                _window=5,
                _istiaatha=True,
                _bismillah=False,
                _sadaka=False,
            )
            if out:
                best = out
        # sadaka only at the last aya
        elif (idx + 1) == len(text_segments) and include_sadaka:
            sadaka_start = (
                len(last_aya.get().imlaey_words) - last_aya.get_start_imlaey_word_idx()
            )
            out = _check_segment(
                _best=best,
                _aya=last_aya,
                _start=sadaka_start,
                _window=3,
                _istiaatha=False,
                _bismillah=False,
                _sadaka=True,
            )
            if out:
                best = out

        print(aya.get().sura_idx, aya.get().aya_idx, aya.get_start_imlaey_word_idx())
        print(
            f"Text: {text_seg}, Min Window: {min_winodw_len}, Max Window: {max_windwo_len}, Overlap: {overlap_len + overlap_penalty}, Window Penlty: {window_penalty}"
        )
        # Initializing step words with min_window_len if not acceptable match
        for start_words in range(
            -(overlap_len + overlap_penalty),
            window_words + window_penalty - (overlap_len + overlap_penalty),
        ):
            # looping over all available windows
            for loop_window_len in range(min_winodw_len, max_windwo_len + 1):
                out = _check_segment(
                    _best=best,
                    _aya=aya,
                    _start=start_words,
                    _window=loop_window_len,
                    _istiaatha=False,
                    _bismillah=True
                    if aya.get().sura_idx not in {1, 9}
                    and include_bismillah
                    and aya.get().aya_idx == 1
                    else False,
                    _sadaka=False,
                )
                window_penalty = 0
                overlap_penalty = 0
                if out:
                    best = out

        # move aya
        if best.segment_scripts is None:
            window_penalty = max_windwo_len
            overlap_penalty = max_windwo_len
        outputs.append((best.segment_scripts, best.ratio))
        aya = aya.step_by_imlaey_words(
            start=best.start,
            window=best.window,
            include_bismillah=best.bisimillah,
        )
        prev_norm_text = norm_text

    return outputs


def check_sura_missing_parts(
    sura_idx: int,
    fixed_segments: list[SegmentScripts],
) -> list[SegmentScripts]:
    """we are checkint quranic verses only (not includes istiaatha, bismillah, or sadaka)"""

    def _find_missings(
        _start_aya: Aya,
        _start: tuple[int, int, QuranWordIndex],
        _end: tuple[int, int, QuranWordIndex],
    ) -> list[SegmentScripts]:
        _missings = []
        _start_aya = _start_aya.set_new(
            sura_idx=_start[0],
            aya_idx=_start[1],
            start_imlaey_word_idx=_start[2].imlaey,
        )
        _loop_aya = _start_aya
        while True:
            if (_loop_aya.get().sura_idx == _end[0]) and (
                _loop_aya.get().aya_idx == _end[1]
            ):
                window = _end[2].imlaey - _loop_aya.get_start_imlaey_word_idx()
                if window > 0:
                    miss_seg = _loop_aya.get_by_imlaey_words(
                        start=0,
                        window=window,
                    )
                    _missings.append(miss_seg)
                break

            # else
            window = (
                len(_loop_aya._encode_imlaey_to_uthmani().imlaey_words)
                - _loop_aya.get_start_imlaey_word_idx()
            )
            if window > 0:
                miss_seg = _loop_aya.get_by_imlaey_words(start=0, window=window)
                _missings.append(miss_seg)
            _loop_aya = _loop_aya.step(1)

        return _missings

    start_aya = Aya(sura_idx=sura_idx)
    start = (
        start_aya.get().sura_idx,
        start_aya.get().aya_idx,
        QuranWordIndex(imlaey=0, uthmani=0),
    )
    missings: list[SegmentScripts] = []
    actual_segments = [s for s in fixed_segments if s is not None]
    last_quran_seg: SegmentScripts | None = None
    for seg in actual_segments:
        if seg.has_quran:
            missings += _find_missings(
                _start_aya=start_aya,
                _start=start,
                _end=seg.start_span,
            )
            start = seg.end_span
            last_quran_seg = seg

    assert last_quran_seg is not None, "No Quan segments"
    if last_quran_seg != start_aya.get().sura_idx:
        end = last_quran_seg.end_span
        missings += _find_missings(
            _start_aya=start_aya,
            _start=start,
            _end=end,
        )
    else:
        start_aya_encoding = start_aya._encode_imlaey_to_uthmani()
        iml_words = len(start_aya_encoding.imlaey_words)
        end = (
            start_aya.get().sura_idx,
            start_aya.get().num_ayat_in_sura,
            QuranWordIndex(
                imlaey=iml_words,
                uthmani=start_aya_encoding.imlaey2uthmani[iml_words - 1] + 1,
            ),
        )
        missings += _find_missings(_start_aya=start_aya, _start=start, _end=end)

    return missings
