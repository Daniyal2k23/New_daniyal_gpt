import streamlit as st
import openai

# Set the OpenAI API key directly
openai.api_key = "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"

st.title("My Own ChatGPT!🤖")

# Initialize the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-4"

# User input
if user_prompt := st.chat_input("Your prompt"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        for chunk in stream:
            token = chunk.choices[0].delta.get("content", "")
            if token:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
