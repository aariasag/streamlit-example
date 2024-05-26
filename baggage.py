from openai import OpenAI
import streamlit as st

MODEL = "gpt-4o"

st.title("💬 Chatbot")
st.caption("🚀 IA Assistant about baggage")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


if not openai_api_key:
   st.info("Please add your OpenAI API key to continue.")
   st.stop()

context = [{'role':'system', 'content':"""
Eres un asistente de pasajeros que solo responde preguntas relacionadas con
los equipajes que permiten las aerolineas. Si una pregunta no está relacionada con estos temas, 
simplemente responde con "Lo siento, solo puedo responder preguntas sobre equipajes"
Para ello deberás preguntarles con que aerolínea vuelan para ir a la página web de la aerolínea y extraer 
la información con la que responderles. 
"""}]
   
client = OpenAI(api_key=openai_api_key)
response = client.chat.completions.create(model=MODEL, 
                                          messages=context,
                                          temperature = 0)
msg = response.choices[0].message.content
st.session_state["messages"] = [{"role": "assistant", "content": msg}]
st.chat_message("assistant").write(msg)

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model=MODEL, messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
