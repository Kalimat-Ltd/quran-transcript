from app.api_utils import get_aya, get_suar_names, step_ayat
import time

if __name__ == "__main__":
    start_time = time.time()
    ayaformat = get_aya(4, 4)
    print('Total time:', time.time() - start_time)
    print(ayaformat)
    print()

    print('Suar Names')
    print(get_suar_names())
    print()

    print('Step ayat')
    print(step_ayat(ayaformat, -10))
    print()
