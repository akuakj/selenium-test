import requests
from utils.logger import get_logger

logger = get_logger(__name__)

class ApiClient:
    BASE_URL = "https://user:senlatest@regoffice.senla.eu"

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({"Content-Type": "application/json"})

    def url(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"