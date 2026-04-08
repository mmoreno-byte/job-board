from pydantic import BaseModel
from typing import Optional, List


class JobSearchRequest(BaseModel):
    keywords: str = ""
    location: str = ""
    job_type: Optional[str] = None
    technologies: Optional[List[str]] = None
    page: int = 1


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    job_type: Optional[str] = None
    description: str
    salary: Optional[str] = None
    posted_date: Optional[str] = None
    source: str
    url: str


class JobSearchResponse(BaseModel):
    jobs: List[Job]
    total_count: int
    page: int
    pages: int


class FilterOptions(BaseModel):
    locations: List[str]
    job_types: List[str]
    technologies: List[str]
