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
    
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def getMonthlyRSAMetrics(self, locationId: str):
        url = f"{self.base_url}/locations/metrics/{locationId}"
        resp = requests.get(
            url,
            params={"metrics_frequency": "MONTHLY", "has_consent": "true"},
            timeout=self.timeout
        )
        if resp.status_code==404:
            logging.error("Metrics information not found")
            return None
        if resp.status_code==500:
            logging.error("Error while calling SBCA Metrics API")
            return None
        resp.raise_for_status()
        return resp.json()
