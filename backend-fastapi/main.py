import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="API Dashboard Restoran",
    description="API sederhana pengelolaan bahan baku dapur.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class BahanIn(BaseModel):
    nama_bahan: str = Field(min_length=1)
    kategori: str = Field(min_length=1)
    stok: int = Field(strict=True, ge=0)
    satuan: str = Field(min_length=1)

    @field_validator("nama_bahan", "kategori", "satuan")
    @classmethod
    def teks_tidak_boleh_kosong(cls, value: str) -> str:
        nilai = value.strip()
        if not nilai:
            raise ValueError("Field tidak boleh kosong")
        return nilai


class BahanOut(BahanIn):
    id: int


class StokUpdate(BaseModel):
    stok: int = Field(strict=True, ge=0)


class PesanRespons(BaseModel):
    pesan: str


FILE_BAHAN = Path(__file__).with_name("bahan_baku.json")


def baca_bahan() -> list[dict]:
    with FILE_BAHAN.open("r", encoding="utf-8") as file:
        return json.load(file)


def simpan_bahan() -> None:
    with FILE_BAHAN.open("w", encoding="utf-8") as file:
        json.dump(bahan_db, file, ensure_ascii=False, indent=2)
        file.write("\n")


bahan_db: list[dict] = baca_bahan()


@app.get(
    "/",
    tags=["Root"],
    summary="Cek status backend",
    description="Memastikan backend Dashboard Restoran sedang berjalan.",
)
def baca_root() -> dict[str, str]:
    return {"pesan": "Backend Dashboard Restoran berjalan"}


@app.get(
    "/bahan",
    tags=["Bahan Baku"],
    response_model=list[BahanOut],
    summary="Ambil semua bahan baku",
    description="Mengembalikan seluruh daftar bahan baku dapur dari penyimpanan JSON lokal.",
)
def baca_semua_bahan() -> list[dict]:
    return bahan_db


@app.post(
    "/bahan",
    status_code=status.HTTP_201_CREATED,
    tags=["Bahan Baku"],
    response_model=BahanOut,
    summary="Tambah bahan baku",
    description="Menambahkan bahan baru, membuat id otomatis, lalu menyimpan seluruh daftar ke JSON.",
)
def tambah_bahan(bahan: BahanIn) -> dict:
    id_baru = max((item["id"] for item in bahan_db), default=0) + 1
    bahan_baru = {"id": id_baru, **bahan.model_dump()}
    bahan_db.append(bahan_baru)
    simpan_bahan()
    return bahan_baru


@app.patch(
    "/bahan/{bahan_id}",
    tags=["Bahan Baku"],
    response_model=BahanOut,
    summary="Ubah stok bahan",
    description="Memperbarui angka stok satu bahan berdasarkan id lalu menyimpannya ke JSON.",
)
def ubah_stok(bahan_id: int, pembaruan: StokUpdate) -> dict:
    for bahan in bahan_db:
        if bahan["id"] == bahan_id:
            bahan["stok"] = pembaruan.stok
            simpan_bahan()
            return bahan
    raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")


@app.delete(
    "/bahan/{bahan_id}",
    tags=["Bahan Baku"],
    response_model=PesanRespons,
    summary="Hapus bahan baku",
    description="Menghapus satu bahan berdasarkan id lalu menyimpan daftar terbaru ke JSON.",
)
def hapus_bahan(bahan_id: int) -> PesanRespons:
    for index, bahan in enumerate(bahan_db):
        if bahan["id"] == bahan_id:
            bahan_db.pop(index)
            simpan_bahan()
            return PesanRespons(pesan=f"{bahan['nama_bahan']} berhasil dihapus")
    raise HTTPException(status_code=404, detail="Bahan baku tidak ditemukan")
