Copyimport openai 
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot") 

# Define the prompts here
prompts = {
    1: "Escribe un correo nuevo",
    2: "Escribe una respuesta a un correo",
    3: "Escribe un post para un blog",
    4: "Escribe un ensayo argumentativo en favor de algo",
    5: "Escribe un artículo académico",
    6: "Escribe una columna periodística",
    7: "Escribe un reportaje",
    8: "Escribe una entrada para Linkedin",
    9: "Escribe una entrada para Facebook",
    10: "Escribe una entrada para Twitter"
}

selected_prompt = st.selectbox("Select a prompt", list(prompts.values()))

if "messages" not in st.session_state:
    # The assistant begins the conversation with the selected prompt.
    st.session_state["messages"] = [{"role": "assistant", "content": prompts[selected_prompt]}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get responses from the chat model
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
