import gradio as gr
import requests
import base64

API_URL = "http://127.0.0.1:8000/api/"  # Change if hosted elsewhere

def ask_ta(question, image):
    if not question.strip():
        return "❌ Please enter a question.", None

    payload = {"question": question.strip()}

    # Encode image to base64 if provided
    if image is not None:
        with open(image, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")
        payload["image"] = img_base64
    else:
        payload["image"] = None

    try:
        res = requests.post(API_URL, json=payload, timeout=30)
        res.raise_for_status()
        output = res.json()
        answer = output.get("answer", "No answer returned.")
        links = output.get("links", [])

        # Format links
        link_text = "\n".join([f"[{l['text']}]({l['url']})" for l in links])
        return answer, link_text or "🔗 No related links found."
    except Exception as e:
        return f"❌ Error: {str(e)}", None

iface = gr.Interface(
    fn=ask_ta,
    inputs=[
        gr.Textbox(label="Your Question"),
        gr.File(label="Upload Image (Optional)", type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Markdown(label="Related Links")
    ],
    title="TDS Virtual TA",
    description="Ask a question and optionally upload a Discourse screenshot. The virtual TA will reply!"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
