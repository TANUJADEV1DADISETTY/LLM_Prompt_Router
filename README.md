# LLM-Powered Prompt Router for Intent Classification

## Overview

This project implements an **LLM-powered prompt routing system** that intelligently classifies user intent and routes requests to specialized AI personas. Instead of using one large prompt for all tasks, the system first determines the user's intent and then delegates the request to a focused expert prompt.

This design improves response accuracy, efficiency, and maintainability and reflects patterns used in production AI systems.

The system follows a **two-step pipeline**:

1. **Intent Classification** – A lightweight LLM call determines the user’s intent.
2. **Prompt Routing** – Based on the detected intent, the request is routed to a specialized expert prompt to generate the final response.

All routing decisions and responses are logged for observability.

---

# System Architecture

```
User Message
      │
      ▼
Intent Classifier (LLM Call #1)
Short prompt → detect intent
      │
      ▼
JSON Output
{
 "intent": "code",
 "confidence": 0.92
}
      │
      ▼
Router
Select expert prompt
      │
      ▼
Expert LLM Call (LLM Call #2)
      │
      ▼
Final Response
      │
      ▼
route_log.jsonl
```

---

# Features

- Intent-based prompt routing
- Multiple specialized AI personas
- Structured JSON output from classifier
- Robust error handling for malformed responses
- Request logging for observability
- Containerized using Docker
- FastAPI backend for testing and integration

---

# Supported Intents

The classifier chooses one of the following intents:

| Intent  | Description                             |
| ------- | --------------------------------------- |
| code    | Programming help, debugging, algorithms |
| data    | Data analysis, statistics, SQL          |
| writing | Writing feedback and improvement        |
| career  | Career advice, resumes, interviews      |
| unclear | Ambiguous requests                      |

---

# Expert Personas

The system includes **four specialized expert prompts**:

### Code Expert

Provides production-quality code with technical explanations and error handling.

### Data Analyst

Interprets datasets using statistical reasoning and suggests visualizations.

### Writing Coach

Identifies issues in writing such as tone, clarity, and verbosity without rewriting the text.

### Career Advisor

Provides actionable career guidance and asks clarifying questions.

---

# Project Structure

```
llm-prompt-router
│
├── app
│   ├── main.py
│   ├── classifier.py
│   ├── router.py
│   ├── prompts.py
│   └── logger.py
│
├── route_log.jsonl
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# Installation

## 1 Clone Repository

```bash
git clone <repository_url>
cd llm-prompt-router
```

---

## 2 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3 Environment Variables

Create a `.env` file from the example.

```
OPENAI_API_KEY=your_api_key_here
```

**Never commit your API keys.**

---

# Running the Application

Start the server using:

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://localhost:8000
```

---

# API Usage

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

---

## Endpoint

### POST /chat

Request:

```json
{
  "message": "how do i sort a list in python?"
}
```

Response:

```json
{
  "intent": "code",
  "confidence": 0.91,
  "response": "Use the sorted() function..."
}
```

---

# Logging

Every request is stored in:

```
route_log.jsonl
```

Example log entry:

```json
{
  "intent": "code",
  "confidence": 0.92,
  "user_message": "how do i sort a list in python?",
  "final_response": "Use sorted() function..."
}
```

Each line represents a **single request in JSON format**.

---

# Error Handling

The system gracefully handles malformed LLM responses.

If the classifier returns invalid JSON, the system defaults to:

```
{
 "intent": "unclear",
 "confidence": 0.0
}
```

The router then asks the user for clarification.

---

# Testing

Test the system using the following example messages:

```
1. how do i sort a list of objects in python?
2. explain this sql query for me
3. This paragraph sounds awkward, can you help me fix it?
4. I'm preparing for a job interview, any tips?
5. what's the average of these numbers: 12, 45, 23, 67, 34
6. Help me make this better.
7. I need to write a function that takes a user id and returns their profile
8. hey
9. Can you write me a poem about clouds?
10. Rewrite this sentence to be more professional.
11. I'm not sure what to do with my career.
12. what is a pivot table
13. fxi thsi bug pls: for i in range(10) print(i)
14. How do I structure a cover letter?
15. My boss says my writing is too verbose.
```

These tests ensure the classifier and router behave correctly across different scenarios.

---

# Docker Setup

The application can be run using Docker.

## Build and Run

```bash
docker-compose up --build
```

The API will be available at:

```
http://localhost:8000
```

---

# Dockerfile

The Dockerfile containerizes the application and installs all dependencies required to run the FastAPI service.

---

# Docker Compose

Docker Compose simplifies running the container and injecting environment variables.

---

# Optional Improvements

Possible extensions for the project include:

- Confidence threshold routing
- Manual intent override (`@code`, `@data`, etc.)
- CLI interface
- Web UI
- Multi-intent detection
- Response caching

---

# Design Decisions

### Two-Step LLM Architecture

Using a classifier before generation:

- reduces cost
- improves response relevance
- allows modular prompt engineering

### JSON Output Enforcement

The classifier returns structured JSON to make routing deterministic.

### Logging

Logging every request allows:

- debugging
- monitoring intent patterns
- improving prompt accuracy

---

# Requirements Checklist

This implementation satisfies all core requirements:

- At least four expert system prompts
- classify_intent function using LLM
- route_and_respond function
- structured JSON output
- handling unclear intents
- JSON Lines logging
- Docker containerization
- README documentation
- environment variable configuration

---

# Technologies Used

- Python
- FastAPI
- OpenAI API
- Docker
- Docker Compose

---

# License

This project is provided for educational purposes.
