bash scripts/text.bash
bash scripts/phoneme.bash
python scripts/unvoice.py
# 修正
python scripts/unvoice_post.py
python scripts/accent.py
# 修正
python scripts/accent_post.py
python scripts/accent_check.py

bash <(cat scripts/text.bash | sed -r 's|emotion|recitation|g')
bash <(cat scripts/phoneme.bash | sed -r 's|emotion(/normal)?|recitation|g')
python <(cat scripts/unvoice.py | sed -r 's|emotion|recitation|g')
# 修正
python <(cat scripts/unvoice_post.py | sed -r 's|emotion|recitation|g')
python <(cat scripts/accent.py | sed -r 's|emotion|recitation|g')
# 修正
python <(cat scripts/accent_post.py | sed -r 's|emotion|recitation|g')
python <(cat scripts/accent_check.py | sed -r 's|emotion|recitation|g')
