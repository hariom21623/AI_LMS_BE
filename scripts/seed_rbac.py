from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission


ROLES = [
    {
        "name": "Super Admin",
        "code": "SUPER_ADMIN",
        "description": (
            "Platform-level administrator with access to all institutes."
        ),
    },
    {
        "name": "Institute Admin",
        "code": "INSTITUTE_ADMIN",
        "description": (
            "Administrator responsible for managing an institute."
        ),
    },
    {
        "name": "Branch Admin",
        "code": "BRANCH_ADMIN",
        "description": (
            "Administrator responsible for managing an assigned branch."
        ),
    },
    {
        "name": "Teacher",
        "code": "TEACHER",
        "description": (
            "Teacher responsible for academic activities."
        ),
    },
    {
        "name": "Student",
        "code": "STUDENT",
        "description": (
            "Student with access to learning activities."
        ),
    },
]


PERMISSIONS = [
    {
        "name": "Create Institute",
        "code": "institute:create",
        "description": "Create a new institute.",
    },
    {
        "name": "Read Institute",
        "code": "institute:read",
        "description": "View institute information.",
    },
    {
        "name": "Update Institute",
        "code": "institute:update",
        "description": "Update institute information.",
    },
    {
        "name": "Delete Institute",
        "code": "institute:delete",
        "description": "Delete an institute.",
    },
    {
        "name": "Create Branch",
        "code": "branch:create",
        "description": "Create a branch under an institute.",
    },
    {
        "name": "Read Branch",
        "code": "branch:read",
        "description": "View branch information.",
    },
    {
        "name": "Update Branch",
        "code": "branch:update",
        "description": "Update branch information.",
    },
    {
        "name": "Delete Branch",
        "code": "branch:delete",
        "description": "Delete a branch.",
    },
    {
        "name": "Create User",
        "code": "user:create",
        "description": "Create a user.",
    },
    {
        "name": "Read User",
        "code": "user:read",
        "description": "View user information.",
    },
    {
        "name": "Update User",
        "code": "user:update",
        "description": "Update a user.",
    },
    {
        "name": "Delete User",
        "code": "user:delete",
        "description": "Delete a user.",
    },
        {
        "name": "Assign User Role",
        "code": "user:role:assign",
        "description": "Assign a role to a user.",
    },
    {
        "name": "Read User Roles",
        "code": "user:role:read",
        "description": "View roles assigned to a user.",
    },
    {
        "name": "Revoke User Role",
        "code": "user:role:revoke",
        "description": "Revoke a role from a user.",
    },
        {
        "name": "Delete User",
        "code": "user:delete",
        "description": "Delete a user.",
    },
    {
        "name": "Assign User Role",
        "code": "user:role:assign",
        "description": "Assign a role to a user.",
    },
    {
        "name": "Read User Roles",
        "code": "user:role:read",
        "description": "View roles assigned to a user.",
    },
    {
        "name": "Revoke User Role",
        "code": "user:role:revoke",
        "description": "Revoke a role from a user.",
    },

]


ROLE_PERMISSIONS = {
    "SUPER_ADMIN": [
        "institute:create",
        "institute:read",
        "institute:update",
        "institute:delete",
        "branch:create",
        "branch:read",
        "branch:update",
        "branch:delete",
        "user:create",
        "user:read",
        "user:update",
        "user:delete",
        "user:role:assign",
        "user:role:read",
        "user:role:revoke",
    ],
    "INSTITUTE_ADMIN": [
        "institute:read",
        "institute:update",
        "branch:create",
        "branch:read",
        "branch:update",
        "branch:delete",
        "user:create",
        "user:read",
        "user:update",
        "user:delete",
    ],
    "BRANCH_ADMIN": [
        "branch:read",
        "branch:update",
        "user:create",
        "user:read",
        "user:update",
    ],
    "TEACHER": [
        "branch:read",
        "user:read",
    ],
    "STUDENT": [
        "branch:read",
    ],
}


def seed_rbac(db: Session) -> None:
    """
    Create initial roles, permissions and role-permission mappings.

    This function is idempotent:
    running it multiple times will not create duplicate records.
    """

    role_map: dict[str, Role] = {}
    permission_map: dict[str, Permission] = {}

    # ---------------------------------------------------------
    # Create / get permissions
    # ---------------------------------------------------------

    for permission_data in PERMISSIONS:

        permission = db.scalar(
            select(Permission).where(
                Permission.code == permission_data["code"]
            )
        )

        if not permission:
            permission = Permission(
                name=permission_data["name"],
                code=permission_data["code"],
                description=permission_data["description"],
                is_active=True,
            )

            db.add(permission)
            db.flush()

        else:
            # Keep existing permission metadata synchronized.
            permission.name = permission_data["name"]
            permission.description = permission_data["description"]
            permission.is_active = True

        permission_map[permission.code] = permission

    # ---------------------------------------------------------
    # Create / get roles
    # ---------------------------------------------------------

    for role_data in ROLES:

        role = db.scalar(
            select(Role).where(
                Role.code == role_data["code"]
            )
        )

        if not role:
            role = Role(
                institute_id=None,
                name=role_data["name"],
                code=role_data["code"],
                description=role_data["description"],
                is_active=True,
            )

            db.add(role)
            db.flush()

        else:
            # Keep existing role metadata synchronized.
            role.name = role_data["name"]
            role.description = role_data["description"]
            role.is_active = True

        role_map[role.code] = role

    # ---------------------------------------------------------
    # Create / get role-permission mappings
    # ---------------------------------------------------------

    for role_code, permission_codes in ROLE_PERMISSIONS.items():

        role = role_map[role_code]

        for permission_code in permission_codes:

            permission = permission_map[permission_code]

            existing_mapping = db.scalar(
                select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id,
                )
            )

            if not existing_mapping:
                db.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id,
                    )
                )

    db.commit()


def main() -> None:
    """
    Run RBAC seed process.
    """

    db = SessionLocal()

    try:
        seed_rbac(db)

        print("RBAC seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()