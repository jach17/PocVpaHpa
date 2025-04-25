import pytest
from unittest.mock import Mock, patch
from requests.exceptions import HTTPError
from app.infrastructure.http.http_client import HttpClient

@pytest.fixture
def mock_session():
    return Mock()

def test_http_client_initialization_without_session():
    with patch('requests.Session') as mock_session_class:
        client = HttpClient(api_host="http://test.com")
        mock_session_class.assert_called_once()
        assert client._session == mock_session_class.return_value

def test_http_client_initialization_with_session(mock_session):
    client = HttpClient(api_host="http://test.com", _session=mock_session)
    assert client._session == mock_session

class TestHttpClientGet:
    def test_get_success(self, mock_session):
        # Configurar mocks
        mock_response = Mock()
        mock_response.json.return_value = {"data": "success"}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response

        # Ejecutar
        client = HttpClient(api_host="http://api.com", _session=mock_session)
        result = client.get("/endpoint", {"param": "value"})

        # Verificar
        mock_session.get.assert_called_once_with(
            "http://api.com/endpoint",
            headers={"Content-Type": "application/json"},
            params={"param": "value"}
        )
        assert result == {"data": "success"}

    def test_get_http_error(self, mock_session):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Server Error")
        mock_session.get.return_value = mock_response

        client = HttpClient(api_host="http://api.com", _session=mock_session)
        
        with pytest.raises(HTTPError) as exc_info:
            client.get("/endpoint")
        
        assert "Server Error" in str(exc_info.value)

class TestHttpClientPost:
    def test_post_dict_payload(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1}
        mock_session.post.return_value = mock_response

        client = HttpClient(api_host="http://api.com", _session=mock_session)
        result = client.post("/Transactions", {"name": "John"})

        mock_session.post.assert_called_once_with(
            "http://api.com/Transactions",
            headers={"Content-Type": "application/json"},
            json={"name": "John"}
        )
        assert result == {"id": 1}

    def test_post_str_payload(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_session.post.return_value = mock_response

        client = HttpClient(api_host="http://api.com", _session=mock_session)
        result = client.post("/data", "raw string data")

        mock_session.post.assert_called_once_with(
            "http://api.com/data",
            headers={"Content-Type": "application/json"},
            data="raw string data"
        )
        assert result == {"status": "ok"}

    def test_post_error(self, mock_session):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Invalid Data")
        mock_session.post.return_value = mock_response

        client = HttpClient(api_host="http://api.com", _session=mock_session)
        
        with pytest.raises(HTTPError) as exc_info:
            client.post("/Transactions", {})
        
        assert "Invalid Data" in str(exc_info.value)

class TestHttpClientPut:
    def test_put_success(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"updated": True}
        mock_session.put.return_value = mock_response

        client = HttpClient(api_host="http://api.com", _session=mock_session)
        result = client.put("/Transactions/1", {"name": "Updated"})

        mock_session.put.assert_called_once_with(
            "http://api.com/Transactions/1",
            headers={"Content-Type": "application/json"},
            json={"name": "Updated"}
        )
        assert result == {"updated": True}

    def test_put_error(self, mock_session):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Not Found")
        mock_session.put.return_value = mock_response

        client = HttpClient(api_host="http://api.com", _session=mock_session)
        
        with pytest.raises(HTTPError) as exc_info:
            client.put("/Transactions/999", {})
        
        assert "Not Found" in str(exc_info.value)