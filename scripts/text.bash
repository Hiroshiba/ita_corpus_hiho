curl https://raw.githubusercontent.com/mmorise/ita-corpus/main/emotion_transcript_utf8.txt > /tmp/text.txt
cat /tmp/text.txt | awk -F':' '{print $2}' | awk -F',' '{print $1}' > text.txt
