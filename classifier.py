import json
import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

CLASSIFIER_PROMPT = """
You are an intent classifier.

Classify the user's message into one of these labels:
code, data, writing, career, unclear.

Return ONLY valid JSON like this:

{
 "intent": "label",
 "confidence": 0.0
}
"""


def classify_intent(message: str):

    try:
        prompt = CLASSIFIER_PROMPT + "\nUser message: " + message

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        result = response.text

        match = re.search(r"\{.*\}", result, re.DOTALL)

        if match:
            parsed = json.loads(match.group())
            return {
                "intent": parsed.get("intent", "unclear"),
                "confidence": parsed.get("confidence", 0.0)
            }

    except Exception as e:
        print("Gemini failed, using fallback classifier")

    # ---- fallback classifier ----
    text = message.lower()

    if any(word in text for word in ["python", "code", "bug", "function", "program"]):
        return {"intent": "code", "confidence": 0.8}

    if any(word in text for word in ["average", "data", "dataset", "statistics"]):
        return {"intent": "data", "confidence": 0.8}

    if any(word in text for word in ["paragraph", "writing", "sentence", "grammar"]):
        return {"intent": "writing", "confidence": 0.8}

    if any(word in text for word in ["career", "job", "interview", "resume"]):
        return {"intent": "career", "confidence": 0.8}

    return {"intent": "unclear", "confidence": 0.3}