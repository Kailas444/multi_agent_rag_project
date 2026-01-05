import gradio as gr
from main import handle_user_query

def ui(query):
    res = handle_user_query(query)
    return res["answer"]

gr.Interface(ui, "text", "text").launch()
