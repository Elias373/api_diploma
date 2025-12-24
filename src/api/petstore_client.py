from typing import Any, Dict
import requests

from .base_client import BaseAPIClient


class PetStoreClient(BaseAPIClient):
    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        return self.get(f"/pet/{pet_id}")

    def create_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        return self.post("/pet", json=pet_data)

    def delete_pet(self, pet_id: int) -> requests.Response:
        return self.delete(f"/pet/{pet_id}")

    def create_order(self, order_data: Dict[str, Any]) -> requests.Response:
        return self.post("/store/order", json=order_data)

    def get_order_by_id(self, order_id: int) -> requests.Response:
        return self.get(f"/store/order/{order_id}")
