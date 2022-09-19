//===-- ChalISelLowering.cpp - Chal DAG Lowering Implementation  ------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file defines the interfaces that Chal uses to lower LLVM code into a
// selection DAG.
//
//===----------------------------------------------------------------------===//

#include "ChalISelLowering.h"
#include "ChalSubtarget.h"
#include "ChalTargetMachine.h"
#include "Chal.h"
#include "llvm/CodeGen/CallingConvLower.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"
#include "llvm/CodeGen/TargetLoweringObjectFileImpl.h"
#include "llvm/CodeGen/ValueTypes.h"
#include "llvm/IR/DiagnosticInfo.h"
#include "llvm/IR/DiagnosticPrinter.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/ErrorHandling.h"
#include "llvm/Support/raw_ostream.h"
using namespace llvm;

#define DEBUG_TYPE "chal-lower"

ChalTargetLowering::ChalTargetLowering(const TargetMachine &TM,
                                     const ChalSubtarget &STI)
    : TargetLowering(TM) {

  // Set up the register classes.
  addRegisterClass(MVT::i64, &Chal::GPRRegClass);

  // Compute derived properties from the register classes
  computeRegisterProperties(STI.getRegisterInfo());

  setStackPointerRegisterToSaveRestore(Chal::R1);

}

const char *ChalTargetLowering::getTargetNodeName(unsigned Opcode) const {
  return nullptr;
}
 
bool ChalTargetLowering::isOffsetFoldingLegal(const GlobalAddressSDNode *GA) const {
  return false;
}

ChalTargetLowering::ConstraintType
ChalTargetLowering::getConstraintType(StringRef Constraint) const {
  return TargetLowering::getConstraintType(Constraint);
}

std::pair<unsigned, const TargetRegisterClass *>
ChalTargetLowering::getRegForInlineAsmConstraint(const TargetRegisterInfo *TRI,
                                                StringRef Constraint,
                                                MVT VT) const {
  return TargetLowering::getRegForInlineAsmConstraint(TRI, Constraint, VT);
}

MachineBasicBlock *
ChalTargetLowering::EmitInstrWithCustomInserter(MachineInstr &MI,
                                               MachineBasicBlock *BB) const {
  return BB;
}

EVT ChalTargetLowering::getSetCCResultType(const DataLayout &, LLVMContext &,
                                          EVT VT) const {
  return MVT::i64;
}

MVT ChalTargetLowering::getScalarShiftAmountTy(const DataLayout &DL,
                                              EVT VT) const {
  return MVT::i64;
}

SDValue ChalTargetLowering::LowerCall(TargetLowering::CallLoweringInfo &CLI,
                                     SmallVectorImpl<SDValue> &InVals) const {
  /*
  auto &Ins = CLI.Ins;
  SelectionDAG &DAG = CLI.DAG;
  for (unsigned i = 0, e = Ins.size(); i != e; ++i)
     InVals.push_back(DAG.getConstant(0, CLI.DL, Ins[i].VT));
  */
  return CLI.Chain;
}

SDValue ChalTargetLowering::LowerFormalArguments(
    SDValue Chain, CallingConv::ID CallConv, bool IsVarArg,
    const SmallVectorImpl<ISD::InputArg> &Ins, const SDLoc &DL,
    SelectionDAG &DAG, SmallVectorImpl<SDValue> &InVals) const {
  return Chain;
}

SDValue
ChalTargetLowering::LowerReturn(SDValue Chain, CallingConv::ID CallConv,
                               bool IsVarArg,
                               const SmallVectorImpl<ISD::OutputArg> &Outs,
                               const SmallVectorImpl<SDValue> &OutVals,
                               const SDLoc &DL, SelectionDAG &DAG) const {
  return Chain;
}

void ChalTargetLowering::ReplaceNodeResults(
  SDNode *N, SmallVectorImpl<SDValue> &Results, SelectionDAG &DAG) const {
}

bool ChalTargetLowering::isLegalAddressingMode(const DataLayout &DL,
                                              const AddrMode &AM, Type *Ty,
                                              unsigned AS,
                                              Instruction *I) const {
  return true;
}

bool ChalTargetLowering::isTruncateFree(Type *Ty1, Type *Ty2) const {
  return false;
}

bool ChalTargetLowering::isTruncateFree(EVT VT1, EVT VT2) const {
  return false;
}
bool ChalTargetLowering::isZExtFree(Type *Ty1, Type *Ty2) const {
  return false;
}

bool ChalTargetLowering::isZExtFree(EVT VT1, EVT VT2) const {
  return false;
}
