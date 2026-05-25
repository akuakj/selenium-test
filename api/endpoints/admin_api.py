from requests import Response
from API.client import ApiClient
from API.models.admin_models import AdminRequest, ProcessRequest
from utils.logger import get_logger

logger = get_logger(__name__)


class AdminAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def send_admin_request(self, payload: AdminRequest) -> Response:
        url = self.client.url("/sendAdminRequest")
        logger.info(f"POST {url} | payload: {payload.model_dump()}")
        response = self.client.session.post(url, json=payload.model_dump())
        logger.info(f"Response {response.status_code}")
        return response

    def request_process(self, payload: ProcessRequest) -> Response:
        url = self.client.url("/requestProcess")
        logger.info(f"POST {url} | payload: {payload.model_dump()}")
        response = self.client.session.post(url, json=payload.model_dump())
        logger.info(f"Response {response.status_code}")
        return response