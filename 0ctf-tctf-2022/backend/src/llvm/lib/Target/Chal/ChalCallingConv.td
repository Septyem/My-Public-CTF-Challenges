//===-- ChalCallingConv.td - Calling Conventions Chal --------*- tablegen -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This describes the calling conventions for the Chal architecture.
//
//===----------------------------------------------------------------------===//

// Chal 64-bit C return-value convention.
def RetCC_Chal64 : CallingConv<[CCIfType<[i64], CCAssignToReg<[R0]>>]>;

// Chal 64-bit C Calling convention.
def CC_Chal64 : CallingConv<[
  // All arguments get passed in integer registers if there is space.
  CCIfType<[i64], CCAssignToReg<[ R0 ]>>,
]>;

def CSR : CalleeSavedRegs<(add)>;
