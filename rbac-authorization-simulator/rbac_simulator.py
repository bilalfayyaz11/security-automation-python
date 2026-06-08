#!/usr/bin/env python3
"""
Role-Based Access Control Simulator

Implements users, roles, permissions, resources, access decisions,
multi-role assignment, role hierarchy, and audit logging.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class Permission:
    """
    Represents a single permission in the RBAC system.
    A permission defines an action that can be performed on a resource.
    """

    action: str
    resource: str

    def __post_init__(self):
        object.__setattr__(self, "action", self.action.lower().strip())
        object.__setattr__(self, "resource", self.resource.lower().strip())

    def __str__(self) -> str:
        return f"{self.action}:{self.resource}"


class Role:
    """
    Represents a role in the RBAC system.
    A role is a collection of permissions and can inherit from parent roles.
    """

    def __init__(self, name: str):
        self.name = name.lower().strip()
        self.permissions: Set[Permission] = set()
        self.parent_roles: Set["Role"] = set()

    def add_permission(self, permission: Permission) -> None:
        self.permissions.add(permission)

    def add_parent_role(self, parent_role: "Role") -> None:
        if parent_role.name == self.name:
            raise ValueError("A role cannot inherit from itself")
        self.parent_roles.add(parent_role)

    def has_permission(self, permission: Permission) -> bool:
        if permission in self.permissions:
            return True

        return any(parent.has_permission(permission) for parent in self.parent_roles)

    def all_permissions(self) -> Set[Permission]:
        permissions = set(self.permissions)
        for parent in self.parent_roles:
            permissions.update(parent.all_permissions())
        return permissions

    def __str__(self) -> str:
        return f"Role: {self.name} ({len(self.all_permissions())} effective permissions)"


class User:
    """
    Represents a user in the RBAC system.
    A user can have multiple roles.
    """

    def __init__(self, username: str):
        self.username = username.lower().strip()
        self.roles: Set[Role] = set()

    def assign_role(self, role: Role) -> None:
        self.roles.add(role)

    def has_permission(self, permission: Permission) -> bool:
        return any(role.has_permission(permission) for role in self.roles)

    def role_names(self) -> List[str]:
        return sorted(role.name for role in self.roles)

    def __str__(self) -> str:
        return f"User: {self.username} (Roles: {self.role_names()})"


class RBACSystem:
    """
    Main RBAC system that manages users, roles, permissions, and access decisions.
    """

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.roles: Dict[str, Role] = {}
        self.audit_log: List[Dict] = []

    def create_role(self, role_name: str) -> Role:
        normalized = role_name.lower().strip()

        if normalized in self.roles:
            return self.roles[normalized]

        role = Role(normalized)
        self.roles[normalized] = role
        return role

    def create_user(self, username: str) -> User:
        normalized = username.lower().strip()

        if normalized in self.users:
            return self.users[normalized]

        user = User(normalized)
        self.users[normalized] = user
        return user

    def assign_role_to_user(self, username: str, role_name: str) -> bool:
        user = self.users.get(username.lower().strip())
        role = self.roles.get(role_name.lower().strip())

        if not user or not role:
            return False

        user.assign_role(role)
        return True

    def check_access(self, username: str, action: str, resource: str) -> bool:
        normalized_username = username.lower().strip()
        user = self.users.get(normalized_username)
        permission = Permission(action, resource)

        allowed = bool(user and user.has_permission(permission))

        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "username": normalized_username,
            "permission": str(permission),
            "decision": "GRANTED" if allowed else "DENIED",
            "roles": user.role_names() if user else [],
        })

        return allowed

    def display_system_state(self) -> None:
        print("\n=== RBAC System State ===")

        print(f"\nRoles ({len(self.roles)}):")
        for role in sorted(self.roles.values(), key=lambda item: item.name):
            print(f"  - {role}")
            if role.parent_roles:
                parents = ", ".join(sorted(parent.name for parent in role.parent_roles))
                print(f"    inherits: {parents}")
            for permission in sorted(role.all_permissions(), key=lambda perm: str(perm)):
                print(f"    * {permission}")

        print(f"\nUsers ({len(self.users)}):")
        for user in sorted(self.users.values(), key=lambda item: item.username):
            print(f"  - {user}")

    def display_audit_log(self) -> None:
        print("\n=== Access Audit Log ===")
        for event in self.audit_log:
            print(
                f"{event['timestamp']} | {event['username']} | "
                f"{event['permission']} | {event['decision']} | roles={event['roles']}"
            )
