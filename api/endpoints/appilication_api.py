from requests import Response
from api.client import ApiClient
from utils.logger import get_logger

logger = get_logger(__name__)


class ApplicationAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_all_applications(self) -> Response:
        path = "/getApplications"
        logger.info(f"GET {self.client.safe_url(path)}")
        response = self.client.session.get(self.client.url(path))
        logger.info(f"Response {response.status_code}")
        return response

    def get_application_by_id(self, application_id: int) -> Response:
        path = f"/getApplStatus/{application_id}"
        logger.info(f"GET {self.client.safe_url(path)}")
        response = self.client.session.get(self.client.url(path))
        logger.info(f"Response {response.status_code}")
        return response