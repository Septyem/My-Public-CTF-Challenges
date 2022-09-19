//===-- ChalMCCodeEmitter.cpp - Convert Chal code to machine code -----------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file implements the ChalMCCodeEmitter class.
//
//===----------------------------------------------------------------------===//

#include "MCTargetDesc/ChalMCTargetDesc.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/MC/MCCodeEmitter.h"
#include "llvm/MC/MCExpr.h"
#include "llvm/MC/MCFixup.h"
#include "llvm/MC/MCInst.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/Support/Endian.h"
#include "llvm/Support/EndianStream.h"
#include <cassert>
#include <cstdint>

using namespace llvm;

#define DEBUG_TYPE "mccodeemitter"

namespace {

class ChalMCCodeEmitter : public MCCodeEmitter {
  const MCRegisterInfo &MRI;
  bool IsLittleEndian;

public:
  ChalMCCodeEmitter(const MCInstrInfo &, const MCRegisterInfo &mri)
      : MRI(mri){ }
  ChalMCCodeEmitter(const ChalMCCodeEmitter &) = delete;
  void operator=(const ChalMCCodeEmitter &) = delete;
  ~ChalMCCodeEmitter() override = default;

  // getBinaryCodeForInstr - TableGen'erated function for getting the
  // binary encoding for an instruction.
  uint64_t getBinaryCodeForInstr(const MCInst &MI,
                                 SmallVectorImpl<MCFixup> &Fixups,
                                 const MCSubtargetInfo &STI) const;

  void encodeInstruction(const MCInst &MI, raw_ostream &OS,
                         SmallVectorImpl<MCFixup> &Fixups,
                         const MCSubtargetInfo &STI) const override;
};

} // end anonymous namespace

MCCodeEmitter *llvm::createChalMCCodeEmitter(const MCInstrInfo &MCII,
                                            MCContext &Ctx) {
  return new ChalMCCodeEmitter(MCII, *Ctx.getRegisterInfo());
}

void ChalMCCodeEmitter::encodeInstruction(const MCInst &MI, raw_ostream &OS,
                                         SmallVectorImpl<MCFixup> &Fixups,
                                         const MCSubtargetInfo &STI) const {
    // Get instruction encoding and emit it
    uint64_t Value = getBinaryCodeForInstr(MI, Fixups, STI);
    OS << char(Value);
}

#include "ChalGenMCCodeEmitter.inc"
