import allure
from src.schemas import Pet


@allure.feature("Pet Resource")
class TestPetResource:
    @allure.title("Create new pet")
    def test_create_pet(self, petstore_client, pet_data_template):
        with allure.step("Create pet with prepared data"):
            allure.attach(
                str(pet_data_template),
                name="Pet data",
                attachment_type=allure.attachment_type.JSON,
            )
            response = petstore_client.post("/pet", json=pet_data_template)

        with allure.step("Validate creation result"):
            assert response.status_code == 200
            response_data = response.json()
            assert "id" in response_data
            assert response_data["name"] == pet_data_template["name"]
            Pet.parse_obj(response_data)

    @allure.title("Get pet by ID")
    def test_get_pet_by_id(self, created_pet, petstore_client):
        pet_id = created_pet["id"]

        with allure.step(f"Retrieve and validate pet ID {pet_id}"):
            response = petstore_client.get(f"/pet/{pet_id}")
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["id"] == pet_id
            assert response_data["name"] == created_pet["name"]
            assert response_data["status"] == created_pet["status"]
            Pet.parse_obj(response_data)

    @allure.title("Delete pet from system")
    def test_delete_pet(self, petstore_client, pet_data_template):
        with allure.step("Create test pet for deletion"):
            create_response = petstore_client.post("/pet", json=pet_data_template)
            assert create_response.status_code == 200
            pet_id = create_response.json()["id"]

        with allure.step(f"Delete pet ID {pet_id} and verify"):
            delete_response = petstore_client.delete(f"/pet/{pet_id}")
            assert delete_response.status_code == 200
            delete_data = delete_response.json()
            assert delete_data["code"] == 200
            assert delete_data["type"] == "unknown"
            assert "message" in delete_data

        with allure.step(f"Verify pet {pet_id} is deleted"):
            get_response = petstore_client.get(f"/pet/{pet_id}")
            assert get_response.status_code == 404
