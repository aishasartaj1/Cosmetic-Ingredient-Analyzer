# Ingredient Analyzer Agent

This Streamlit application implements an Ingredient Analyzer Agent that helps users analyze cosmetic product ingredients using Retrieval-Augmented Generation (RAG) via Vectorize portal and Anthropic's Claude 3.

## Features

- Upload images of ingredient labels for OCR-based extraction
- Paste ingredient lists directly
- RAG-powered ingredient information lookup using Vectorize
- Detailed analysis of each ingredient including:
  - Purpose/use
  - Safety level (1-10 scale)
  - Allergen/toxicity warnings
  - Skin type suitability
- Export analysis results as CSV

## Prerequisites

- Python 3.12 or higher
- Tesseract OCR installed on your system
  - Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd my-project
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On Unix/macOS:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   ANTHROPIC_API_KEY=your-anthropic-api-key
   VECTORIZE_API_KEY=your-vectorize-api-key
   ```

5. Initialize Vectorize:
   - Sign up for Vectorize at [portal.vectorize.com](https://portal.vectorize.com)
   - Create a new collection named "cosmetic_ingredients"
   - Upload your cosmetic ingredients dataset
   - Get your API key and add it to the `.env` file

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

1. Choose your input method:
   - Upload an image of a product's ingredient label
   - Paste a comma-separated list of ingredients

2. Click "Analyze Ingredients" to process the ingredients

3. View the analysis results in the table:
   - Purpose/function of each ingredient
   - Safety ratings and warnings
   - Download the analysis as CSV if needed

## How it Works

1. **Input Processing**:
   - OCR (pytesseract) extracts text from uploaded images
   - Text input is cleaned and normalized

2. **RAG Analysis**:
   - Each ingredient is looked up in the Vectorize database
   - Relevant information is retrieved and processed
   - Claude 3 analyzes the information and provides structured insights

3. **Results**:
   - Analysis is presented in a clear, tabular format
   - Results can be exported for further use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]
