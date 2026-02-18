import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str):
        r = requests.get(f"{self.base_url}{path}", timeout=30)
        r.raise_for_status()
        return r.json()

    def post_json(self, path: str, payload: dict):
        r = requests.post(f"{self.base_url}{path}", json=payload, timeout=180)
        r.raise_for_status()
        return r.json()

    def post_file_png(self, path: str, file):
        files = {"file": (file.name, file.getvalue(), "image/png")}
        r = requests.post(f"{self.base_url}{path}", files=files, timeout=180)
        r.raise_for_status()
        return r.json()
