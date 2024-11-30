# pip install bitsandbytes accelerate
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from prep_dataset import process_json, get_prompt
from pathlib import Path
import argparse
#login()

parser = argparse.ArgumentParser()
parser.add_argument("--prompt_number",  type=int, default=1)
args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it", device_map="cuda")
dataset = process_json()
user_prompt_prefix = '<bos><start_of_turn>user\n'
user_prompt_suffix = '<end_of_turn>\n<start_of_turn>model\n'


for i in range(len(dataset)):
    print("Finished", i, "Total", len(dataset))
    memory = ""
    prompts = get_prompt(args.prompt_number, dataset, i)
    for prompt in prompts:
        #print("User prompt:", prompt)
        memory += user_prompt_prefix + prompt + user_prompt_suffix
    
        input_ids = tokenizer.encode(memory, add_special_tokens=False, return_tensors="pt").to("cuda")
        outputs = model.generate(input_ids, max_length=5000, do_sample=True)
        output_text = tokenizer.decode(outputs[0])
        last_index = output_text.rfind('<start_of_turn>model\n')
        output_text = output_text[last_index:]
        memory += output_text + '<end_of_turn>\n'
    Path("./gemma_2b_results/").mkdir(parents=True, exist_ok=True)
    with open('./gemma_2b_results/' + str(i) + '.txt', 'w') as handle:
        print(output_text, file=handle)


