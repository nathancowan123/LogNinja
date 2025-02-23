from transformers import GPT2LMHeadModel, GPT2Tokenizer

# ✅ Load a pre-trained GPT-2 model (Base Model)
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# ✅ Define path to save the model
save_path = "/home/bruce/knife_spider/loggiedaemon/LogNinja/app/model/ninja_model"

# ✅ Save the model & tokenizer
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"✅ Model saved successfully at {save_path}!")
