import streamlit as st
import torch
from torch.nn import Module, Linear, CrossEntropyLoss
from transformers import GPT2Config, GPT2Model

DEVICE = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


class GPT2Generator(Module):
    def __init__(self, bos_token_id, eos_token_id, pad_index, vocab_size, n_layer, device):
        super().__init__()
        self.config = GPT2Config(bos_token_id=bos_token_id, eos_token_id=eos_token_id, vocab_size=vocab_size,
                                 n_layer=n_layer)
        self.pad_index = pad_index
        self.gpt = GPT2Model(self.config)
        self.lm_head = Linear(self.config.n_embd, self.config.vocab_size, bias=False)
        self.loss = CrossEntropyLoss(ignore_index=self.pad_index)
        self.device = device
        self.to(self.device)
        self._step = 1
        self.max_len = 30

    def forward(self, batch, label):
        pred_size = label.shape[-1]
        batch = self.gpt(batch)
        batch = batch.last_hidden_state[:, -pred_size:, :]
        batch = self.lm_head(batch)
        batch = batch.swapaxes(1, 2)
        batch = batch[:, :, :-1]
        label = label[:, 1:]
        return self.loss(batch, label)

    def generate(self, batch, max_len=30):
        if not batch:
            return []
        batch = batch + [self.config.bos_token_id]
        input_length = len(batch)

        for _ in range(max_len):
            input_tensor = torch.tensor(batch, device=self.device).reshape((1, -1))

            input_tensor = self.gpt(input_tensor)
            input_tensor = input_tensor.last_hidden_state
            input_tensor = self.lm_head(input_tensor)

            next_token = torch.argmax(input_tensor[:, -1, :], axis=-1).item()

            if next_token == self.config.eos_token_id:
                return batch

            batch.append(next_token)

        return batch[input_length:]

    def set_max_len(self, max_len):
        self.max_len = max_len

    def step_generate(self, batch=None, top_k=5):
        if batch is None:
            batch = []
        self._step += 1
        batch = [self.config.bos_token_id] + batch
        input_tensor = torch.tensor(batch, device=self.device).reshape((1, -1))

        input_tensor = self.gpt(input_tensor)
        input_tensor = input_tensor.last_hidden_state
        input_tensor = self.lm_head(input_tensor)

        _, indices = torch.topk(input_tensor[:, -1, :], k=top_k)
        indices = torch.squeeze(indices)
        return indices.tolist()


@st.cache
def get_model():
    pad_token_id = 0
    bos_token_id = 392
    eos_token_id = 393
    vocab_size = 394

    return GPT2Generator(
        bos_token_id, eos_token_id, pad_index=pad_token_id,
        vocab_size=vocab_size, n_layer=2, device=DEVICE
    )

