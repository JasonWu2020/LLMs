from transformers import AutoModelForCausalLM, AutoTokenizer
from prep_dataset import process_json
from pathlib import Path
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--root_path",  type=str)
args = parser.parse_args()
root_path = args.root_path + '/'
sanitized_path = args.root_path + '_sanitized/'

model_name = "neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8"
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
        max_new_tokens=2000,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


for model_dir in os.listdir(root_path):
    for txt_file in os.listdir(root_path + model_dir):
        print(model_dir, txt_file)
        messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        ]
        with open(root_path + model_dir + '/' + txt_file, 'r') as handle:
            content = handle.read()
        prompt = "Given this piece of code, remove any unnecessary tags such as ``` \
or python, any explanations, and format as natural language. If there are multiple solutions, take the one specified to be the best. \
The output will be directly ran as a python file, \
so only output code with no explanation. Here is the code: " + content

        messages.append({"role": "user", "content": prompt})
        result = run_model(messages=messages)
        Path(sanitized_path + model_dir + '/').mkdir(parents=True, exist_ok=True)
        with open(sanitized_path + model_dir + '/' + txt_file, 'w') as handle:
            print(result, file=handle)

