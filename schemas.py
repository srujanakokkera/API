from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Annotated
from datetime import datetime
import re

class Employee(BaseModel):
    employeeId: Annotated[int, Field(ge=1)]
    firstName: Annotated[str, Field()]
    lastName: Annotated[str, Field()]
    gender: Annotated[str, Field()]
    dob: Annotated[str, Field()]
    mobile: Annotated[str, Field()]
    email: Annotated[str, Field()]
    address: Annotated[str, Field()]
    joiningDate: Annotated[str, Field()]

    @field_validator("firstName", "lastName")
    @classmethod
    def name_must_be_letters(cls, value):
        if not re.fullmatch(r"[A-Za-z]+", value):
            raise ValueError("Must contain only letters")
        return value

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):
        allowed = {"Male", "Female", "Other"}
        if value.capitalize() not in allowed:
            raise ValueError("Gender must be Male, Female, or Other")
        return value.capitalize()

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value):
        if not re.fullmatch(r"^[6-9]\d{9}$", value):
            raise ValueError("Mobile number must be 10 digits and start with 6-9")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value.endswith(("@gmail.com", "@yahoo.com", "@outlook.com")):
            raise ValueError("Email must be from gmail.com, yahoo.com, or outlook.com")
        return value

    @field_validator("address")
    @classmethod
    def validate_address(cls, value):
        if not re.fullmatch(r"[A-Za-z0-9\s,\.\-]+", value):
            raise ValueError("Address contains invalid characters")
        return value

    @model_validator(mode="after")
    def validate_dates(self) -> "Employee":
        try:
            dob_date = datetime.strptime(self.dob, "%m/%d/%Y")
        except ValueError:
            raise ValueError("dob must be a valid date in MM/DD/YYYY format")

        try:
            joining_date = datetime.strptime(self.joiningDate, "%m/%d/%Y")
        except ValueError:
            raise ValueError("joiningDate must be a valid date in MM/DD/YYYY format")

        if joining_date <= dob_date:
            raise ValueError("joiningDate must be after dob")

        age_at_joining = joining_date.year - dob_date.year - (
            (joining_date.month, joining_date.day) < (dob_date.month, dob_date.day)
        )

        if age_at_joining < 18:
            raise ValueError("Employee must be at least 18 years old at the time of joining")

        return self
