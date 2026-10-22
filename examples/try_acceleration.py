import torch

from trajectory_ops import trajectory_acceleration

positions = torch.tensor([0.0, 1.0, 8.0, 27.0, 64.0], dtype=torch.float32)
acceleration = trajectory_acceleration(positions)

print("positions:", positions)
print("acceleration:", acceleration)
