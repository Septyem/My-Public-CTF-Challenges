//===-- ChalInstrInfo.h - Chal Instruction Information ------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file contains the Chal implementation of the TargetInstrInfo class.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_Chal_ChalINSTRINFO_H
#define LLVM_LIB_TARGET_Chal_ChalINSTRINFO_H

#include "ChalRegisterInfo.h"
#include "llvm/CodeGen/TargetInstrInfo.h"

#define GET_INSTRINFO_HEADER
#include "ChalGenInstrInfo.inc"

namespace llvm {

class ChalInstrInfo : public ChalGenInstrInfo {
  const ChalRegisterInfo RI;

public:
  ChalInstrInfo();

  const ChalRegisterInfo &getRegisterInfo() const { return RI; }

  void copyPhysReg(MachineBasicBlock &MBB, MachineBasicBlock::iterator I,
                   const DebugLoc &DL, MCRegister DestReg, MCRegister SrcReg,
                   bool KillSrc) const override;

};
}

#endif
