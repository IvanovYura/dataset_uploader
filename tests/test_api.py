from tests.base import TestBase


class ApiTest(TestBase):

    def test_create_dataset(self):
        response = self.client.post(
            'api/dataset',
            json={
                'file_ids': [1, 2]
            }
        )

        self.assertEqual(response.status_code, 201)
