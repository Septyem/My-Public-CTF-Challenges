//===-- ChalSelectionDAGInfo.h - Chal SelectionDAG Info -----------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file defines the Chal subclass for SelectionDAGTargetInfo.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_Chal_ChalSELECTIONDAGINFO_H
#define LLVM_LIB_TARGET_Chal_ChalSELECTIONDAGINFO_H

#include "llvm/CodeGen/SelectionDAGTargetInfo.h"

namespace llvm {

class ChalSelectionDAGInfo : public SelectionDAGTargetInfo {
public:
  unsigned getCommonMaxStoresPerMemFunc() const { return 128; }

};

}

#endif
