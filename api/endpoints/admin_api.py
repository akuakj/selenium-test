from requests import Response
from api.client import ApiClient
from api.models.admin_models import AdminRequest, ProcessRequest
from utils.logger import get_logger

logger = get_logger(__name__)


class AdminAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def send_admin_request(self, payload: AdminRequest) -> Response:
        path = "/sendAdminRequest"
        logger.info(f"POST {self.client.safe_url(path)} | payload: {payload.model_dump()}")
        response = self.client.session.post(self.client.url(path), json=payload.model_dump())
        logger.info(f"Response {response.status_code}")
        return response

    def request_process(self, payload: ProcessRequest) -> Response:
        path = "/requestProcess"
        logger.info(f"POST {self.client.safe_url(path)} | payload: {payload.model_dump()}")
        response = self.client.session.post(self.client.url(path), json=payload.model_dump())
        logger.info(f"Response {response.status_code}")
        return response