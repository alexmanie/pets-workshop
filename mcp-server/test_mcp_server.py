import unittest
from unittest.mock import patch, MagicMock
import json
from mcp_server import list_dogs, get_dog, search_dogs
from models.dog import AdoptionStatus


class TestMCPServer(unittest.TestCase):

    def _create_mock_dog(self, dog_id, name, breed):
        dog = MagicMock()
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        return dog

    def _create_mock_detailed_dog(self, dog_id, name, breed, age=3, description="A friendly dog", gender="Male", status=AdoptionStatus.AVAILABLE):
        dog = MagicMock()
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.age = age
        dog.description = description
        dog.gender = gender
        dog.status = status
        return dog

    @patch('mcp_server.get_session')
    def test_list_dogs_success(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        dog1 = self._create_mock_dog(1, "Buddy", "Labrador")
        dog2 = self._create_mock_dog(2, "Max", "German Shepherd")

        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.all.return_value = [dog1, dog2]

        result = json.loads(list_dogs())

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], "Buddy")
        self.assertEqual(result[0]['breed'], "Labrador")
        self.assertEqual(result[1]['id'], 2)
        self.assertEqual(result[1]['name'], "Max")
        self.assertEqual(result[1]['breed'], "German Shepherd")
        session.close.assert_called_once()

    @patch('mcp_server.get_session')
    def test_list_dogs_empty(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.all.return_value = []

        result = json.loads(list_dogs())
        self.assertEqual(result, [])
        session.close.assert_called_once()

    @patch('mcp_server.get_session')
    def test_list_dogs_structure(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.all.return_value = [dog]

        result = json.loads(list_dogs())
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result[0].keys()), {'id', 'name', 'breed'})

    @patch('mcp_server.get_session')
    def test_get_dog_success(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        dog = self._create_mock_detailed_dog(1, "Buddy", "Labrador")
        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.filter.return_value = query
        query.first.return_value = dog

        result = json.loads(get_dog(1))

        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], "Buddy")
        self.assertEqual(result['breed'], "Labrador")
        self.assertEqual(result['age'], 3)
        self.assertEqual(result['gender'], "Male")
        self.assertEqual(result['status'], "AVAILABLE")
        session.close.assert_called_once()

    @patch('mcp_server.get_session')
    def test_get_dog_not_found(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.filter.return_value = query
        query.first.return_value = None

        result = json.loads(get_dog(9999))
        self.assertIn('error', result)
        self.assertEqual(result['error'], "Dog not found")
        session.close.assert_called_once()

    @patch('mcp_server.get_session')
    def test_search_dogs_by_name(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.filter.return_value = query
        query.all.return_value = [dog]

        result = json.loads(search_dogs("Buddy"))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Buddy")
        session.close.assert_called_once()

    @patch('mcp_server.get_session')
    def test_search_dogs_no_results(self, mock_get_session):
        session = MagicMock()
        mock_get_session.return_value = session

        query = MagicMock()
        session.query.return_value = query
        query.join.return_value = query
        query.filter.return_value = query
        query.all.return_value = []

        result = json.loads(search_dogs("nonexistent"))
        self.assertEqual(result, [])
        session.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
