#include <unistd.h>
#include <stdio.h>

int main(int argc, char *argv[], char *envp[]) {
  char *args[] = { "/bin/bash", NULL };
  execve(args[0], args, envp);

  perror("Running bash failed");
  return 1;
}