import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# Load tokenizer & model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Load training data
def load_dataset(filepath):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=filepath,
        block_size=128
    )

dataset = load_dataset("log_ninja_data.txt")
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./ninja_model",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=2
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
)

# Train the model
trainer.train()

# Save trained model
model.save_pretrained("./ninja_model")
tokenizer.save_pretrained("./ninja_model")

print("✅ Training complete! Model saved to ./ninja_model")
