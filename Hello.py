import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.runnable import RunnablePassthrough

icon_dic = {'human': '😁', 'ai': '😒'}

st.set_page_config(
    page_title="Rude GPT",
    page_icon="😑",
)

st.header('Rude GPT😑', divider='rainbow')

st.write("# What are you looking at 😒?")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()
    
    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")
        
    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)

llm = ChatOpenAI(
    temperature=0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),
    ]
)

def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})

def send_message(message, role, save):
    with st.chat_message(name=role, avatar=icon_dic[role]):
        st.markdown(message)
    if save:
        save_message(message, role)

def print_message_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], False)

def reset_message():
    st.session_state["messages"] = []

with st.sidebar:
    language = st.selectbox(
        "Select Language.",
        (
            "English",
            "Korean",
            "Japanese",
            "Chinese",
            "Thai",
            "Hindi",
            "Spanish",
            "Arabic",
            "French",
            "Russian",
        ),
        on_change=reset_message
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
I want you to act as an expert in role playing and improvisation specializing in rude behavior. Make your answers sound like you are rude. You must response to {language}
"""),
        ("human", "{message}")
    ]
)

message = st.chat_input("What do you want? 😑")
if message:
    print_message_history()
    send_message(message, "human", True)
    
    chain = (
        {"language": RunnablePassthrough(), "message": RunnablePassthrough()} | prompt | llm
    )

    with st.chat_message(name="ai", avatar="😒"):
        chain.invoke({"language": language, "message": message})