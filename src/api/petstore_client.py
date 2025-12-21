from typing import Any, Dict, List, Optional

from .base_client import BaseAPIClient


class PetStoreClient(BaseAPIClient):
    def find_pets_by_status(self, status: str = "available") -> List[Dict]:
        response = self.get(f"/pet/findByStatus?status={status}")
        response.raise_for_status()
        return response.json()

    def get_pet_by_id(self, pet_id: int) -> Dict:
        response = self.get(f"/pet/{pet_id}")
        response.raise_for_status()
        return response.json()

    def create_pet(self, pet_data: Dict[str, Any]) -> Dict:
        response = self.post("/pet", json=pet_data)
        response.raise_for_status()
        return response.json()

    def delete_pet(self, pet_id: int, api_key: Optional[str] = None) -> Dict:
        headers = {}
        if api_key:
            headers["api_key"] = api_key

        response = self.delete(f"/pet/{pet_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def create_order(self, order_data: Dict[str, Any]) -> Dict:
        response = self.post("/store/order", json=order_data)
        response.raise_for_status()
        return response.json()

    def get_order_by_id(self, order_id: int) -> Dict:
        response = self.get(f"/store/order/{order_id}")
        response.raise_for_status()
        return response.json()