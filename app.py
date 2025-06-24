import streamlit as st
import pytesseract
from PIL import Image
import io
from typing import List, Dict, Literal
import pandas as pd
from langchain.tools.base import BaseTool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import vectorize_client as v
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Initialize Vectorize client
api = v.ApiClient(v.Configuration(
    access_token=os.getenv("VECTORIZE_API_KEY"),
    host="https://api.vectorize.io/v1"
))

# Initialize pipeline API
pipelines_api = v.PipelinesApi(api)

class RAGTool(BaseTool):
    name: Literal["ingredient_lookup"] = "ingredient_lookup"
    description: str = "Look up information about a cosmetic ingredient using RAG"
    
    def _run(self, ingredient: str) -> str:
        # Search for ingredient information using Vectorize
        try:
            response = pipelines_api.retrieve_documents(
                os.getenv("VECTORIZE_ORG_ID"),  # Organization ID from environment
                os.getenv("VECTORIZE_PIPELINE_ID"),  # Pipeline ID from environment
                v.RetrieveDocumentsRequest(
                    question=f"What are the properties, uses, and safety information of {ingredient}?",
                    num_results=3
                )
            )
            
            # Combine the retrieved information
            context = "\n".join([doc.text for doc in response.documents])
            
            # Use GPT-4 to analyze the ingredient based on the retrieved information
            llm = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0
            )
            
            prompt = PromptTemplate.from_template(
                """Based on the following information about the cosmetic ingredient {ingredient}, 
                provide a detailed analysis including its purpose, safety level, and any warnings.
                Focus on information from both CosmeticsInfo.org and INCIDecoder sources.
                
                Context: {context}
                
                Return ONLY a JSON object with these exact keys (no additional text or explanation):
                {{
                    "purpose": "The main functions and uses of the ingredient",
                    "safety_level": A number from 1-10 (1 being unsafe, 10 being very safe),
                    "warnings": "Any potential risks or allergen warnings",
                    "skin_types": "What skin types this ingredient is suitable/unsuitable for"
                }}
                
                Ensure the response is valid JSON with no markdown formatting."""
            )
            
            response = llm.invoke(prompt.format(
                ingredient=ingredient,
                context=context
            ))
            
            return response.content
            
        except Exception as e:
            st.error(f"Error retrieving information for {ingredient}: {str(e)}")
            return str(e)

class IngredientAnalysisTool(BaseTool):
    name: Literal["analyze_ingredients"] = "analyze_ingredients"
    description: str = "Analyze a list of cosmetic ingredients and provide a safety assessment"
    
    def _run(self, ingredients: List[str]) -> pd.DataFrame:
        results = []
        rag_tool = RAGTool()
        
        for ingredient in ingredients:
            try:
                # Get the analysis from RAG tool
                response = rag_tool._run(ingredient)
                
                # Try to parse the response as JSON
                try:
                    # Clean the response string to ensure it's valid JSON
                    # Remove any potential markdown formatting
                    cleaned_response = response.replace("```json", "").replace("```", "").strip()
                    analysis = json.loads(cleaned_response)
                except json.JSONDecodeError:
                    st.error(f"Failed to parse response for {ingredient}. Response format was not valid JSON.")
                    continue
                    
                analysis['ingredient'] = ingredient
                results.append(analysis)
            except Exception as e:
                st.error(f"Error analyzing ingredient {ingredient}: {str(e)}")
                continue
        
        if not results:
            st.error("No ingredients could be successfully analyzed.")
            return pd.DataFrame()
            
        df = pd.DataFrame(results)
        # Reorder columns to show ingredient first, then purpose, followed by other columns
        columns = ['ingredient', 'purpose', 'safety_level', 'warnings', 'skin_types']
        return df[columns]

def extract_ingredients_from_image(image) -> List[str]:
    """Extract ingredients from an image using OCR."""
    text = pytesseract.image_to_string(image)
    # Basic ingredient list extraction - you might want to enhance this
    ingredients = [i.strip() for i in text.split(',')]
    return ingredients

def clean_ingredients(text: str) -> List[str]:
    """Clean and normalize ingredient list from text."""
    ingredients = [i.strip() for i in text.split(',')]
    return ingredients

def main():
    st.title("Cosmetic Ingredient Analyzer")
    st.write("Upload a photo of ingredients or paste the ingredient list to analyze")
    
    # Initialize tools
    rag_tool = RAGTool()
    analysis_tool = IngredientAnalysisTool()
    
    # File upload
    uploaded_file = st.file_uploader("Upload an image of the ingredient list", type=["jpg", "png", "jpeg"])
    
    # Text input
    text_input = st.text_area("Or paste the ingredients here (comma-separated)")
    
    ingredients = []
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        ingredients = extract_ingredients_from_image(image)
        st.write("Extracted Ingredients:", ingredients)
    
    elif text_input:
        ingredients = clean_ingredients(text_input)
        st.write("Processed Ingredients:", ingredients)
    
    if ingredients and st.button("Analyze Ingredients"):
        with st.spinner("Analyzing ingredients..."):
            try:
                # Analyze ingredients
                df = analysis_tool._run(ingredients)
                
                # Display results
                st.subheader("Analysis Results")
                st.dataframe(df)
                
                # Option to download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Analysis as CSV",
                    data=csv,
                    file_name="ingredient_analysis.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main() 