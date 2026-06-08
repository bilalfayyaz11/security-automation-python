# Encrypted Evidence Vault

## What This Does

This implementation provides a secure encrypted evidence storage platform using Linux Unified Key Setup (LUKS), cryptographic key management, integrity verification, and audit logging.

The solution protects sensitive forensic artifacts inside an encrypted container that remains inaccessible without authorized credentials. Multiple authentication mechanisms are supported through passphrases and key files, while SHA-256 integrity validation ensures evidence tampering can be detected immediately.

This architecture demonstrates security practices commonly used by Digital Forensics, Incident Response (DFIR), Cybersecurity Operations, Compliance, and Security Engineering teams responsible for protecting sensitive investigative data.

## Architecture

    +------------------------------------------------+
    | Evidence Files                                 |
    | case_001.txt                                   |
    | case_002.txt                                   |
    | chain_of_custody.log                           |
    +----------------------+-------------------------+
                           |
                           v
    +------------------------------------------------+
    | Encrypted Storage Layer                        |
    | LUKS Encrypted Container                       |
    | evidence_vault.img                             |
    +----------------------+-------------------------+
                           |
                           v
    +------------------------------------------------+
    | Access Control Layer                           |
    | Passphrase Authentication                      |
    | Backup Passphrase                              |
    | Key File Authentication                        |
    +----------------------+-------------------------+
                           |
                           v
    +------------------------------------------------+
    | Management Services                            |
    | vault_manager.sh                               |
    | verify_evidence.sh                             |
    | audit_log.sh                                   |
    +----------------------+-------------------------+
                           |
                           v
    +------------------------------------------------+
    | Security Controls                              |
    | SHA-256 Integrity Verification                 |
    | Audit Logging                                  |
    | GPG Key Backup                                 |
    +------------------------------------------------+

## Prerequisites

- Ubuntu 24.04 LTS
- cryptsetup
- GnuPG
- tree
- sudo privileges
- ext4 filesystem support
- SHA-256 utilities

## Setup & Installation

sudo apt update

sudo apt install -y cryptsetup gnupg tree

mkdir -p ~/evidence-lab

cd ~/evidence-lab

dd if=/dev/zero of=evidence_vault.img bs=1M count=100

sudo cryptsetup luksFormat evidence_vault.img

sudo cryptsetup luksOpen evidence_vault.img evidence_vault

sudo mkfs.ext4 /dev/mapper/evidence_vault

sudo mkdir -p /mnt/evidence_vault

sudo mount /dev/mapper/evidence_vault /mnt/evidence_vault

## How to Reproduce

Create and encrypt a vault:

sudo cryptsetup luksFormat evidence_vault.img

Open the vault:

sudo cryptsetup luksOpen evidence_vault.img evidence_vault

Mount the encrypted filesystem:

sudo mount /dev/mapper/evidence_vault /mnt/evidence_vault

Generate evidence integrity checksums:

cd /mnt/evidence_vault

sha256sum *.txt > evidence_checksums.sha256

Run evidence verification:

~/evidence-lab/verify_evidence.sh

Check vault status:

~/evidence-lab/vault_manager.sh status

Close vault securely:

~/evidence-lab/vault_manager.sh close

Create encrypted key backup:

gpg --symmetric --cipher-algo AES256 vault.key

## Tools Used

- Linux
- Ubuntu 24.04
- LUKS
- cryptsetup
- GnuPG
- SHA-256
- Bash
- ext4
- tree
- sudo

## Key Skills Demonstrated

- Linux disk encryption
- LUKS container management
- Secure evidence handling
- Cryptographic key management
- Multi-factor vault access
- File integrity verification
- SHA-256 hashing
- Audit trail creation
- Security automation scripting
- Incident response evidence protection
- Digital forensics workflow support
- Secure backup management

## Real-World Use Case

Organizations handling sensitive investigative data must ensure evidence remains confidential, tamper-evident, and accessible only to authorized personnel. Security Operations Centers (SOC), DFIR teams, law enforcement agencies, compliance departments, and incident response teams frequently use encrypted storage solutions to maintain chain-of-custody requirements. This implementation demonstrates how encrypted evidence repositories can be protected through layered controls including encryption, authentication, integrity verification, audit logging, and secure key backup procedures.

## Lessons Learned

- Encryption alone is insufficient without proper key management.
- Multiple key slots provide operational resilience and recovery options.
- Integrity validation is essential for detecting unauthorized evidence modification.
- Audit logs provide accountability and traceability for evidence access.
- Automated management scripts reduce operational errors during vault handling.

## Troubleshooting Log

Issue:
tree utility was not available in the default Ubuntu 24.04 environment.

Resolution:
Installed tree using apt before executing verification commands.

Issue:
verify_evidence.sh was missing when integrity testing was attempted.

Resolution:
Created the verification script and made it executable before running integrity validation.

Issue:
Evidence integrity validation failed after intentional tampering.

Resolution:
Restored the modified file and re-ran SHA-256 validation successfully.

Issue:
Original verification logic only checked whether the mount directory existed.

Resolution:
Improved validation logic to confirm the encrypted vault was actually mounted before performing integrity checks.

Issue:
LUKS key slot verification output differs between older and modern LUKS2 implementations.

Resolution:
Used full luksDump output for validation rather than relying on legacy key slot formatting.
