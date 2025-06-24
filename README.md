# Cosmetic Ingredient Analyzer with RAG

This Streamlit application analyzes cosmetic product ingredients using Retrieval-Augmented Generation (RAG) powered by Vectorize and OpenAI's GPT-4. The knowledge base is built from web-crawled data from two authoritative sources:

1. [CosmeticsInfo.org](https://cosmeticsinfo.org) - A comprehensive database of cosmetic ingredients maintained by the Personal Care Products Council
2. [INCIDecoder](https://incidecoder.com) - A detailed ingredient dictionary with explanations of cosmetic formulations

## Features

- Upload images of ingredient labels for OCR-based extraction
- Paste ingredient lists directly
- RAG-powered ingredient information lookup using Vectorize
- Detailed analysis of each ingredient including:
  - Purpose/use in cosmetic formulations
  - Safety level (1-10 scale)
  - Potential warnings or allergen information
  - Suitable/unsuitable skin types
- Export analysis results as CSV

## Technical Implementation

### RAG Pipeline
- **Data Source**: Web crawled content from CosmeticsInfo.org and INCIDecoder
- **Vector Database**: Vectorize
- **LLM**: OpenAI GPT-4 Turbo for analysis and response generation

### Key Components
1. **Vectorize Integration**:
   - Stores and retrieves relevant ingredient information
   - Semantic search for ingredient properties and safety data
   - Returns top 3 most relevant document chunks per query

2. **LLM Analysis**:
   - Processes retrieved information using GPT-4
   - Structures data into consistent format
   - Provides safety ratings and recommendations

3. **Image Processing**:
   - Uses Tesseract OCR for ingredient label extraction
   - Supports JPG, PNG, and JPEG formats

## Prerequisites

- Python 3.12 or higher
- Tesseract OCR installed on your system
  - Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/aishasartaj1/my-project.git
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

4. Create a `.env` file in the project root with your configuration:
   ```
   OPENAI_API_KEY=your-openai-api-key
   VECTORIZE_API_KEY=your-vectorize-api-key
   VECTORIZE_ORG_ID=your-vectorize-organization-id
   VECTORIZE_PIPELINE_ID=your-vectorize-pipeline-id
   ```

5. Update the configuration:
   - Sign up for OpenAI and get your API key
   - Sign up for Vectorize at [portal.vectorize.com](https://portal.vectorize.com)
   - Create a new pipeline for ingredient analysis
   - Add your Vectorize organization ID and pipeline ID to the `.env` file

## Running the Application

1. Ensure your virtual environment is activated
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to http://localhost:8504

## Example Ingredients to Test

Here are some common ingredients you can test with the analyzer:
- Niacinamide
- Hyaluronic Acid
- Glycerin
- Retinol
- Vitamin C
- Salicylic Acid
- Squalane
- Panthenol
- Ceramide NP
- Peptides

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Deployment

**Note**: This application uses OpenAI and Vectorize APIs which have usage limits. Consider your API usage and costs before deploying publicly.

To deploy your own instance:

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your forked repository
4. Add the following secrets in Streamlit Cloud settings:
   - `OPENAI_API_KEY`
   - `VECTORIZE_API_KEY`
   - `VECTORIZE_ORG_ID`
   - `VECTORIZE_PIPELINE_ID`
5. Deploy!

Note: Make sure you have Tesseract installed on your deployment environment. Streamlit Cloud comes with Tesseract pre-installed.
