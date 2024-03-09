from app.quran_utils import Aya

if __name__ == "__main__":
    start_aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 1, 1)
    start_aya.set(114, 2)
    print(start_aya.get())
    for idx, aya in enumerate(start_aya.get_ayat_after()):
        print(aya.get())
    print('idx', idx)

    # -------------------------------------------------------------------
    # Test set rasm
    # -------------------------------------------------------------------
    start_aya = Aya('quran-script/quran-uthmani-imlaey-map.json', 114, 1)

    print('Before: ')
    print(start_aya.get())

    uthmani_list = [[word] for word in start_aya.get().uthmani.split()]
    imlaey_list = [[word] for word in start_aya.get().imlaey.split()]
    start_aya.set_rasm_map(uthmani_list, imlaey_list)

    print('After: ')
    print(start_aya.get())
