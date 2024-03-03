from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sila_app import models
from sila_app import validate_data
from config.database import engine, get_db
import csv
from io import StringIO
import json
api_router = APIRouter()
models.Base.metadata.create_all(bind=engine)


@api_router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    csv_data = StringIO(contents.decode("utf-8"))
    csv_reader = csv.DictReader(csv_data)
    try:
        for row in csv_reader:
            student_data = json.loads(row["student"])
            subject_data = json.loads(row["subject"])
            teacher_data = json.loads(row["teacher"])
            department_data = json.loads(row["\ufeffdepartment"])

            if department_data:
                validate_data.create_department(db=db, department_data=department_data)
            if student_data:
                student_id = validate_data.create_student(db=db, student_data=student_data)
            if teacher_data:
                validate_data.create_teacher(db=db, teacher_data=teacher_data)
            if subject_data:
                subject_id = validate_data.create_subject(db=db, subject_data=subject_data)
            if subject_data and student_data:
                student_subject_data = {"student_id": student_id.id, "subject_id": subject_id.id}
                validate_data.create_subject_student(db=db, subject_student_data=student_subject_data)
    except Exception as e:
        return {"message": f"{e}"}
    return {"message": "CSV data inserted successfully"}

@api_router.post("/student/data", status_code=status.HTTP_201_CREATED)
def insert_data_payload(data: dict, db: Session = Depends(get_db)):
    try:
        student_data = data.get("student")
        subject_data = data.get("subject")
        teacher_data = data.get("teacher")
        department_data = data.get("department")
        if department_data:
            validate_data.create_department(db=db, department_data=department_data)
        if student_data:
            student_id = validate_data.create_student(db=db, student_data=student_data)
        if teacher_data:
            validate_data.create_teacher(db=db, teacher_data=teacher_data)
        if subject_data:
            subject_id = validate_data.create_subject(db=db, subject_data=subject_data)
        if subject_data and student_data:
            student_subject_data = {"student_id": student_id.id, "subject_id": subject_id.id}
            validate_data.create_subject_student(db=db, subject_student_data=student_subject_data)

        return {"message": "Data inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/student/data", status_code=status.HTTP_201_CREATED)
def get_students_data(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    print(students)
    return students


@api_router.put("/students/{student_id}", status_code=status.HTTP_201_CREATED)
def update_student(student_id: int, update_data: validate_data.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student = validate_data.update_student(db, student, update_data)
    return updated_student


@api_router.delete("/students/{student_id}", status_code=status.HTTP_201_CREATED)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return student
