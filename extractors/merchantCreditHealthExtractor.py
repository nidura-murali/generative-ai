import logging
from llms.groqClient import GroqLLMClient

# Configure logging once for this module (INFO and above)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    force=True,  # ensure config applies under uvicorn --reload
)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = '''
You are an experienced merchant credit underwriting analyst.

You are given the past 12 months of retail sales metrics for a merchant.

Your task is to evaluate the merchant's creditworthiness based strictly on the provided data and produce a structured underwriting decision.

Input:
The input contains monthly sales metrics for the past year.

Evaluation guidelines:

Positive signals:
- consistent or growing sales
- stable revenue patterns
- low volatility month-to-month

Risk signals:
- declining sales trend
- large fluctuations or volatility
- sudden drops in revenue
- missing months of data

Based on these factors, determine the merchant’s credit health.

Extract the following fields:

- merchant_active_period (first seen month - last seen month)
- final_credit_risk_rating (LOW, MEDIUM, HIGH)
- underwriting_recommendation_decision (APPROVE, HOLD, REJECT)
- recommendation_explanation (clear reasoning)
- key_drivers (list of main positive signals)
- potential_risks (list of risks detected)
- opportunities (growth potential indicators)
- actionable_insights (practical recommendations)
- recommended_credit_limit:
  {
    "min": number,
    "max": number,
    "currency": "USD"
  }
- confidence (HIGH, MEDIUM, LOW)
- needsClarification (boolean)
- clarificationQuestion (string only if clarification is required)

Rules:
- Use only the provided data for analysis
- Do not fabricate information
- Use null if information is missing
- If the input data is incomplete or ambiguous, set needsClarification=true and provide clarificationQuestion
- Return ONLY a valid JSON object
- Do not include explanations outside the JSON
'''
def extract_merchant_credit_health(user_input: str):
    # Placeholder implementation - replace with actual logic
    logger.info("Extracting merchant credit health from user input: %s", user_input)
    # Simulate extraction logic
    grokClient = GroqLLMClient()
    merchant_credit_health = grokClient.generate(
        SYSTEM_PROMPT,
        f'Metrics input: "{user_input}"'
    )
    logger.info("Extracted merchant credit health: %s", merchant_credit_health)
    return merchant_credit_health