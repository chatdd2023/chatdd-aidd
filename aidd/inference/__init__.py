from aidd.inference.cnn import MolCNN, ProtCNN
from aidd.inference.gnn_graphmvp import GraphMVP
from aidd.inference.mcnn import MCNN
from aidd.inference.mgnn import MGNN

SUPPORTED_MOL_ENCODER = {
    "cnn": MolCNN,
    "graphmvp": GraphMVP,
    "mgnn": MGNN,
}

SUPPORTED_PROTEIN_ENCODER = {
    "cnn": ProtCNN,
    "mcnn": MCNN
}



