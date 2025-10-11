# import libraries
import os
from openai import OpenAI
from dotenv import load_dotenv

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
    target_language = "Japanese"
    translated_text = translate(text, target_language)
    print("Original text:", text)
    print("Target language:", target_language)
    print("Translated text:", translated_text)