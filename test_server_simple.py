from fastapi import FastAPI
import uvicorn
from openenv.core.env_server.http_server import create_app
from models import MyAssistantBotAction, MyAssistantBotObservation
from server.my_assistant_bot_environment import MyAssistantBotEnvironment

print("🛠️ Creating App...")
app = create_app(
    MyAssistantBotEnvironment,
    MyAssistantBotAction,
    MyAssistantBotObservation,
    env_name="test_env"
)

if __name__ == "__main__":
    print("🚀 Running Uvicorn on 8005...")
    uvicorn.run(app, host="127.0.0.1", port=8005)
