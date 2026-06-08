# RBAC Authorization Simulator

## What This Does

This implementation provides a Python-based Role-Based Access Control simulator for modeling authorization decisions. It implements users, roles, permissions, resources, multi-role assignment, role inheritance, and access decision auditing.

The simulator demonstrates how access control systems decide whether a user should be allowed to perform a specific action on a protected resource. It includes a document-management scenario with admin, editor, viewer, and auditor roles, plus a custom multi-role scenario showing how one user can inherit permissions from multiple job functions.

This type of authorization model is used across cloud platforms, databases, operating systems, enterprise applications, Kubernetes, identity systems, and internal security platforms.

## Architecture

    +-----------------------------+
    | Users                        |
    | alice / bob / charlie / dana |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Assigned Roles               |
    | admin / editor / viewer      |
    | auditor / manager / developer|
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Permission Evaluation Engine |
    | rbac_simulator.py            |
    | - Direct role permissions    |
    | - Inherited permissions      |
    | - Multi-role permissions     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Access Decisions             |
    | GRANTED / DENIED             |
    | audit_log entries            |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y python3 tree git

mkdir -p ~/rbac-authorization-simulator

cd ~/rbac-authorization-simulator

## How to Reproduce

Run the main RBAC scenario:

python3 test_rbac.py

Run the basic inline functionality check:

python3 << 'PY'
from rbac_simulator import RBACSystem, Permission

rbac = RBACSystem()
admin = rbac.create_role("admin")
admin.add_permission(Permission("read", "file"))

user = rbac.create_user("testuser")
user.assign_role(admin)

result = rbac.check_access("testuser", "read", "file")
print("Access granted!" if result else "Access denied!")
PY

Run the custom multi-role scenario:

python3 custom_test.py

Verify Python syntax:

python3 -m py_compile rbac_simulator.py test_rbac.py custom_test.py

Review the file tree:

tree .

## Tools Used

- Python 3
- dataclasses
- sets
- dictionaries
- type hints
- datetime
- Bash
- Linux
- tree
- Git

## Key Skills Demonstrated

- Role-Based Access Control design
- Authorization logic implementation
- User-role assignment
- Permission modeling
- Multi-role access evaluation
- Role inheritance
- Immutable permission objects
- Hashable security primitives
- Audit logging for access decisions
- Access-control test scenario design
- IAM fundamentals
- Security engineering logic
- Cloud authorization concepts

## Real-World Use Case

A production platform can use RBAC to control access to sensitive actions such as reading documents, updating records, deleting resources, managing users, or viewing audit logs. For example, an enterprise document platform may allow viewers to read documents, editors to read and write documents, admins to delete documents and manage users, and auditors to review access logs. This simulator demonstrates the core authorization decision pattern behind systems such as AWS IAM, Azure RBAC, Kubernetes RBAC, database roles, and internal enterprise access platforms.

## Lessons Learned

- RBAC simplifies access control by assigning permissions to roles instead of assigning permissions directly to every user.
- Users can have multiple roles, and their effective permissions are the union of all assigned roles.
- Permission objects must be immutable and hashable when used inside sets.
- Role inheritance makes authorization models easier to scale because higher-level roles can inherit lower-level capabilities.
- Audit logs are essential because access decisions should be explainable after the fact.

## Troubleshooting Log

Issue:
The starter implementation left critical methods as pass, so permissions, role assignment, and access checks could not work.

Resolution:
Implemented all access-control methods including permission equality, role permission assignment, user role assignment, role permission lookup, user permission lookup, role creation, user creation, and access evaluation.

Issue:
Permissions were intended to be stored in sets, but set membership requires reliable equality and hashing.

Resolution:
Implemented Permission as a frozen dataclass so permission objects are immutable, comparable, and hashable.

Issue:
The base scenario only demonstrated simple direct role assignment.

Resolution:
Added role hierarchy so editor inherits viewer permissions and admin inherits editor permissions.

Issue:
The base scenario did not show access decision traceability.

Resolution:
Added audit logging so every access check records timestamp, username, permission, decision, and active roles.

Issue:
The base scenario did not test users with multiple roles.

Resolution:
Added a custom multi-role scenario where one user receives both manager and developer roles.
