import pytest
import torch

from trajectory_ops import trajectory_acceleration


def specification(values):
    return torch.diff(values, n=2, dim=-1)

def test_input_dtype():
    values = [0.0, 1.0, 8.0]
    assert trajectory_acceleration(values).dtype != torch.float32

def test_output_shape():
    values = torch.zeros((2, 3, 7), dtype=torch.float32)
    assert trajectory_acceleration(values).shape == (2, 3, 5)


def test_output_dtype():
    values = torch.tensor([0.0, 1.0, 8.0], dtype=torch.float32)
    assert trajectory_acceleration(values).dtype == torch.float32


def test_exact_numeric_values_match_specification():
    values = torch.tensor([0.0, 1.0, 8.0, 27.0, 64.0], dtype=torch.float32)
    assert torch.equal(trajectory_acceleration(values), specification(values))


def test_cubic_trajectory_has_different_accelerations():
    values = torch.tensor([0.0, 1.0, 8.0, 27.0, 64.0], dtype=torch.float32)
    result = trajectory_acceleration(values)
    assert torch.equal(result, torch.tensor([6.0, 12.0, 18.0]))
    assert not torch.equal(result, values[:3])
    assert torch.unique(result).numel() == result.numel()


def test_batch_dimension_matches_specification():
    row = torch.tensor([0.0, 1.0, 8.0, 27.0, 64.0], dtype=torch.float32)
    values = row.repeat(4, 1)
    assert torch.equal(trajectory_acceleration(values), specification(values))


def test_integer_input_raises_from_extension():
    values = torch.tensor([0, 1, 8, 27], dtype=torch.int64)
    with pytest.raises(RuntimeError, match="dtype"):
        trajectory_acceleration(values)
