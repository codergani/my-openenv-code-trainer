from my_assistant_bot.client import MyAssistantBotEnv
from my_assistant_bot.models import MyAssistantBotAction

with MyAssistantBotEnv(base_url="http://127.0.0.1:8000").sync() as env:
    env.reset()
    env.step(MyAssistantBotAction(message="4"))
    import requests
    resp = requests.get("http://127.0.0.1:8000/state", headers={"X-Session-ID": env._session_id})
    print("Raw HTTP State:", resp.json())
