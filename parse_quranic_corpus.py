import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional
import json

from quran_transcript import Aya
from quran_transcript.alphabet import uthmani as uth
from quran_transcript.alphabet import BeginHamzatWasl


@dataclass
class WordPart:
    sura: int
    aya: int
    word_index: int
    part_index: int
    form: str
    tag: str
    features: Dict[str, Optional[str]] = field(default_factory=dict)


@dataclass
class QuranWord:
    sura: int
    aya: int
    word_index: int
    uthmani_word: str
    parts: List[WordPart] = field(default_factory=list)

    @property
    def combined_form(self) -> str:
        return "".join(
            part.form for part in sorted(self.parts, key=lambda p: p.part_index)
        )


def parse_corpus_data(corpus_text: str) -> List[QuranWord]:
    # prepare aya
    sura_to_aya_to_uthmani_word = [[] for _ in range(114)]
    start_aya = Aya(1, 1)
    for aya in start_aya.get_ayat_after():
        info = aya.get()
        sura_to_aya_to_uthmani_word[info.sura_idx - 1].append(info.uthmani_words)

    # Skip header and copyright lines
    lines = [line.strip() for line in corpus_text.split("\n")]
    data_lines = []
    found_header = False

    for line in lines:
        if line.startswith("LOCATION\tFORM\tTAG\tFEATURES"):
            found_header = True
            continue
        if not found_header or not line or line.startswith("#"):
            continue
        if line.startswith("(") and "\t" in line:
            data_lines.append(line)

    # Group parts by word
    words_dict: Dict[Tuple[int, int, int], QuranWord] = {}

    for line in data_lines:
        parts = line.split("\t")
        if len(parts) < 4:
            continue

        loc_str, form, tag, features_str = parts[:4]

        # Parse location (1:1:1:1)
        loc_parts = loc_str.strip("()").split(":")
        try:
            sura = int(loc_parts[0])
            aya = int(loc_parts[1])
            word_idx = int(loc_parts[2])
            part_idx = int(loc_parts[3])
        except (ValueError, IndexError):
            continue

        # Parse features into dictionary
        features = {}
        for item in features_str.split("|"):
            if ":" in item:
                key, value = item.split(":", 1)
                features[key] = value
            else:
                features[item] = None

        # Create WordPart
        word_part = WordPart(
            sura=sura,
            aya=aya,
            word_index=word_idx,
            part_index=part_idx,
            form=form,
            tag=tag,
            features=features,
        )

        # Group into QuranWord
        word_key = (sura, aya, word_idx)
        if word_key not in words_dict:
            try:
                words_dict[word_key] = QuranWord(
                    sura=sura,
                    aya=aya,
                    word_index=word_idx,
                    uthmani_word=sura_to_aya_to_uthmani_word[sura - 1][aya - 1][
                        word_idx - 1
                    ],
                )
            except Exception as e:
                print(sura, aya, word_idx)
                print(Aya(sura, aya))
                print(sura_to_aya_to_uthmani_word[sura - 1][aya - 1])
                raise e

        words_dict[word_key].parts.append(word_part)

    # Sort parts within each word
    for word in words_dict.values():
        word.parts.sort(key=lambda p: p.part_index)

    quran_words = list(words_dict.values())
    sura_to_aya_to_q_word = [[] for _ in range(114)]
    for q_word in quran_words:
        sura_idx = q_word.sura - 1
        aya_idx = q_word.aya - 1
        if aya_idx >= len(sura_to_aya_to_q_word[sura_idx]):
            sura_to_aya_to_q_word[sura_idx].append([])
        sura_to_aya_to_q_word[sura_idx][aya_idx].append(q_word)

    for sura_idx in range(len(sura_to_aya_to_uthmani_word)):
        for aya_idx in range(len(sura_to_aya_to_uthmani_word[sura_idx])):
            uthmani_len = len(sura_to_aya_to_uthmani_word[sura_idx][aya_idx])
            q_word_len = len(sura_to_aya_to_q_word[sura_idx][aya_idx])
            if uthmani_len != q_word_len:
                print(
                    f"Index: ({sura_idx + 1}, {aya_idx + 1})# of Uthmani words: {uthmani_len}, # of corpus words: {q_word_len}"
                )
                print("-" * 10)

    print("Print attempt to fix mislighnment")
    miss_aligned = {
        (2, 181): 3,
        (8, 6): 4,
        (13, 37): 8,
        (37, 130): 3,
    }
    for sura_abs_idx, aya_abs_idx in miss_aligned:
        sura_idx = sura_abs_idx - 1
        aya_idx = aya_abs_idx - 1
        word_idx = miss_aligned[(sura_abs_idx, aya_abs_idx)] - 1
        sura_to_aya_to_q_word[sura_idx][aya_idx][word_idx].uthmani_word = " ".join(
            sura_to_aya_to_uthmani_word[sura_idx][aya_idx][word_idx : word_idx + 2]
        )
        print(sura_to_aya_to_q_word[sura_idx][aya_idx][word_idx].uthmani_word)
        for idx in range(word_idx + 1, len(sura_to_aya_to_q_word[sura_idx][aya_idx])):
            sura_to_aya_to_q_word[sura_idx][aya_idx][
                idx
            ].uthmani_word = sura_to_aya_to_uthmani_word[sura_idx][aya_idx][idx + 1]

    # fixed_quran_words = []
    # for sura_idx in range(len(sura_to_aya_to_q_word)):
    #     for aya_idx in range(len(sura_to_aya_to_q_word[sura_idx])):
    #         fixed_quran_words += sura_to_aya_to_q_word[sura_idx][aya_idx]

    return quran_words


