import requests
import json
import gradio as gr

url="http://localhost:11434/api/generate"

headers={

    'Content-Type':'application/json'
}

history=[]

def generate_response(prompt):
    history.append(prompt)
    final_prompt="\n".join(history)

    data={
        "model":"codeassist",
        "prompt":final_prompt,
        "stream":False
    }

    response=requests.post(url,headers=headers,data=json.dumps(data))

    print("History==",history,final_prompt)
    print("respon==========",response)

    if response.status_code==200:
        response=response.text
        data=json.loads(response)
        actual_response=data['response']
        return actual_response
    else:
        print("error:",response.text)

# outputs = gr.Textbox(
#     lines=18,
#     label="LLM Response",
#     interactive=False
# )

# interface=gr.Interface(
#     fn=generate_response,
#     inputs=gr.Textbox(lines=4,placeholder="Enter your Prompt"),
#     outputs=gr.Textbox(lines=15)
# )
# interface.launch()

with gr.Blocks() as demo:
    gr.Markdown("## Code Assistant")

    with gr.Row():
        with gr.Column(scale=1):
            prompt = gr.Textbox(
                lines=6,
                label="Prompt",
                placeholder="Enter your prompt"
            )
            submit = gr.Button("Submit")

        with gr.Column(scale=1):
            output = gr.Textbox(
                lines=25,
                label="Output",
                interactive=False
            )

    submit.click(
        fn=generate_response,
        inputs=prompt,
        outputs=output
    )

demo.launch()
