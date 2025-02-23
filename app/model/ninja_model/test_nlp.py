import sys
import os
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# ✅ Ensure Python knows where to find the `app` package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

def load_model_and_tokenizer(model_name="gpt2"):
    """✅ Load GPT-2 model and tokenizer"""
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as padding
    return model, tokenizer

def load_data_from_txt(file_path, max_entries=250):  # 🔥 Reduce max dataset size
    """✅ Read ninja logs from a .txt file in smaller chunks"""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

    if len(lines) < 10:
        raise ValueError("❌ Error: Not enough data in log_ninja_training_data.txt!")

    lines = lines[:max_entries]  # 🔥 Limit dataset size to 250 instead of 500
    train_size = int(len(lines) * 0.8)
    return lines[:train_size], lines[train_size:]

def tokenize_data(tokenizer, training_data, validation_data, max_length=30):  
    """✅ Tokenize data and add labels for training"""
    train_encodings = tokenizer(training_data, truncation=True, padding=True, max_length=max_length)
    val_encodings = tokenizer(validation_data, truncation=True, padding=True, max_length=max_length)

    # 🔥 Add labels (same as input_ids) for loss computation
    train_encodings["labels"] = train_encodings["input_ids"].copy()
    val_encodings["labels"] = val_encodings["input_ids"].copy()

    return train_encodings, val_encodings

def create_datasets(train_encodings, val_encodings):
    """✅ Convert tokenized data into a Hugging Face Dataset"""
    train_dataset = Dataset.from_dict({
        "input_ids": torch.tensor(train_encodings["input_ids"]),
        "attention_mask": torch.tensor(train_encodings["attention_mask"]),
        "labels": torch.tensor(train_encodings["labels"])  # 🔥 Include labels
    })
    val_dataset = Dataset.from_dict({
        "input_ids": torch.tensor(val_encodings["input_ids"]),
        "attention_mask": torch.tensor(val_encodings["attention_mask"]),
        "labels": torch.tensor(val_encodings["labels"])  # 🔥 Include labels
    })
    return train_dataset, val_dataset

def train_model(model, train_dataset, val_dataset):
    """✅ Train the model"""
    use_fp16 = torch.cuda.is_available()  # ✅ Only enable FP16 if a GPU is available

    training_args = TrainingArguments(
        output_dir="./log_ninja_trained",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        save_steps=500,
        save_total_limit=2,
        eval_strategy="steps",
        eval_steps=500,
        logging_dir="./logs",
        fp16=use_fp16,  # ✅ Prevents crashes on CPU, optimizes GPU training
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    trainer.train()
    return trainer

def save_model_and_tokenizer(model, tokenizer, save_directory):
    """✅ Save fine-tuned model and tokenizer"""
    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)

def main():
    model, tokenizer = load_model_and_tokenizer()
    
    # ✅ Load Data from TXT instead of function
    training_data, validation_data = load_data_from_txt("/home/bruce/knife_spider/loggiedaemon/LogNinja/app/data/log_ninja_data.txt")
    
    train_encodings, val_encodings = tokenize_data(tokenizer, training_data, validation_data)
    train_dataset, val_dataset = create_datasets(train_encodings, val_encodings)
    trainer = train_model(model, train_dataset, val_dataset)

    # ✅ Save the fine-tuned model
    save_model_and_tokenizer(model, tokenizer, "/home/bruce/knife_spider/loggiedaemon/LogNinja/app/model/ninja_model_finetuned")
    
    print("✅ Training completed! Log Ninja now understands system health.")

if __name__ == "__main__":
    main()
