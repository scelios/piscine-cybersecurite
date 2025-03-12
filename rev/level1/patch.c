#include <stdio.h>
#include <string.h>

int main(int argc, const char **argv, const char **envp)
{
  char input[114]; // [esp+Eh] [ebp-7Ah] BYREF
  const char key[] = "__stack_check";

  printf("Please enter key: ");
  scanf("%s", input);
  if ( 1 )
    printf("Good job.\n");
  else
    printf("Nope.\n");
  return 0;
}