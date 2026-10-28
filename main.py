from typing import Optional

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Employee
from schema import EmployeeResponse, EmployeeResponseWithPagination

app = FastAPI(
    title='Pagination app',
    version='1.0'
)

Base.metadata.create_all(bind=engine)


@app.get('/employees', response_model=EmployeeResponseWithPagination)
def get_all_employees(
    page_size: int = Query(10, ge=1),
    current_page: int = Query(1, ge=1),
    department: Optional[str] = Query(None),
    designation: Optional[str] = Query(None),
    salary_lte: Optional[float] = Query(None),
    salary_gte: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)

    if department:
        query = query.filter(Employee.department == department)
    if designation:
        query = query.filter(Employee.designation == designation)
    if salary_lte is not None:
        query = query.filter(Employee.salary <= salary_lte)
    if salary_gte is not None:
        query = query.filter(Employee.salary >= salary_gte)

    total_size = query.count()
    total_pages = max(1, (total_size + page_size - 1) // page_size)

    if current_page > total_pages:
        current_page = total_pages

    employees = query.offset((current_page - 1) * page_size).limit(page_size).all()

    employee_data = [
        EmployeeResponse(
            id=employee.id,
            name=employee.name,
            department=employee.department,
            designation=employee.designation,
            salary=employee.salary,
        )
        for employee in employees
    ]

    return EmployeeResponseWithPagination(
        employees=employee_data,
        current_page=current_page,
        total_pages=total_pages,
        page_size=page_size,
        next_page=current_page + 1 if current_page < total_pages else None,
        prev_page=current_page - 1 if current_page > 1 else None,
        total_size=total_size,
    )

