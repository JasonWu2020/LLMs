
python3 run_gemma_2B.py --prompt_number 1
python3 run_gemma_7B.py --prompt_number 1
python3 run_llama_1B.py --prompt_number 1
python3 run_llama_3B.py --prompt_number 1
python3 run_llama_8B.py --prompt_number 1
python3 run_qwen_1B.py --prompt_number 1
python3 run_qwen_3B.py --prompt_number 1
python3 run_qwen_7B.py --prompt_number 1
mkdir prompt_1
mv -t prompt_1 gemma_2b_results gemma_7b_results llama_1b_results llama_3b_results llama_8b_results qwen_1b_results qwen_3b_results qwen_7b_results

python3 run_gemma_2B.py --prompt_number 2
python3 run_gemma_7B.py --prompt_number 2
python3 run_llama_1B.py --prompt_number 2
python3 run_llama_3B.py --prompt_number 2
python3 run_llama_8B.py --prompt_number 2
python3 run_qwen_1B.py --prompt_number 2
python3 run_qwen_3B.py --prompt_number 2
python3 run_qwen_7B.py --prompt_number 2
mkdir prompt_2
mv -t prompt_2 gemma_2b_results gemma_7b_results llama_1b_results llama_3b_results llama_8b_results qwen_1b_results qwen_3b_results qwen_7b_results


python3 run_gemma_2B.py --prompt_number 3
python3 run_gemma_7B.py --prompt_number 3
python3 run_llama_1B.py --prompt_number 3
python3 run_llama_3B.py --prompt_number 3
python3 run_llama_8B.py --prompt_number 3
python3 run_qwen_1B.py --prompt_number 3
python3 run_qwen_3B.py --prompt_number 3
python3 run_qwen_7B.py --prompt_number 3
mkdir prompt_3
mv -t prompt_3 gemma_2b_results gemma_7b_results llama_1b_results llama_3b_results llama_8b_results qwen_1b_results qwen_3b_results qwen_7b_results


python3 run_gemma_2B.py --prompt_number 4
python3 run_gemma_7B.py --prompt_number 4
python3 run_llama_1B.py --prompt_number 4
python3 run_llama_3B.py --prompt_number 4
python3 run_llama_8B.py --prompt_number 4
python3 run_qwen_1B.py --prompt_number 4
python3 run_qwen_3B.py --prompt_number 4
python3 run_qwen_7B.py --prompt_number 4
mkdir prompt_4
mv -t prompt_4 gemma_2b_results gemma_7b_results llama_1b_results llama_3b_results llama_8b_results qwen_1b_results qwen_3b_results qwen_7b_results
