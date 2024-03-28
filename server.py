from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.quran_utils import Aya, AyaFormat


QURAN_MAP_PATH = 'quran-script/quran-uthmani-imlaey-map.json'


@asynccontextmanager
async def lifespan(app: FastAPI):
    # StartUP event (called before start)

    # Get Sura names
    start_aya = Aya(QURAN_MAP_PATH, sura_idx=1, aya_idx=1)
    suar_names = []
    for sura_idx in range(1, 115, 1):
        start_aya.set(sura_idx=sura_idx, aya_idx=1)
        sura_name = start_aya.get().sura_name
        suar_names.append(sura_name)
    global SUAR_NAMES
    SUAR_NAMES = suar_names

    global AYA
    # the aya which we rely on is the first aya that has no rasm_map
    for aya in start_aya.get_ayat_after():
        if aya.get().rasm_map is None:
            AYA = aya
            break

    yield
    # Shutdow event (called before shutdown)

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get/")
def get(sura_idx: int, aya_idx: int) -> dict:
    new_aya = AYA.set_new(sura_idx=sura_idx, aya_idx=aya_idx)
    return new_aya.get().__dict__


@app.get("/get_suar_names/")
async def get_suar_list() -> list[str]:
    """
    get list of Holy Quan suar names
    """
    return SUAR_NAMES


@app.get("/step_ayat/")
def step_ayat(sura_idx: int, aya_idx: int, step: int) -> dict:
    new_aya = AYA.set_new(sura_idx=sura_idx, aya_idx=aya_idx)
    new_aya = new_aya.step(step)
    return new_aya.get().__dict__
