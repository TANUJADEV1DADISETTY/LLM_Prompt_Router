from fastapi import FastAPI
from pydantic import BaseModel

from classifier import classify_intent
from router import route_and_respond
from logger import log_request

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "AI Intent Router Service Running"}


@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message

    intent_data = classify_intent(message)

    response = route_and_respond(message, intent_data)

    log_request(
        intent_data["intent"],
        intent_data["confidence"],
        message,
        response
    )

    return {
        "intent": intent_data["intent"],
        "confidence": intent_data["confidence"],
        "response": response
    }