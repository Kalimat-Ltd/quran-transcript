from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
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
    start_aya.set(1, 1)
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
    global AYA
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


@app.get("/get_first_aya_to_annotate/")
async def walk():
    global AYA
    for new_aya in AYA.get_ayat_after():
        uthmani_words: list[list[str]] = (
            [[word] for word in new_aya.get().uthmani.split(' ')])
        imlaey_words: list[list[str]] = (
            [[word] for word in new_aya.get().imlaey.split(' ')])
        if new_aya.get().rasm_map is None:
            if len(uthmani_words) == len(imlaey_words):
                new_aya.set_rasm_map(
                    uthmani_list=uthmani_words,
                    imlaey_list=imlaey_words)
            else:
                AYA = new_aya
                break
    return new_aya.get().__dict__


class RasmMap(BaseModel):
    sura_idx: int
    aya_idx: int
    uthmani_words: list[list[str]]
    imlaey_words: list[list[str]]


# src: https://fastapi.tiangolo.com/advanced/response-change-status-code/
@app.post('/save_rasm_map/', status_code=200)
async def save_rasm_map(rasm_map: RasmMap, response: Response):
    sura_idx = rasm_map.sura_idx
    aya_idx = rasm_map.aya_idx
    uthmani_words = rasm_map.uthmani_words
    imlaey_words = rasm_map.imlaey_words
    global AYA
    new_aya = AYA.set_new(sura_idx=sura_idx, aya_idx=aya_idx)
    try:
        new_aya.set_rasm_map(
            uthmani_list=uthmani_words, imlaey_list=imlaey_words)
    except AssertionError:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE










