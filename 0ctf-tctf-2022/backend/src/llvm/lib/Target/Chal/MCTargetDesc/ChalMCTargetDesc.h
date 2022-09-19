//===-- ChalMCTargetDesc.h - Chal Target Descriptions -------------*- C++ -*-===//
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

#ifndef LLVM_LIB_TARGET_Chal_MCTARGETDESC_ChalMCTARGETDESC_H
#define LLVM_LIB_TARGET_Chal_MCTARGETDESC_ChalMCTARGETDESC_H

#include "llvm/Config/config.h"
#include "llvm/MC/MCContext.h"
#include "llvm/Support/DataTypes.h"

#include <memory>

namespace llvm {
class MCAsmBackend;
class MCCodeEmitter;
class MCContext;
class MCInstrInfo;
class MCObjectTargetWriter;
class MCRegisterInfo;
class MCSubtargetInfo;
class MCTargetOptions;
class Target;

MCCodeEmitter *createChalMCCodeEmitter(const MCInstrInfo &MCII,
                                      MCContext &Ctx);

MCAsmBackend *createChalAsmBackend(const Target &T, const MCSubtargetInfo &STI,
                                  const MCRegisterInfo &MRI,
                                  const MCTargetOptions &Options);

std::unique_ptr<MCObjectTargetWriter> createChalELFObjectWriter(uint8_t OSABI);
}

// Defines symbolic names for Chal registers.  This defines a mapping from
// register name to register number.
//
#define GET_REGINFO_ENUM
#include "ChalGenRegisterInfo.inc"

// Defines symbolic names for the Chal instructions.
//
#define GET_INSTRINFO_ENUM
#define GET_INSTRINFO_MC_HELPER_DECLS
#include "ChalGenInstrInfo.inc"

#define GET_SUBTARGETINFO_ENUM
#include "ChalGenSubtargetInfo.inc"

#endif
