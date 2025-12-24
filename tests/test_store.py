import allure
from src.schemas import Order


@allure.feature("Store Resource")
class TestStoreResource:

    @allure.title("Create order for pet")
    def test_create_order(self, petstore_client, created_pet):
        order_data = {
            "petId": created_pet["id"],
            "quantity": 1,
            "status": "placed",
            "complete": False,
        }

        with allure.step("Create order with prepared data"):
            allure.attach(
                str(order_data),
                name="Order data",
                attachment_type=allure.attachment_type.JSON,
            )
            response = petstore_client.post("/store/order", json=order_data)

        with allure.step("Validate order creation"):
            assert response.status_code == 200
            response_data = response.json()
            assert "id" in response_data
            assert response_data["petId"] == created_pet["id"]
            Order.parse_obj(response_data)

    @allure.title("Get order by ID")
    def test_get_order_by_id(self, petstore_client, created_pet):
        order_data = {
            "petId": created_pet["id"],
            "quantity": 1,
            "status": "placed",
            "complete": False,
        }

        with allure.step("Create test order"):
            create_response = petstore_client.post("/store/order", json=order_data)
            assert create_response.status_code == 200
            order_id = create_response.json()["id"]

        with allure.step(f"Retrieve and validate order ID {order_id}"):
            response = petstore_client.get(f"/store/order/{order_id}")
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["id"] == order_id
            Order.parse_obj(response_data)
