import asyncio
import websockets
import json
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # 或者直接写在这里

MCP_SERVER_URL = "ws://localhost:8000"

async def fetch_openai_reply(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

async def run_client():
    async with websockets.connect(MCP_SERVER_URL) as websocket:
        prompt = "你觉得 Claude 和你谁更聪明？"

        openai_response = await fetch_openai_reply(prompt)

        message = {
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": openai_response
                }
            ]
        }

        await websocket.send(json.dumps(message))
        print("✅ OpenAI 回复已发送到 Claude-Mock Server")

        response = await websocket.recv()
        print("📨 Claude-Mock Server 回应：", response)

if __name__ == "__main__":
    asyncio.run(run_client())