def filter_words(
    quran_words: list[QuranWord],
    regs: str,
    tags: list[str] | str,
    part_idx: int | None = None,
    print_sets=False,
    verbose=True,
):
    if isinstance(tags, str):
        tags = [tags]
    tags = set(tags)
    word_forms = set()
    counter = 0
    for q_word in quran_words:
        re_outs = re.finditer(regs, q_word.uthmani_word)
        for re_out in re_outs:
            for target_tag in tags:
                if part_idx is not None:
                    parts = [q_word.parts[0]]
                else:
                    parts = q_word.parts
                for part in parts:
                    if (part.tag == target_tag) or (target_tag == "all"):
                        counter += 1
                        word_forms.add(q_word.uthmani_word)
                        if verbose:
                            print(f"Case: `{counter}`")
                            print(re_out)
                            print(q_word.uthmani_word)
                            print("Index: ", q_word.sura, q_word.aya, q_word.word_index)
                            print("-" * 40)
                            print("\n" * 2)

    if print_sets:
        print(f"Word Forms `{len(word_forms)}`")
        for word in word_forms:
            print(f"'{word}'")

    return word_forms


def write_begin_hamzat_wasl(quran_words: list[QuranWord], path: str):
    al_group_jamda = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}{uth.lam}",
        tags=["N", "PN", "ADJ", "IMPN", "PRON", "DEM", "REL", "T", "LOC"],
        part_idx=0,
        verbose=False,
        print_sets=False,
    )
    al_group_zaeda = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}{uth.lam}",
        tags="DET",
        part_idx=0,
        verbose=False,
        print_sets=False,
    )

    verbs_group = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}",
        tags="V",
        part_idx=0,
        verbose=False,
        print_sets=False,
    )

    names_group = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}",
        tags=["N", "PN", "ADJ", "IMPN", "PRON", "DEM", "REL", "T", "LOC"],
        part_idx=0,
        verbose=False,
        print_sets=False,
    )
    names_group = names_group - al_group_jamda

    names_verbs_inter = names_group.intersection(verbs_group)
    hazat_wasl_begin = BeginHamzatWasl(
        verbs_nouns_inter=names_verbs_inter,
        damma_aarida_verbs={
            "ٱمْشُوا۟",
            "ٱبْنُوا۟",
            "ٱقْضُوٓا۟",
            "ٱئْتُوا۟",
            "ٱئْتُونِى",
        },
        verbs=verbs_group,
        nouns=names_group,
    )
    data = asdict(hazat_wasl_begin)
    for k in data:
        data[k] = list(data[k])
    with open(path, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Example usage:
if __name__ == "__main__":
    file_path = "./quran-script/quranic-corpus-morphology-0.4.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        corpus_text = f.read()

    quran_words = parse_corpus_data(corpus_text)

    # Filtering
    print("\n\nVerbs start with Lam\n\n")
    filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}{uth.lam}",
        tags="V",
    )

    # print("\n\nالأسماء المعرفة\n\n")
    # filter_words(
    #     quran_words,
    #     regs=f"{uth.lam}{uth.kasra}?{uth.lam}{uth.shadda}{uth.fatha}{uth.haa}.(?![{uth.baa}{uth.waw}])",
    #     # tags=["PN", "N"],
    #     tags="all",
    #     part_idx=0,
    #     print_sets=True,
    # )

    # # Filtering
    # print("\n\nالاسم المعرف بال\n\n")
    # filter_words(
    #     quran_words,
    #     regs=f"^{uth.hamzat_wasl}{uth.lam}",
    #     tags="DET",
    # )

    print("\n\nالاسم المكتوب بال الجامدة\n\n")
    al_group_jamda = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}{uth.lam}",
        tags=["N", "PN", "ADJ", "IMPN", "PRON", "DEM", "REL", "T", "LOC"],
        part_idx=0,
        verbose=False,
        print_sets=False,
    )
    print(f"Al group Jameda: {len(al_group_jamda)}")
    al_group_zaeda = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}{uth.lam}",
        tags="DET",
        part_idx=0,
        verbose=False,
        print_sets=False,
    )
    print(f"Al group Zeda: {len(al_group_zaeda)}")

    print("\n\nالأفعلا \n\n")
    verbs_group = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}",
        tags="V",
        part_idx=0,
        verbose=False,
        print_sets=False,
    )
    print(f"Len of verbs: {len(verbs_group)}")

    print("\n\nالأسماء\n\n")
    names_group = filter_words(
        quran_words,
        regs=f"^{uth.hamzat_wasl}",
        tags=["N", "PN", "ADJ", "IMPN", "PRON", "DEM", "REL", "T", "LOC"],
        part_idx=0,
        verbose=False,
        print_sets=False,
    )
    names_group = names_group - al_group_jamda
    print(f"Len of names: {len(names_group)}")

    print(f"Names Verb Intersection: {verbs_group.intersection(names_group)}")
    print(f"Names Al Zeda Intersection: {names_group.intersection(al_group_zaeda)}")
    print(f"Verbs Al Zeda Intersection: {verbs_group.intersection(al_group_zaeda)}")
    print(f"Verbs Al Jamida Intersection: {verbs_group.intersection(al_group_jamda)}")

    write_begin_hamzat_wasl(quran_words, "./quran-script/begin_with_hamzat_wasl.json")
