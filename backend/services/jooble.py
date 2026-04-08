import os
import httpx
from typing import Optional, List
from models.schemas import Job, JobSearchRequest, JobSearchResponse


JOBBLE_API_URL = "https://jooble.org/api"


def get_api_key() -> Optional[str]:
    """Obtiene la API key de la variable de entorno."""
    return os.getenv("JOBBLE_API_KEY")


def search_jobs(request: JobSearchRequest) -> JobSearchResponse:
    """
    Busca trabajos usando la API de Jooble.
    Documentación: https://es.jooble.org/api/about
    """
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "API key de Jooble no configurada. "
            "Regístrate gratis en https://es.jooble.org/api/ y "
            "configura la variable de entorno JOBBLE_API_KEY"
        )

    headers = {"Content-Type": "application/json"}

    payload = {
        "keywords": request.keywords or "developer informatica",
        "location": request.location,
        "page": request.page,
    }

    if request.job_type:
        type_mapping = {
            "remote": "freelnace",
            "hybrid": "fulltime",
            "on-site": "fulltime"
        }
        payload["employment"] = type_mapping.get(request.job_type, "")

    if request.technologies:
        payload["keywords"] = f"{request.keywords} {' '.join(request.technologies)}".strip()

    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            f"{JOBBLE_API_URL}/{api_key}",
            json=payload,
            headers=headers
        )

    if response.status_code != 200:
        raise httpx.HTTPStatusError(
            f"Jooble API error: {response.status_code}",
            request=response.request,
            response=response
        )

    data = response.json()
    jobs = _parse_jooble_response(data)

    total_count = data.get("totalCount", len(jobs))
    pages = max(1, (total_count // 20) + (1 if total_count % 20 else 0))

    return JobSearchResponse(
        jobs=jobs,
        total_count=total_count,
        page=request.page,
        pages=pages
    )


def _parse_jooble_response(data: dict) -> List[Job]:
    """Convierte la respuesta de Jooble al schema interno."""
    jooble_jobs = data.get("jobs", [])

    jobs = []
    for idx, job in enumerate(jooble_jobs):
        job_id = job.get("id")
        if job_id is not None:
            job_id = str(job_id)
        else:
            job_id = f"jooble-{idx}"
        jobs.append(Job(
            id=job_id,
            title=job.get("title", "Sin título"),
            company=job.get("company", "Empresa no especificada"),
            location=job.get("location", ""),
            job_type=_infer_job_type(job),
            description=job.get("snippet", job.get("description", "")),
            salary=job.get("salary", None),
            posted_date=_parse_date(job.get("updated", "")),
            source="Jooble",
            url=job.get("link", "")
        ))

    return jobs


def _infer_job_type(job: dict) -> Optional[str]:
    """Infiere el tipo de trabajo desde la respuesta de Jooble."""
    employment = job.get("employment", "").lower()
    if "freelance" in employment or "remote" in employment:
        return "remote"
    elif "part" in employment:
        return "part-time"
    return "fulltime"


def _parse_date(date_str: str) -> Optional[str]:
    """Convierte fecha de Jooble a formato simple YYYY-MM-DD."""
    if not date_str:
        return None
    if len(date_str) >= 10:
        return date_str[:10]
    return date_str
