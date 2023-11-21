from pymongo import MongoClient
import ast
import openai
import json
import streamlit as st

def textToMql(query,cursor):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages = [
    {
        "role": "system",
        "content": f"You are a helpful assistant. The following is the document for reference from the given collection by the user {cursor}. Generate a MongoDB query to: {query} and give the filter in JSON format in one line. If there is a projection, provide it in JSON format in the next line (if any specified by the user, else 'Null').In the subsequent line, provide the sorting condition (if any specified by the user) in a single new line. If a sorting condition is given, its contents should be given in a single new line. In the subsequent line, provide the limit (if any specified by the user, else 0). For example:\n\nQ: 'Names of top 'n'(n is a number) restaurants based on filter, projection, sort condition given by user'\n\nA: {{\"column_name\": \"value\"}}\n{{\"projection_name\": 1}}\n[(\"sort_name\", -1)]\n n (value of n, i.e., limit). Note: Don't forget to add '\' in the provided JSON output if there is an apostrophe('). Also, make sure to give the JSON output in double quotes.\nA:"
    }
],
    max_tokens=500,   
    )
    return response.choices[0].message.content

def clear_text():
    st.session_state["uri"] = ""
    st.session_state["query"] = ""
    # st.session_state["db_name"] = ""
    # st.session_state["collection"] = ""

def chat_with_mongodb_app():
    st.title("Chat With Your MongoDB Database!")

    uri = st.text_input("Enter the Link to Your MongoDB Database ", key="uri")
    # db_name = st.text_input("Enter the DB name of Your MongoDB Database ", key="db_name")
    # collection = st.text_input("Enter the Collection of Your MongoDB Database ", key="collection")
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
        db = client.sample_restaurants
        coll = db.restaurants
        cursor = coll.find_one()
        output =textToMql(cursor, query)
        j_filter, j_projection, j_list, limit_str = output.split("\n")

        # Convert limit to integer
        limit = int(limit_str)
        if j_list != "Null":
            j_sort = ast.literal_eval(j_list)
        else: 
            j_sort = None
        # Convert filter to JSON object
        json_object_1 = json.loads(j_filter)
        if j_projection != "Null":
            json_object_2 = json.loads(j_projection)

        if j_projection != 'None':
            if j_sort != None:
                cursor_ans = coll.find(json_object_1, json_object_2).sort(j_sort)
                if limit>0:
                    cursor_ans = coll.find(json_object_1, json_object_2).sort(j_sort).limit(limit)
                else: 
                    cursor_ans = coll.find(json_object_1, json_object_2).sort(j_sort) 
            else:
                if limit>0:
                    cursor_ans = coll.find(json_object_1, json_object_2).limit(limit)
                else: 
                    cursor_ans = coll.find(json_object_1, json_object_2)
        else:
            cursor_ans = coll.find(json_object_1)

        answer_placeholder.text("Answer: ")
        for doc in cursor_ans:
            answer_placeholder.text(doc)

    if col2.button("Clear", on_click=clear_text):
        uri_placeholder.empty()
        query_placeholder.empty()
        db_name_placeholder.empty()
        collection_placeholder.empty()

if __name__ == "__main__":
    chat_with_mongodb_app()
