import openai
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    st.title("Choose a Prompt")
    prompt_choices = {
        "Nuevo Correo Electrónico": 0,
        "Respuesta de Correo Electrónico": 1,
        "Ensayo a Favor": 2,
        "Ensayo en Contra": 3,
        "Ensayo Descriptivo": 4,
        "Columna Periodística": 5,
        "Artículo para Blog": 6,
        "Ensayo Libre": 7,
    }
    prompt_choice = st.selectbox("Select a Prompt", list(prompt_choices.keys()))

st.title("💬 Chatbot")

# Define the prompts
prompts = [
    "¿Qué quieres escribir?",  # Saludo inicial modificado
    "Escribe un correo electrónico de respuesta.",
    "Escribe un ensayo argumentativo a favor de algo.",
    "Escribe un ensayo argumentativo en contra de algo.",
    "Escribe un ensayo descriptivo.",
    "Escribe una columna periodística.",
    "Escribe un artículo para un blog.",
    "Escribe un ensayo libre."
]

# Use the selected prompt
selected_prompt_index = prompt_choices[prompt_choice]
selected_prompt = prompts[selected_prompt_index]

if "messages" not in st.session_state:
    # The assistant begins the conversation with the selected prompt.
    st.session_state["messages"] = [{"role": "assistant", "content": selected_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get responses from chat model
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
