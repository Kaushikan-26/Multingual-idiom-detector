import json
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from torch.utils.data import Dataset
from tqdm import tqdm

DATA_DIR = "Gemma"          # <--- your folder name
MODEL_DIR = "trained_idiom_model"


# ===== Custom Dataset Loader =====
class IdiomDataset(Dataset):
    def __init__(self, tokenizer):
        self.samples = []
        self.tokenizer = tokenizer

        print("Loading JSON files from:", DATA_DIR)

        for file in tqdm(os.listdir(DATA_DIR)):
            if file.endswith(".json"):
                path = os.path.join(DATA_DIR, file)

                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Each file contains a list of idioms
                if isinstance(data, list):
                    for item in data:
                        idiom = item.get("idiom", "")
                        meaning = item.get("meaning", "")
                        example = item.get("example", "")

                        text = (
                            f"Idiom: {idiom}\n"
                            f"Meaning: {meaning}\n"
                            f"Example: {example}\n"
                            f"###\n"
                        )
                        self.samples.append(text)

                # Single idiom in file
                if isinstance(data, dict):
                    idiom = data.get("idiom", "")
                    meaning = data.get("meaning", "")
                    example = data.get("example", "")

                    text = (
                        f"Idiom: {idiom}\n"
                        f"Meaning: {meaning}\n"
                        f"Example: {example}\n"
                        f"###\n"
                    )
                    self.samples.append(text)

        print(f"Total training samples: {len(self.samples)}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        enc = self.tokenizer(
            self.samples[idx],
            truncation=True,
            max_length=256,
            padding="max_length",
            return_tensors="pt"
        )
        return {
            "input_ids": enc["input_ids"].squeeze(),
            "attention_mask": enc["attention_mask"].squeeze(),
            "labels": enc["input_ids"].squeeze()
        }


# ===== Training Script =====
def main():
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
    tokenizer.pad_token = tokenizer.eos_token

    model = GPT2LMHeadModel.from_pretrained("distilgpt2")

    dataset = IdiomDataset(tokenizer)

    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        save_steps=300,
        save_total_limit=2,
        logging_steps=50
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    print("🚀 Training started...")
    trainer.train()

    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print("🎉 Training complete. Model saved at:", MODEL_DIR)


if __name__ == "__main__":
    main()
