search_dir=/home/djordje/Documents/GitHub/slagalica-ocr/downloads
for entry in "$search_dir"/*
do
  echo "$entry"
  ./run.sh "local" "$entry"
done