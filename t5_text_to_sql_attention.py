# -*- coding: utf-8 -*-
"""t5_text_to_sql_attention.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CEIBMZe5hZMAx-pyoy-RrQVgdqL_PLYg
"""

pip install transformers torch seaborn matplotlib

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import seaborn as sns
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
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    # Visualize attention using seaborn heatmaps for cross-attention
    visualize_cross_attention(padded_cross_attention, input_tokens, output_tokens)

def visualize_cross_attention(cross_attention, input_tokens, output_tokens):
    num_layers = len(cross_attention)
    num_heads = cross_attention[0].shape[1]

    for layer in range(num_layers):
        for head in range(num_heads):
            attention = cross_attention[layer][0][head].detach().cpu().numpy()
            plt.figure(figsize=(10, 8))
            sns.heatmap(attention, xticklabels=input_tokens, yticklabels=output_tokens, cmap='viridis')
            plt.title(f'Layer {layer + 1}, Head {head + 1}')
            plt.xlabel('Input Tokens')
            plt.ylabel('Output Tokens')
            plt.show()

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Visualize model view attention and cross-attention heatmaps
visualize_model_view(query, schema)

"""# **FOR COMPLETE WORDS**"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import seaborn as sns
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
    cross_attention = model_output.cross_attentions

    # Convert input and output ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0].cpu().numpy())
    output_tokens = tokenizer.convert_ids_to_tokens(generated_tokens[0].cpu().numpy())

    # Decode token IDs to get complete words
    input_tokens = tokenizer.convert_tokens_to_string(input_tokens).split()
    output_tokens = tokenizer.convert_tokens_to_string(output_tokens).split()

    # Determine maximum length
    max_len = max(len(input_tokens), len(output_tokens))
    tgt_len = len(output_tokens)
    src_len = len(input_tokens)

    # Pad tokens to the same length if necessary
    input_tokens += ['<pad>'] * (max_len - len(input_tokens))
    output_tokens += ['<pad>'] * (max_len - len(output_tokens))

    # Pad attention weights
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    # Visualize cross-attention for all layers and heads
    visualize_all_cross_attention(padded_cross_attention, input_tokens, output_tokens)

def visualize_all_cross_attention(cross_attention, input_tokens, output_tokens):
    num_layers = len(cross_attention)
    num_heads = cross_attention[0].shape[1]

    for layer in range(num_layers):
        for head in range(num_heads):
            attention = cross_attention[layer][0][head].detach().cpu().numpy()
            plt.figure(figsize=(10, 8))
            sns.heatmap(attention, xticklabels=input_tokens, yticklabels=output_tokens, cmap='viridis')
            plt.title(f'Layer {layer + 1}, Head {head + 1}')
            plt.xlabel('Input Tokens')
            plt.ylabel('Output Tokens')
            plt.show()

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Visualize model view attention and cross-attention heatmaps
visualize_model_view(query, schema)

"""# **Top 3 Attention weights**"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
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

def get_top_attention_tokens(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)

    # Generate the SQL query to use as decoder input
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_attentions=True)
    generated_tokens = outputs.sequences

    # Prepare decoder inputs for the forward pass
    decoder_input_ids = torch.cat([torch.tensor([[model.config.decoder_start_token_id]]).to(model.device), generated_tokens[:, :-1]], dim=-1)

    # Perform forward pass to get attention weights
    model_output = model(input_ids=input_data, decoder_input_ids=decoder_input_ids, output_attentions=True, return_dict=True)
    cross_attention = model_output.cross_attentions

    # Convert input and output ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0].cpu().numpy())
    output_tokens = tokenizer.convert_ids_to_tokens(generated_tokens[0].cpu().numpy())

    # Decode token IDs to get complete words
    input_tokens = tokenizer.convert_tokens_to_string(input_tokens).split()
    output_tokens = tokenizer.convert_tokens_to_string(output_tokens).split()

    # Determine maximum length
    max_len = max(len(input_tokens), len(output_tokens))
    tgt_len = len(output_tokens)
    src_len = len(input_tokens)

    # Pad tokens to the same length if necessary
    input_tokens += ['<pad>'] * (max_len - len(input_tokens))
    output_tokens += ['<pad>'] * (max_len - len(output_tokens))

    # Pad attention weights
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    # Extract top attention tokens
    top_attention_tokens = extract_top_attention_tokens(padded_cross_attention, input_tokens, output_tokens)
    return top_attention_tokens

