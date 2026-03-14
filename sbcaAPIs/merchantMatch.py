import requests
import logging

# Configure logging once for this module (INFO and above)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,  # ensure config applies under uvicorn --reload
    )
logger = logging.getLogger(__name__)
class MerchantApiClient:
    
    
    def __init__(self, base_url: str):
        self.base_url = base_url

    def searchMerchant(self, country_code: str, id_type: str, id_value: str):
        response = requests.get(
            f"{self.base_url}/locations/matches",
            params={
                "country_code": country_code,
                "id_type": id_type,
                "id_value": id_value
            },
            timeout=5
        )
        logger.info("Mercahnt API Response: %s", response)
        if response.status_code == 404:
            logger.error("Merchant not found for country_code=%s, id_type=%s, id_value=%s", country_code, id_type, id_value)
            return None
        if response.status_code == 500:
            logger.error("Server error while calling SBCA Mathing API")
            return None
        response.raise_for_status()
        return response.json()