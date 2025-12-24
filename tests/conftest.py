from datetime import datetime
from typing import Dict, Generator
import pytest
from src.api.petstore_client import PetStoreClient
from src.config import APIConfig


@pytest.fixture(scope="session")
def api_config() -> APIConfig:
    return APIConfig.from_env()


@pytest.fixture(scope="session")
def petstore_client(api_config: APIConfig) -> PetStoreClient:
    return PetStoreClient(api_config)


@pytest.fixture
def unique_pet_name() -> str:
    return f"TestPet_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"


@pytest.fixture
def pet_data_template(unique_pet_name: str) -> Dict:
    return {
        "name": unique_pet_name,
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available",
    }


@pytest.fixture
def created_pet(
    petstore_client: PetStoreClient, pet_data_template: Dict
) -> Generator[Dict, None, None]:
    response = petstore_client.post("/pet", json=pet_data_template)
    assert response.status_code == 200
    response_data = response.json()
    pet_with_id = {**pet_data_template, "id": response_data["id"]}
    yield pet_with_id
    petstore_client.delete(f"/pet/{pet_with_id['id']}")


@pytest.fixture
def created_order(
    petstore_client: PetStoreClient, created_pet: Dict
) -> Generator[Dict, None, None]:
    order_data = {
        "petId": created_pet["id"],
        "quantity": 1,
        "status": "placed",
        "complete": False,
    }
    response = petstore_client.post("/store/order", json=order_data)
    assert (
        response.status_code == 200
    ), f"Failed to create order: {response.status_code}"
    response_data = response.json()
    order_with_id = {**order_data, "id": response_data["id"]}
    yield order_with_id
