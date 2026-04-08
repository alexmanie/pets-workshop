import unittest
from unittest.mock import patch, MagicMock
import json
from app import app  # Changed from relative import to absolute import

# filepath: server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    def _create_mock_dog(self, dog_id, name, breed, color=None):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed', 'color'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.color = color
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed, 'color': color}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_success(self, mock_query):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        dog1 = self._create_mock_dog(1, "Buddy", "Labrador")
        dog2 = self._create_mock_dog(2, "Max", "German Shepherd")
        mock_dogs = [dog1, dog2]
        
        self._setup_query_mock(mock_query, mock_dogs)
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        # Verify first dog
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['name'], "Buddy")
        self.assertEqual(data[0]['breed'], "Labrador")
        
        # Verify second dog
        self.assertEqual(data[1]['id'], 2)
        self.assertEqual(data[1]['name'], "Max")
        self.assertEqual(data[1]['breed'], "German Shepherd")
        
        # Verify query was called
        mock_query.assert_called_once()
        
    @patch('app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        # Arrange
        self._setup_query_mock(mock_query, [])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
        
    @patch('app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        # Arrange
        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        self._setup_query_mock(mock_query, [dog])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {'id', 'name', 'breed'})


    def _setup_color_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock for color filtering"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.filter.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_by_color_success(self, mock_query):
        """Test successful retrieval of dogs filtered by color"""
        # Arrange
        dog1 = self._create_mock_dog(1, "Buddy", "Labrador", "Golden")
        dog2 = self._create_mock_dog(3, "Luna", "Poodle", "Golden")
        mock_dogs = [dog1, dog2]

        self._setup_color_query_mock(mock_query, mock_dogs)

        # Act
        response = self.app.get('/api/dogs/color/Golden')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['color'], "Golden")
        self.assertEqual(data[1]['color'], "Golden")

    @patch('app.db.session.query')
    def test_get_dogs_by_color_empty(self, mock_query):
        """Test retrieval by color when no matching dogs exist"""
        # Arrange
        self._setup_color_query_mock(mock_query, [])

        # Act
        response = self.app.get('/api/dogs/color/Purple')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    @patch('app.db.session.query')
    def test_get_dogs_by_color_structure(self, mock_query):
        """Test the response structure for dogs filtered by color"""
        # Arrange
        dog = self._create_mock_dog(1, "Max", "Beagle", "Brown")
        self._setup_color_query_mock(mock_query, [dog])

        # Act
        response = self.app.get('/api/dogs/color/Brown')

        # Assert
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {'id', 'name', 'breed', 'color'})

    @patch('app.db.session.query')
    def test_get_dogs_by_color_case_insensitive(self, mock_query):
        """Test that color filtering is case-insensitive"""
        # Arrange
        dog = self._create_mock_dog(1, "Rex", "Husky", "Black")
        self._setup_color_query_mock(mock_query, [dog])

        # Act
        response = self.app.get('/api/dogs/color/black')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)


if __name__ == '__main__':
    unittest.main()