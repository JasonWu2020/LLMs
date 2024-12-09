# Setting up the Environment

1. Create a virtual environment with Python 3.10, preferably through conda
2. Run ```pip3 install -r requirements.txt```
3. Go to the HuggingFace page for each of the models as specified by the model name
4. Apply for verification on models that require it
5. Uncomment the login() command and run the python script. This will download the model checkpoints to your local device. 


# Running all the models
We can select which model we want to evaluate by running the appropriate python file. Specify which prompt to test with the ```--prompt_number`` command. For instance to run the Llama 8B model on prompt 3, run
```
python3 run_llama_8B.py --prompt_number 3
```
The output will be saved in a folder with the model name. 

Use the bash script ```run_models_all_prompts.sh``` to run all models and prompts. This script will create different folders for each prompt, in which it will store the output of each model.

# Processing the Output

1. We must first sanitize the output. Use the ```sanitize_generated_code.py``` file to extract only the code blocks. This script takes an entire prompt folder, and creates a sanitized version of the folder. 
2. Run the command with ```python3 sanitize_generated_code.py --root_path ./path_to_prompt_folder```
3. To submit the results, use the ```submit_local.py``` function. Change the root_dir path to where the ```prompt_X_sanitized``` are located, and create an empty ```results`` folder for it to write into. 