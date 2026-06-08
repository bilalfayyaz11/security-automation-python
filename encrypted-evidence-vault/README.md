# Encrypted Evidence Vault

## What This Does

This implementation builds a secure encrypted evidence vault for storing sensitive forensic files with confidentiality, integrity verification, controlled access, and audit logging.

The system uses LUKS encryption to protect evidence at rest, SHA-256 checksums to detect tampering, GPG to protect key backups, and shell automation to open, close, verify, and audit vault activity.

This type of system is useful for cybersecurity investigations, incident response, digital forensics, compliance evidence handling, and secure internal case management where sensitive data must remain protected even if the storage file is copied or exposed.

## Architecture

    +--------------------------------+
    | Evidence Source Files          |
    | case_001.txt / case_002.txt    |
    +---------------+----------------+
                    |
                    v
    +--------------------------------+
    | Encrypted Vault Container      |
    | evidence_vault.img             |
    | LUKS Encryption Layer          |
    +---------------+----------------+
                    |
                    v
    +--------------------------------+
    | Device Mapper Layer            |
    | /dev/mapper/evidence_vault     |
    +---------------+----------------+
                    |
                    v
    +--------------------------------+
    | Mounted Secure Storage         |
    | /mnt/evidence_vault            |
    +---------------+----------------+
                    |
       +------------+-------------+
       |                          |
       v                          v
+---------------------+    +----------------------+
| Integrity Checking  |    | Access Automation    |
| SHA-256 Checksums   |    | vault_manager.sh     |
| verify_evidence.sh  |    +----------------------+
+---------------------+              |
       |                              v
       v                     +----------------------+
+---------------------+      | Audit Trail          |
| Tamper Detection    |      | vault_audit.log      |
+---------------------+      +----------------------+

## Prerequisites

- Ubuntu 24.04
- sudo access
- cryptsetup
- GnuPG
- tree
- coreutils
- util-linux
- Bash
- Git

## Setup & Installation

sudo apt update

sudo apt install -y cryptsetup gnupg tree git coreutils util-linux

cryptsetup --version

gpg --version

tree --version

sha256sum --version

mount --version

## How to Reproduce

Create the working directory:

mkdir -p ~/evidence-lab

cd ~/evidence-lab

Create a 100MB encrypted container image:

dd if=/dev/zero of=evidence_vault.img bs=1M count=100

Initialize LUKS encryption:

sudo cryptsetup luksFormat evidence_vault.img

Open the encrypted container:

sudo cryptsetup luksOpen evidence_vault.img evidence_vault

Create an ext4 filesystem inside the encrypted mapping:

sudo mkfs.ext4 /dev/mapper/evidence_vault

Create and mount the secure storage location:

sudo mkdir -p /mnt/evidence_vault

sudo mount /dev/mapper/evidence_vault /mnt/evidence_vault

Create sample evidence files and a chain-of-custody record:

sudo cp evidence-samples/case_001.txt /mnt/evidence_vault/

sudo cp evidence-samples/case_002.txt /mnt/evidence_vault/

sudo cp evidence-samples/chain_of_custody.log /mnt/evidence_vault/

Generate integrity checksums:

sudo bash -c 'cd /mnt/evidence_vault && sha256sum *.txt > evidence_checksums.sha256'

Run integrity verification:

./verify_evidence.sh

Manage vault access:

./vault_manager.sh status

./vault_manager.sh close

./vault_manager.sh open

Record audit events:

./audit_log.sh "VAULT_OPENED" "Evidence vault accessed for review"

./audit_log.sh "EVIDENCE_VERIFIED" "Integrity check passed for all files"

Create an encrypted backup of the vault key:

sudo gpg --symmetric --cipher-algo AES256 --output vault.key.gpg vault.key

## Tools Used

- Linux
- Bash
- cryptsetup
- LUKS
- dm-crypt
- ext4
- GnuPG
- SHA-256
- coreutils
- util-linux
- tree
- Git

## Key Skills Demonstrated

- Linux disk encryption using LUKS
- Secure handling of forensic evidence
- Key-file based vault access
- Backup passphrase management
- Filesystem creation inside encrypted containers
- Secure mounting and unmounting workflows
- Evidence integrity verification with SHA-256
- Tamper detection through checksum validation
- Audit logging for access accountability
- Bash automation for security operations
- Practical DFIR evidence protection workflow
- Platform security and compliance-oriented storage design

## Real-World Use Case

A security operations or incident response team can use this type of encrypted vault to preserve forensic artifacts such as suspicious files, malware samples, packet captures, logs, memory captures, investigation notes, and chain-of-custody records. The vault protects sensitive evidence from unauthorized access, while checksum verification helps detect tampering and audit logs provide accountability for access events.

## Lessons Learned

- Encrypted containers are useful when sensitive data must be protected as a portable file.
- LUKS key slots allow multiple authentication methods, including passphrases and automation key files.
- Key files require strict permissions because access to the key can unlock the encrypted container.
- Integrity checks are essential because encryption protects confidentiality but does not prove evidence was unchanged after access.
- Audit logging improves accountability by recording who accessed or verified evidence and when.
- Binary vault images and raw key files should not be committed to public repositories.

## Troubleshooting Log

Issue:
tree was missing from the fresh Ubuntu environment.

Resolution:
Installed tree using apt.

Issue:
The original GPG command failed because vault.key was created with root ownership and 400 permissions, preventing the ubuntu user from reading it.

Resolution:
Created the encrypted backup using sudo gpg and then changed ownership of vault.key.gpg back to the ubuntu user.

Issue:
The original verification script checked only whether the mount directory existed.

Resolution:
Replaced directory existence checking with mountpoint -q so the script verifies that the encrypted vault is actually mounted.

Issue:
Modern LUKS2 output may not display older Key Slot formatting.

Resolution:
Used full cryptsetup luksDump output instead of relying only on legacy grep patterns.

Issue:
The raw key file and encrypted vault image are sensitive or oversized for normal GitHub publishing.

Resolution:
Only automation scripts, sample evidence exports, encrypted key backup, audit log, and documentation are prepared for version control.
