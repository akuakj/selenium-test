from requests import Response
from api.client import ApiClient
from api.models.user_models import UserRequest
from utils.logger import get_logger

logger = get_logger(__name__)

class UserAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def send_user_request(self, payload: UserRequest) -> Response:
        path = "/sendUserRequest"
        logger.info(f"POST {self.client.safe_url(path)} | payload: {payload.model_dump()}")
        response = self.client.session.post(self.client.url(path), json=payload.model_dump())
        logger.info(f"Response {response.status_code}")
        return response
