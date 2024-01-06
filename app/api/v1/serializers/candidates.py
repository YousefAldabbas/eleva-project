from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from beanie import PydanticObjectId
from fastapi import Query
from pydantic import BaseModel, EmailStr, field_validator

from app.core.constants import CANDIDATE_SUPPORTED_FILTERS
from app.core.enums import Gender, Order
from app.core.utils import ResponseModel

from .base import BaseUserSerializer


class Candidates(BaseModel):
    """
    Candidates pydantic model to be used in query projection
    """

    _id: PydanticObjectId
    uuid: UUID
    first_name: str
    last_name: str
    email: str
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: Gender
    created_at: datetime
    updated_at: datetime


class RegisterCandidateSerializer(BaseUserSerializer):
    """Register Candidate Serializer"""

    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: Gender


class UpdateCandidateSerializer(BaseModel):
    """Update Candidate Serializer"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    career_level: Optional[str] = None
    job_major: Optional[str] = None
    years_of_experience: Optional[int] = None
    degree_type: Optional[str] = None
    skills: Optional[List[str]] = None
    nationality: Optional[str] = None
    city: Optional[str] = None
    salary: Optional[int] = None
    gender: Optional[Gender] = None


class CandidatesSearchSerializer(BaseModel):
    """
    Candidates search serializer
    sort: sort field it can be one of candidate fields
    """

    page: int = Query(1, ge=1)
    page_size: int = Query(10, ge=1, le=100)

    sort: Optional[str] = Query(None)
    order: Optional[Order] = Query(default=Order.ASC)
    first_name: Optional[str] = Query(None)
    last_name: Optional[str] = Query(None)
    email: Optional[EmailStr] = Query(None)
    career_level: Optional[str] = Query(None)
    job_major: Optional[str] = Query(None)
    years_of_experience: Optional[int] = Query(None)
    degree_type: Optional[str] = Query(None)
    skills: Optional[str] = Query(None)
    nationality: Optional[str] = Query(None)
    city: Optional[str] = Query(None)
    salary: Optional[int] = Query(None)
    gender: Optional[Gender] = Query(None)

    @field_validator("sort")
    @classmethod
    def validate_sort(cls, v):
        """
        Validate sort field to be one of candidate fields
        """
        if v and v not in CANDIDATE_SUPPORTED_FILTERS:
            raise ValueError("Invalid sort field")
        return v


class CandidateOut(ResponseModel):
    """Candidate Out Serializer"""

    data: Candidates


class SearchCandidatesOut(ResponseModel):
    """Search Candidates Out Serializer"""

    data: List[Candidates]


class GenerateReportOut(ResponseModel):
    """
    Generate Report Out Serializer
    """

    data: Any
