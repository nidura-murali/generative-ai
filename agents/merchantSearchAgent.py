from extractors.merchantInfoExtractor import extract_merchant_info
from sbcaAPIs.merchantMatch import MerchantApiClient
from utils.responseBuilder import build_success_response, build_not_found_response
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

    def handle_merchant_search(self, user_input: str):
        extraction = extract_merchant_info(user_input)

        if extraction.needsClarification:
            return extraction.clarificationQuestion

        merchants = self.merchant_api.searchMerchant(
            extraction.countryCode,
            extraction.idType.value,
            extraction.idValue
        )

        logger.info("Merchant API Search Result: %s", merchants)

        if not merchants:
            logger.error("Could not find merchants for the search %s", merchants)
            return build_not_found_response(
                extraction.idType.value,
                extraction.idValue,
                extraction.countryCode
            )
        logger.info("Merchant API Search Result First Merchant: %s", merchants[0])
        return merchants