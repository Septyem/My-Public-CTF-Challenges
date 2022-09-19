//===-- ChalInstrFormats.td - Target Description for Chal Target ---------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file describes the Chal instructions in TableGen format.
//
//===----------------------------------------------------------------------===//
class InstChal<dag outs, dag ins, string asmstr, list<dag> pattern, bits<8> Opcode>
  : Instruction {
  field bits<8> Inst;
  let Size = 1;

  let Namespace = "Chal";

  let Inst{0-7} = Opcode;

  dag OutOperandList = outs;
  dag InOperandList = ins;
  let AsmString = asmstr;
  let Pattern = pattern;
}

