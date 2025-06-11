import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/askQuestion"

def ask_backend(question):
    response = requests.post(API_URL, json={"question": question})
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

iface = gr.Interface(
    fn=ask_backend,
    inputs=gr.Textbox(lines=2, label="Ask your question about TDS"),
    outputs=gr.Markdown(label="Answer"),
    title="TDS RAG Assistant",
    description="Enter a question and get an answer from the course material."
)

iface.launch()
    