# %%writefile app.py
import torch
import streamlit as st
from unsloth import FastLanguageModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set up the Streamlit app
st.set_page_config(page_title="Therapy Chatbot", layout="wide")

# Custom CSS to style the chat interface
st.markdown("""
<style>
.stTextInput > div > div > input {
    border-radius: 20px;
}
.stButton > button {
    border-radius: 20px;
    float: right;
}
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Load the model and tokenizer
@st.cache_resource
def load_model():
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="rashid996958/llama3.2-ChatBot-MentalHealthCounceling",
        max_seq_length=5020,
        dtype=None,
        load_in_4bit=True
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FastLanguageModel.for_inference(model)
    return model, tokenizer, device

model, tokenizer, device = load_model()

# Custom prompt template
data_prompt = """Analyze the provided text from a mental health perspective. Identify any indicators of emotional distress, coping mechanisms, or psychological well-being. Highlight any potential concerns or positive aspects related to mental health, and provide a brief explanation for each observation.

### Input:
{}

### Response:
{}"""

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# New Chat Button: Clears the chat history to start a new session
if st.button("New Chat"):
    st.session_state.chat_history = []

# Chat interface
st.markdown("<h1 style='text-align: center;'>Therapy Chatbot 🤗</h1>", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(message["user"])
    with st.chat_message("assistant"):
        st.write(message["ai"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"user": user_input, "ai": ""})

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate bot response
    formatted_prompt = data_prompt.format(user_input, "")

    inputs = tokenizer([
        formatted_prompt
    ], return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        use_cache=True
    )
    answer = tokenizer.batch_decode(outputs)
    clean_response = answer[0].split("### Response:")[-1].strip()

    # Update the last message in chat history with bot response
    st.session_state.chat_history[-1]["ai"] = clean_response

    # Display bot response
    with st.chat_message("assistant"):
        st.write(clean_response)

# Clean up memory
torch.cuda.empty_cache()
