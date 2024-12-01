import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain.llms.base import LLM
from pydantic import BaseModel
import requests
import pandas as pd
import tempfile
from dotenv import load_dotenv


# Custom LLM class for Gemini API
class GeminiLLM(LLM, BaseModel):
    api_key: str

    def _call(self, prompt: str, **kwargs) -> str:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(f"{url}?key={self.api_key}", headers=headers, json=payload)
        if response.status_code == 200:
            try:
                result = response.json()
                # Log the raw API response for debugging
                print(f"API Response: {result}")
                return result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "").strip()
            except Exception as e:
                return f"Error while parsing response: {str(e)}"
        else:
            return f"Error: API returned status {response.status_code} - {response.text}"

    def _llm_type(self) -> str:
        return "gemini"


# Main application function
def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your CSV 📈")
    st.header("Ask your CSV 📈")

    # File uploader for CSV
    user_csv = st.file_uploader("Upload a CSV file", type="csv")
    if user_csv is not None:
        # Read the CSV file directly from the uploaded file
        df = pd.read_csv(user_csv)
        st.write("Here's a preview of your CSV:", df.head())

        user_question = st.text_input("Ask a question about your CSV")

        # Use your Gemini API key here
        gemini_api_key = "AIzaSyCzZuWE1y4wZ21Bb7KgfdQYJd1hWFy0l7k" # Replace with your actual API key
        llm = GeminiLLM(api_key=gemini_api_key)  # Corrected instance creation

        # Save the uploaded CSV file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode="w", newline="") as tmp_file:
            df.to_csv(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name

        # Create CSV agent using LangChain
        agent_executor = create_csv_agent(
            llm,
            tmp_file_path,  # Pass the file path here, not the DataFrame
            verbose=True,
            allow_dangerous_code=True
        )

        if user_question and user_question.strip():
            try:
                response = agent_executor.run(user_question)
                st.write(response)
            except Exception as e:
                st.error(f"Failed to process your question. Error details: {e}")


if __name__ == "__main__":
    main()
