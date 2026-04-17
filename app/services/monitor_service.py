import requests
import time

class MonitorService:
    def check_url(self, address):
        try:
            start = time.time()
            response = requests.get(address, timeout=5)
            end = time.time()

            response_time = int((end - start) * 1000)

            status = "UP" if 200 <= response.status_code < 300 else "DOWN"

            return status, response_time

        except requests.exceptions.RequestException:
            return "DOWN", None