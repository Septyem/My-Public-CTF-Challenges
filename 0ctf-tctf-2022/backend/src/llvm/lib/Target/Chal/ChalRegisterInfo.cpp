//===-- ChalRegisterInfo.cpp - Chal Register Information ----------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file contains the Chal implementation of the TargetRegisterInfo class.
//
//===----------------------------------------------------------------------===//

#include "ChalRegisterInfo.h"
#include "ChalSubtarget.h"
#include "Chal.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/RegisterScavenging.h"
#include "llvm/CodeGen/TargetInstrInfo.h"
#include "llvm/IR/DiagnosticInfo.h"
#include "llvm/Support/ErrorHandling.h"

#define GET_REGINFO_TARGET_DESC
#include "ChalGenRegisterInfo.inc"
using namespace llvm;

ChalRegisterInfo::ChalRegisterInfo()
    : ChalGenRegisterInfo(Chal::R0) {}

const MCPhysReg *
ChalRegisterInfo::getCalleeSavedRegs(const MachineFunction *MF) const {
  return CSR_SaveList;
}

BitVector ChalRegisterInfo::getReservedRegs(const MachineFunction &MF) const {
  BitVector Reserved(getNumRegs());
  markSuperRegs(Reserved, Chal::R1);
  return Reserved;
}

void ChalRegisterInfo::eliminateFrameIndex(MachineBasicBlock::iterator MI, int SPAdj,
                           unsigned FIOperandNum,
                           RegScavenger *RS) const {
}

Register ChalRegisterInfo::getFrameRegister(const MachineFunction &MF) const {
  return Chal::R1;
}
