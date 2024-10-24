from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Bedrock client
bedrock = boto3.client(service_name='bedrock-runtime')

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Prepare the prompt for the LLM
        prompt = f"You are a VALORANT esports expert. Answer the following question: {request.message}"

        # Call Amazon Bedrock
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",  # Use the appropriate model ID
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"]
            })
        )

        # Parse the response
        response_body = json.loads(response['body'].read())
        assistant_response = response_body['completion']

        return ChatResponse(response=assistant_response.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
