import json, sys, io
import os
import signal
from contextlib import contextmanager
import json
import ast
import builtins
from collections import Counter
class TimeoutException(Exception): pass


# # Define a custom exit function
# def safe_exit(*args, **kwargs):
#     print("exit() was called, but the program will continue.")

# # Create a safe execution context
# execution_context = {
#     "__builtins__": {**builtins.__dict__, "exit": safe_exit, "quit": safe_exit},
#     "sys": {**vars(sys), "exit": safe_exit}
# }

def extract_imports(code):
    """
    Extracts import statements from Python code using AST.
    
    Parameters:
    - code (str): The Python code to analyze.
    
    Returns:
    - dict: A dictionary with import names as keys and modules as values.
    """
    tree = ast.parse(code)
    imports = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = __import__(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = __import__(node.module, fromlist=[alias.name for alias in node.names])
            for alias in node.names:
                imports[alias.name] = getattr(module, alias.name)
    
    return imports



@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)



# Path to the JSONL file

sample_test_arr = []
with open('./test_cases.txt', 'r') as f:
      for line in f.readlines():
        if line.startswith('{'):
            sample_test_arr.append(json.loads(line))




for prompt_idx in range(1, 5):
    root_dir = './prompt_' + str(prompt_idx) + '_sanitized/'
    for model in os.listdir(root_dir):
        correct_list = [] # 1 if correct, 0 if not
        with open('./results/' + model + '.txt', 'a') as model_writer:
            model_writer.writelines(root_dir + '/')
        for i in range(22):
            print(root_dir, model, i)
            with open(root_dir + model + '/' + str(i) + '.txt', 'r') as file:
                code = file.read()

            sample_tests = sample_test_arr[i]

            
            stdin_backup, stdout_backup = sys.stdin, sys.stdout
            all_correct = True
            try: 
                this_output = sample_tests['output']
                sys.stdin = io.StringIO(sample_tests['input'].lstrip())
                sys.stdout = io.StringIO()
                with time_limit(1):
                    exec(code, {}, {})
                this_result = sys.stdout.getvalue().strip()
                sys.stdin, sys.stdout = stdin_backup, stdout_backup
                if this_result.isalpha():
                    this_result = this_result.lower()
                if this_output.isalpha():
                    this_output = this_output.lower()
                #print(this_result)
                if this_result.split() != this_output.strip().split():
                    print('Test failed: wrong answer')
                    correct_list.append(0)
                else:
                    print("Test passed")
                    correct_list.append(1)

            except SystemExit as e:
                this_result = sys.stdout.getvalue().strip()
                sys.stdin, sys.stdout = stdin_backup, stdout_backup
                if this_result.split() != this_output.strip().split():
                    correct_list.append(0)
                else:
                    correct_list.append(1)
                sys.stdin, sys.stdout = stdin_backup, stdout_backup
                print(f'Used exit function {e}')
            except TimeoutException as e:
                sys.stdin, sys.stdout = stdin_backup, stdout_backup
                print('Test failed: time limit exceeded')
                correct_list.append(0)
            except Exception as e:
                sys.stdin, sys.stdout = stdin_backup, stdout_backup
                print(f'Test failed: runtime error: {e}')
                correct_list.append(0)
            finally:
                sys.stdin, sys.stdout = stdin_backup, stdout_backup
                print('All tests completed')
                

        with open('./results/' + model + '.txt', 'a') as model_writer:
            print('Model accuracy is ', sum(correct_list), '/', len(correct_list), file=model_writer)
            print(correct_list, file=model_writer)
print("Finished")