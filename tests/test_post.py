import allure
from src.schemas import Pet, Order


@allure.feature("POST Tests")
class TestPostMethods:

    @allure.title("POST /pet - create pet")
    def test_create_pet(self, petstore):
        pet_data = {
            "name": "NewPet",
            "photoUrls": ["https://example.com/photo.jpg"],
            "status": "available"
        }

        response = petstore.create_pet(pet_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "NewPet"
        Pet.parse_obj(data)

        # Cleanup
        pet_id = data["id"]
        petstore.delete_pet(pet_id)

    @allure.title("POST /store/order - create order")
    def test_create_order(self, petstore):
        # Create pet for order
        pet_resp = petstore.create_pet({
            "name": "OrderPet",
            "photoUrls": [],
            "status": "available"
        })
        pet_id = pet_resp.json()["id"]

        try:
            order_data = {
                "petId": pet_id,
                "quantity": 1,
                "status": "placed",
                "complete": False
            }

            response = petstore.create_order(order_data)
            assert response.status_code == 200
            data = response.json()
            assert "id" in data
            assert data["petId"] == pet_id
            Order.parse_obj(data)
        finally:
            petstore.delete_pet(pet_id)