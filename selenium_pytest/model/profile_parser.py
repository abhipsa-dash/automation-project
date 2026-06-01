import json
import os
from selenium_pytest.model.llm_client import call_llm

_XPATH_SYSTEM_PROMPT = """You are a Selenium XPath expert.
Given the HTML of a LinkedIn form page, extract the most reliable XPath for each form field.
Prefer attributes like id, name, aria-label, data-testid over fragile class names.
Return ONLY a valid JSON object, no explanation."""

def extract_about_xpaths(html: str) -> dict:
    """Send the About/summary form HTML to the LLM and get back field XPaths."""
    # Find the form section by locating the text editor or summary keyword
    for keyword in ("summary", "about", "tiptap"):
        anchor = html.lower().find(keyword)
        if anchor != -1:
            break
    start = max(0, anchor - 500)
    focused = html[start:start + 10000]

    user_prompt = """Analyze this LinkedIn About/Summary form HTML and return a JSON object with XPaths for:
{
  "about_textbox": "xpath for the text editor / textarea where the about text is typed",
  "save_button": "xpath for the Save button"
}

IMPORTANT RULES:
- NEVER use dynamic IDs like \":r6:\", \":rc:\", or any UUID/colon-based IDs - they change on every load.
- Prefer stable attributes: data-testid, aria-label, placeholder, role, or meaningful text content.
- For the tiptap rich text editor use: //div[@data-testid='ui-core-tiptap-text-editor-wrapper']
- For the save button use: //button[normalize-space()='Save'] or //button[@aria-label='Save']
- Return ONLY the JSON.

HTML:
""" + focused

    raw = call_llm(system_prompt=_XPATH_SYSTEM_PROMPT, user_content=user_prompt)
    return json.loads(raw)


def extract_education_xpaths(html: str) -> dict:
    """Send the education form HTML to the LLM and get back field XPaths."""
    # Find the education form section by locating the School field
    anchor = html.lower().find("school")
    if anchor == -1:
        anchor = html.lower().find("education")
    start = max(0, anchor - 500)
    focused = html[start:start + 10000]

    user_prompt = """Analyze this LinkedIn education form HTML and return a JSON object with XPaths for:
{
  "school": "xpath for the school/institution name input",
  "degree": "xpath for the degree input or select",
  "field": "xpath for the field of study input",
  "start_year": "xpath for the start year select or input (null if not present or if only dynamic id available)",
  "end_year": "xpath for the end year select or input (null if not present or if only dynamic id available)",
  "save_button": "xpath for the Save button"
}

IMPORTANT RULES:
- NEVER use dynamic IDs like \":r6:\", \":rc:\", \":rd:\", \"eeff4...\", or any UUID/colon-based IDs - they change on every load.
- Prefer stable attributes: placeholder, aria-label, aria-labelledby, data-testid, name, or meaningful text content.
- For inputs use: //input[@placeholder='<exact placeholder text>']
- For the save button use: //button[normalize-space()='Save']
- If no stable attribute exists for a field, return null for that key.

HTML:
""" + focused

    raw = call_llm(system_prompt=_XPATH_SYSTEM_PROMPT, user_content=user_prompt)
    result = json.loads(raw)
    return result

SYSTEM_PROMPT = """You are a LinkedIn profile data extractor.
Given a markdown file containing a user's profile information, extract all relevant data and return it as a JSON object using EXACTLY this schema:

{
  "title": "string — the headline/title",
  "about": "string — the about/bio text",
  "education": [
    {
      "school": "string",
      "degree": "string",
      "field": "string",
      "start": "string",
      "end": "string"
    }
  ],
  "skills": ["string", "string"],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "url": "string"
    }
  ]
}

Return ONLY the JSON object. No explanation or extra text.
If a field is missing in the input, use an empty string "" or empty list [].
"""

_DEFAULT_USER_MD = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "selpy_app", "input", "user.md"
)


def parse_profile(user_md_path: str = None) -> dict:
    """
    Read user.md, send it to the LLM, and return a structured profile dict.

    Returns:
        {
            "title": str,
            "about": str,
            "education": [{"school", "degree", "field", "start", "end"}],
            "skills": [str],
            "projects": [{"name", "description", "url"}]
        }
    """
    path = user_md_path or _DEFAULT_USER_MD

    if not os.path.exists(path):
        raise FileNotFoundError(f"user.md not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        user_md_content = f.read()

    raw = call_llm(system_prompt=SYSTEM_PROMPT, user_content=user_md_content)

    try:
        profile = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw output:\n{raw}")

    # Ensure all expected keys exist with safe defaults
    profile.setdefault("title", "")
    profile.setdefault("about", "")
    profile.setdefault("education", [])
    profile.setdefault("skills", [])
    profile.setdefault("projects", [])

    return profile
