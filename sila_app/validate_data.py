from sqlalchemy.orm import Session
from sila_app import models
from pydantic import BaseModel
from fastapi import HTTPException


class DepartmentCreate(BaseModel):
    name: str


class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    department_id: int
    teacher_email: str
    teacher_phone: int
    teacher_address: str


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    department_id: int
    student_email: str
    student_phone: int
    student_address: str


class StudentUpdate(BaseModel):
    department_id: int
    student_email: str
    student_phone: int
    student_address: str


class SubjectCreate(BaseModel):
    name: str
    department_id: int


class StudentSubjectCreate(BaseModel):
    student_id: int
    subject_id: int


def create_student(db: Session, student_data: StudentCreate):
    student_data_dict = student_data
    existing_student = db.query(models.Student).filter(
        models.Student.student_email == student_data_dict["student_email"]).first()
    if existing_student:
        raise HTTPException(status_code=400,
                            detail=f"A student with the email '{student_data_dict['email']}' already exists.")
    db_student = models.Student(**student_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_subject(db: Session, subject_data: SubjectCreate):
    existing_student = db.query(models.Subject).filter(
        models.Subject.name == subject_data["name"],
        models.Subject.department_id == subject_data["department_id"]).first()
    if existing_student:
        raise HTTPException(status_code=400,
                            detail=f"A student with the email '{subject_data['name']}' already exists.")
    db_student = models.Subject(**subject_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_subject_student(db: Session, subject_student_data: SubjectCreate):
    existing_student = db.query(models.StudentsSubject).filter(
        models.StudentsSubject.student_id == subject_student_data["student_id"],
        models.StudentsSubject.subject_id == subject_student_data["subject_id"]).first()
    if existing_student:
        raise HTTPException(status_code=400,
                            detail=f"A student with the email '{subject_student_data['name']}' already exists.")
    db_student = models.StudentsSubject(**subject_student_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_department(db: Session, department_data: DepartmentCreate):
    existing_student = db.query(models.Department).filter(
        models.Department.name == department_data["name"]).first()
    if existing_student:
        raise HTTPException(status_code=400,
                            detail=f"A student with the email '{department_data['name']}' already exists.")
    db_department = models.Department(**department_data)
    print(db_department)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def create_teacher(db: Session, teacher_data: TeacherCreate):
    existing_student = db.query(models.Teacher).filter(
        models.Teacher.teacher_email == teacher_data["teacher_email"]).first()
    if existing_student:
        raise HTTPException(status_code=400,
                            detail=f"A student with the email '{teacher_data['teacher_email']}' already exists.")
    db_teacher = models.Teacher(**teacher_data)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def update_student(db: Session, student: models.Student, update_data: StudentUpdate):
    for field, value in update_data.dict().items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student
