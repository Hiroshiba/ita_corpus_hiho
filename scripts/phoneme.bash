base=/mnt/dataset/ita_corpus/

output=phoneme.txt
echo -n '' >$output

ls $base/itako_voice_label/emotion/normal/*.lab | sort -V |
    while read f; do
        cat $f | awk '{print $NF}' | tr '\n' ' ' >>$output
        echo '' >>$output
    done
