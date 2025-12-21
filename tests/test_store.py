import allure
from src.schemas import Order


@allure.feature("Store Resource")
class TestStoreResource:

    @allure.title("Create order with POST /store/order")
    @allure.story("Create operations")
    def test_create_order(self, petstore_client, created_pet):
        order_data = {
            "petId": created_pet["id"],
            "quantity": 1,
            "status": "placed",
            "complete": False,
        }

        with allure.step(f"Prepare order for pet ID={created_pet['id']}"):
            allure.attach(
                str(order_data),
                name="Order request data",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Send POST request to create order"):
            response = petstore_client.create_order(order_data)

        with allure.step("Verify order response structure"):
            assert "id" in response
            assert response["petId"] == created_pet["id"]
            assert response["status"] == "placed"
            assert response["quantity"] == 1

        with allure.step("Validate order response schema"):
            Order.parse_obj(response)

    @allure.title("Get order by ID with GET /store/order/{id}")
    @allure.story("Read operations")
    def test_get_order_by_id(self, petstore_client, created_pet):
        with allure.step("Create order for testing"):
            order_data = {
                "petId": created_pet["id"],
                "quantity": 1,
                "status": "placed",
                "complete": False,
            }
            create_response = petstore_client.create_order(order_data)
            order_id = create_response["id"]
            allure.attach(
                f"Created order ID={order_id} for retrieval test",
                name="Test order info",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(f"Send GET request for order ID={order_id}"):
            response = petstore_client.get_order_by_id(order_id)

        with allure.step("Verify order data in response"):
            assert response["id"] == order_id
            assert response["petId"] == created_pet["id"]
            assert response["status"] == "placed"

        with allure.step("Validate order response schema"):
            Order.parse_obj(response)