from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = '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'

def clear_text():
    st.session_state["uri"] = ""
    st.session_state["query"] = ""

def chat_with_db_app():
    st.title("Chat With Your MySQL Database!")

    uri = st.text_input("Enter the Link to Your MySQL Database ", key="uri")
    query = st.text_input("Enter Your Query", key="query")
    uri_placeholder = st.empty()
    query_placeholder = st.empty()
    answer_placeholder = st.empty()

    col1, col2 = st.columns(2)

    if col1.button("Submit"):
        db = SQLDatabase.from_uri(uri)
        toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0,model="gpt-4"))
        agent_executor = create_sql_agent(
            llm=ChatOpenAI(temperature=0, max_tokens=750,model="gpt-3.5-turbo-16k"),
            toolkit=toolkit,
            verbose=True,
            handle_parsing_errors=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        answer = agent_executor.run(query)
        answer_placeholder.text("Answer: " + answer)

    if col2.button("Clear", on_click=clear_text):
        uri_placeholder.empty()
        query_placeholder.empty()

if __name__ == "__main__":
    chat_with_db_app()