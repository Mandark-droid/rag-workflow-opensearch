import gradio as gr
from query_handler import answer_query


def rag_interface(user_input):
    return answer_query(user_input)


iface = gr.Interface(
    fn=rag_interface,
    inputs=gr.Textbox(lines=2, placeholder="Ask anything..."),
    outputs=gr.Textbox(lines=10),
    title="Real-Time RAG with OpenSearch & Qwen2.5",
    description="Type your question and get answers based on your docs indexed in OpenSearch."
)

if __name__ == '__main__':
    iface.launch()
