from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from database import Base


class DepartmentEnum(str, Enum):
    HR = "HR"
    IT = "IT"
    Finance = "Finance"
    Marketing = "Marketing"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(SQLAlchemyEnum(DepartmentEnum), nullable=False)
    designation = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)


