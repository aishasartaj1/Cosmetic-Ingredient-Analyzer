# Agent Engineering Bootcamp Project

This is a Python project for the Agent Engineering Bootcamp that demonstrates integration with LiteLLM for AI model interactions.

## Setup

1. Make sure you have Python installed
2. Install dependencies:
   ```bash
   uv add litellm python-dotenv
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. Run the example:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py` - Main application file with LiteLLM integration example
- `.env` - Environment variables (API keys)
- `README.md` - Project documentation

## Notes

- Make sure to never commit your `.env` file to version control
- The example uses GPT-4, but you can modify the model in `main.py` to use other models
- Always handle API errors appropriately in production code
