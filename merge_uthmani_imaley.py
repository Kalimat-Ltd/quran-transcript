import argparse
from pathlib import Path
import json
import xmltodict


def save_quran_script(quran_dict: dict,
                      out_path: str | Path):
    """
    save the quran dict into json and xml format
    """
    default_extentions = ['xml', 'json']
    extention = Path(out_path).name.split('.')[-1]
    assert extention in default_extentions, \
        f'valid extentions: {default_extentions}'

    match extention:
        case 'xml':
            with open(Path(out_path), 'w+', encoding='utf8') as f:
                xml_str = xmltodict.unparse(quran_dict, pretty=True)
                f.write(xml_str)

        case 'json':
            with open(Path(out_path), 'w+', encoding='utf8') as f:
                json.dump(quran_dict, f, indent=2, ensure_ascii=False)


def merge_uthmani_imlaey(
    uthmani_file: str | Path,
    imlaey_file: str | Path,
    prefix='@',
    uthmani='uthmani',
    imlaey='imlaey',
    bismillah='bismillah'
        ) -> dict:
    """
    Merge the uthmani script and Imlaey into a single dictionary of Tanzil
    https://tanzil.net/download/
    Uthmanic: without (pause marks, sajda signs, hizb signs)
    Imlaey: without (pause marks, sajda signs, hizb signs and tatweel sign)
    {
        "quran":{
                "sura": [
                    {
                        "aya": [
                            {
                                "@index": (int): aya number
                                "@uthmani" (str): the string of uthmanic script
                                "@imlaey"" (str): thestring of the Imlaey script
                                "@bismillah_uthmani" (str): if the firist aya except for sura "Alfateha" & "Altuba"
                                "@bismillah_imlaey" (str): if the firist aya except for sura "Alfateha" & "Altuba"
                            }
                        ]
                    }
                ]
            }
    }
    Example:
    to acess sura Al Imran (3) and aya (10)
    quran_dict['quran']['sura'][3 - 1]['aya'][10 - 1]
    """

    with open(uthmani_file, 'r', encoding='utf8') as f:
        quran_uthmani_dict = xmltodict.parse(f.read())

    with open(imlaey_file, 'r', encoding='utf8') as f:
        quran_imlaey_dict = xmltodict.parse(f.read())

    quran_merged_dict = quran_uthmani_dict.copy()

    for sura_idx in range(len(quran_uthmani_dict['quran']['sura'])):
        for aya_idx in range(len(quran_uthmani_dict['quran']['sura'][sura_idx]['aya'])):

            # add uthmani aya
            key = f'{prefix}{uthmani}'
            quran_merged_dict['quran']['sura'][sura_idx]['aya'][aya_idx][key] = \
                quran_uthmani_dict['quran']['sura'][sura_idx]['aya'][aya_idx]['@text']

            # add emlaey aya
            key = f'{prefix}{imlaey}'
            quran_merged_dict['quran']['sura'][sura_idx]['aya'][aya_idx][key] = \
                quran_imlaey_dict['quran']['sura'][sura_idx]['aya'][aya_idx]['@text']

            # add @bismillah_uthmani
            key = f'{prefix}{bismillah}_{uthmani}'
            del_key = f'{prefix}{bismillah}'
            if (aya_idx == 0 and
                    del_key in quran_uthmani_dict['quran']['sura'][sura_idx]['aya'][aya_idx].keys()):
                quran_merged_dict['quran']['sura'][sura_idx]['aya'][aya_idx][key] = \
                    quran_uthmani_dict['quran']['sura'][sura_idx]['aya'][aya_idx][del_key]

                del quran_merged_dict['quran']['sura'][sura_idx]['aya'][aya_idx][del_key]

            # add @bismillah_imlaey
            key = f'{prefix}{bismillah}_{imlaey}'
            del_key = f'{prefix}{bismillah}'
            if (aya_idx == 0 and
                    del_key in quran_imlaey_dict['quran']['sura'][sura_idx]['aya'][aya_idx].keys()):
                quran_merged_dict['quran']['sura'][sura_idx]['aya'][aya_idx][key] = \
                    quran_imlaey_dict['quran']['sura'][sura_idx]['aya'][aya_idx][del_key]

            # remove "@text" key
            del quran_merged_dict['quran']['sura'][sura_idx]['aya'][aya_idx]['@text']

    return quran_merged_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'Merge Uthmani and Imlaey Script into a single scipt')
    parser.add_argument(
        '--uthmani-file',
        type=Path,
        help='The path to the input file "file.xml"')
    parser.add_argument(
        '--imlaey-file',
        type=Path,
        help='The path to the input file "file.xml"')
    parser.add_argument(
        '--output-file',
        type=Path,
        help='The path to the output file either ".json" or ".xml"')

    args = parser.parse_args()

    ext = args.uthmani_file.name.split('.')[-1]
    assert ext == 'xml', \
        f'Uthmani file extention has to be ".xml" your input: .{ext}'

    ext = args.imlaey_file.name.split('.')[-1]
    assert ext == 'xml', \
        f'Emlaey file extention has to be ".xml" your input: .{ext}'

    quran_merged = merge_uthmani_imlaey(
        uthmani_file=args.uthmani_file,
        imlaey_file=args.imlaey_file,
    )

    save_quran_script(
        quran_dict=quran_merged,
        out_path=args.output_file
    )

    print(json.dumps(quran_merged, indent=2, ensure_ascii=False))
