from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.api.v1.serializers import candidates as candidates_serializers
from app.core.exceptions.candidates import CandidateNotFound
from app.models import Candidate


async def get_candidate(candidate_uuid: str) -> Candidate:
    """
    Async function to get candidate by uuid.

    :param candidate_uuid: candidate uuid
    :return: candidate
    """
    candidate = await Candidate.find_one(Candidate.uuid == UUID(candidate_uuid))
    if not candidate:
        raise CandidateNotFound

    return candidate


UUIDCandidate = Annotated[Candidate, Depends(get_candidate)]