def extract_top_attention_tokens(attention, input_tokens, output_tokens):
    num_layers = len(attention)
    num_heads = attention[0].shape[1]
    top_attention_tokens = {}

    for layer in range(num_layers):
        layer_attention = []
        for head in range(num_heads):
            attn = attention[layer][0][head].detach().cpu().numpy()
            # Get top 3 attention weights and their indices
            top_indices = np.unravel_index(np.argsort(attn, axis=None)[-3:], attn.shape)
            top_values = attn[top_indices]
            # Map to tokens
            top_tokens = [(input_tokens[src_idx], output_tokens[tgt_idx], top_values[idx])
                          for idx, (tgt_idx, src_idx) in enumerate(zip(*top_indices))]
            layer_attention.append(top_tokens)
        top_attention_tokens[f'Layer {layer + 1}'] = layer_attention
    return top_attention_tokens

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Get top attention tokens
top_attention_tokens = get_top_attention_tokens(query, schema)

# Display top attention tokens
for layer, heads in top_attention_tokens.items():
    print(f"{layer}:")
    for head_idx, tokens in enumerate(heads):
        print(f"  Head {head_idx + 1}:")
        for input_token, output_token, value in tokens:
            print(f"    Input: {input_token}, Output: {output_token}, Attention Weight: {value:.4f}")

"""# **Top First Attention **"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
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

def get_top_attention_tokens(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)

    # Generate the SQL query to use as decoder input
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_attentions=True)
    generated_tokens = outputs.sequences

    # Prepare decoder inputs for the forward pass
    decoder_input_ids = torch.cat([torch.tensor([[model.config.decoder_start_token_id]]).to(model.device), generated_tokens[:, :-1]], dim=-1)

    # Perform forward pass to get attention weights
    model_output = model(input_ids=input_data, decoder_input_ids=decoder_input_ids, output_attentions=True, return_dict=True)
    cross_attention = model_output.cross_attentions

    # Convert input and output ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0].cpu().numpy())
    output_tokens = tokenizer.convert_ids_to_tokens(generated_tokens[0].cpu().numpy())

    # Decode token IDs to get complete words
    input_tokens = tokenizer.convert_tokens_to_string(input_tokens).split()
    output_tokens = tokenizer.convert_tokens_to_string(output_tokens).split()

    # Determine maximum length
    max_len = max(len(input_tokens), len(output_tokens))
    tgt_len = len(output_tokens)
    src_len = len(input_tokens)

    # Pad tokens to the same length if necessary
    input_tokens += ['<pad>'] * (max_len - len(input_tokens))
    output_tokens += ['<pad>'] * (max_len - len(output_tokens))

    # Pad attention weights
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    # Extract top attention tokens
    top_attention_tokens = extract_top_attention_tokens(padded_cross_attention, input_tokens, output_tokens)
    return top_attention_tokens

def extract_top_attention_tokens(attention, input_tokens, output_tokens):
    num_layers = len(attention)
    num_heads = attention[0].shape[1]
    top_attention_tokens = {}

    for layer in range(num_layers):
        layer_attention = []
        for head in range(num_heads):
            attn = attention[layer][0][head].detach().cpu().numpy()
            # Get the highest attention weight and its index
            top_index = np.unravel_index(np.argmax(attn, axis=None), attn.shape)
            top_value = attn[top_index]
            # Map to tokens
            input_token = input_tokens[top_index[1]]
            output_token = output_tokens[top_index[0]]
            layer_attention.append((input_token, output_token, top_value))
        top_attention_tokens[f'Layer {layer + 1}'] = layer_attention
    return top_attention_tokens

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Get top attention tokens
top_attention_tokens = get_top_attention_tokens(query, schema)

# Display top attention tokens
for layer, heads in top_attention_tokens.items():
    print(f"{layer}:")
    for head_idx, tokens in enumerate(heads):
        input_token, output_token, value = tokens
        print(f"  Head {head_idx + 1}:")
        print(f"    Input: {input_token}, Output: {output_token}, Attention Weight: {value:.4f}")

"""# **With network graph | TOP 1**"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("juierror/text-to-sql-with-table-schema")
model = AutoModelForSeq2SeqLM.from_pretrained("juierror/text-to-sql-with-table-schema")

