#!/usr/bin/env python3
"""
RBAC simulator demonstration.

Models a document management access-control system with admin,
editor, viewer, and auditor roles.
"""

from rbac_simulator import Permission, RBACSystem


def main():
    rbac = RBACSystem()

    print("=== Setting up RBAC System ===\n")

    admin = rbac.create_role("admin")
    editor = rbac.create_role("editor")
    viewer = rbac.create_role("viewer")
    auditor = rbac.create_role("auditor")

    viewer.add_permission(Permission("read", "document"))

    editor.add_parent_role(viewer)
    editor.add_permission(Permission("write", "document"))

    admin.add_parent_role(editor)
    admin.add_permission(Permission("delete", "document"))
    admin.add_permission(Permission("manage", "users"))

    auditor.add_permission(Permission("read", "audit-log"))

    alice = rbac.create_user("alice")
    bob = rbac.create_user("bob")
    charlie = rbac.create_user("charlie")
    dana = rbac.create_user("dana")

    alice.assign_role(admin)
    bob.assign_role(editor)
    charlie.assign_role(viewer)
    dana.assign_role(viewer)
    dana.assign_role(auditor)

    rbac.display_system_state()

    print("\n=== Testing Access Control ===\n")

    test_cases = [
        ("alice", "delete", "document", True),
        ("alice", "manage", "users", True),
        ("bob", "write", "document", True),
        ("bob", "delete", "document", False),
        ("charlie", "read", "document", True),
        ("charlie", "write", "document", False),
        ("dana", "read", "audit-log", True),
        ("dana", "delete", "document", False),
        ("unknown", "read", "document", False),
    ]

    passed = 0

    for username, action, resource, expected in test_cases:
        result = rbac.check_access(username, action, resource)
        status = "GRANTED" if result else "DENIED"
        check = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        print(f"{check} {username} -> {action}:{resource} = {status}")

    print(f"\nPassed: {passed}/{len(test_cases)}")

    rbac.display_audit_log()


if __name__ == "__main__":
    main()
