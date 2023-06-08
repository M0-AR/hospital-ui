import pandas as pd

# Load data into a pandas dataframe
data = pd.read_csv("test.txt")

# Preprocessing the data
data = data.dropna()  # remove missing values
data = data.drop_duplicates()  # remove duplicate values
data = data.sample(frac=1)  # shuffle the data

import transformers
from transformers import AutoTokenizer

# Instantiate a tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

# Tokenize the text
text = data['text'].values
tokenized_text = tokenizer(text, padding=True, truncation=True)

from transformers import AutoModelWithLMHead

# Instantiate a model
model = AutoModelWithLMHead.from_pretrained("distilgpt2")

from transformers import TrainingArguments, Trainer

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='steps',
    eval_steps=1000,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=1,
    save_steps=1000,
    save_total_limit=2
)

# Instantiate a trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_text,
    eval_dataset=tokenized_text
)

# Train the model
trainer.train()

from transformers import EvalPrediction

# Evaluate the model
eval_result = trainer.evaluate()

# Extract the perplexity score
perplexity = eval_result['perplexity']

# Extract the BLEU score
bleu_score = eval_result['bleu']


from transformers import pipeline

# Instantiate a text generation pipeline
text_generator = pipeline("text-generation", model=model)

# Generate text
generated_text = text_generator("The brown fine fox jumps over the lazy frog.", max_length=100)

