"""Tests for the API routers."""
import pytest
from app import app


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the application.

    Yields:
        flask.testing.FlaskClient: A test client for the application.
    """
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """
    Test the index page endpoint.

    Makes a GET request to the index page and asserts that the response status code is 200.

    Args:
        client: The Flask test client.

    Returns:
        None
    """
    response = client.get('/')
    assert response.status_code == 200


def test_get_random_dog_image(client):
    """
    Test to ensure that the endpoint for fetching a random
    dog image returns either a status code 200.

    Args:
        client: Flask test client.

    Returns:
        None
    """
    response = client.get('/get_random_dog_image?color=white')
    assert response.status_code == 200


def test_get_random_dog_color(client):
    """
    Test to ensure that the endpoint for fetching a random dog
    image returns either a status code 404.

    Args:
        client: Flask test client.

    Returns:
        None
    """
    response = client.get('/get_random_dog_image?color=green')
    assert response.status_code == 404


def test_upload_file(client):
    """
    Test case to check if uploading a file to the server returns a status code 405.

    Uploads a file (dog image) with associated data to the server using a POST request.
    The test verifies that the server returns a status code 405 (Method Not Allowed),
    as there is no handler for the POST request on the specified endpoint '/upload'.

    Args:
        client: A test client for making requests to the Flask application.

    Raises:
        AssertionError: If the response status code is not 405.
    """
    data = {'color': 'black', 'breed': 'labrador'}
    response = client.post('/upload', data=data,
                           content_type='multipart/form-data',
                           environ_overrides={'HTTP_CONTENT_TYPE': 'multipart/form-data'},
                           follow_redirects=True)
    assert response.status_code == 405
