import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "app" / "models"


def run(command):
    print("\n> " + " ".join(command) + "\n")
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def create_model(name):
    snake = name.strip().replace("-", "_").replace(" ", "_")
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", snake).lower()
    snake = re.sub(r"_+", "_", snake).strip("_")

    if not snake:
        print("ERROR: Invalid model name.")
        sys.exit(1)

    class_name = "".join(part.capitalize() for part in snake.split("_"))
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    target = MODELS_DIR / f"{snake}.py"

    if target.exists():
        print(f"Model already exists: {target}")
        sys.exit(1)

    table_name = snake if snake.endswith("s") else snake + "s"

    content = (
        "from sqlalchemy import String\n"
        "from sqlalchemy.orm import Mapped, mapped_column\n\n"
        "from app.db.database import Base\n\n\n"
        f"class {class_name}(Base):\n"
        f'    __tablename__ = "{table_name}"\n\n'
        "    # TODO: Add the real fields.\n"
        "    # Example:\n"
        "    # id: Mapped[str] = mapped_column(primary_key=True)\n"
        "    # name: Mapped[str] = mapped_column(String(150), nullable=False)\n"
    )

    target.write_text(content, encoding="utf-8")
    print(f"Model created: {target}")
    print("Next: register it in app/models/__init__.py")


def main():
    parser = argparse.ArgumentParser(description="AI-LMS DB helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("model", help="Create model template")
    p.add_argument("name")

    p = sub.add_parser("migration", help="Create Alembic migration")
    p.add_argument("message")

    sub.add_parser("upgrade", help="Apply all migrations")
    sub.add_parser("downgrade", help="Rollback one migration")
    sub.add_parser("current", help="Show current migration")
    sub.add_parser("check", help="Check schema differences")
    sub.add_parser("history", help="Show migration history")

    args = parser.parse_args()

    if args.command == "model":
        create_model(args.name)
    elif args.command == "migration":
        run(["alembic", "revision", "--autogenerate", "-m", args.message])
    elif args.command == "upgrade":
        run(["alembic", "upgrade", "head"])
    elif args.command == "downgrade":
        run(["alembic", "downgrade", "-1"])
    elif args.command == "current":
        run(["alembic", "current"])
    elif args.command == "check":
        run(["alembic", "check"])
    elif args.command == "history":
        run(["alembic", "history"])


if __name__ == "__main__":
    main()
