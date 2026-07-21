import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

# -----------------------------
# App
# -----------------------------

app = FastAPI(
title="Nexus AI",
description="Modern AI Assistant API",
version="2.0.0",
)

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------

class Message(BaseModel):
role: Literal["system", "user", "assistant"]
content: str


class ChatRequest(BaseModel):
message: str
history: list[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
reply: str


# -----------------------------
# OpenAI
# -----------------------------

client = OpenAI(
api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# Prompt
# -----------------------------

SYSTEM_PROMPT = """
You are Nexus AI.

You are intelligent, friendly, and helpful.

Explain things clearly.

Teach instead of just answering.

Write clean modern code.

Be encouraging.

Never invent information.
"""

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
return {
"status": "online",
"name": "Nexus AI",
"version": "2.0"
}


@app.get("/health")
def health():
return {
"status": "healthy"
}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

try:

messages = [
{
"role": "system",
"content": SYSTEM_PROMPT,
}
]

messages.extend(
[m.model_dump() for m in req.history]
)

messages.append(
{
"role": "user",
"content": req.message,
}
)

response = client.responses.create(
model="gpt-5",
input=messages,
)

return ChatResponse(
reply=response.output_text
)

except Exception as e:
raise HTTPException(
status_code=500,
detail=str(e),
)
