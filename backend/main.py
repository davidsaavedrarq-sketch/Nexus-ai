import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

# --------------------------------------------------
# FastAPI Setup
# --------------------------------------------------

app = FastAPI(
title="Nexus AI",
description="Intelligent AI Assistant API",
version="1.0.0"
)

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Change this to your domain when deploying
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------

class Message(BaseModel):
role: Literal["system", "user", "assistant"]
content: str


class ChatRequest(BaseModel):
message: str
history: list[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
reply: str


# --------------------------------------------------
# OpenAI Setup
# --------------------------------------------------

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
print("⚠️ OPENAI_API_KEY not found. Running in demo mode.")

client = OpenAI(api_key=api_key) if api_key else None

# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are Nexus AI.

Your personality:

• Intelligent without sounding arrogant.
• Friendly, calm, and confident.
• Explain difficult concepts simply.
• Encourage curiosity and learning.
• Never make users feel stupid for asking questions.
• Admit when you're uncertain instead of guessing.
• Keep responses clear and organized.
• Be creative when appropriate.
• Think like an experienced software engineer and teacher.

When helping with programming:
- Write clean, modern code.
- Explain WHY something works.
- Point out mistakes politely.
- Suggest improvements.
- Follow best practices.

When chatting casually:
- Be conversational.
- Show a little humor when it fits.
- Never be rude or sarcastic.

Your mission is to help people build, learn, create, and solve problems.
"""

# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/")
def root():
return {
"status": "online",
"service": "Nexus AI",
"version": "1.0.0"
}


@app.get("/health")
def health():
return {
"status": "healthy"
}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

try:

if not client:
return ChatResponse(
reply=(
f"You said:\n\n"
f"'{req.message}'\n\n"
"⚠️ Nexus AI is running in demo mode.\n"
"Add your OPENAI_API_KEY to enable real AI responses."
)
)

messages = [
{
"role": "system",
"content": SYSTEM_PROMPT
}
]

messages.extend(
[message.model_dump() for message in req.history]
)

messages.append(
{
"role": "user",
"content": req.message
}
)

response = client.chat.completions.create(
model="gpt-5",
messages=messages,
temperature=0.7,
max_tokens=1000,
)

reply = response.choices[0].message.content

return ChatResponse(reply=reply)

except Exception as e:
raise HTTPException(
status_code=500,
detail=f"Nexus AI Error: {str(e)}"
)
