//===-- ChalTargetMachine.cpp - Define TargetMachine for Chal ---------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// Implements the info about Chal target spec.
//
//===----------------------------------------------------------------------===//

#include "ChalTargetMachine.h"
#include "ChalTargetTransformInfo.h"
#include "Chal.h"
#include "MCTargetDesc/ChalMCAsmInfo.h"
#include "TargetInfo/ChalTargetInfo.h"
#include "llvm/CodeGen/Passes.h"
#include "llvm/CodeGen/TargetLoweringObjectFileImpl.h"
#include "llvm/CodeGen/TargetPassConfig.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/PassManager.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Support/FormattedStream.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Scalar/SimplifyCFG.h"
#include "llvm/Transforms/Utils/SimplifyCFGOptions.h"
using namespace llvm;

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitializeChalTarget() {
  // Register the target.
  RegisterTargetMachine<ChalTargetMachine> Z(getTheChalTarget());
}

static std::string computeDataLayout(const Triple &TT) {
  return "e-m:e-p:64:64-i64:64-i128:128-n32:64-S128";
}

static Reloc::Model getEffectiveRelocModel(Optional<Reloc::Model> RM) {
  return RM.value_or(Reloc::PIC_);
}

ChalTargetMachine::ChalTargetMachine(const Target &T, const Triple &TT,
                                   StringRef CPU, StringRef FS,
                                   const TargetOptions &Options,
                                   Optional<Reloc::Model> RM,
                                   Optional<CodeModel::Model> CM,
                                   CodeGenOpt::Level OL, bool JIT)
    : LLVMTargetMachine(T, computeDataLayout(TT), TT, CPU, FS, Options,
                        getEffectiveRelocModel(RM),
                        getEffectiveCodeModel(CM, CodeModel::Small), OL),
      TLOF(std::make_unique<TargetLoweringObjectFileELF>()),
      Subtarget(TT, std::string(CPU), std::string(FS), *this) {
  initAsmInfo();
}

namespace {
class ChalPassConfig : public TargetPassConfig {
public:
  ChalPassConfig(ChalTargetMachine &TM, PassManagerBase &PM)
      : TargetPassConfig(TM, PM) {}

  ChalTargetMachine &getChalTargetMachine() const {
    return getTM<ChalTargetMachine>();
  }

  void addIRPasses() override;
  bool addInstSelector() override;
  void addMachineSSAOptimization() override;
  void addPreEmitPass() override;

};
}

void ChalPassConfig::addIRPasses() {
}

bool ChalPassConfig::addInstSelector() {
  addPass(createChalISelDag(getChalTargetMachine()));

  return false;
}

void ChalPassConfig::addMachineSSAOptimization() {
}

void ChalPassConfig::addPreEmitPass() {
}


TargetPassConfig *ChalTargetMachine::createPassConfig(PassManagerBase &PM) {
  return new ChalPassConfig(*this, PM);
}

TargetTransformInfo
ChalTargetMachine::getTargetTransformInfo(const Function &F) const {
  return TargetTransformInfo(ChalTTIImpl(this, F));
}
