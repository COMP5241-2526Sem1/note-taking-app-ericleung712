# import libraries
import os
from openai import OpenAI
from dotenv import load_dotenv
from .note_generation_prompt import SYSTEM_PROMPT_TEMPLATE
from datetime import datetime

load_dotenv()  # Load environment variables from .env
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini" # Specify the model to use

# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0): # default values for temperature and top_p parameters 
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        model=model
    )

    return response.choices[0].message.content

# A function to generate structured notes from text using the LLM model
def generate_note_from_text(user_input, language="English"):
    """
    Generate structured note from user input text.
    
    Args:
        user_input (str): The user's unstructured note description
        language (str): Target language for title and content (default: "English")
    
    Returns:
        dict: Structured note with title, content, tags, event_date, event_time
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    system_prompt_filled = SYSTEM_PROMPT_TEMPLATE.format(
        language=language,
        today=today_str        
    )
    # 在 prompt template 裡加一行：Today is {today}
    # 例如：
    # ... (prompt內容)
    # Today is {today}
    # ... (prompt內容)
    
    messages = [
        {"role": "system", "content": system_prompt_filled},
        {"role": "user", "content": f"{user_input}"}
    ]
    import json
    raw = call_llm_model(model, messages)
    try:
        note = json.loads(raw)
    except Exception:
        # 若 LLM 回傳非純 JSON,嘗試只取第一個 {...}
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            note = json.loads(match.group(0))
        else:
            raise ValueError("LLM did not return valid JSON")
    return note

# A function to translate to text using the LLM model
def translate(text, target_language):
    messages = [
        # tell AI what is his role
        {
            "role": "system",
            "content": "You are a helpful assistant. You help people translate text from one language to another without changing the meaning of the text.",
        },
        # User's promt
        {
            "role": "user",
            "content": f"Translate the following text to {target_language}: {text}",
        }
    ]

    return call_llm_model(model, messages)

# main function to test the LLM model
if __name__ == "__main__":
    text = "Hello, how are you?"
    target_language = "Chinese"
    translated_text = translate(text, target_language)
    print("Original text:", text)
    print("Target language:", target_language)
    print("Translated text:", translated_text)