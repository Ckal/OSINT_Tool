import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import pandas as pd

class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, max_len):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]
        inputs = self.tokenizer.encode_plus(
            row['text'],
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt'
        )
        return {
            'input_ids': inputs['input_ids'].flatten(),
            'attention_mask': inputs['attention_mask'].flatten(),
            'labels': torch.tensor(row['label'], dtype=torch.long)
        }

def train_model(model_name, train_data_path, output_dir, epochs=3, batch_size=16, max_len=128):
    # Load the dataset
    df = pd.read_csv(train_data_path)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dataset = CustomDataset(df, tokenizer, max_len)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Load the model
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(df['label'].unique()))

    # Define training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        evaluation_strategy="epoch",
        save_total_limit=2,
        save_steps=10_000,
        logging_dir=f'{output_dir}/logs',
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

if __name__ == "__main__":
    model_name = "bert-base-uncased"
    train_data_path = "data/example_dataset.csv"
    output_dir = "output"
    train_model(model_name, train_data_path, output_dir)