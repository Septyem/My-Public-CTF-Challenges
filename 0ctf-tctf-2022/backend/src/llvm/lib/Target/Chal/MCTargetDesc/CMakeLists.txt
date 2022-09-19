add_llvm_component_library(LLVMChalDesc
  ChalMCTargetDesc.cpp
  ChalAsmBackend.cpp
  #ChalInstPrinter.cpp
  ChalMCCodeEmitter.cpp
  ChalELFObjectWriter.cpp

  LINK_COMPONENTS
  MC
  ChalInfo
  Support

  ADD_TO_COMPONENT
  Chal
  )
