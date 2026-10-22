#include <torch/extension.h>

torch::Tensor trajectory_acceleration(torch::Tensor input) {
  TORCH_CHECK(input.device().is_cpu(), "input must be a CPU tensor");
  TORCH_CHECK(input.scalar_type() == torch::kFloat32,
              "input must have dtype torch.float32");
  TORCH_CHECK(input.dim() >= 1, "input must have at least one dimension");

  const auto time_size = input.size(-1);
  TORCH_CHECK(time_size >= 3,
              "the last dimension must contain at least three time points");

  auto values = input.contiguous();
  auto output_shape = values.sizes().vec();
  output_shape.back() = time_size - 2;
  auto output = torch::empty(output_shape, values.options());

  const auto trajectory_count = values.numel() / time_size;
  const float* input_data = values.data_ptr<float>();
  float* output_data = output.data_ptr<float>();

  for (int64_t trajectory = 0; trajectory < trajectory_count; ++trajectory) {
    const float* current = input_data + trajectory * time_size;
    float* result = output_data + trajectory * (time_size - 2);

    for (int64_t time = 0; time < time_size - 2; ++time) {
      const float next_step = current[time + 2] - current[time + 1];
      const float previous_step = current[time + 1] - current[time];
      result[time] = next_step - previous_step;
    }
  }

  return output;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, module) {
  module.def("trajectory_acceleration", &trajectory_acceleration,
             "Second finite difference along the last dimension");
}
