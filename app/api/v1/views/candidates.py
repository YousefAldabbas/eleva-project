from typing import Any
from fastapi import APIRouter, Depends, Query, Response, status

from app.api.v1 import dependencies as deps
from app.api.v1.serializers import candidates as candidates_serializers
from app.api.v1.services import candidates as candidates_service
from app.core.constants import ResponseMessages
from app.core.utils import response_handler

router = APIRouter(dependencies=[Depends(deps.has_group("user"))])


@router.get(
    "/all-candidates",
    response_model=candidates_serializers.SearchCandidatesOut,
)
async def search_candidates(
    search: candidates_serializers.CandidatesSearchSerializer = Depends(),
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) -> dict[str, Any]:
    return response_handler(
        data=await candidates_service.get_all_candidates(search),
        status=status.HTTP_200_OK,
        message=msg,
    )


@router.get("/generate-report")
async def generate_report(page_size: int = Query(100), page: int = Query(1)) -> Response:
    # background_tasks.add_task(candidates_service.generate_report)

    return Response(
        content=await candidates_service.generate_report(page_size, page),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=candidates_report.csv"},
    )


@router.post("/", response_model=candidates_serializers.CandidateOut)
async def create_candidate(
    payload: candidates_serializers.RegisterCandidateSerializer,
    msg: str = Depends(deps.message_locale(ResponseMessages.Created)),
) -> dict[str, Any]:
    return response_handler(
        data=await candidates_service.create_candidate(payload),
        status=status.HTTP_201_CREATED,
        message=msg,
    )


@router.get("/{candidate_uuid}", response_model=candidates_serializers.CandidateOut)
async def get_candidate_by_uuid(
    candidate: deps.UUIDCandidate,
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) -> dict[str, Any]:
    return response_handler(
        data=candidates_serializers.Candidates(**candidate.model_dump()),
        status=status.HTTP_200_OK,
        message=msg,
    )


@router.patch(
    "/{candidate_uuid}",
    response_model=candidates_serializers.CandidateOut,
)
async def update_user(
    candidate: deps.UUIDCandidate,
    paylaod: candidates_serializers.UpdateCandidateSerializer,
    msg: str = Depends(deps.message_locale(ResponseMessages.Updated)),
) -> dict[str, Any]:
    return response_handler(
        data=await candidates_service.update_candidate(candidate, paylaod),
        status=status.HTTP_202_ACCEPTED,
        message=msg,
    )


@router.delete(
    "/{candidate_uuid}",
    response_model=candidates_serializers.DeleteCandidateOut,
)
async def delete_candidate(
    candidate: deps.UUIDCandidate,
    msg: str = Depends(deps.message_locale(ResponseMessages.Deleted)),
) -> dict[str, Any]:
    return response_handler(
        data=await candidates_service.delete_candidate(candidate),
        status=status.HTTP_202_ACCEPTED,
        message=msg,
    )
