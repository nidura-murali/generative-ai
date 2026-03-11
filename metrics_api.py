import requests
import logging

# Configure logging once for this module (INFO and above)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,  # ensure config applies under uvicorn --reload
    )
logger = logging.getLogger(__name__)
class MetricsApiClient:
    
    def __init__(self, base_url="http://localhost:8081", timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def getMonthlyRSAMetrics(self, locationId: str):
        url = f"{self.base_url}/locations/metrics/{locationId}"
        resp = requests.get(
            url,
            params={"metrics_frequency": "MONTHLY", "has_consent": "true"},
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()
