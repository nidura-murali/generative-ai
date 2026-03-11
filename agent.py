from extractor import extract_entities
from merchant_api import MerchantApiClient
from metrics_api import MetricsApiClient
from response_builder import build_success_response, build_not_found_response
import logging


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,  
    )
logger = logging.getLogger(__name__)

class MerchantSearchAgent:
    def __init__(self, merchant_api: MerchantApiClient, metrics_api:MetricsApiClient):
        self.merchant_api = merchant_api
        self.metrics_api = metrics_api

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
        try:
            payload = build_success_response(merchants[0])  
        except ValueError as e:
            logger.error("Response is not valid JSON. Body: %s", build_success_response(merchants[0]).text[:500])
            raise

        location_id = (
            payload.get("response", {}).get("locationId") or payload.get("locationId")
        )

        if not location_id:
            logger.warning("locationId missing in response JSON. Body: %s", str(payload)[:500])
            raise ValueError("locationId missing in response JSON")

        logger.info("locationId = %s", location_id)
        metricsResponse = self.metrics_api.getMonthlyRSAMetrics(location_id)
        logger.info("Metrics API Response: %s", metricsResponse)
        return build_success_response(merchants[0])