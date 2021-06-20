bash text.bash
bash phoneme.bash
python unvoice.py
# 修正
python unvoice_post.py
python accent.py
# 修正
python accent_post.py
python accent_check.py


bash <(cat text.bash | sed -r 's|emotion|recitation|g')
bash <(cat phoneme.bash | sed -r 's|emotion(/normal)?|recitation|g')
python <(cat unvoice.py | sed -r 's|emotion|recitation|g')
# 修正
python <(cat unvoice_post.py | sed -r 's|emotion|recitation|g')
python <(cat accent.py | sed -r 's|emotion|recitation|g')
# 修正
python <(cat accent_post.py | sed -r 's|emotion|recitation|g')
python <(cat accent_check.py | sed -r 's|emotion|recitation|g')
