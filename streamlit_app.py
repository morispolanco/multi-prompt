import openai
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot")

# Define the prompts
prompts = [
    "¿Qué quieres escribir? Selecciona una opción:\n\n"
    "1. Nuevo Correo Electrónico\n"
    "2. Respuesta de Correo Electrónico\n"
    "3. Ensayo a Favor\n"
    "4. Ensayo en Contra\n"
    "5. Ensayo Descriptivo\n"
    "6. Columna Periodística\n"
    "7. Artículo para Blog\n"
    "8. Ensayo Libre\n"
]

# Use the selected prompt
selected_prompt_index = 0  # Inicialmente, mostramos las opciones de prompts
selected_prompt = prompts[selected_prompt_index]

if "messages" not in st.session_state:
    # El asistente comienza la conversación con el saludo y las opciones de prompts.
    st.session_state["messages"] = [{"role": "assistant", "content": selected_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor, agrega tu clave de API de OpenAI para continuar.")
        st.stop()

    openai.api_key = openai_api_key
    user_input = prompt.strip().lower()  # Convertir la respuesta del usuario a minúsculas

    # Definir los prompts en función de la respuesta del usuario
    if user_input == "1" or "nuevo correo electrónico" in user_input:
        selected_prompt_index = 1
    elif user_input == "2" or "respuesta de correo electrónico" in user_input:
        selected_prompt_index = 2
    elif user_input == "3" or "ensayo a favor" in user_input:
        selected_prompt_index = 3
    elif user_input == "4" or "ensayo en contra" in user_input:
        selected_prompt_index = 4
    elif user_input == "5" or "ensayo descriptivo" in user_input:
        selected_prompt_index = 5
    elif user_input == "6" or "columna periodística" in user_input:
        selected_prompt_index = 6
    elif user_input == "7" or "artículo para blog" in user_input:
        selected_prompt_index = 7
    elif user_input == "8" or "ensayo libre" in user_input:
        selected_prompt_index = 8
    else:
        st.info("Opción no válida. Por favor, selecciona un número o una opción válida.")

    selected_prompt = prompts[selected_prompt_index]
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Obtenemos respuestas del modelo de chat
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
