from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.model_loader import load_model
from app.utils import split_input
import openai
import torch
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from env variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS Middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer, model = load_model()

class InputRequest(BaseModel):
    input_type: str  # 'code' or 'requirement'
    content: str
    engine: str = 'huggingface'  # or 'openai'

@app.post("/generate-testcases")
async def generate_test_cases(req: InputRequest):
    try:
        if req.engine.lower() == "openai":
            return await generate_using_openai(req.content, req.input_type)
        else:
            return generate_using_huggingface(req.content, req.input_type)
    except Exception as e:
        return {"error": str(e)}

def generate_using_huggingface(content: str, input_type: str):
    prompt = f"Generate test cases for the following {input_type}:\n{content}\nTest cases:\n"
    chunks = split_input(prompt, tokenizer)

    results = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=150)
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        results.append(generated)

    return {"test_cases": results}

async def generate_using_openai(content: str, input_type: str):
    prompt = f"Generate test cases for this {input_type}:\n{content}\nTest cases:\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return {"test_cases": [response['choices'][0]['message']['content']]}
