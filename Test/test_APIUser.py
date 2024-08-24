import requests
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://reqres.in/api/users"

def test_api_response_structure(caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(BASE_URL)
        logger.info("Request URL: %s", response.url)
        logger.info("Response Code: %s", response.status_code)
        logger.info("Response Body: %s", response.text)

        assert response.status_code == 200

        # Validate the main structure
        json_data = response.json()
        logger.info("JSON Data: %s", json_data)
        assert "page" in json_data
        assert "per_page" in json_data
        assert "total" in json_data
        assert "total_pages" in json_data
        assert "data" in json_data
        assert "support" in json_data

        # Validate the 'data' array structure
        for user in json_data["data"]:
            assert "id" in user
            assert "email" in user
            assert "first_name" in user
            assert "last_name" in user
            assert "avatar" in user

        # Validate the 'support' section structure
        support = json_data["support"]
        assert "url" in support
        assert "text" in support

@pytest.mark.parametrize("page", [1, 2])
def test_api_pagination(page, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(BASE_URL, params={"page": page})
        logger.info("Request URL: %s", response.url)
        logger.info("Response Code: %s", response.status_code)
        logger.info("Response Body: %s", response.text)

        assert response.status_code == 200

        json_data = response.json()
        assert json_data["page"] == page

@pytest.mark.parametrize("per_page", [6, 12])
def test_api_per_page(per_page, caplog):
    with caplog.at_level(logging.INFO):
        response = requests.get(BASE_URL, params={"per_page": per_page})
        logger.info("Request URL: %s", response.url)
        logger.info("Response Code: %s", response.status_code)
        logger.info("Response Body: %s", response.text)

        assert response.status_code == 200

        json_data = response.json()
        assert len(json_data["data"]) == per_page
