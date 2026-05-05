"""create users and tasks

Revision ID: 20260505_0001
Revises:
Create Date: 2026-05-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260505_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.Enum("todo", "doing", "done", name="taskstatus"), nullable=True),
        sa.Column(
            "priority",
            sa.Enum("low", "medium", "high", name="taskpriority"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_id"), "tasks", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tasks_id"), table_name="tasks")
    op.drop_table("tasks")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
