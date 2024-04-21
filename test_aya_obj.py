from app.quran_utils import Aya, normalize_aya, search, WordSpan
import time

if __name__ == "__main__":
    # -------------------------------------------------------------------
    # Test General Use
    # -------------------------------------------------------------------
    # start_aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 1, 1)
    # start_aya.set(114, 2)
    # # print(start_aya.get())
    # start = time.time()
    # for idx, aya in enumerate(start_aya.get_ayat_after()):
    #     print(aya.get())
    # print('idx', idx)
    # print(f'Total Time: {time.time() - start:f}')
    # print(start_aya)

    # -------------------------------------------------------------------
    # Test set rasm
    # -------------------------------------------------------------------
    # start_aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 113, 1)
    #
    # print('Before: ')
    # print(start_aya.get())
    #
    # uthmani_list = [[word] for word in start_aya.get().uthmani.split()]
    # imlaey_list = [[word] for word in start_aya.get().imlaey.split()]
    # start_aya.set_rasm_map(uthmani_list, imlaey_list)
    #
    # print('After: ')
    # print(start_aya.get())

    # -------------------------------------------------------------------
    # Test General Step
    # -------------------------------------------------------------------
    # start_aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 114, 1)
    # steps = [0, 1, 293, 493, 292, -1, -2, -11]
    # # steps = [-1]
    # for step in steps:
    #     print(f'Step={step}')
    #     print(start_aya.step(step))
    #     print('#' * 30)

    # -------------------------------------------------------------------
    # Test get_fromatted_rasmp_map
    # -------------------------------------------------------------------
    # aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 111, 1)
    # print(aya.get_formatted_rasm_map())

    # -------------------------------------------------------------------
    # Test set_new
    # -------------------------------------------------------------------
    # aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 111, 1)
    # new_aya = aya.set_new(4, 4)
    # print('OLD AYA')
    # print(aya)
    # print()
    # print('NEW AYA')
    # print(new_aya)

    # -------------------------------------------------------------------
    # Test normaliz text
    # -------------------------------------------------------------------
    # aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 2, 5)
    # norm_aya = normalize_aya(
    #     aya.get().imlaey,
    #     remove_spaces=True,
    #     ignore_hamazat=True,
    #     ignore_alef_maksoora=True,
    #     ignore_haa_motatrefa=True,
    #     ignore_taa_marboota=True,
    #     ignore_small_alef=True,
    #     ignore_tashkeel=True,
    # )
    # print(aya.get().imlaey)
    # print(norm_aya)

    # -------------------------------------------------------------------
    # Test search
    # -------------------------------------------------------------------
    # start_aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 1, 1)
    # search_aya = start_aya.set_new(1, 1)
    # # search_text = "الحمد لله"
    # search_text = "وأن لو"
    # results = search(
    #     start_aya,
    #     search_text,
    #     # search_aya.get().imlaey,
    #     ignore_hamazat=True,
    #     ignore_alef_maksoora=True,
    #     ignore_haa_motatrefa=True,
    #     ignore_taa_marboota=True,
    #     ignore_small_alef=True,
    #     ignore_tashkeel=True,
    # )
    # for item in results:
    #     span, aya = item
    #     print(f'SPAN={span}, Imlaey={aya.get().imlaey}')
    #     print('-' * 20)

    # -------------------------------------------------------------------
    # Test _encode_imlaey_to_uthmani
    # -------------------------------------------------------------------
    # aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 1, 5)
    # print(aya)
    # print(aya._encode_imlaey_to_uthmani())

    # -------------------------------------------------------------------
    # Test _encode_imlaey_to_uthmani
    # -------------------------------------------------------------------
    aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 72, 16)
    span = WordSpan(0, 7)
    print(aya.imlaey_to_uthmani(span))











