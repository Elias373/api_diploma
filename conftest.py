import pytest
import requests
import logging
import json
import allure


@pytest.fixture(scope="session")
def base_url():
    return "https://petstore.swagger.io/v2"


def attach_to_allure(request_data, response_data):
    if request_data and response_data:
        allure_data = {
            "request": {
                "method": request_data.get("method"),
                "endpoint": request_data.get("endpoint")
            },
            "response": {
                "status": response_data.get("status_code"),
                "time": response_data.get("time")
            }
        }

        allure.attach(
            json.dumps(allure_data, indent=2),
            name=f"{request_data.get('method')} {request_data.get('endpoint')}",
            attachment_type=allure.attachment_type.JSON
        )


@pytest.fixture
def api_client(base_url):
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })

        def request(self, method, endpoint, **kwargs):
            full_url = f"{self.base_url}{endpoint}"

            logging.info(f"{method} {endpoint}")

            try:
                response = self.session.request(method, full_url, **kwargs)

                # ВАЖНО: Убедиться, что method передается правильно
                request_data = {
                    "method": method,  # ← Должен быть "DELETE" для DELETE запроса
                    "endpoint": endpoint
                }

                response_data = {
                    "status_code": response.status_code,
                    "time": f"{response.elapsed.total_seconds():.3f}s"
                }

                logging.info(f"Status: {response.status_code} ({response_data['time']})")

                attach_to_allure(request_data, response_data)

                return response

            except requests.RequestException as e:
                logging.error(f"Error: {str(e)}")
                raise

    return APIClient(base_url)


@pytest.fixture
def petstore(api_client):
    class PetStoreAPI:
        def __init__(self, client):
            self.client = client

        def find_pets_by_status(self, status="available"):
            return self.client.request('GET', f'/pet/findByStatus?status={status}')

        def get_pet_by_id(self, pet_id):
            return self.client.request('GET', f'/pet/{pet_id}')

        def create_pet(self, pet_data):
            return self.client.request('POST', '/pet', json=pet_data)

        def delete_pet(self, pet_id):
            return self.client.request('DELETE', f'/pet/{pet_id}')  # ← Здесь "DELETE"

        def create_order(self, order_data):
            return self.client.request('POST', '/store/order', json=order_data)

    return PetStoreAPI(api_client)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)