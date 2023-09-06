import openai
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot")

# Saludo inicial del chatbot
initial_prompt = "¿Qué quieres escribir?"

if "messages" not in st.session_state:
    # El asistente comienza la conversación con el saludo.
    st.session_state["messages"] = [{"role": "assistant", "content": initial_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor, agrega tu clave de API de OpenAI para continuar.")
        st.stop()

    openai.api_key = openai_api_key
    user_input = prompt.strip()

    # Agregar el mensaje del usuario a la conversación
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Obtener una respuesta del modelo de chat
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
