//===-- ChalSubtarget.h - Define Subtarget for the Chal -----------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file declares the Chal specific subclass of TargetSubtargetInfo.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_Chal_ChalSUBTARGET_H
#define LLVM_LIB_TARGET_Chal_ChalSUBTARGET_H

#include "ChalFrameLowering.h"
#include "ChalISelLowering.h"
#include "ChalInstrInfo.h"
#include "ChalSelectionDAGInfo.h"
#include "llvm/CodeGen/SelectionDAGTargetInfo.h"
#include "llvm/CodeGen/TargetSubtargetInfo.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/Target/TargetMachine.h"

#define GET_SUBTARGETINFO_HEADER
#include "ChalGenSubtargetInfo.inc"

namespace llvm {
class StringRef;

class ChalSubtarget : public ChalGenSubtargetInfo {
  virtual void anchor();
  ChalInstrInfo InstrInfo;
  ChalFrameLowering FrameLowering;
  ChalTargetLowering TLInfo;
  ChalSelectionDAGInfo TSInfo;

private:
  void initializeEnvironment();
  void initSubtargetFeatures(StringRef CPU, StringRef FS);
  bool probeJmpExt();

public:
  // This constructor initializes the data members to match that
  // of the specified triple.
  ChalSubtarget(const Triple &TT, const std::string &CPU, const std::string &FS,
               const TargetMachine &TM);

  ChalSubtarget &initializeSubtargetDependencies(StringRef CPU, StringRef FS);

  // ParseSubtargetFeatures - Parses features string setting specified
  // subtarget options.  Definition of function is auto generated by tblgen.
  void ParseSubtargetFeatures(StringRef CPU, StringRef TuneCPU, StringRef FS);

  const ChalInstrInfo *getInstrInfo() const override { return &InstrInfo; }
  const ChalFrameLowering *getFrameLowering() const override {
    return &FrameLowering;
  }
  const ChalTargetLowering *getTargetLowering() const override {
    return &TLInfo;
  }
  const ChalSelectionDAGInfo *getSelectionDAGInfo() const override {
    return &TSInfo;
  }
  const TargetRegisterInfo *getRegisterInfo() const override {
    return &InstrInfo.getRegisterInfo();
  }
};
} // End llvm namespace

#endif
