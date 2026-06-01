import os
from groq import Groq
from dotenv import load_dotenv

_ENV_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "selpy_app", "input", ".env"
)
load_dotenv(_ENV_PATH)


def call_llm(system_prompt: str, user_content: str, model: str = "llama-3.1-8b-instant") -> str:
    """Send a prompt to the Groq API and return the raw response string."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY is not set. Add your key to data/selpy_app/input/.env"
        )

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return response.choices[0].message.content
