from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

def test_llm():
    try:
        # Make sure to set your API key in the .env file
        response = completion(
            model="openai/gpt-4",  # Using GPT-4 that you paid for
            messages=[{"content": "Hello, how are you?", "role": "user"}]
        )
        print("AI Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_llm()
