import streamlit as st
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import tiktoken
from langchain.memory import ConversationBufferMemory
from htmlTemplates import css,bot_template, user_template
# from langchain.chains import ConversationalChain

def handle_userinput(user_question):
    response=st.session_state.conversation({'question' : user_question})
    st.session_state.chat_history = response['chat_history']
    for i,message in enumerate(st.session_state.chat_history):
        if i % 2==0:
            st.write(user_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)


def handle_userinput(user_question):
    #this sets up memory to remember previous conversation
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2==0:
            st.write(user_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)


def main():

    load_dotenv()


    #this sets up the application on streamlit
    st.set_page_config(page_title='Ask your CSV' , page_icon=":chart:")
    st.header('Ask your CSV :chart:')

    user_csv = st.file_uploader('Upload your CSV file', type='csv')

    if user_csv is not None:
        user_question = st.text_input('Ask a question about your CSV: ')

        llm = OpenAI(temperature = 0)
        agent = create_csv_agent(llm, user_csv, verbose = True)

        if user_question is not None and user_question != "":
            response = agent.run(user_question)
            st.write(response)



if __name__=='__main__':
    main()