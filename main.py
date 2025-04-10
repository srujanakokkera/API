from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List


app = FastAPI()
templates = Jinja2Templates(directory="templates")

employee_list = []

class Employee(BaseModel):
    employeeId: str
    firstName: str
    lastName: str
    gender: str
    dob: str
    mobile: str
    email: str
    address: str
    joiningDate: str

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
def submit_employee(employee: Employee):
    employee_list.append(employee)
    return {"message": "Employee submitted successfully!"}

@app.get("/employees", response_model=List[Employee])
def get_employees():
    return employee_list
