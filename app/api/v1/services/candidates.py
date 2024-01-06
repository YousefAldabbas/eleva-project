import re
import uuid
from datetime import datetime

from app.api.v1.serializers import candidates as candidates_serializers
from app.core.constants import CANDIDATE_SUPPORTED_FILTERS
from app.core.exceptions import CandidateEmailAlreadyExists, CandidateNotFound
from app.core.helpers import hash_helper
from app.core.utils import logger
from app.core.utils.generate_csv import sync_generate_csv_report
from app.models import Candidate


async def generate_report(page_size: int, page: int):
    """Generate report for candidates"""
    candidates = (
        await Candidate.find_many(projection_model=candidates_serializers.Candidates)
        .skip((page - 1) * page_size)
        .limit(page_size)
        .to_list()
    )
    logger.info(f"Generating CSV report for {len(candidates)} candidates")
    return sync_generate_csv_report(candidates)


async def get_all_candidates(search: candidates_serializers.CandidatesSearchSerializer):
    """
    Async function to get all candidates base on the provided search criteria.

    :param search: CandidatesSearchSerializer
    :return: list of candidates
    """

    data = search.model_dump(exclude_none=True)
    # Filter out unsupported filters
    query = {k: v for k, v in data.items() if k in CANDIDATE_SUPPORTED_FILTERS}

    # Pagination
    skip = (data["page"] - 1) * data["page_size"]
    limit = data["page_size"]

    sort_field = data.get("sort")
    order = data.get("order")

    if sort_field:
        sort_criteria = [(sort_field, 1 if order == "asc" else -1)]
    else:
        # Default sort criteria
        sort_criteria = [("created_at", -1)]
    # Regex search for first_name and last_name
    # it will be case insensitive and will match any string that contains the provided value
    for key, value in query.items():
        if key in {"first_name", "last_name"}:
            query[key] = (
                {"$regex": re.escape(value), "$options": "i"} if value else None
            )
        else:
            query[key] = value

    return (
        await Candidate.find(query, projection_model=candidates_serializers.Candidates)
        .sort(sort_criteria)
        .skip(skip)
        .limit(limit)
        .to_list()
    )


async def get_candidate(candidate_uuid: str) -> Candidate:
    """
    Async function to get candidate by uuid.

    :param candidate_uuid: candidate uuid
    :return: candidate
    """
    candidate = await Candidate.find_one(Candidate.uuid == candidate_uuid)
    if not candidate:
        raise CandidateNotFound

    return candidates_serializers.Candidates(**candidate.model_dump())


async def create_candidate(
    payload: candidates_serializers.RegisterCandidateSerializer,
) -> Candidate:
    """
    Async function to create candidate.

    :param payload: RegisterCandidateSerializer
    :return: candidate
    """
    data = payload.model_dump()

    if await Candidate.find_one(Candidate.email == payload.email):
        raise CandidateEmailAlreadyExists

    data["password"] = hash_helper.get_password_hash(data["password"])
    candidate = await Candidate(**data).insert()

    return candidates_serializers.Candidates(**candidate.model_dump())


async def update_candidate(
    candidate: Candidate, payload: candidates_serializers.UpdateCandidateSerializer
) -> Candidate:
    """
    Async function to update candidate.

    :param candidate: Candidate
    :param payload: UpdateCandidateSerializer
    :return: candidate
    """
    data = payload.model_dump(exclude_none=True)
    if data.get("password"):
        data["password"] = hash_helper.get_password_hash(data["password"])
    data["updated_at"] = datetime.utcnow()
    candidate = await candidate.update({"$set": data})

    return candidates_serializers.Candidates(**candidate.model_dump())


async def delete_candidate(candidate_uuid: str):
    """
    Async function to delete candidate.
    """

    candidate = await Candidate.find_one(Candidate.uuid == uuid.UUID(candidate_uuid))
    if not candidate:
        raise CandidateNotFound
    await candidate.delete()
