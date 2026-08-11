#!/usr/bin/env python3
"""
Sync publishable course material into the Jekyll site under docs/.

The Week-XX/ folders are the working source of truth. This script copies ONLY
the labs and flipped-material readings into docs/, adding the Jekyll front
matter each page needs. Quizzes, tests, exams, slides, and internal planning
documents are never touched by this script and are also excluded by .gitignore.

Run from the repository root after editing any lab or flipped-material file:

    python3 scripts/sync-docs.py

Re-running is safe: generated pages are overwritten from source every time.
"""

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"

# --- Explicit publish list -------------------------------------------------
# Nothing is published unless it appears here. Deliberately explicit rather
# than a glob, so adding a file to the website is always a visible change.

LABS = [
    ("Week-01/Week1_Lab1_Local_Dev_Environment.md",   "Lab_01.md", "Lab 1: Local Development Environment Setup"),
    ("Week-02/Week2_Lab2_SSH_Scripting_Services.md",  "Lab_02.md", "Lab 2: SSH, Bash Scripting, and Service Management"),
    ("Week-03/Week3_Lab3_AWS_CLI.md",                 "Lab_03.md", "Lab 3: AWS CLI — Authentication, Networking, and Your First EC2 Instance"),
    ("Week-04/Week4_Lab4_Terraform_Basics.md",        "Lab_04.md", "Lab 4: Terraform Basics"),
    ("Week-05/Week5_Lab5_Packer_CloudInit.md",        "Lab_05.md", "Lab 5: Packer & Cloud-Init"),
    ("Week-06/Week6_Lab6_Ansible_Intro.md",           "Lab_06.md", "Lab 6: Introduction to Ansible"),
    ("Week-09/Week9_Lab7_Terraform_Modules.md",       "Lab_07.md", "Lab 7: Terraform Variables & Modules"),
    ("Week-10/Week10_Lab8_Ansible_Loops_Roles.md",    "Lab_08.md", "Lab 8: Ansible Loops, Conditionals, Handlers & Roles"),
    ("Week-11/Week11_Lab9_PXE_Provisioning.md",       "Lab_09.md", "Lab 9: Bare-Metal Provisioning with PXE"),
    ("Week-12/Week12_Lab10_S3_Remote_Backend.md",     "Lab_10.md", "Lab 10: Migrating to an S3 Remote Backend"),
]

FLIPPED = [
    ("Week-01/Week1_Flipped_Material.md",   "Week_01.md", "Week 1 Flipped Material"),
    ("Week-02/Week2_Flipped_Material.md",   "Week_02.md", "Week 2 Flipped Material"),
    ("Week-03/Week3_Flipped_Material.md",   "Week_03.md", "Week 3 Flipped Material"),
    ("Week-04/Week4_Flipped_Material.md",   "Week_04.md", "Week 4 Flipped Material"),
    ("Week-05/Week5_Flipped_Material.md",   "Week_05.md", "Week 5 Flipped Material"),
    ("Week-06/Week6_Flipped_Material.md",   "Week_06.md", "Week 6 Flipped Material"),
    ("Week-07/Week7_Flipped_Material.md",   "Week_07.md", "Week 7 Flipped Material"),
    ("Week-09/Week9_Flipped_Material.md",   "Week_09.md", "Week 9 Flipped Material"),
    ("Week-10/Week10_Flipped_Material.md",  "Week_10.md", "Week 10 Flipped Material"),
    ("Week-11/Week11_Flipped_Material.md",  "Week_11.md", "Week 11 Flipped Material"),
    ("Week-12/Week12_Flipped_Material.md",  "Week_12.md", "Week 12 Flipped Material"),
]

# Guard: refuse to publish anything that looks like assessment material, even
# if someone adds it to the lists above by mistake.
FORBIDDEN = ("quiz", "test", "exam", "answer", "solution", "midterm")


def escape_yaml(value: str) -> str:
    return value.replace('"', '\\"')


def build_page(source: Path, title: str, back_label: str) -> str:
    body = source.read_text(encoding="utf-8")

    # Course material contains Packer {{timestamp}} and Ansible/Jinja {{ var }}
    # syntax. Jekyll's Liquid engine would try to evaluate those and silently
    # render them as empty strings — including inside fenced code blocks.
    # Wrapping the body in {% raw %} disables Liquid for the content while
    # leaving Markdown rendering untouched.
    return (
        "---\n"
        f'title: "{escape_yaml(title)}"\n'
        "---\n"
        "\n"
        f"[&larr; {back_label}]({{{{ '/' | relative_url }}}})\n"
        "\n"
        "{% raw %}\n"
        f"{body.rstrip()}\n"
        "{% endraw %}\n"
    )


def sync(entries, subdir: str, back_label: str) -> int:
    target_dir = DOCS / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for rel_source, out_name, title in entries:
        lowered = Path(rel_source).name.lower()
        if any(word in lowered for word in FORBIDDEN):
            sys.exit(f"REFUSING to publish assessment-like file: {rel_source}")

        source = REPO_ROOT / rel_source
        if not source.exists():
            sys.exit(f"Missing source file: {rel_source}")

        (target_dir / out_name).write_text(
            build_page(source, title, back_label), encoding="utf-8"
        )
        print(f"  {rel_source}  ->  docs/{subdir}/{out_name}")
        written += 1
    return written


def main() -> None:
    print("Syncing labs...")
    n_labs = sync(LABS, "labs", "Back to course index")
    print("Syncing flipped material...")
    n_flipped = sync(FLIPPED, "flipped-material", "Back to course index")
    print(f"\nDone. {n_labs} labs and {n_flipped} flipped-material pages written to docs/.")
    print("Slides, quizzes, tests, exams, and planning documents were not touched.")


if __name__ == "__main__":
    main()
