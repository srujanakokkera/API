from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class EmployeePersonal(Base):
    __tablename__ = "employee_personal"

    employeeId = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    gender = Column(String(10))
    dob = Column(String(20))

    contact = relationship("EmployeeContact", back_populates="personal", uselist=False)

class EmployeeContact(Base):
    __tablename__ = "employee_contact"

    id = Column(Integer, ForeignKey("employee_personal.employeeId"), primary_key=True)
    mobile = Column(String(20))
    email = Column(String(100), unique=True)
    address = Column(String(200))
    joiningDate = Column(String(20))

    personal = relationship("EmployeePersonal", back_populates="contact")
