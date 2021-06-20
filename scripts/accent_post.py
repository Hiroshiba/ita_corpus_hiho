from pathlib import Path

text_list = Path("accent_memo.txt").read_text().replace("\t", " ").splitlines()

phoneme_list = [s.split() for s in text_list[1::6]]
accent_start_list = [s.split() for s in text_list[2::6]]
accent_end_list = [s.split() for s in text_list[3::6]]
accent_phrase_start_list = [s.split() for s in text_list[4::6]]
accent_phrase_end_list = [s.split() for s in text_list[5::6]]

text = "\n".join([" ".join(s) for s in accent_start_list])
Path("emotion_accent_start.txt").write_text(text)

text = "\n".join([" ".join(s) for s in accent_end_list])
Path("emotion_accent_end.txt").write_text(text)

text = "\n".join([" ".join(s) for s in accent_phrase_start_list])
Path("emotion_accent_phrase_start.txt").write_text(text)

text = "\n".join([" ".join(s) for s in accent_phrase_end_list])
Path("emotion_accent_phrase_end.txt").write_text(text)
