import os
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
gpt_4_05 = {
    "model": "gpt-4",
    "api_key": openai_api_key,
    "temperature": 0.5,
    "seed": 42,
}

gpt_3_05 = {
    "model": "gpt-3.5-turbo",
    "api_key": openai_api_key,
    "temperature": 0.5,
    "seed": 42,
}


palm_config_list = [
    {
        "model": "models/chat-bison-001",
        "temperature": 0.5,
        "api_key": google_api_key,
        "api_base": "https://generativelanguage.googleapis.com/v1beta3/",
    }
]
