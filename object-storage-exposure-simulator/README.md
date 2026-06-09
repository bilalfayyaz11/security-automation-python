# Local Object Storage Exposure Simulator

## What This Does

This implementation provides a local S3-compatible object storage exposure simulator using MinIO.

The system creates private and public buckets, uploads simulated sensitive files, intentionally applies unsafe anonymous read policies, verifies exposure through unauthenticated HTTP requests, and generates scanner output plus a security exposure report.

This type of workflow helps Cloud Security, DevSecOps, SOC, Platform Engineering, and Security Engineering teams understand how public object storage misconfigurations lead to real data exposure incidents.

## Architecture

    +-----------------------------+
    | Simulated Sensitive Data    |
    | sensitive-data/*.txt        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Local Object Storage        |
    | MinIO Server                |
    | S3-Compatible API :9000     |
    | Console :9001               |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Storage Buckets             |
    | private-bucket              |
    | public-bucket               |
    | exposed-data                |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Access Policy Layer         |
    | Anonymous Download Enabled  |
    | Public Exposure Simulated   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Exposure Detection          |
    | storage-scanner.sh          |
    | curl + mc validation        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Reports            |
    | reports/storage-scan.txt    |
    | reports/exposure-report.txt |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- curl
- wget
- tree
- MinIO server
- MinIO client
- Bash
- Open ports 9000 and 9001 inside the local environment

## Setup & Installation

sudo apt update

sudo apt install -y wget curl tree net-tools

curl -LO https://dl.min.io/server/minio/release/linux-amd64/minio

chmod +x minio

sudo mv minio /usr/local/bin/

curl -LO https://dl.min.io/client/mc/release/linux-amd64/mc

chmod +x mc

sudo mv mc /usr/local/bin/

minio --version

mc --version

## How to Reproduce

Create the runtime directories:

mkdir -p ~/object-storage-exposure-simulator

cd ~/object-storage-exposure-simulator

mkdir -p minio-storage/data sensitive-data reports scripts

Start MinIO:

MINIO_ROOT_USER=minioadmin MINIO_ROOT_PASSWORD=minioadmin nohup minio server ~/object-storage-exposure-simulator/minio-storage/data --console-address ":9001" > reports/minio-server.log 2>&1 &

echo $! > reports/minio.pid

Verify MinIO health:

curl -I http://localhost:9000/minio/health/live

Configure the MinIO client:

mc alias set localminio http://localhost:9000 minioadmin minioadmin

Create buckets:

mc mb localminio/private-bucket

mc mb localminio/public-bucket

mc mb localminio/exposed-data

Upload files:

mc cp sensitive-data/customer-data.txt localminio/private-bucket/

mc cp sensitive-data/api-keys.txt localminio/public-bucket/

mc cp sensitive-data/financial-report.txt localminio/exposed-data/

Apply unsafe public access policies:

mc anonymous set download localminio/public-bucket

mc anonymous set download localminio/exposed-data

Verify public exposure:

curl http://localhost:9000/public-bucket/api-keys.txt

curl http://localhost:9000/exposed-data/financial-report.txt

Verify private access is blocked:

curl -I http://localhost:9000/private-bucket/customer-data.txt

Run the exposure scanner:

scripts/storage-scanner.sh | tee reports/storage-scan.txt

Generate the exposure report:

scripts/generate-report.sh

Review final structure:

tree

## Detection Rules Implemented

- Public object access validation
- Anonymous download policy detection
- Private bucket access verification
- Exposed object identification
- Direct unauthenticated HTTP access testing
- Bucket risk classification
- Security report generation

## Tools Used

- MinIO
- MinIO Client
- curl
- Bash
- Linux
- tree
- nohup
- HTTP status validation

## Key Skills Demonstrated

- Object storage security assessment
- S3-compatible bucket administration
- Public access misconfiguration detection
- Anonymous access validation
- Cloud storage exposure simulation
- Security scanning automation
- Bash-based detection scripting
- HTTP evidence collection
- Cloud security risk reporting
- DevSecOps security validation
- Security engineering fundamentals
- Data exposure investigation workflow

## Real-World Use Case

Object storage services such as AWS S3, Azure Blob Storage, Google Cloud Storage, and S3-compatible platforms are commonly used to store backups, reports, logs, application data, and customer files. A misconfigured public bucket can expose sensitive information such as credentials, customer records, financial documents, backups, or internal reports. This simulator demonstrates how security teams can validate whether object storage files are publicly reachable and generate evidence-based exposure reports before real data is compromised.

## Lessons Learned

- Bucket listing permissions and direct object access permissions are not always the same.
- Public object storage exposure must be verified through unauthenticated HTTP access.
- Sensitive data should never be uploaded before access controls are confirmed.
- Anonymous download policies create high-risk exposure when applied to sensitive buckets.
- Automated scanning helps identify exposed objects faster than manual console review.

## Troubleshooting Log

Issue:
The original scanner checked bucket root paths, which can be misleading.

Resolution:
Updated the scanner to list objects through the authenticated MinIO client and then test direct unauthenticated HTTP access to each object.

Issue:
MinIO server or client download URLs may redirect or fail in some environments.

Resolution:
Used curl -LO for MinIO and mc downloads because it handles redirects reliably.

Issue:
Ports 9000 or 9001 may already be in use.

Resolution:
Checked active listeners before startup and used pkill minio before starting a clean MinIO process.

Issue:
The private bucket may block listing but public buckets can still expose known object paths.

Resolution:
Validated exposure at the object URL level instead of relying only on bucket-level HTTP status.

Issue:
This environment intentionally uses simulated secrets and customer data.

Resolution:
Kept all data synthetic and documented that real credentials, real customer records, or real financial data must never be used in exposure simulations.
