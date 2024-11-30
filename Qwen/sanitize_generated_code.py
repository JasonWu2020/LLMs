import re
import argparse
import os
from pathlib import Path
def extract_python_code(document):
    # Find all code blocks between START_OF_CODE and END_OF_CODE
    blocks = re.split(r'```python', document)
    extracted_code = []

    for block in blocks[1:]:  # Skip the first split segment as it is before the first ```python
        # Find the end of the current block
        end_index = block.find("```")
        if end_index != -1:
            # Extract content before the closing ```
            code = block[:end_index].strip()
            # Append the code if it's non-empty
            if code:
                extracted_code.append(code)

    # Combine extracted blocks with a newline separator
    result = "\n\n".join(extracted_code)
    return result.replace('python\n', "")





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

