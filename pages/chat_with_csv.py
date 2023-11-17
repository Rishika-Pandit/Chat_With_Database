from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
import streamlit as st
import os
import tempfile
import openai

def clear_text():
    st.session_state["query"] = ""

def chat_with_csv_app():
    # Configure Streamlit page
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV")
    OPENAI_API_KEY = st.text_input("Enter Your OpenAI Key ", key="key")
    openai.api_key =  OPENAI_API_KEY
    query = st.text_input("Enter Your Query", key="query")
    query_placeholder = st.empty()

    # Allow the user to upload a CSV file
    file = st.file_uploader("upload file", type="csv")

    col1, col2 = st.columns(2)

    if col1.button("Submit"):
        if file is not None:
            # Create a temporary file to store the uploaded CSV data
            with tempfile.NamedTemporaryFile(mode='w+', suffix=".csv", delete=False) as f:
                # Convert bytes to a string before writing to the file
                data_str = file.getvalue().decode('utf-8')
                f.write(data_str)
                f.flush()

                # Create an instance of the OpenAI language model with temperature set to 0
                llm = llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model="gpt-4")

                # Create a CSV agent using the OpenAI language model and the temporary file
                agent = create_csv_agent(llm, f.name, verbose=True)

                if query:
                    # Run the agent on the user's question and get the response
                    response = agent.run(query)
                    st.write(response)

    if col2.button("Clear", on_click=clear_text):
        query_placeholder.empty()

if __name__ == "__main__":
    chat_with_csv_app()