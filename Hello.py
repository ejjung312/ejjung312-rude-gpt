import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

icon_dic = {'human': '😁', 'ai': '😒'}

st.set_page_config(
    page_title="Rude GPT",
    page_icon="😑",
)

st.write("# Say Anything 😒")

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

chat = ChatOpenAI(
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

message = st.chat_input("What do you want? 😑")
if message:
    print_message_history()
    send_message(message, "human", True)
    
    with st.chat_message(name="ai", avatar="😒"):
        result = chat.invoke(message)