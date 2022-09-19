//===-- Chal.h - Top-level interface for Chal representation ------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_Chal_Chal_H
#define LLVM_LIB_TARGET_Chal_Chal_H

#include "MCTargetDesc/ChalMCTargetDesc.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Pass.h"
#include "llvm/PassRegistry.h"
#include "llvm/Target/TargetMachine.h"

namespace llvm {
class ChalTargetMachine;

FunctionPass *createChalISelDag(ChalTargetMachine &TM);
} // namespace llvm

#endif
