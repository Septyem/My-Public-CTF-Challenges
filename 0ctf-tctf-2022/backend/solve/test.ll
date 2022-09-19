; ModuleID = 'test.bc'
source_filename = "test.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

define dso_local i32 @main() #0 {
entry:
  %x = add i64 0,1
  br label %aaa

aaa:
  %i = phi i64 [ 12, %aaa ], [ 134, %entry ]

  %a0 = or i64 %i, 5
  %a1 = mul i64 %a0, 7
  %a2 = sdiv i64 %a1, 34
  %a3 = add i64 %a2, 37
  %a4 = mul i64 %i, 66
  %a5 = sdiv i64 %a4, 27
  %a6 = add i64 %a5, 80
  %a = mul i64 %a3, %a6

  br label %aaa

  %r = trunc i64 %a to i32
  ret i32 %r
}
