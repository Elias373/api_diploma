import allure
from src.schemas import Pet


@allure.feature("GET Tests")
class TestGetMethods:

    @allure.title("GET /pet/findByStatus - find available pets")
    def test_find_available_pets(self, petstore):
        response = petstore.find_pets_by_status("available")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            Pet.parse_obj(data[0])

    @allure.title("GET /pet/{id} - get pet by ID")
    def test_get_pet_by_id(self, petstore):
        pet_data = {
            "name": "TestPet",
            "photoUrls": ["https://example.com/photo.jpg"],
            "status": "available"
        }
        create_resp = petstore.create_pet(pet_data)
        pet_id = create_resp.json()["id"]

        try:
            response = petstore.get_pet_by_id(pet_id)
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == pet_id
            assert data["name"] == "TestPet"
            Pet.parse_obj(data)
        finally:
            petstore.delete_pet(pet_id)