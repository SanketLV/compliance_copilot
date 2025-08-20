import os
from dotenv import load_dotenv
from portia import Config, LLMProvider, Portia, example_tool_registry

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE,
    default_model="google/gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
)

portia = Portia(config=google_config, tools=example_tool_registry)
