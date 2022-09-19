//===-- Chal.td - Describe the Chal Target Machine -----------*- tablegen -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

include "llvm/Target/Target.td"

include "ChalRegisterInfo.td"
include "ChalCallingConv.td"
include "ChalInstrInfo.td"

def ChalInstrInfo : InstrInfo;

class Proc<string Name, list<SubtargetFeature> Features>
 : Processor<Name, NoItineraries, Features>;

def : Proc<"generic", []>;

def ChalInstPrinter : AsmWriter {
  string AsmWriterClassName  = "InstPrinter";
  bit isMCAsmWriter = 1;
}

def ChalAsmParser : AsmParser {
  bit HasMnemonicFirst = 0;
}

def ChalAsmParserVariant : AsmParserVariant {
  int Variant = 0;
  string Name = "Chal";
  string BreakCharacters = ".";
  string TokenizingCharacters = "#()[]=:.<>!+*";
}

def Chal : Target {
  let InstructionSet = ChalInstrInfo;
  let AssemblyWriters = [ChalInstPrinter];
  let AssemblyParsers = [ChalAsmParser];
  let AssemblyParserVariants = [ChalAsmParserVariant];
}
