from fastapi import APIRouter, Depends, Query, Response, status

from app.api.v1.dependancies.validate_authorization import (
    AuthorizedCandidate,
    has_group,
)
from app.api.v1.serializers import candidates as candidates_serializers
from app.api.v1.services import candidates as candidates_service
from app.core.utils import response_handler

router = APIRouter()


@router.get("/me", response_model=candidates_serializers.CandidateOut)
async def get_current_candidate(candidate: AuthorizedCandidate):
    """
    API endpoint to get current candidate information.
    """

    return response_handler(data=candidate, status=status.HTTP_200_OK)


@router.post("", response_model=candidates_serializers.CandidateOut)
async def create_candidate(payload: candidates_serializers.RegisterCandidateSerializer):
    """
    API endpoint to create new candidate.
    """

    return response_handler(
        data=await candidates_service.create_candidate(payload),
        status=status.HTTP_201_CREATED,
    )


@router.patch("", response_model=candidates_serializers.CandidateOut)
async def update_user(
    candidate: AuthorizedCandidate,
    paylaod: candidates_serializers.UpdateCandidateSerializer,
):
    """
    API endpoint to update candidate information.
    """

    return response_handler(
        data=await candidates_service.update_candidate(candidate, paylaod),
        status=status.HTTP_202_ACCEPTED,
    )


@router.delete(
    "/{candidate_uuid}",
    # response_model=candidates_serializers.CandidateOut,
    dependencies=[Depends(has_group("user"))],
)
async def delete_candidate(candidate_uuid: str):
    """
    API endpoint to delete candidate.
    """

    return response_handler(
        data=await candidates_service.delete_candidate(candidate_uuid),
        status=status.HTTP_202_ACCEPTED,
    )


@router.get(
    "/all-candidates",
    response_model=candidates_serializers.SearchCandidatesOut,
    dependencies=[Depends(has_group("user"))],
)
async def search_candidates(
    search: candidates_serializers.CandidatesSearchSerializer = Depends(),
):
    """
    API endpoint to get all candidates based on the provided search criteria.
    """
    return response_handler(
        data=await candidates_service.get_all_candidates(search),
        status=status.HTTP_200_OK,
    )


@router.get(
    "/generate-report",
    response_model=candidates_serializers.GenerateReportOut,
    dependencies=[Depends(has_group("user"))],
)
async def generate_report(
    response: Response, page_size: int = Query(100), page: int = Query(1)
):
    """
    API endpoint to generate candidates report.
    """
    # background_tasks.add_task(candidates_service.generate_report)
    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=candidates_report.csv"
    response.headers["Content-Type"] = "text/csv"

    return response_handler(
        data=await candidates_service.generate_report(page_size, page),
        status=status.HTTP_200_OK,
    )
