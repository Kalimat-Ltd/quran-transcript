from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.quran_utils import Aya, AyaFormat


QURAN_MAP_PATH = 'quran-script/quran-uthmani-imlaey-map.json'


@asynccontextmanager
async def lifespan(app: FastAPI):
    # StartUP event (called before start)

    start_aya = Aya(QURAN_MAP_PATH)
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
async def get(sura_idx: int, aya_idx: int) -> dict:
    new_aya = AYA.set_new(sura_idx=sura_idx, aya_idx=aya_idx)
    return new_aya.get().__dict__