def prepare_input(question: str, table: List[str]):
    table_prefix = "table:"
    question_prefix = "question:"
    join_table = ",".join(table)
    inputs = f"{question_prefix} {question} {table_prefix} {join_table}"
    input_ids = tokenizer(inputs, max_length=700, return_tensors="pt", truncation=True).input_ids
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

def get_top_attention_tokens(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)

    # Generate the SQL query to use as decoder input
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_attentions=True)
    generated_tokens = outputs.sequences

    # Prepare decoder inputs for the forward pass
    decoder_input_ids = torch.cat([torch.tensor([[model.config.decoder_start_token_id]]).to(model.device), generated_tokens[:, :-1]], dim=-1)

    # Perform forward pass to get attention weights
    model_output = model(input_ids=input_data, decoder_input_ids=decoder_input_ids, output_attentions=True, return_dict=True)
    cross_attention = model_output.cross_attentions

    # Convert input and output ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0].cpu().numpy())
    output_tokens = tokenizer.convert_ids_to_tokens(generated_tokens[0].cpu().numpy())

    # Decode token IDs to get complete words
    input_tokens = tokenizer.convert_tokens_to_string(input_tokens).split()
    output_tokens = tokenizer.convert_tokens_to_string(output_tokens).split()

    # Determine maximum length
    max_len = max(len(input_tokens), len(output_tokens))
    tgt_len = len(output_tokens)
    src_len = len(input_tokens)

    # Pad tokens to the same length if necessary
    input_tokens += ['<pad>'] * (max_len - len(input_tokens))
    output_tokens += ['<pad>'] * (max_len - len(output_tokens))

    # Pad attention weights
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    # Extract top attention tokens
    top_attention_tokens = extract_top_attention_tokens(padded_cross_attention, input_tokens, output_tokens)
    return top_attention_tokens

def extract_top_attention_tokens(attention, input_tokens, output_tokens):
    num_layers = len(attention)
    num_heads = attention[0].shape[1]
    top_attention_tokens = {}

    for layer in range(num_layers):
        layer_attention = []
        for head in range(num_heads):
            attn = attention[layer][0][head].detach().cpu().numpy()
            # Get the highest attention weight and its index
            top_index = np.unravel_index(np.argmax(attn, axis=None), attn.shape)
            top_value = attn[top_index]
            # Map to tokens
            input_token = input_tokens[top_index[1]]
            output_token = output_tokens[top_index[0]]
            layer_attention.append((input_token, output_token, top_value))
        top_attention_tokens[f'Layer {layer + 1}'] = layer_attention
    return top_attention_tokens

def visualize_attention_graph(top_attention_tokens):
    G = nx.DiGraph()

    # Add nodes
    for layer, heads in top_attention_tokens.items():
        for head_idx, (input_token, output_token, value) in enumerate(heads):
            input_node = f"{input_token}"
            output_node = f"{output_token}"
            G.add_edge(input_node, output_node, weight=value)

    pos = nx.spring_layout(G, seed=42)  # positions for all nodes
    edges = G.edges(data=True)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=7000, node_color="lightblue", alpha=0.9)

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        edgelist=edges,
        width=[d['weight'] * 10 for (u, v, d) in edges],
        alpha=0.6,
        edge_color="b"
    )

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", font_weight="bold")

    plt.title("Top Attention Tokens Visualization")
    plt.show()

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Get top attention tokens
top_attention_tokens = get_top_attention_tokens(query, schema)

# Visualize attention graph
visualize_attention_graph(top_attention_tokens)

"""# **Network graph with All layers and heads**"""

