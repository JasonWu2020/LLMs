import jsonlines


def get_prompt(prompt_num, dataset, idx):
    # Base Prompt
    if prompt_num == 1:
        return ["Write code in python3.8. Only output the solution, without any explanation. \
Use the python tag and ``` to delineate start and end of a code blocks. \
You also must include code to read the input and print the solution according to the specifications. \
This is very important, as the output you provide will be directly \
sent to the server to be RUN AS CODE. Here is the problem: " + dataset[idx]]
   
    # Reason and Solve
    elif prompt_num == 2:
        return ["Reason about this follwing coding problem, but do not write any code: " + dataset[idx],
"Now, solve the problem in python3.8. Only output the solution, without any explanation. \
Use the python tag and ``` to delineate start and end of code blocks. \
You also must include code to read the input and print the solution according to the specifications. \
This is very important, as the output you provide will be directly \
sent to the server to be RUN AS CODE"]
    
    # Generate, critique
    elif prompt_num == 3:
        return ["Write code in python3.8. Only output the solution, without any explanation or tags. \
You also must include code to read the input and print the solution according to the specifications. \
This is very important, as the output you provide will be directly \
sent to the server to be RUN AS CODE. Here is the problem: " + dataset[idx],
"Critique the outputted solution, and then generate another solution adhering to the same input and output \
specifications. Use the python tag and ``` to delineate start and end of code blocks."]
    
    # Reason, Generate, Critique
    elif prompt_num == 4:
        return ["Reason about this follwing coding problem, but do not write any code: " + dataset[idx],
    "Now, solve the problem in python3.8. Only output the solution, without any explanation or tags. \
    You also must include code to read the input and print the solution according to the specifications. \
    This is very important, as the output you provide will be directly \
    sent to the server to be RUN AS CODE",
    "Critique the outputted solution, and then generate another solution adhering to the same input and output \
    specifications. Use the python tag and ``` to delineate start and end of code blocks."]

    # Simple Prompt
    elif prompt_num == 5:
        return ['Solve the problem in python:' + dataset[idx] + '\nMake sure to read input and write output. Output only code with no explanation']
    
    # Reason and Solve, Explicit, not helpful
    elif prompt_num == 6:
        return ["Reason about this follwing coding problem, but do not write any code: " + dataset[idx],
"Now, solve the following problem in python3.8:" + dataset[idx] + "\nOnly output the solution, without any explanation. \
Use the python tag and ``` to delineate start and end of code blocks. \
You also must include code to read the input and print the solution according to the specifications. \
This is very important, as the output you provide will be directly \
sent to the server to be RUN AS CODE"]

    # Reason, Generate, Critique, diff version
    elif prompt_num == 7:
        return ["Reason about this follwing coding problem, but do not write any code: " + dataset[idx],
"Now, solve the problem in python3.8.",
"Critique the outputted solution, and generate an updated solution. \
Be sure to read the input and print the solution according to the specifications. Here is the problem again: " + dataset[idx]]
    import pdb; pdb.set_trace()





def process_json(file_path='./dev.jsonl'):
    lst = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            if obj['difficulty'] < 900:
                lst.append(obj['body'] + '\nInput Specification ' + obj['input_specification'] + '\nOutput Specification' + obj['output_specification'])
    return lst


lst = process_json()
with jsonlines.open('./easy_problems.jsonl', mode='w') as handle:
    with jsonlines.open('./dev.jsonl') as reader:
        for obj in reader:
            if obj['difficulty'] < 900:
                handle.write(obj)