from fastapi import APIRouter, HTTPException  # type: ignore

from app.schemas.analyzer import AnalyzerRequest, AnalyzerResponse
from app.services.analyzer_service import AnalyzerService


router = APIRouter(
    prefix="/repositories",
    tags=["repository-analysis"],
)

analyzer_service = AnalyzerService()


@router.post(
    "/analyze",
    response_model=AnalyzerResponse,
    summary="Analyze a cloned repository",
    description="Analyze the structure and contents of a cloned repository.",
)
async def analyze_repository(
    request: AnalyzerRequest,
) -> AnalyzerResponse:
    """
    Analyze a locally cloned repository.
    """
    try:
        result = analyzer_service.analyze_repository(
            request.repository_path
        )

        return AnalyzerResponse(**result)

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Repository analysis failed: {str(exc)}",
        ) from exc