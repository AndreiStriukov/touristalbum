from django.test import TestCase

class AlbumTest(TestCase):
    def test_albums(self):
        response = self.client.get('/albums/')
        
        self.assertEqual(response.status_code, 200)

class PhotoTest(TestCase):
    def test_albums(self):
        response = self.client.get('/photo/').content.decode()
        
        self.assertIn('Фотографии', response)
