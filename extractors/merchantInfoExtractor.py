import json
from utils.schemas import ExtractionResult
from llms.groqClient import GroqLLMClient
import logging


# Configure logging once for this module (INFO and above)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    force=True,  # ensure config applies under uvicorn --reload
)
logger = logging.getLogger(__name__)


SYSTEM_PROMPT = '''
You are a merchant search extraction agent. Extract below fields from the user input. Respond ONLY in JSON format with the following structure:

Extract:
- countryCode (ISO-3 like IND, USA, BRA)
- idType (MERCHANT_ID, MMH_ID, TAX_ID)
- idValue (string)
- confidence (HIGH, MEDIUM, LOW)
- needsClarification (boolean)
- clarificationQuestion (string, only if needsClarification is true)

Rules:
- Use null if missing
- If ambiguous, ask a clarification question
- Respond ONLY in valid JSON
'''

def extract_merchant_info(user_input: str) -> ExtractionResult:
    grok_llm = GroqLLMClient()
    response = grok_llm.generate(
        SYSTEM_PROMPT,
        f'User input: "{user_input}"'
    )

    try:
        logger.info("LLM Response: %s", response)
        data = json.loads(response)
        logger.info("json modified data after LLM Response: %s", response)
        return ExtractionResult(**data)
    except Exception as e:
        logger.error("Exception while processing LLM response: %s", str(e))
        return ExtractionResult(
            countryCode=None,
            idType=None,
            idValue=None,
            confidence="LOW",
            needsClarification=True,
            clarificationQuestion="Could you clarify the country and ID type?"
        )