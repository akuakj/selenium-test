from requests import Response
from api.client import ApiClient
from api.models.user_models import UserRequest
from utils.logger import get_logger

# вынести в один клиент
logger = get_logger(__name__)

class UserAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def send_user_request(self, payload: UserRequest) -> Response:
        url = self.client.url("/sendUserRequest")
        logger.info(f"POST {url} | payload: {payload.model_dump()}")
        response = self.client.session.post(url, json=payload.model_dump())
        logger.info(f"Response {response.status_code}")
        return response
