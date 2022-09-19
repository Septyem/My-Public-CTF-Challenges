add_llvm_component_group(Chal)

set(LLVM_TARGET_DEFINITIONS Chal.td)

tablegen(LLVM ChalGenAsmMatcher.inc -gen-asm-matcher)
tablegen(LLVM ChalGenAsmWriter.inc -gen-asm-writer)
tablegen(LLVM ChalGenCallingConv.inc -gen-callingconv)
tablegen(LLVM ChalGenDAGISel.inc -gen-dag-isel)
tablegen(LLVM ChalGenInstrInfo.inc -gen-instr-info)
tablegen(LLVM ChalGenMCCodeEmitter.inc -gen-emitter)
tablegen(LLVM ChalGenRegisterInfo.inc -gen-register-info)
tablegen(LLVM ChalGenSubtargetInfo.inc -gen-subtarget)

add_public_tablegen_target(ChalCommonTableGen)

add_llvm_target(ChalCodeGen
  ChalAsmPrinter.cpp
  ChalFrameLowering.cpp
  ChalInstrInfo.cpp
  ChalISelDAGToDAG.cpp
  ChalISelLowering.cpp
  ChalRegisterInfo.cpp
  ChalSubtarget.cpp
  ChalTargetMachine.cpp

  LINK_COMPONENTS
  Analysis
  AsmPrinter
  CodeGen
  Core
  MC
  ChalDesc
  ChalInfo
  IPO
  Scalar
  SelectionDAG
  Support
  Target
  TransformUtils

  ADD_TO_COMPONENT
  Chal
  )

add_subdirectory(AsmParser)
add_subdirectory(MCTargetDesc)
add_subdirectory(TargetInfo)
