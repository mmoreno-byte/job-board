from fastapi import APIRouter, HTTPException
from models.schemas import Job, JobSearchResponse, FilterOptions, JobSearchRequest
from services import jooble

router = APIRouter(prefix="/jobs", tags=["jobs"])

MOCK_JOBS = [
    {
        "id": "1",
        "title": "Python Developer",
        "company": "TechCorp",
        "location": "Madrid",
        "job_type": "remote",
        "description": "Buscamos desarrollador Python con experiencia en FastAPI y bases de datos.",
        "salary": "35.000€ - 45.000€",
        "posted_date": "2026-03-25",
        "source": "Jooble",
        "url": "https://example.com/job/1"
    },
    {
        "id": "2",
        "title": "Frontend React",
        "company": "Web Solutions",
        "location": "Barcelona",
        "job_type": "hybrid",
        "description": "Empresa busca desarrollador React con TypeScript.",
        "salary": "30.000€ - 40.000€",
        "posted_date": "2026-03-24",
        "source": "Jooble",
        "url": "https://example.com/job/2"
    },
    {
        "id": "3",
        "title": "Full Stack JavaScript",
        "company": "DevStudio",
        "location": "Valencia",
        "job_type": "on-site",
        "description": "Desarrollador Full Stack con Node.js y React.",
        "salary": "28.000€ - 38.000€",
        "posted_date": "2026-03-23",
        "source": "Jooble",
        "url": "https://example.com/job/3"
    },
    {
        "id": "4",
        "title": "Data Analyst",
        "company": "Data Insights",
        "location": "Madrid",
        "job_type": "remote",
        "description": "Analista de datos con Python, SQL y experiencia en Power BI.",
        "salary": "32.000€ - 42.000€",
        "posted_date": "2026-03-26",
        "source": "Jooble",
        "url": "https://example.com/job/4"
    },
    {
        "id": "5",
        "title": "Backend Java",
        "company": "Enterprise SA",
        "location": "Barcelona",
        "job_type": "hybrid",
        "description": "Desarrollador Java Spring Boot con experiencia en microservicios.",
        "salary": "40.000€ - 50.000€",
        "posted_date": "2026-03-22",
        "source": "Jooble",
        "url": "https://example.com/job/5"
    },
]


@router.get("/filters/options")
def get_filter_options() -> FilterOptions:
    return FilterOptions(
        locations=["Madrid", "Barcelona", "Valencia", "Sevilla", "Remote"],
        job_types=["remote", "hybrid", "on-site"],
        technologies=["Python", "JavaScript", "React", "Node.js", "Java", "SQL", "AWS", "Docker"]
    )


@router.post("/search")
def search_jobs(request: JobSearchRequest) -> JobSearchResponse:
    """
    Busca ofertas de trabajo.
    Usa API real de Jooble si JOBBLE_API_KEY está configurada,
    si no usa datos mock.
    """
    api_key = jooble.get_api_key()

    if api_key:
        try:
            return jooble.search_jobs(request)
        except ValueError as e:
            raise HTTPException(status_code=503, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error en Jooble API: {str(e)}")

    filtered_jobs = MOCK_JOBS

    if request.keywords:
        kw = request.keywords.lower()
        filtered_jobs = [
            j for j in filtered_jobs
            if kw in j["title"].lower() or kw in j["description"].lower()
        ]

    if request.location:
        if request.location == "Remote":
            filtered_jobs = [j for j in filtered_jobs if j["job_type"] == "remote"]
        else:
            filtered_jobs = [
                j for j in filtered_jobs
                if request.location.lower() in j["location"].lower()
            ]

    if request.job_type and request.job_type != "all":
        filtered_jobs = [j for j in filtered_jobs if j["job_type"] == request.job_type]

    if request.technologies:
        for tech in request.technologies:
            tech_lower = tech.lower()
            filtered_jobs = [
                j for j in filtered_jobs
                if tech_lower in j["title"].lower() or tech_lower in j["description"].lower()
            ]

    jobs = [Job(**j) for j in filtered_jobs]

    return JobSearchResponse(
        jobs=jobs,
        total_count=len(jobs),
        page=request.page,
        pages=1
    )


@router.get("/{job_id}")
def get_job(job_id: str) -> Job:
    for job_data in MOCK_JOBS:
        if job_data["id"] == job_id:
            return Job(**job_data)
    raise HTTPException(status_code=404, detail="Job not found")
