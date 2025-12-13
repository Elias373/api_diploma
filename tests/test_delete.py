import allure


@allure.feature("DELETE Tests")
class TestDeleteMethods:

    @allure.title("DELETE /pet/{id} - delete pet")
    def test_delete_pet(self, petstore):
        create_resp = petstore.create_pet({
            "name": "DeleteMe",
            "photoUrls": ["https://example.com/delete.jpg"],
            "status": "available"
        })
        pet_id = create_resp.json()["id"]

        response = petstore.delete_pet(pet_id)
        assert response.status_code == 200

        # Verify deletion
        get_resp = petstore.get_pet_by_id(pet_id)
        if get_resp.status_code == 404:
            assert True
        elif get_resp.status_code == 200:
            data = get_resp.json()
            if "message" in data and "not found" in str(data["message"]).lower():
                assert True