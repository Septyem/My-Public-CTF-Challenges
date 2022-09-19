//===-- ChalSubtarget.cpp - Chal Subtarget Information ----------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file implements the Chal specific subclass of TargetSubtargetInfo.
//
//===----------------------------------------------------------------------===//

#include "ChalSubtarget.h"
#include "Chal.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/Host.h"

using namespace llvm;

#define DEBUG_TYPE "chal-subtarget"

#define GET_SUBTARGETINFO_TARGET_DESC
#define GET_SUBTARGETINFO_CTOR
#include "ChalGenSubtargetInfo.inc"

void ChalSubtarget::anchor() {}

ChalSubtarget &ChalSubtarget::initializeSubtargetDependencies(StringRef CPU,
                                                            StringRef FS) {
  initSubtargetFeatures(CPU, FS);
  ParseSubtargetFeatures(CPU, /*TuneCPU*/ CPU, FS);
  return *this;
}

void ChalSubtarget::initSubtargetFeatures(StringRef CPU, StringRef FS) {
  return;
}

ChalSubtarget::ChalSubtarget(const Triple &TT, const std::string &CPU,
                           const std::string &FS, const TargetMachine &TM)
    : ChalGenSubtargetInfo(TT, CPU, /*TuneCPU*/ CPU, FS),
      FrameLowering(initializeSubtargetDependencies(CPU, FS)),
      TLInfo(TM, *this) {}
