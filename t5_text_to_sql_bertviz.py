# -*- coding: utf-8 -*-
"""t5_text_to_sql_bertviz.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pDzGxNj0T8i8z9sWkTS03xOYdcinUxPj
"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

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

def inference(question: str, table: List[str]) -> str:
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

"""## BERTVIZ With same inputs done"""

pip install bertviz

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from bertviz import head_view

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

def inference(question: str, table: List[str]) -> str:
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

def visualize_attention(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)

    # Generate the SQL query to use as decoder input
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_attentions=True)
    generated_tokens = outputs.sequences

    # Prepare decoder inputs for the forward pass
    decoder_input_ids = torch.cat([torch.tensor([[model.config.decoder_start_token_id]]).to(model.device), generated_tokens[:, :-1]], dim=-1)

    # Perform forward pass to get attention weights
    model_output = model(input_ids=input_data, decoder_input_ids=decoder_input_ids, output_attentions=True, return_dict=True)
    attention = model_output.encoder_attentions  # Get encoder attention weights

    # Convert input ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0])

    # Visualize attention
    head_view(
            attention,
            tokens=input_tokens
        )

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Visualize attention
visualize_attention(query, schema)

"""# BertViz same with Model_view"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from bertviz import model_view

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

def inference(question: str, table: List[str]) -> str:
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

def pad_attention_weights(attention, tgt_len, src_len):
    padded_attention = []
    for layer_attention in attention:
        # Pad each head's attention matrix
        layer_attention_padded = torch.nn.functional.pad(
            layer_attention,
            (0, src_len - layer_attention.shape[-1], 0, tgt_len - layer_attention.shape[-2]),
            value=0
        )
        padded_attention.append(layer_attention_padded)
    return torch.stack(padded_attention)

def visualize_model_view(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)

    # Generate the SQL query to use as decoder input
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_attentions=True)
    generated_tokens = outputs.sequences

    # Prepare decoder inputs for the forward pass
    decoder_input_ids = torch.cat([torch.tensor([[model.config.decoder_start_token_id]]).to(model.device), generated_tokens[:, :-1]], dim=-1)

    # Perform forward pass to get attention weights
    model_output = model(input_ids=input_data, decoder_input_ids=decoder_input_ids, output_attentions=True, return_dict=True)
    encoder_attention = model_output.encoder_attentions
    decoder_attention = model_output.decoder_attentions
    cross_attention = model_output.cross_attentions

    # Convert input and output ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0].cpu().numpy())
    output_tokens = tokenizer.convert_ids_to_tokens(generated_tokens[0].cpu().numpy())

    # Determine maximum length
    max_len = max(len(input_tokens), len(output_tokens))
    tgt_len = len(output_tokens)
    src_len = len(input_tokens)

    # Pad tokens to the same length if necessary
    input_tokens += ['<pad>'] * (max_len - len(input_tokens))
    output_tokens += ['<pad>'] * (max_len - len(output_tokens))

    # Pad attention weights
    padded_encoder_attention = [pad_attention_weights(layer, max_len, max_len) for layer in encoder_attention]
    padded_decoder_attention = [pad_attention_weights(layer, max_len, max_len) for layer in decoder_attention]
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    print(padded_encoder_attention[0].shape)
    print(padded_decoder_attention[0].shape)
    print(padded_cross_attention[0].shape)

    # Visualize attention using model_view
    model_view(
        encoder_attention=padded_encoder_attention,
        decoder_attention=padded_decoder_attention,
        cross_attention=padded_cross_attention,
        encoder_tokens=input_tokens,
        decoder_tokens=output_tokens
    )

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Visualize model view attention
visualize_model_view(query, schema)