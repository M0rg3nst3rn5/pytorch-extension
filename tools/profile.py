import torch

from trajectory_ops import trajectory_acceleration

values = torch.randn(1024, 7, 500, dtype=torch.float32)
trajectory_acceleration(values)
