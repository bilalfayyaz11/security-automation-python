#!/usr/bin/env python3
from rbac_simulator import Permission, RBACSystem

rbac = RBACSystem()

manager = rbac.create_role("manager")
manager.add_permission(Permission("read", "reports"))
manager.add_permission(Permission("write", "reports"))

developer = rbac.create_role("developer")
developer.add_permission(Permission("read", "code"))
developer.add_permission(Permission("write", "code"))

user = rbac.create_user("john")
user.assign_role(manager)
user.assign_role(developer)

print(f"Can read reports: {rbac.check_access('john', 'read', 'reports')}")
print(f"Can delete reports: {rbac.check_access('john', 'delete', 'reports')}")
print(f"John's roles: {user.role_names()}")
print(f"Can write code: {rbac.check_access('john', 'write', 'code')}")
print(f"Can write reports: {rbac.check_access('john', 'write', 'reports')}")
