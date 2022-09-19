add_llvm_component_library(LLVMChalAsmParser
  ChalAsmParser.cpp

  LINK_COMPONENTS
  MC
  MCParser
  ChalDesc
  ChalInfo
  Support

  ADD_TO_COMPONENT
  Chal
  )
