import gradio as gr
import time
from main import rag_chatbot
from src.ingestion.ingest_files import ingest_files_data_folder
from src.services.models.embeddings import Embeddings
from src.services.models.llm import LLM
from src.services.vectorial_db.faiss_index import FAISSIndex

# Initialize instances for the LLM, embeddings, and FAISS index
llm = LLM()
embeddings = Embeddings()
index = FAISSIndex(embeddings=embeddings.get_embeddings)

# Load the FAISS index, ingest data if it doesn't exist
try:
    index.load_index()
except FileNotFoundError:
    ingest_files_data_folder(index)
    index.save_index()

# Manage global conversation storage
conversations = {"New Conversation": []}

def chatbot_wrapper(input_text, conversation_name):
    """
    Wrapper for the chatbot.
    """
    history = conversations.get(conversation_name, [])
    response, updated_history = rag_chatbot(llm, input_text, history, index)
    updated_history.append({"role": "assistant", "content": response})
    conversations[conversation_name] = updated_history
    return updated_history, ""  # Clear the input field after the response

def add_user_text(conversation_name, user_input):
    """
    Add user input to the selected conversation.
    """
    if conversation_name not in conversations:
        conversations[conversation_name] = []
    conversations[conversation_name].append({"role": "user", "content": user_input})
    return conversations[conversation_name], user_input

def new_conversation(new_name):
    """
    Create a new conversation and reset the interface.
    """
    if new_name not in conversations:
        conversations[new_name] = []
    return (
        gr.update(choices=list(conversations.keys()), value=new_name),  # Update the dropdown
        [],  # Clear chatbot history
        "",  # Clear the input field 'new_conversation_name'
    )

def load_conversation(conversation_name):
    """
    Load the selected conversation's history.
    """
    history = conversations.get(conversation_name, [])
    formatted_history = [
        {"role": entry["role"], "content": entry["content"]} for entry in history
    ]
    return formatted_history

def update_temperature(temperature):
    """Placeholder function for updating temperature."""
    global current_temperature
    current_temperature = temperature 
    return temperature


def update_max_tokens(max_tokens):
    """Placeholder function for updating max tokens."""
    global current_max_tokens
    current_max_tokens = max_tokens
    return max_tokens

custom_css = """
#chatbot, .gradio-row, .gradio-column, .gradio-container {
    border: 1px solid #28a745 !important; /* Verde para todas as bordas */
    border-radius: 8px; /* Bordas arredondadas */
    padding: 10px; /* Espaçamento interno */
}

.gradio-textbox, .gradio-file, .gradio-dropdown, .gradio-slider {
    border: 1px solid #28a745 !important; /* Verde para entradas */
    border-radius: 5px;
    padding: 5px;
}

.gradio-button {
    background-color: #6c757d !important; /* Cinza para botões */
    color: white !important; /* Texto branco nos botões */
    border-radius: 5px;
    border: 1px solid #6c757d;
    padding: 10px;
    font-weight: bold; /* Texto em negrito */
    cursor: pointer;
}

.gradio-button:hover {
    background-color: #5a6268 !important; /* Cinza escuro para hover */
    border: 1px solid #5a6268 !important;
}
"""


# Create the Gradio interface
with gr.Blocks( css = "custom_css", theme= "Ocean",fill_width=True) as demo:
    with gr.Row():
        # Sidebar for conversation management
        with gr.Column(scale=1):
            with gr.Row():
                conversation_selector = gr.Dropdown(
                    label="Conversations",
                    choices=list(conversations.keys()),
                    value="New Conversation",
                    interactive=True, container=True, min_width=100
                )
            with gr.Row():
                new_conversation_name = gr.Textbox(label="New Conversation", container=True)
            with gr.Row():
                new_conversation_button = gr.Button("Create Conversation")

            with gr.Row():
                temperature = gr.Slider(0.0, 2, value=1, label="Temperature")
            with gr.Row():
                max_tokens = gr.Slider(1, 1000, value=800, label="Max Tokens")

            # Register slider values (currently placeholder functions)
            t = temperature.release(update_temperature, inputs=[temperature])
            mt = max_tokens.release(update_max_tokens, inputs=[max_tokens])

        # Chatbot UI
        with gr.Column(scale=4):
            chatbot_ui = gr.Chatbot(
                [], type="messages", elem_id="chatbot", avatar_images=(r"img/user.png", r"img/gpt.png")
            )
            txt = gr.Textbox(
                scale=4, show_label=False, placeholder="Enter text and press Enter"
            )
            file_input = gr.File(label="Upload a file")

        

    

    # Event chains
    new_conversation_button.click(
        new_conversation,
        inputs=new_conversation_name,
        outputs=[conversation_selector, chatbot_ui, new_conversation_name],
    )

    conversation_selector.change(
        load_conversation,
        inputs=[conversation_selector],
        outputs=[chatbot_ui],
    )

    txt.submit(
        add_user_text,
        inputs=[conversation_selector, txt],
        outputs=[chatbot_ui, txt],  # Update history and clear input field
    ).then(
        chatbot_wrapper, inputs=[txt, conversation_selector], outputs=[chatbot_ui, txt]  # Clear input after chatbot response
    )


demo.launch()
