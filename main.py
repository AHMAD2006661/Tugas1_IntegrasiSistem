from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="API Data Mahasiswa - Tugas 1 Integrasi Sistem",
    description="REST API CRUD data mahasiswa (nama, alamat, IPK, semester, hobi)",
    version="1.0.0",
)

# Model data (dipakai saat POST, semua field wajib diisi)
class Mahasiswa(BaseModel):
    nama: str
    alamat: str
    ipk: float = Field(..., ge=0, le=4)        # IPK 0.00 - 4.00
    semester: int = Field(..., ge=1, le=14)    # semester 1 - 14
    hobi: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nama": "Budi Alfatoni",
                    "alamat": "Jl. Cepogo No. 12, Boyolali",
                    "ipk": 3.95,
                    "semester": 5,
                    "hobi": "Bermain game",
                }
            ]
        }
    }

# Model untuk update (dipakai saat PUT, boleh isi sebagian saja)
class MahasiswaUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = Field(None, ge=0, le=4)
    semester: Optional[int] = Field(None, ge=1, le=14)
    hobi: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ipk": 3.6,
                    "semester": 6,
                }
            ]
        }
    }

# Simulasi database
mahasiswa_db = {}

# ROOT
@app.get("/")
def read_root():
    return {"Maestro": "Ramz Handsome Boy"}

# READ ALL (GET) - menampilkan semua mahasiswa
@app.get("/mahasiswa")
async def read_all_mahasiswa():
    data = [{"id": mahasiswa_id, **mahasiswa} for mahasiswa_id, mahasiswa in mahasiswa_db.items()]
    return {"total": len(data), "data": data}

# CREATE (POST)
@app.post("/mahasiswa/{mahasiswa_id}", status_code=201)
async def create_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):
    if mahasiswa_id in mahasiswa_db:
        raise HTTPException(status_code=400, detail="Mahasiswa dengan ID ini sudah ada")
    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()
    return {"message": "Mahasiswa berhasil ditambahkan", "mahasiswa": mahasiswa_db[mahasiswa_id]}

# READ (GET) - menampilkan satu mahasiswa
@app.get("/mahasiswa/{mahasiswa_id}")
async def read_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return {"mahasiswa_id": mahasiswa_id, "mahasiswa": mahasiswa_db[mahasiswa_id]}

# UPDATE (PUT)
@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(mahasiswa_id: int, mahasiswa: MahasiswaUpdate):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    # hanya field yang diisi yang akan diperbarui
    updated_data = mahasiswa.model_dump(exclude_unset=True)
    mahasiswa_db[mahasiswa_id].update(updated_data)
    return {"message": "Data mahasiswa berhasil diperbarui", "mahasiswa": mahasiswa_db[mahasiswa_id]}

# DELETE (DELETE)
@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    deleted_mahasiswa = mahasiswa_db.pop(mahasiswa_id)
    return {"message": "Mahasiswa berhasil dihapus", "mahasiswa": deleted_mahasiswa}