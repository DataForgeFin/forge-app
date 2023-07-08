from fastapi import APIRouter, HTTPException

from apps import models

DATABASE = []


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.post("/", status_code=201)
async def create_patient(item: models.Patient):
    if item.patient_id in [patient.patient_id for patient in DATABASE]:
        raise HTTPException(status_code=409, detail="patient_id already exists")
    DATABASE.append(item)
    return item


@router.get("/")
async def read_patient_list(skip: int = 0, limit: int = 10):
    return DATABASE[skip : skip + limit]


@router.get("/{patient_id}")
async def read_patient(patient_id: str):
    return list(filter(lambda x: x.patient_id == patient_id, DATABASE))[0]


@router.put("/")
async def update_patient(item: models.Patient):
    global DATABASE  # pylint: disable=global-statement
    if item.patient_id not in [patient.patient_id for patient in DATABASE]:
        raise HTTPException(status_code=409, detail="patient_id doesn't exist")
    DATABASE = [item if item.patient_id == i.patient_id else i for i in DATABASE]
    return item


@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    global DATABASE  # pylint: disable=global-statement
    if patient_id not in [patient.patient_id for patient in DATABASE]:
        raise HTTPException(status_code=409, detail="patient_id doesn't exist")
    DATABASE = [i for i in DATABASE if i.patient_id != patient_id]
    return {"message": f"patient {patient_id} deleted!"}
