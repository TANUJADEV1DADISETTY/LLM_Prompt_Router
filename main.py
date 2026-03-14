from classifier import classify_intent
from router import route_and_respond
from logger import log_request

def check_manual_override(message: str):

    if message.startswith("@"):
        parts = message.split(" ", 1)

        intent = parts[0][1:]  # remove '@'

        if len(parts) > 1:
            message = parts[1]
        else:
            message = ""

        return intent, message

    return None, message


def main():

    message = input("Enter your message: ")

    # Check manual override
    override_intent, cleaned_message = check_manual_override(message)

    if override_intent:
        intent_data = {
            "intent": override_intent,
            "confidence": 1.0
        }
        message = cleaned_message
    else:
        intent_data = classify_intent(message)

    print("\nDetected Intent:")
    print(intent_data)

    response = route_and_respond(message, intent_data)

    print("\nAI Response:")
    print(response)

    log_request(
        intent_data["intent"],
        intent_data["confidence"],
        message,
        response
    )


if __name__ == "__main__":
    main()