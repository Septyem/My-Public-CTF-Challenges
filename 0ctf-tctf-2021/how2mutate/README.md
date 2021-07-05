### solution

The function `util_Realloc` in honggfuzz has a somewhat different api with realloc, and will double free with size 0.
