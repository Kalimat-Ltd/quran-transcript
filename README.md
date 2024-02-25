# Quran Script Description
[TODO]

# `merge_uthmani_imlaey.py`
Merging Uthmani Quran and Imlaye Quran scipts of [tanzil](https://tanzil.net/download/) into a single scipt (".xml" and ".json")
* Uthmanic: without (pause marks, sajda signs, hizb signs)
* Imlaey: without (pause marks, sajda signs, hizb signs and tatweel sign)
Usage:
```bash
usage: Merge Uthmani and Imlaey Script into a single scipt [-h] [--uthmani-file UTHMANI_FILE] [--imlaey-file IMLAEY_FILE] [--output-file OUTPUT_FILE]

options:
  -h, --help            show this help message and exit
  --uthmani-file UTHMANI_FILE
                        The path to the input file "file.xml"
  --imlaey-file IMLAEY_FILE
                        The path to the input file "file.xml"
  --output-file OUTPUT_FILE
                        The path to the output file either ".json" or ".xml"
```

Example within the repo (json):
```bash
python merge_uthman_imlaey.py --uthmani-file quran-script/quran-uthmani-without-pause-sajda-hizb-marks.xml --imlaey-file quran-script/quran-simple-imlaey-without-puase-sajda-hizb-marks-and-tatweel.xml --output-file quran-script/quran-uthmani-imlaey.json
```

Example within the repo (json):
```bash
python merge_uthman_imlaey.py --uthmani-file quran-script/quran-uthmani-without-pause-sajda-hizb-marks.xml --imlaey-file quran-script/quran-simple-imlaey-without-puase-sajda-hizb-marks-and-tatweel.xml --output-file quran-script/quran-uthmani-imlaey.xml
```

