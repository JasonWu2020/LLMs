from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from prep_dataset import process_json, get_prompt
from pathlib import Path
import argparse 
from huggingface_hub import login
#login()

parser = argparse.ArgumentParser()
parser.add_argument("--prompt_number",  type=int, default=1)
args = parser.parse_args()
model_name = "meta-llama/Llama-3.2-3B-Instruct"
dataset = process_json()

model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    device_map="auto",
    #attn_implementation="flash_attention_2"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def run_model(messages):
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=5000,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

for i in range(len(dataset)):
    print("Finished", i, "Total", len(dataset))
    messages = [
    {"role": "system", "content": "You are a helpful assistant."},  
    ]
    prompts = get_prompt(args.prompt_number, dataset, i)
    for prompt in prompts:
        messages.append({"role": "user", "content": prompt})
        response = run_model(messages)
        messages.append({"role":"model", "content":response})
    Path("./llama_3b_results/").mkdir(parents=True, exist_ok=True)
    with open('./llama_3b_results/' + str(i) + '.txt', 'w') as handle:
        print(response, file=handle)
