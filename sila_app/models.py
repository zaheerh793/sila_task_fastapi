from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.database import Base


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, unique=True)

    teachers = relationship("Teacher", back_populates="department")
    students = relationship("Student", back_populates="department")
    subjects = relationship("Subject", back_populates="department")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    teacher_email = Column(String(100), unique=True)
    teacher_phone = Column(Integer)
    teacher_address = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="teachers")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    student_email = Column(String(100), unique=True)
    student_phone = Column(Integer)
    student_address = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="subjects")


class StudentsSubject(Base):
    __tablename__ = "student_subjects"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))



