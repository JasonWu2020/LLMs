import re
import argparse
import os
from pathlib import Path
def extract_python_code(document):
    """
    Extract Python code blocks between START_OF_CODE and END_OF_CODE tags,
    excluding any markdown or code formatting tags like ``` or `python`.
    """
    # Find all code blocks between START_OF_CODE and END_OF_CODE
    code_blocks = re.findall(r"<START_OF_CODE>\s*(.*?)\s*<END_OF_CODE>", document, re.DOTALL)
    # Remove any markdown or code formatting tags
    sanitized_blocks = [re.sub(r"```.*?(\n|$)", "", block).strip() for block in code_blocks]
    # Join all blocks with double newlines
    return "\n\n".join(sanitized_blocks).strip()



parser = argparse.ArgumentParser()
parser.add_argument("--root_path",  type=str)
args = parser.parse_args()
root_path = args.root_path + '/'
sanitized_path = args.root_path + '_sanitized/'


for model_dir in os.listdir(root_path):
    for txt_file in os.listdir(root_path + model_dir):
        with open(root_path + model_dir + '/' + txt_file, 'r') as handle:
            content = handle.read()
        result = extract_python_code(content)
        Path(sanitized_path + model_dir + '/').mkdir(parents=True, exist_ok=True)
        with open(sanitized_path + model_dir + '/' + txt_file, 'w') as handle:
            print(result, file=handle)

