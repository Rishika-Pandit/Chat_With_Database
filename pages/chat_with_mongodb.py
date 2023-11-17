from pymongo import MongoClient

import openai
import json
import streamlit as st

def textToMql(query,cursor):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages = [
    {
        "role": "system",
        "content": f"You are a helpful assistant. The following is the document for reference from the given collection by the user {cursor}. Generate a MongoDB query to: {query} and give the filter in JSON format in one line. In the next line, provide the limit (if any specified by the user, else 0). For example:\n\nQ: 'Top 'n'(n is a number) restaurants based on filter condition given by user'\n\nA: {{\"column_name\": \"value\"}}\n n (value of n, i.e., limit). Note: Don't forget to add '\' in the provided JSON output if there is an apostrophe('). Also, make sure to give the JSON output in double quotes.\nA:"
    }
],
    max_tokens=500,   
    )
    return response.choices[0].message.content

def clear_text():
    st.session_state["uri"] = ""
    st.session_state["query"] = ""
    st.session_state["db_name"] = ""
    st.session_state["collection"] = ""

def chat_with_mongodb_app():
    st.title("Chat With Your MongoDB Database!")

    uri = st.text_input("Enter the Link to Your MongoDB Database ", key="uri")
    db_name = st.text_input("Enter the DB name of Your MongoDB Database ", key="db_name")
    collection = st.text_input("Enter the Collection of Your MongoDB Database ", key="collection")
    OPENAI_API_KEY = st.text_input("Enter Your OpenAI Key ", key="key")
    openai.api_key =  OPENAI_API_KEY
    query = st.text_input("Enter Your Query", key="query")
    uri_placeholder = st.empty()
    db_name_placeholder = st.empty()
    collection_placeholder = st.empty()
    query_placeholder = st.empty()
    answer_placeholder = st.empty()

    col1, col2 = st.columns(2)

    if col1.button("Submit"):
        client = MongoClient(uri)

        # database and collection code goes here
        db = client.db_name
        coll = db.collection
        cursor = coll.find_one()
        output =textToMql(query,cursor)
        j_string, limit_str = output.split("\n")

        # Convert limit to integer
        limit = int(limit_str)

        # Check data type with type() method
        j_string = j_string.replace("{$sort:", '{"$sort":')
        # Convert filter to JSON object
        json_object = json.loads(j_string)

        if limit>0:
            cursor_ans = coll.find(json_object).limit(limit)
        else:
            cursor_ans = coll.find(json_object)

        # answer_placeholder.text("Answer: ")
        for doc in cursor_ans:
            answer_placeholder.text(doc)

    if col2.button("Clear", on_click=clear_text):
        uri_placeholder.empty()
        query_placeholder.empty()
        db_name_placeholder.empty()
        collection_placeholder.empty()

if __name__ == "__main__":
    chat_with_mongodb_app()
