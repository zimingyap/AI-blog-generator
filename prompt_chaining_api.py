"""
FastAPI implementation of the Prompt Chaining blog generator
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
from sse_starlette.sse import EventSourceResponse
import json
from prompt_chaining import PromptChaining
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the PromptChaining class
blog_generator = PromptChaining(os.getenv("OPEN_AI_API_KEY"))

@app.get("/generate-blog/stream")
async def generate_blog(request: Request, domain: str, target_audience: str):
    async def event_generator():
        try:
            # Step 1: Generate topics
            topics = blog_generator.generate_blog_topics(domain, target_audience)
            event_data = {'event': 'topics', 'data': {'topics': topics}}
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(0.1)

            if await request.is_disconnected():
                return

            # Step 2: Create outline
            chosen_topic = topics[0]
            outline = blog_generator.create_outline(chosen_topic)
            event_data = {'event': 'outline', 'data': {'outline': outline, 'topic': chosen_topic}}
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(0.1)

            if await request.is_disconnected():
                return

            # Step 3: Generate content
            content = blog_generator.write_content(outline)
            event_data = {'event': 'initial_content', 'data': {'content': content}}
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(0.1)

            if await request.is_disconnected():
                return

            # Step 4: Polish content
            final_content = blog_generator.edit_and_polish(content)
            event_data = {'event': 'final_content', 'data': {'content': final_content}}
            yield f"data: {json.dumps(event_data)}\n\n"

        except Exception as e:
            print(f"Error in generation: {str(e)}")
            error_data = {'event': 'error', 'data': {'error': str(e)}}
            yield f"data: {json.dumps(error_data)}\n\n"

    return EventSourceResponse(event_generator()) 