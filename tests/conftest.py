from datetime import datetime
from typing import Dict, Generator

import allure
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"TestPet_{timestamp}"


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
    with allure.step("SETUP: Create pet for testing"):
        response = petstore_client.create_pet(pet_data_template)
        pet_with_id = {**pet_data_template, "id": response["id"]}
        allure.attach(
            f"Created pet: ID={response['id']}, Name='{pet_data_template['name']}'",
            name="Test pet info",
            attachment_type=allure.attachment_type.TEXT
        )

    yield pet_with_id

    with allure.step("TEARDOWN: Clean up test pet"):
        petstore_client.delete_pet(response["id"])
        allure.attach(
            f"Successfully deleted pet ID={response['id']}",
            name="Cleanup info",
            attachment_type=allure.attachment_type.TEXT
        )


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

    with allure.step("SETUP: Create order for testing"):
        response = petstore_client.create_order(order_data)
        order_with_id = {**order_data, "id": response["id"]}
        allure.attach(
            f"Created order: ID={response['id']}, PetID={created_pet['id']}",
            name="Test order info",
            attachment_type=allure.attachment_type.TEXT
        )

    yield order_with_id

    with allure.step("TEARDOWN: Clean up test order"):
        allure.attach(
            f"Note: PetStore API doesn't provide DELETE for orders. Order ID={response['id']} remains in system.",
            name="Cleanup note",
            attachment_type=allure.attachment_type.TEXT
        )
