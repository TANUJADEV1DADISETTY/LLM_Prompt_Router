import os
from dotenv import load_dotenv
from google import genai
from prompts import SYSTEM_PROMPTS

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def route_and_respond(message: str, intent_data: dict):

    intent = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)

    if confidence < 0.7 or intent == "unclear":
        return (
            "I'm not completely sure what you need help with. "
            "Are you asking about coding, data analysis, writing improvement, "
            "or career advice?"
        )

    system_prompt = SYSTEM_PROMPTS.get(intent)

    if not system_prompt:
        return "Sorry, I couldn't find the correct expert."

    prompt = system_prompt + "\nUser message: " + message

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        print("Gemini failed, using fallback response")

        # ---- fallback responses ----
        if intent == "code":
            return (
                "To sort a list of objects in Python, use the sorted() function "
                "with a key parameter.\n\nExample:\n\n"
                "users = [\n"
                " {'name': 'Alice', 'age': 30},\n"
                " {'name': 'Bob', 'age': 25}\n"
                "]\n\n"
                "sorted_users = sorted(users, key=lambda x: x['age'])\n"
                "print(sorted_users)"
            )

        if intent == "data":
            return (
                "To analyze numbers like averages, you can calculate the mean "
                "by summing the values and dividing by the count."
            )

        if intent == "writing":
            return (
                "Your writing may contain unclear phrasing or filler words. "
                "Try simplifying sentences and removing unnecessary words."
            )

        if intent == "career":
            return (
                "For career improvement, focus on building relevant skills, "
                "creating a strong resume, and practicing interview questions."
            )

        return "I'm unable to generate a response right now."