import allure
from src.schemas import Pet


@allure.feature("Pet Resource")
class TestPetResource:

    @allure.title("Create pet with POST /pet")
    @allure.story("Create operations")
    def test_create_pet(self, petstore_client, pet_data_template):
        with allure.step("Send POST request to create pet"):
            response = petstore_client.create_pet(pet_data_template)

        with allure.step("Verify response structure"):
            assert "id" in response
            assert response["name"] == pet_data_template["name"]
            assert response["status"] == pet_data_template["status"]

        with allure.step("Validate response schema"):
            Pet.parse_obj(response)

    @allure.title("Get pet by ID with GET /pet/{id}")
    @allure.story("Read operations")
    def test_get_pet_by_id(self, created_pet, petstore_client):
        pet_id = created_pet["id"]

        with allure.step(f"Send GET request for pet ID={pet_id}"):
            response = petstore_client.get_pet_by_id(pet_id)

        with allure.step("Verify pet data in response"):
            assert response["id"] == pet_id
            assert response["name"] == created_pet["name"]
            assert response["status"] == created_pet["status"]

        with allure.step("Validate response schema"):
            Pet.parse_obj(response)

    @allure.title("Delete pet with DELETE /pet/{id}")
    @allure.story("Delete operations")
    def test_delete_pet(self, petstore_client, pet_data_template):
        with allure.step("Create pet for deletion"):
            create_response = petstore_client.create_pet(pet_data_template)
            pet_id = create_response["id"]
            allure.attach(
                f"Created pet ID={pet_id} for deletion test",
                name="Test pet for deletion",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(f"Send DELETE request for pet ID={pet_id}"):
            delete_response = petstore_client.delete_pet(pet_id)

        with allure.step("Verify delete response"):
            assert delete_response["code"] == 200
            assert delete_response.get("type") == "unknown"
            assert delete_response.get("message") == str(pet_id)
            assert set(delete_response.keys()) == {"code", "type", "message"}

        with allure.step("Verify pet is actually deleted from system"):

            response = petstore_client.get(f"/pet/{pet_id}")
            assert response.status_code == 404
