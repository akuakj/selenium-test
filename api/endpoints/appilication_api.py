from requests import Response
from API.client import ApiClient
from logger import get_logger

logger = get_logger(__name__)


class ApplicationAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_all_applications(self) -> Response:
        url = self.client.url("/getApplications")
        logger.info(f"GET {url}")
        response = self.client.session.get(url)
        logger.info(f"Response {response.status_code}")
        return response

    def get_application_by_id(self, application_id: int) -> Response:
        url = self.client.url(f"/getApplStatus/{application_id}")
        logger.info(f"GET {url}")
        response = self.client.session.get(url)
        logger.info(f"Response {response.status_code}")
        return response