from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from prep_dataset import process_json, get_prompt
from pathlib import Path
import argparse 
import argparse 
from huggingface_hub import login

#login()

parser = argparse.ArgumentParser()
parser.add_argument("--prompt_number",  type=int, default=1)
args = parser.parse_args()

parser = argparse.ArgumentParser()
parser.add_argument("--prompt_number",  type=int, default=1)
args = parser.parse_args()
model_name_or_path = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"
# To use a different branch, change revision
# For example: revision="gptq-4bit-32g-actorder_True"
model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             revision="main")

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
dataset = process_json()
for i in range(len(dataset)):
    print("Finished", i, "Total", len(dataset))
    prompts = get_prompt(args.prompt_number, dataset, i)
    memory = ""
    for prompt in prompts:
        #print("User Prompt: ", prompt)
        prompt_template=f'''<s>[INST] {prompt} [/INST]'''
        memory += prompt_template
        input_ids = tokenizer(memory, return_tensors='pt').input_ids.cuda()
        output = model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=5000)
        output_text = tokenizer.decode(output[0])
        last_index = output_text.rfind('[/INST]')
        output_text = output_text[last_index:]
        memory += output_text
    Path("./mistral_7b_results/").mkdir(parents=True, exist_ok=True)
    with open('./mistral_7b_results/' + str(i) + '.txt', 'w') as handle:
        print(output_text, file=handle)

