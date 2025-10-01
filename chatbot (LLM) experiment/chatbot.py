import os
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# === CONFIG ===
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
HISTORY_FILE = "chat_history.json"
SUMMARY_FILE = "summary.txt"
DOCS_FOLDER = "docs"
MAX_TOKENS = 2048
SYSTEM_PROMPT = "<|system|>\nYou are Melody Quinn, a sassy, brilliant young woman who is in love with you, and who never hesitates to speak her mind.\n"

# === Load Model and Tokenizer ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float32)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# === Load or Create History ===
def load_memory():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"summary": SYSTEM_PROMPT.strip(), "recent": []}

def save_memory(memory):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def truncate_recent(recent, max_tokens):
    temp = [memory["summary"]] + recent
    while True:
        prompt = "\n".join(temp)
        input_ids = tokenizer(prompt, return_tensors="pt", truncation=False).input_ids
        if input_ids.shape[-1] <= max_tokens:
            return recent
        if len(recent) > 1:
            recent = recent[1:]  # Trim oldest
            temp = [memory["summary"]] + recent
        else:
            break
    return recent

# === Document Ingestion ===
def ingest_documents():
    if not os.path.exists(DOCS_FOLDER):
        return []
    chunks = []
    for fname in os.listdir(DOCS_FOLDER):
        path = os.path.join(DOCS_FOLDER, fname)
        if fname.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                parts = [text[i:i+1000] for i in range(0, len(text), 1000)]
                for part in parts:
                    chunks.append(part.strip())
    return chunks

def summarize_text(text):
    prompt = SYSTEM_PROMPT.strip() + f"\n<|user|>\nSummarize the following in a way Melody can use later:\n{text}\n<|assistant|>"
    input_ids = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(
        **input_ids,
        max_new_tokens=150,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    return result[len(prompt):].strip().split("<|user|>")[0].strip()

memory = load_memory()
print("Melody is loaded with memory and document support! Type 'exit', 'reset', or 'ingest'.\n")

# === Chat Loop ===
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    elif user_input.lower() == "reset":
        print("Memory wiped.")
        memory = {"summary": SYSTEM_PROMPT.strip(), "recent": []}
        save_memory(memory)
        continue
    elif user_input.lower() == "ingest":
        chunks = ingest_documents()
        for chunk in chunks:
            summary = summarize_text(chunk)
            memory["summary"] += f"\n{summary}"
        print("Documents summarized and added to Melody's memory.")
        save_memory(memory)
        continue

    memory["recent"].append(f"<|user|>\n{user_input}\n<|assistant|>")
    memory["recent"] = truncate_recent(memory["recent"], MAX_TOKENS)
    prompt = memory["summary"] + "\n" + "\n".join(memory["recent"])

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    response_text = response[len(prompt):].strip().split("<|user|>")[0].strip()

    print(f"Melody: {response_text}")
    memory["recent"].append(response_text)
    save_memory(memory)
