from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    department: str = Field(..., min_length=2, max_length=50)
    designation: str = Field(..., min_length=2, max_length=50)
    salary: NonNegativeFloat


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[NonNegativeFloat] = None


class EmployeeResponseWithPagination(BaseModel):
    employees: List[EmployeeResponse]
    current_page: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None
    total_pages: int
    page_size: int
    total_size: int


class GetEmployeeQueryParams(BaseModel):
    page_size: Optional[int] = 10
    current_page: int = 1
    department: Optional[str] = None
    designation: Optional[str] = None
    salary_lte: Optional[float] = None
    salary_gte: Optional[float] = None

