//===-- ChalELFObjectWriter.cpp - Chal ELF Writer ---------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#include "MCTargetDesc/ChalMCTargetDesc.h"
#include "llvm/BinaryFormat/ELF.h"
#include "llvm/MC/MCELFObjectWriter.h"
#include "llvm/MC/MCFixup.h"
#include "llvm/MC/MCObjectWriter.h"
#include "llvm/MC/MCValue.h"
#include "llvm/Support/ErrorHandling.h"
#include <cstdint>

using namespace llvm;

namespace {

class ChalELFObjectWriter : public MCELFObjectTargetWriter {
public:
  ChalELFObjectWriter(uint8_t OSABI);
  ~ChalELFObjectWriter() override = default;

protected:
  unsigned getRelocType(MCContext &Ctx, const MCValue &Target,
                        const MCFixup &Fixup, bool IsPCRel) const override;
};

} // end anonymous namespace

ChalELFObjectWriter::ChalELFObjectWriter(uint8_t OSABI)
    : MCELFObjectTargetWriter(/*Is64Bit*/ true, OSABI, 62,
                              /*HasRelocationAddend*/ false) {}

unsigned ChalELFObjectWriter::getRelocType(MCContext &Ctx, const MCValue &Target,
                                          const MCFixup &Fixup,
                                          bool IsPCRel) const {
  return 1;
}

std::unique_ptr<MCObjectTargetWriter>
llvm::createChalELFObjectWriter(uint8_t OSABI) {
  return std::make_unique<ChalELFObjectWriter>(OSABI);
}
