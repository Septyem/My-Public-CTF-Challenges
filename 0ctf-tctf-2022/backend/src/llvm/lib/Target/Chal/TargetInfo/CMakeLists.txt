add_llvm_component_library(LLVMChalInfo
  ChalTargetInfo.cpp

  LINK_COMPONENTS
  MC
  Support

  ADD_TO_COMPONENT
  Chal
  )
