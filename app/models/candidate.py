from pydantic import Field

from app.core.enums import Gender
from .common import Person


class Candidate(Person):
    career_level: str = Field(max_length=255)
    job_major: str = Field(max_length=255)
    years_of_experience: int = Field(default=0)
    degree_type: str = Field(max_length=255)
    skills: list = Field(default=[])
    nationality: str = Field(max_length=255)
    city: str = Field(max_length=255)
    salary: int = Field(default=0)
    gender: Gender

    class Settings:
        collection = "candidates"

    class Config:
        json_schema_extra = {
            "example": {
                "uuid": "5f2f7b9f-0c5e-4d9e-9f2d-5b2f7b9f0c5e",
                "first_name": "Yousef",
                "last_name": "Aldabbas",
                "email": "yousefaldabbas0@dummy.com",
                "career_level": "Senior",
                "job_major": "Software Engineer",
                "years_of_experience": 3,
                "degree_type": "Bachelor",
                "skills": ["Python", "FastAPI"],
                "nationality": "Jordanian",
                "city": "Amman",
                "salary": 1111,
                "gender": "Male",
            }
        }
