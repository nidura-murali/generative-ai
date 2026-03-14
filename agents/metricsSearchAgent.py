import logging
from sbcaAPIs.merchantsMetrics import MetricsApiClient 
from agents.merchantSearchAgent import MerchantSearchAgent
from utils.responseBuilder import build_locationId_response
from core.settings import get_settings
from sbcaAPIs.merchantMatch import MerchantApiClient
from extractors.merchantCreditHealthExtractor import extract_merchant_credit_health
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,  
    )
logger = logging.getLogger(__name__)

settings = get_settings()
merchant_api = MerchantApiClient(settings.SBCA_HOST)
merchantSearchAgent = MerchantSearchAgent(merchant_api)

class MetricsSearchAgent:
    def __init__(self, metrics_api: MetricsApiClient):
        self.metrics_api = metrics_api

    def handle_metrics_search(self,user_input: str):
        #get merchant unique identifier
        logging.info("Handling metrics search for user input: %s", user_input)
        merchants = merchantSearchAgent.handle_merchant_search(user_input)
        locationId = build_locationId_response(merchants[0])

        #fetch metrics using locationId
        metrics = self.metrics_api.getMonthlyRSAMetrics(locationId)
        return extract_merchant_credit_health(metrics)
        

    