from pathlib import Path

text_list = Path("unvoice_memo.txt").read_text().replace("\t", " ").splitlines()

phoneme_list = [s.split() for s in text_list[2::3]]

text = "\n".join([" ".join(s) for s in phoneme_list])
Path("emotion_phoneme.txt").write_text(text)
