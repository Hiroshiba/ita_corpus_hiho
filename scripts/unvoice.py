import re
from difflib import SequenceMatcher
from pathlib import Path

from openjtalk_label_getter import OutputType, openjtalk_label_getter

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

    openjtalk_phoneme_list = []
    for label in label_list:
        phoneme, a, b, c = re.match(
            r".+?\^.+?\-(.+?)\+.+?\=.+?/A:(.+?)\+(.+?)\+(.+?)/B:.+", label.label
        ).groups()

        openjtalk_phoneme_list.append(phoneme)

    input_phoneme_list = input_phoneme_text.split()

    output_phoneme_list = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(
        None, input_phoneme_list, openjtalk_phoneme_list
    ).get_opcodes():
        pi = input_phoneme_list[i1:i2]
        po = openjtalk_phoneme_list[j1:j2]

        if tag == "equal":
            output_phoneme_list += po
        elif (pi == ["i"] and po == ["I"]) or (pi == ["u"] and po == ["U"]):
            output_phoneme_list += po
        else:
            output_phoneme_list += pi

    output_text += text + "\n"
    output_text += "\t".join(input_phoneme_list) + "\n"
    output_text += "\t".join(output_phoneme_list) + "\n"

Path("unvoice_memo.txt").write_text(output_text)
