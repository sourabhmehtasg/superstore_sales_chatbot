import streamlit as st
from streamlit_chat import message
import requests
import sqlite3 as sl
import os
import openai
import pandas as pd
from tabulate import tabulate

# open ai request
# OPENAI_API_KEY
openai.api_key = "<OPEN_AI_KEY>"




#  sqlite dB
con = sl.connect('sales.db')


st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

# API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
# headers = {"Authorization": st.secrets['api_key']}

st.header("Streamlit Chat - Demo")
# st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(user_input):
    gpt_query = """ ### SQLite SQL tables, with their properties:
    #
    # SALES (row_id,order_id,order_date,ship_date,ship_mode,customer_id,customer_name,segment,city,state,country,market,region,product_id,category,sub_category,product_name,sales,quantity,discount,profit,shipping_cost,order_priority)
    #
    ### """ + user_input

    print("----------->", gpt_query)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=gpt_query,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )
	# response = requests.post(API_URL, headers=headers, json=payload)
    print(response)
    print(">>>>>>>>>>>>>>>>>>>")
    print(response["choices"][0]["text"])
    
    return response

def get_text():
    input_text = st.text_input("You: ","what are top 10 customers by sales?", key="input")
    return input_text 


user_input = get_text()

if user_input:
    # output = query({
    #     "inputs": {
    #         "past_user_inputs": st.session_state.past,
    #         "generated_responses": st.session_state.generated,
    #         "text": user_input,
    #     },"parameters": {"repetition_penalty": 1.33},
    # })
    # query format
    output = query(user_input)
    ls = []
    with con:
        q = output["choices"][0]["text"]
        print("????????????? q:= ", q)
        data = con.execute(q)
        for row in data:
            ls.append(row)

    df = pd.DataFrame(ls)
    # reply = "\n ".join(tup for tup in ls)
    reply = "\n ".join(map(str, ls))
    print("=====================================")
    print(reply)
    
    print("=====================================")
    st.session_state.past.append(user_input)
    # st.session_state.generated.append(str(st.write(df)))
    st.session_state.generated.append(reply)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')