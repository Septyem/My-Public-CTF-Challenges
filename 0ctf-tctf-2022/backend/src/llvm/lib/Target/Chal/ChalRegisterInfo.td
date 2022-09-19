//===-- ChalRegisterInfo.td - Chal Register defs -------------*- tablegen -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

//===----------------------------------------------------------------------===//
//  Declarations that describe the Chal register file
//===----------------------------------------------------------------------===//

// Registers are identified with 4-bit ID numbers.
// Ri - 64-bit integer registers
class Ri<bits<16> Enc, string n>
  : Register<n> {
  let HWEncoding = Enc;
  let Namespace = "Chal";
}

foreach I = 0-3 in {
  // 64-bit Integer registers
  def R#I  : Ri<I,  "r"#I>,  DwarfRegNum<[I]>;
}

def GPR : RegisterClass<"Chal", [i64], 64, (add
  R0, // Return value
  R1, // Stack Ptr
  R2,
  R3
)>;
