import httpx


class TestOcr:
    client = httpx.Client(base_url="http://127.0.0.1:20000")

    def test_base64(self):
        data = {
            "img": 'data:image/png;base64,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',
            "length": 4
        }
        response = self.client.post("/ocr", json=data)
        response.raise_for_status()
        json_data = response.json()
        assert json_data['code'] == 'nc8c'


t = TestOcr()
t.test_base64()