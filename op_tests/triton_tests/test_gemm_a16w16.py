import torch
import triton
import pytest
from aiter.ops.triton.gemm_a16w16 import gemm_a16w16


def generate_gemm_a16w16_inputs(M, N, K, dtype, layout="TN"):
    if layout[0] == "T":
        x = torch.randn((M, K), dtype=dtype).cuda()
    else:
        x = torch.randn((K, M), dtype=dtype).cuda().T

    if layout[1] == "T":
        weight = torch.randn((K, N), dtype=dtype).cuda()
    else:
        weight = torch.randn((N, K), dtype=dtype).cuda().T

    return x, weight


def get_x_vals():

    x_vals = [(1024 * v, 1024 * v, 1024 * v) for v in range(1, 9)]
    x_vals += [(4864, 4096, 8192), (9728, 8192, 65536), (4864, 8192, 4160)]
    x_vals += [
        (1, 1280, 8192),
        (32, 1280, 8192),
        (64, 1280, 8192),
        (128, 1280, 8192),
        (192, 1280, 8192),
        (256, 1280, 8192),
        (320, 1280, 8192),
        (512, 1280, 8192),
        (1024, 1280, 8192),
        (2048, 1280, 8192),
        (4096, 1280, 8192),
        (8192, 1280, 8192),
        (16384, 1280, 8192),
        (1, 8192, 1024),
        (32, 8192, 1024),
        (64, 8192, 1024),
        (128, 8192, 1024),
        (192, 8192, 1024),
        (256, 8192, 1024),
        (320, 8192, 1024),
        (512, 8192, 1024),
        (1024, 8192, 1024),
        (2048, 8192, 1024),
        (4096, 8192, 1024),
        (8192, 8192, 1024),
        (16384, 8192, 1024),
    ]
    return x_vals


@pytest.mark.parametrize("M, N, K", get_x_vals())
@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16])
def test_gemm_a16_w16(M: int, N: int, K: int, dtype):
    x, w = generate_gemm_a16w16_inputs(M, N, K, dtype)

    torch_out = torch.matmul(x, w)

    triton_out = gemm_a16w16(x, w, dtype)

    triton.testing.assert_close(triton_out, torch_out, atol=1e-1, rtol=1e-1)
