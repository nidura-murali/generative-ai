from extractor import extract_entities
from merchant_api import MerchantApiClient
from response_builder import build_success_response, build_not_found_response
import logging


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,  
    )
logger = logging.getLogger(__name__)

class MerchantSearchAgent:
    def __init__(self, merchant_api: MerchantApiClient):
        self.merchant_api = merchant_api

    def handle_query(self, user_input: str):
        extraction = extract_entities(user_input)

        if extraction.needsClarification:
            return extraction.clarificationQuestion

        merchants = self.merchant_api.search(
            extraction.countryCode,
            extraction.idType.value,
            extraction.idValue
        )

        logger.info("Merchant API Search Result: %s", merchants)

        if not merchants:
            logger.error("Error while Merchant API Search Result: %s", merchants)
            return build_not_found_response(
                extraction.idType.value,
                extraction.idValue,
                extraction.countryCode
            )
        logger.info("Merchant API Search Result First Merchant: %s", merchants[0])
        return build_success_response(merchants[0])