import torch
import torch.nn as nn
import json
from transformers import AutoModel

from aidd.inference import SUPPORTED_MOL_ENCODER

activation = {
    "sigmoid": nn.Sigmoid(),
    "softplus": nn.Softplus(),
    "relu": nn.ReLU(),
    "gelu": nn.GELU(),
    "tanh": nn.Tanh(),
}


class MLP(nn.Module):
    def __init__(self, config, input_dim, output_dim):
        super(MLP, self).__init__()
        self.model = nn.Sequential()
        hidden_dims = [input_dim] + config["hidden_size"] + [output_dim]
        for i in range(len(hidden_dims) - 1):
            self.model.append(nn.Linear(hidden_dims[i], hidden_dims[i + 1]))
            if i != len(hidden_dims) - 2:
                self.model.append(nn.Dropout(config["dropout"]))
                if config["activation"] != "none":
                    self.model.append(activation[config["activation"]])
                if config["batch_norm"]:
                    self.model.append(nn.BatchNorm1d())
    
    def forward(self, h):
        return self.model(h)


# TODO: choose header for different encoder
HEAD4ENCODER = {
    "deepeik": MLP,
    "momu": nn.Linear,
    "molfm": nn.Linear,
    "molclr": nn.Linear,
    "graphmvp": nn.Linear,
    "biomedgpt-1.6b": nn.Linear,
    "kvplm": MLP
}


class DPModel(nn.Module):

    def __init__(self, config, out_dim):
        super(DPModel, self).__init__()
        # prepare model
        if config["model"] == "DeepEIK":
            self.encoder = SUPPORTED_MOL_ENCODER[config["model"]](config["network"])
        else:
            self.encoder = SUPPORTED_MOL_ENCODER[config["model"]](config["network"]["structure"])
        encoder_ckpt = config["network"]["structure"]["init_checkpoint"]
        if encoder_ckpt != "":
            ckpt = torch.load(encoder_ckpt, map_location="cpu")
            param_key = config["network"]["structure"]["param_key"]
            if param_key != "":
                ckpt = ckpt[param_key]
                missing_keys, unexpected_keys = self.encoder.load_state_dict(ckpt, strict=False)
                print("missing_keys: ", missing_keys)
                print("unexpected_keys: ", unexpected_keys)
            
        self.proj_head = HEAD4ENCODER[config["network"]["structure"]["name"]](self.encoder.output_dim, out_dim)
        
    def forward(self, drug):
        h = self.encoder.encode_mol(drug, proj=False, return_node_feats=False)  # encoder_struct
        return self.proj_head(h)
    
