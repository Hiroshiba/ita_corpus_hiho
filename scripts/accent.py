import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import List

from openjtalk_label_getter import OutputType, openjtalk_label_getter

false_code = "0"
true_code = "1"
unknown_code = "?"

text_list = Path("text.txt").read_text().splitlines()
input_phoneme_text_list = Path("phoneme.txt").read_text().splitlines()

output_text = ""
for text, input_phoneme_text in zip(text_list, input_phoneme_text_list):
    log_path = Path("/tmp/log.txt")

    label_list = openjtalk_label_getter(
        text=text,
        openjtalk_command="open_jtalk",
        dict_path=Path("/var/lib/mecab/dic/open-jtalk/naist-jdic"),
        htsvoice_path=Path(
            "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
        ),
        output_wave_path=None,
        output_log_path=log_path,
        output_type=OutputType.full_context_label,
        without_span=False,
    )

    is_type1 = False
    openjtalk_phoneme_list = []
    is_accent_start_list = []
    is_accent_end_list = []
    is_accent_phrase_start_list = []
    is_accent_phrase_end_list = []
    for label in label_list:
        phoneme, a, b, c = re.match(
            r".+?\^.+?\-(.+?)\+.+?\=.+?/A:(.+?)\+(.+?)\+(.+?)/B:.+", label.label
        ).groups()

        if phoneme in "AIUEO":
            phoneme = phoneme.lower()

        is_accent_end = a == "0"

        if b == "1":
            is_type1 = is_accent_end

        if b == "1" and is_type1:
            is_accent_start = True
        elif b == "2" and not is_type1:
            is_accent_start = True
        else:
            is_accent_start = False

        openjtalk_phoneme_list.append(phoneme)
        is_accent_start_list.append(is_accent_start)
        is_accent_end_list.append(is_accent_end)
        is_accent_phrase_start_list.append(b == "1")
        is_accent_phrase_end_list.append(c == "1")

    input_phoneme_list = input_phoneme_text.split()

    output_accent_start_list: List[str] = []
    output_accent_end_list: List[str] = []
    output_accent_phrase_start_list: List[str] = []
    output_accent_phrase_end_list: List[str] = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(
        None, input_phoneme_list, openjtalk_phoneme_list
    ).get_opcodes():
        p = input_phoneme_list[i1:i2]
        s = is_accent_start_list[j1:j2]
        e = is_accent_end_list[j1:j2]
        ps = is_accent_phrase_start_list[j1:j2]
        pe = is_accent_phrase_end_list[j1:j2]

        if tag == "equal":
            output_accent_start_list += [true_code if t else false_code for t in s]
            output_accent_end_list += [true_code if t else false_code for t in e]
            output_accent_phrase_start_list += [
                true_code if t else false_code for t in ps
            ]
            output_accent_phrase_end_list += [
                true_code if t else false_code for t in pe
            ]
        elif p == ["sil"] or p == ["pau"]:
            output_accent_start_list += [false_code]
            output_accent_end_list += [false_code]
            output_accent_phrase_start_list += [false_code]
            output_accent_phrase_end_list += [false_code]
        else:
            output_accent_start_list += [unknown_code] * len(p)
            output_accent_end_list += [unknown_code] * len(p)
            output_accent_phrase_start_list += [unknown_code] * len(p)
            output_accent_phrase_end_list += [unknown_code] * len(p)

    output_text += text + "\n"
    output_text += "\t".join(input_phoneme_list) + "\n"
    output_text += "\t".join(output_accent_start_list) + "\n"
    output_text += "\t".join(output_accent_end_list) + "\n"
    output_text += "\t".join(output_accent_phrase_start_list) + "\n"
    output_text += "\t".join(output_accent_phrase_end_list) + "\n"

Path("accent_memo.txt").write_text(output_text)
