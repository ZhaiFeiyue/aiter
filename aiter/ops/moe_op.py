# SPDX-License-Identifier: MIT
# Copyright (c) 2024, Advanced Micro Devices, Inc. All rights reserved.

import torch
from torch import Tensor
from typing import Optional
from ..jit.core import (
    compile_ops,
)
from .enum import ActivationType, Enum, QuantType


@compile_ops("module_moe_asm")
def topk_softmax(
    topk_weights: Tensor,
    topk_indices: Tensor,
    token_expert_indices: Tensor,
    gating_output: Tensor,
    need_renorm: bool,
): ...


@compile_ops("module_moe_asm")
def moe_sum(input: Tensor, output: Tensor): ...


@compile_ops("module_moe_asm")
def moe_align_block_size(
    topk_ids: Tensor,
    num_experts: int,
    block_size: int,
    sorted_token_ids: Tensor,
    experts_ids: Tensor,
    token_nums: Tensor,
    num_tokens_post_pad: Tensor,
): ...


@compile_ops("module_moe_asm")
def fmoe(
    out: Tensor,
    input: Tensor,
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
): ...


@compile_ops("module_moe_asm")
def fmoe_int8_g1u0(
    out: Tensor,
    input: Tensor,
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
    input_scale: Tensor,
    fc1_scale: Tensor,
    fc2_scale: Tensor,
    fc2_smooth_scale: Tensor,
    activation: Optional[Enum] = ActivationType.Silu,
): ...


@compile_ops("module_moe_asm")
def fmoe_g1u1(
    out: Tensor,
    input: Tensor,
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
    input_scale: Tensor,
    fc1_scale: Tensor,
    fc2_scale: Tensor,
    fc2_smooth_scale: Optional[Tensor] = None,
    activation: Optional[Enum] = ActivationType.Silu,
): ...


@compile_ops("module_moe_asm")
def fmoe_g1u1_tkw1(
    out: Tensor,
    input: Tensor,
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
    input_scale: Tensor,
    fc1_scale: Tensor,
    fc2_scale: Tensor,
    fc2_smooth_scale: Optional[Tensor] = None,
    activation: Optional[Enum] = ActivationType.Silu,
): ...


@compile_ops("module_moe_asm")
def fmoe_int8_g1u0_a16(
    out: Tensor,
    input: Tensor,  # bf16
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
    fc1_scale: Tensor,
    fc2_scale: Tensor,
    fc1_smooth_scale: Tensor,
    fc2_smooth_scale: Tensor,
): ...


@compile_ops("module_moe_asm")
def fmoe_g1u1_a16(
    out: Tensor,
    input: Tensor,  # bf16
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
    fc1_scale: Tensor,
    fc2_scale: Tensor,
    fc1_smooth_scale: Tensor,
    fc2_smooth_scale: Tensor,
): ...


@compile_ops("module_moe_asm")
def fmoe_fp8_blockscale_g1u1(
    out: Tensor,
    input: Tensor,
    gate: Tensor,
    down: Tensor,
    sorted_token_ids: Tensor,
    sorted_weights: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    topk: int,
    input_scale: Tensor,
    fc1_scale: Tensor,
    fc2_scale: Tensor,
    fc_scale_blkn: int = 128,
    fc_scale_blkk: int = 128,
    fc2_smooth_scale: Optional[Tensor] = None,
    activation: ActivationType = ActivationType.Silu,
): ...


@compile_ops("module_moe_asm")
def moe_stage1_g1u1(
    input: torch.Tensor,
    w1: torch.Tensor,
    w2: torch.Tensor,
    sorted_token_ids: torch.Tensor,
    sorted_expert_ids: torch.Tensor,
    num_valid_ids: torch.Tensor,
    out: torch.Tensor,
    inter_dim: int,
    kernelName: str,
    block_m: int,
    ksplit: int = 0,
    activation: ActivationType = ActivationType.Silu,
    quant_type: QuantType = QuantType.No,
    a1_scale: Optional[torch.Tensor] = None,
    w1_scale: Optional[torch.Tensor] = None,
    sorted_weights: Optional[torch.Tensor] = None,
) -> None: ...


@compile_ops("module_moe")
def ck_moe(
    hidden_states: Tensor,
    w1: Tensor,
    w2: Tensor,
    topk_weight: Tensor,
    topk_ids: Tensor,
    fc1_scale: Optional[Tensor] = None,
    fc2_scale: Optional[Tensor] = None,
    fc1_smooth_scale: Optional[Tensor] = None,
    fc2_smooth_scale: Optional[Tensor] = None,
    block_m: Optional[int] = 32,
    expert_mask: Optional[Tensor] = None,
): ...


@compile_ops("module_moe_ck2stages")
def ck_moe_stage1(
    hidden_states: Tensor,
    w1: Tensor,
    w2: Tensor,
    sorted_token_ids: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    out: Tensor,
    topk: int,
    w1_scale: Optional[Tensor] = None,
    a1_scale: Optional[Tensor] = None,
    block_m: Optional[int] = 32,
    sorted_weights: Optional[Tensor] = None,
    act_op: Optional[int] = 0,
): ...


@compile_ops("module_moe_ck2stages")
def ck_moe_stage2(
    inter_states: Tensor,
    w1: Tensor,
    w2: Tensor,
    sorted_token_ids: Tensor,
    sorted_expert_ids: Tensor,
    num_valid_ids: Tensor,
    out: Tensor,
    topk: int,
    w2_scale: Optional[Tensor] = None,
    a2_scale: Optional[Tensor] = None,
    block_m: Optional[int] = 32,
    sorted_weights: Optional[Tensor] = None,
): ...