from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("juierror/text-to-sql-with-table-schema")
model = AutoModelForSeq2SeqLM.from_pretrained("juierror/text-to-sql-with-table-schema")

def prepare_input(question: str, table: List[str]):
    table_prefix = "table:"
    question_prefix = "question:"
    join_table = ",".join(table)
    inputs = f"{question_prefix} {question} {table_prefix} {join_table}"
    input_ids = tokenizer(inputs, max_length=700, return_tensors="pt", truncation=True).input_ids
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

def get_all_attention_tokens(question: str, table: List[str]):
    input_data = prepare_input(question=question, table=table)
    input_data = input_data.to(model.device)

    # Generate the SQL query to use as decoder input
    outputs = model.generate(inputs=input_data, num_beams=10, top_k=10, max_length=700, return_dict_in_generate=True, output_attentions=True)
    generated_tokens = outputs.sequences

    # Prepare decoder inputs for the forward pass
    decoder_input_ids = torch.cat([torch.tensor([[model.config.decoder_start_token_id]]).to(model.device), generated_tokens[:, :-1]], dim=-1)

    # Perform forward pass to get attention weights
    model_output = model(input_ids=input_data, decoder_input_ids=decoder_input_ids, output_attentions=True, return_dict=True)
    cross_attention = model_output.cross_attentions

    # Convert input and output ids to tokens
    input_tokens = tokenizer.convert_ids_to_tokens(input_data[0].cpu().numpy())
    output_tokens = tokenizer.convert_ids_to_tokens(generated_tokens[0].cpu().numpy())

    # Decode token IDs to get complete words
    input_tokens = tokenizer.convert_tokens_to_string(input_tokens).split()
    output_tokens = tokenizer.convert_tokens_to_string(output_tokens).split()

    # Determine maximum length
    max_len = max(len(input_tokens), len(output_tokens))
    tgt_len = len(output_tokens)
    src_len = len(input_tokens)

    # Pad tokens to the same length if necessary
    input_tokens += ['<pad>'] * (max_len - len(input_tokens))
    output_tokens += ['<pad>'] * (max_len - len(output_tokens))

    # Pad attention weights
    padded_cross_attention = [pad_attention_weights(layer, max_len, max_len) for layer in cross_attention]

    all_attention_tokens = extract_all_attention_tokens(padded_cross_attention, input_tokens, output_tokens)
    return all_attention_tokens

def extract_all_attention_tokens(attention, input_tokens, output_tokens):
    num_layers = len(attention)
    num_heads = attention[0].shape[1]
    all_attention_tokens = {}

    for layer in range(num_layers):
        layer_attention = []
        for head in range(num_heads):
            attn = attention[layer][0][head].detach().cpu().numpy()
            for i in range(attn.shape[0]):
                for j in range(attn.shape[1]):
                    layer_attention.append((input_tokens[j], output_tokens[i], attn[i][j]))
        all_attention_tokens[f'Layer {layer + 1}'] = layer_attention
    return all_attention_tokens

def visualize_attention_graph(all_attention_tokens):
    for layer, heads in all_attention_tokens.items():
        G = nx.DiGraph()

        # Add nodes and edges
        for input_token, output_token, value in heads:
            if value > 0.1:  # Filter to show only significant weights
                G.add_edge(input_token, output_token, weight=value)

        pos = nx.spring_layout(G, seed=42)  # positions for all nodes
        edges = G.edges(data=True)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=7000, node_color="lightblue", alpha=0.9)

        # Draw edges
        nx.draw_networkx_edges(
            G, pos,
            edgelist=edges,
            width=[d['weight'] * 10 for (u, v, d) in edges],
            alpha=0.6,
            edge_color="b"
        )

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", font_weight="bold")

        plt.title(f"Attention Visualization for {layer}")
        plt.show()

# Example usage
schema = ["id", "name", "age", "location"]
query = "get people name with age greater than 25 and name is mehdi and lives in karachi"
sql_query = inference(question=query, table=schema)
print(f"The generated SQL query is: {sql_query}")

# Get all attention tokens
all_attention_tokens = get_all_attention_tokens(query, schema)

# Visualize attention graph
visualize_attention_graph(all_attention_tokens)