import csv
import os
from datetime import datetime
from io import StringIO
from typing import List

import cloudinary
import cloudinary.api
import cloudinary.uploader
import pandas as pd

from app.core.constants import CANDIDATE_SUPPORTED_FILTERS as headers
from app.core.utils.custom_logger import logger
from app.models import Candidate


def generate_csv_report(candidates: List[Candidate]):
    candidate_data = [
        {field: getattr(candidate, field) for field in headers}
        for candidate in candidates
    ]
    file_name: str = f"candidates_report_{datetime.utcnow().day}.csv"
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(candidate_data)

    logger.info("Report generated successfully")
    cloudinary.config(
        cloud_name="XXXXXXXXXX",
        api_key="XXXXXXXXXXX",
        api_secret="XXXXXXXX",
        secure=True,
    )
    cloudinary.uploader.upload(file_name, folder="elev")

    logger.info("Report uploaded successfully")
    os.remove(file_name)

    logger.info("Report deleted successfully")


def sync_generate_csv_report(candidates):
    """
    Generate CSV report from candidates data
    """

    logger.info("Generating CSV report")
    df = pd.DataFrame(candidates)
    csv_data = StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    logger.info("CSV report generated successfully")
    return csv_data.getvalue()
