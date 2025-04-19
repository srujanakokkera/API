from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import EmployeePersonal, EmployeeContact
from schemas import Employee
from fastapi.templating import Jinja2Templates
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@router.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(employee: Employee):
    db = next(get_db())

    if db.query(EmployeePersonal).filter_by(employeeId=employee.employeeId).first():
        raise HTTPException(status_code=400, detail="Employee ID already exists.")
    if db.query(EmployeeContact).filter_by(email=employee.email).first():
        raise HTTPException(status_code=400, detail="This email is already registered.")
    if db.query(EmployeeContact).filter_by(mobile=employee.mobile).first():
        raise HTTPException(status_code=400, detail="This mobile number is already registered.")

    personal = EmployeePersonal(
        employeeId=employee.employeeId,
        firstName=employee.firstName,
        lastName=employee.lastName,
        gender=employee.gender,
        dob=employee.dob
    )

    contact = EmployeeContact(
        id=employee.employeeId,
        mobile=employee.mobile,
        email=employee.email,
        address=employee.address,
        joiningDate=employee.joiningDate
    )

    db.add(personal)
    db.add(contact)
    db.commit()
    db.close()
    return {"status": 201, "message": "Employee submitted successfully!"}

@router.get("/employees", response_model=List[Employee])
def list_employees():
    db = next(get_db())
    results = (
        db.query(EmployeePersonal, EmployeeContact)
        .join(EmployeeContact, EmployeePersonal.employeeId == EmployeeContact.id)
        .all()
    )

    employees = []
    for personal, contact in results:
        emp = Employee(
            employeeId=personal.employeeId,
            firstName=personal.firstName,
            lastName=personal.lastName,
            gender=personal.gender,
            dob=personal.dob,
            mobile=contact.mobile,
            email=contact.email,
            address=contact.address,
            joiningDate=contact.joiningDate
        )
        employees.append(emp)

    db.close()
    return employees
