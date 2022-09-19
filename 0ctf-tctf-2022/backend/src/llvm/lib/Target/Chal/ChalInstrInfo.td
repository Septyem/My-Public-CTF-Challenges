//===-- ChalInstrInfo.td - Target Description for Chal Target ---------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file describes the Chal instructions in TableGen format.
//
//===----------------------------------------------------------------------===//
include "ChalInstrFormats.td"

def i64immAny : PatLeaf<(i64 imm), [{return true; }]>;
def brtarget : Operand<OtherVT>;

def OP0: InstChal<(outs GPR:$r0), (ins GPR:$r1, GPR:$r2), "calc $r0, $r1, $r2", [], 0>;
def OP1: InstChal<(outs GPR:$r0), (ins GPR:$r1, i64imm:$imm0), "op1 $r0, $r1, $imm0", [], 1>;
def OP2: InstChal<(outs GPR:$r0), (ins i64imm:$imm0, i64imm:$imm1), "op2 $r0, $imm0, $imm1", [], 2>;
def OP3: InstChal<(outs GPR:$r0), (ins i64imm:$imm0), "op3 $r0, $imm0", [], 3>;
def OP4: InstChal<(outs), (ins brtarget:$dst), "op4 $dst", [], 4>;

//def : Pat<(mul (sdiv 15, (add GPR:$r1, 34)), (add (or GPR:$r2, 5), 2)), (OP0 GPR:$r1, GPR:$r2)>;
def : Pat<(mul (add (sdiv (mul (or GPR:$r1, 5), 7), 34), 37), (add (sdiv (mul GPR:$r2, 66), 27), 80)),
    (OP0 GPR:$r1, GPR:$r2)>;
def : Pat<(i64immAny:$imm0), (OP3 i64immAny:$imm0)>;
def : Pat<(br bb:$dst), (OP4 bb:$dst)>;


