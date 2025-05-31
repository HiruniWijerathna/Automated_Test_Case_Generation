from transformers import AutoTokenizer, AutoModelForCausalLM
import os

MODEL_NAME = "microsoft/CodeGPT-small-py"
MODEL_DIR = "models"

def load_model():
    local_dir = os.path.join(MODEL_DIR, MODEL_NAME.replace("/", "-"))

    if not os.path.exists(local_dir):
        print("Downloading model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        os.makedirs(local_dir, exist_ok=True)
        tokenizer.save_pretrained(local_dir)
        model.save_pretrained(local_dir)
    else:
        tokenizer = AutoTokenizer.from_pretrained(local_dir)
        model = AutoModelForCausalLM.from_pretrained(local_dir)

    return tokenizer, model
