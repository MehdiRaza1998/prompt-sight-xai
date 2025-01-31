# -*- coding: utf-8 -*-
"""t5_text_to_sql_LIME.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ES9e49-o-Eoyysezqr-V1gNxL34jfaSN
"""

pip install lime transformers torch

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from lime.lime_text import LimeTextExplainer
import matplotlib.pyplot as plt
import numpy as np

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("juierror/text-to-sql-with-table-schema")
model = AutoModelForSeq2SeqLM.from_pretrained("juierror/text-to-sql-with-table-schema")

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from lime.lime_text import LimeTextExplainer
import matplotlib.pyplot as plt
import numpy as np

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("juierror/text-to-sql-with-table-schema")
model = AutoModelForSeq2SeqLM.from_pretrained("juierror/text-to-sql-with-table-schema")

def prepare_input(question: str, table: List[str]):
    table_prefix = "table:"
    question_prefix = "question:"
    join_table = ",".join(table)
    inputs = f"{question_prefix} {question} {table_prefix} {join_table}"
    input_ids = tokenizer(inputs, max_length=700, return_tensors="pt").input_ids
    return input_ids

def inference_with_probs(question: str, table: List[str]) -> tuple:
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_scores=True)
    result = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
    probs = torch.exp(outputs.sequences_scores[0])
    return result, probs

def lime_explain(question: str, table: List[str]):
    # Define a function that takes a list of questions and returns the probabilities
    def predict_probs(questions):
        probs_list = []
        for i, q in enumerate(questions):
            print(f"Processing sample {i+1}/{len(questions)}")  # Print progress
            _, probs = inference_with_probs(q, table)
            probs_list.append(probs.detach().cpu().numpy())
        return np.array(probs_list).reshape(-1, 1)  # Ensure 2-dimensional array

    # Create a LIME explainer
    explainer = LimeTextExplainer(class_names=["SQL_query"])

    # Explain the prediction for the given question
    exp = explainer.explain_instance(question, predict_probs, num_features=6, num_samples=462, labels=(0,))  # Increase num_samples

    # Print the explanation
    print(exp.as_list(label=0))  # Specify the label index

    # Show the explanation using a static plot
    fig, ax = plt.subplots(figsize=(10, 6))
    exp.show_in_notebook(text=question)  # Use show_in_notebook for Colab
    exp.as_pyplot_figure(label=0)  # Use as_pyplot_figure for static plots
    plt.show()

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"

# LIME explanation
lime_explain(query, schema)

"""LIME for text to text"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from lime.lime_text import LimeTextExplainer
import numpy as np
import matplotlib.pyplot as plt

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("juierror/text-to-sql-with-table-schema")
model = AutoModelForSeq2SeqLM.from_pretrained("juierror/text-to-sql-with-table-schema")

def prepare_input(question: str, table: List[str]):
    table_prefix = "table:"
    question_prefix = "question:"
    join_table = ",".join(table)
    inputs = f"{question_prefix} {question} {table_prefix} {join_table}"
    input_ids = tokenizer(inputs, max_length=700, return_tensors="pt").input_ids
    return input_ids

def generate_sequence_with_probs(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_scores=True)
    result = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)

    # Use the forward method to obtain token-level probabilities
    with torch.no_grad():
        outputs = model(input_ids=input_data, decoder_input_ids=outputs.sequences)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1)
        probs = probs.max(dim=-1).values

    print(f"Generated sequence: {result}")
    print(f"Probabilities shape: {probs.shape}")
    return result, probs

def custom_predict_fn(questions):
    all_probs = []
    max_length = 0

    # First pass to determine the maximum length of the probs tensors
    for i, question in enumerate(questions):
        print(f"Processing sample {i+1}/{len(questions)}")  # Print progress
        _, probs = generate_sequence_with_probs(question, schema)
        max_length = max(max_length, probs.shape[1])

    # Second pass to pad the probs tensors to the maximum length
    for i, question in enumerate(questions):
        _, probs = generate_sequence_with_probs(question, schema)
        padded_probs = torch.zeros((1, max_length))
        padded_probs[:, :probs.shape[1]] = probs
        all_probs.append(padded_probs.detach().cpu().numpy().flatten())  # Flatten the probs array

    all_probs = np.array(all_probs)
    print(f"All probabilities shape: {all_probs.shape}")
    return all_probs

def lime_explain(question: str, table: List[str]):
    explainer = LimeTextExplainer()
    exp = explainer.explain_instance(question, custom_predict_fn, num_features=6, num_samples=5)  # Remove the labels parameter
    print(exp.as_list())  # Print the explanation

    # Plot the explanation
    fig, ax = plt.subplots(figsize=(10, 6))
    exp.show_in_notebook(text=question)
    plt.show()

# Example usage
schema = ["id", "name", "age", "location"]
query = "give me user names"

# LIME explanation
lime_explain(query, schema)