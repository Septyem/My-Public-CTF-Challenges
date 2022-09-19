//===-- ChalTargetInfo.cpp - Chal Target Implementation ---------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#include "TargetInfo/ChalTargetInfo.h"
#include "llvm/MC/TargetRegistry.h"

using namespace llvm;

Target &llvm::getTheChalTarget() {
  static Target TheChalTarget;
  return TheChalTarget;
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitializeChalTargetInfo() {
  TargetRegistry::RegisterTarget(getTheChalTarget(), "chal", "Chal (little endian)",
                                 "Chal", [](Triple::ArchType) { return false; },
                                 true);
}
