import unittest
import hashlib
from unittest.mock import patch, MagicMock
from fetch_feeds import extract_image, extract_content, generate_id

class TestFetchFeeds(unittest.TestCase):
    """Clase de pruebas unitarias para el script fetch_feeds.py."""

    @patch('requests.get')
    def test_extract_image_success(self, mock_get):
        """Prueba que extract_image funcione con una respuesta válida."""
        mock_response = MagicMock()
        mock_response.content = b'<meta property="og:image" content="http://example.com/image.jpg" />'
        mock_get.return_value = mock_response
        
        result = extract_image("http://example.com")
        self.assertEqual(result, "http://example.com/image.jpg")
        
    @patch('requests.get')
    def test_extract_image_no_image(self, mock_get):
        """Prueba que extract_image devuelva None si no hay imagen."""
        mock_response = MagicMock()
        mock_response.content = b'<html><body>No image here</body></html>'
        mock_get.return_value = mock_response
        
        result = extract_image("http://example.com")
        self.assertIsNone(result)

    def test_extract_content_with_content(self):
        """Prueba que extract_content priorice el campo 'content'."""
        entry = {'content': [{'value': 'Contenido completo'}]}
        result = extract_content(entry)
        self.assertEqual(result, 'Contenido completo')

    def test_extract_content_with_summary(self):
        """Prueba que extract_content use el campo 'summary' si no hay 'content'."""
        entry = {'summary': 'Un resumen breve.'}
        result = extract_content(entry)
        self.assertEqual(result, 'Un resumen breve.')

    def test_generate_id(self):
        """Prueba que generate_id sea determinista y único."""
        link1 = "http://example.com/post1"
        link2 = "http://example.com/post2"
        self.assertEqual(generate_id(link1), hashlib.md5(link1.encode('utf-8')).hexdigest())
        self.assertNotEqual(generate_id(link1), generate_id(link2))

if __name__ == '__main__':
    unittest.main()