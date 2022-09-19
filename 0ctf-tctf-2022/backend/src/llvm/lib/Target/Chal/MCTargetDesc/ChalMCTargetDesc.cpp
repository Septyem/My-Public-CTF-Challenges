//===-- ChalMCTargetDesc.cpp - Chal Target Descriptions ---------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file provides Chal specific target descriptions.
//
//===----------------------------------------------------------------------===//

#include "MCTargetDesc/ChalMCTargetDesc.h"
#include "MCTargetDesc/ChalMCAsmInfo.h"
#include "TargetInfo/ChalTargetInfo.h"
#include "llvm/MC/MCInstrAnalysis.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/Host.h"

#define GET_INSTRINFO_MC_DESC
#define ENABLE_INSTR_PREDICATE_VERIFIER
#include "ChalGenInstrInfo.inc"

#define GET_SUBTARGETINFO_MC_DESC
#include "ChalGenSubtargetInfo.inc"

#define GET_REGINFO_MC_DESC
#include "ChalGenRegisterInfo.inc"

using namespace llvm;

static MCInstrInfo *createChalMCInstrInfo() {
  MCInstrInfo *X = new MCInstrInfo();
  InitChalMCInstrInfo(X);
  return X;
}

static MCRegisterInfo *createChalMCRegisterInfo(const Triple &TT) {
  MCRegisterInfo *X = new MCRegisterInfo();
  InitChalMCRegisterInfo(X, Chal::R1 /* RAReg doesn't exist */);
  return X;
}

static MCSubtargetInfo *createChalMCSubtargetInfo(const Triple &TT,
                                                 StringRef CPU, StringRef FS) {
  return createChalMCSubtargetInfoImpl(TT, CPU, /*TuneCPU*/ CPU, FS);
}

static MCStreamer *createChalMCStreamer(const Triple &T, MCContext &Ctx,
                                       std::unique_ptr<MCAsmBackend> &&MAB,
                                       std::unique_ptr<MCObjectWriter> &&OW,
                                       std::unique_ptr<MCCodeEmitter> &&Emitter,
                                       bool RelaxAll) {
  return createELFStreamer(Ctx, std::move(MAB), std::move(OW), std::move(Emitter),
                           RelaxAll);
}

static MCInstPrinter *createChalMCInstPrinter(const Triple &T,
                                             unsigned SyntaxVariant,
                                             const MCAsmInfo &MAI,
                                             const MCInstrInfo &MII,
                                             const MCRegisterInfo &MRI) {
  //if (SyntaxVariant == 0)
  //  return new ChalInstPrinter(MAI, MII, MRI);
  return nullptr;
}

namespace {

class ChalMCInstrAnalysis : public MCInstrAnalysis {
public:
  explicit ChalMCInstrAnalysis(const MCInstrInfo *Info)
      : MCInstrAnalysis(Info) {}
};

} // end anonymous namespace

static MCInstrAnalysis *createChalInstrAnalysis(const MCInstrInfo *Info) {
  return new ChalMCInstrAnalysis(Info);
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitializeChalTargetMC() {
  for (Target *T : {&getTheChalTarget()}) {
    // Register the MC asm info.
    RegisterMCAsmInfo<ChalMCAsmInfo> X(*T);

    // Register the MC instruction info.
    TargetRegistry::RegisterMCInstrInfo(*T, createChalMCInstrInfo);

    // Register the MC register info.
    TargetRegistry::RegisterMCRegInfo(*T, createChalMCRegisterInfo);

    // Register the MC subtarget info.
    TargetRegistry::RegisterMCSubtargetInfo(*T,
                                            createChalMCSubtargetInfo);

    // Register the object streamer
    TargetRegistry::RegisterELFStreamer(*T, createChalMCStreamer);

    // Register the MCInstPrinter.
    TargetRegistry::RegisterMCInstPrinter(*T, createChalMCInstPrinter);

    // Register the MC instruction analyzer.
    TargetRegistry::RegisterMCInstrAnalysis(*T, createChalInstrAnalysis);
  }

  TargetRegistry::RegisterMCCodeEmitter(getTheChalTarget(),
                                        createChalMCCodeEmitter);
  TargetRegistry::RegisterMCAsmBackend(getTheChalTarget(),
                                       createChalAsmBackend);

}
