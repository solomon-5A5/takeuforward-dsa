#!/usr/bin/env python3
"""
Dynamically scans each topic folder, counts .java and .py solution files,
and regenerates README.md with live progress bars and stats.

Run manually:   python scripts/update_readme.py
Or via CI:       Triggered automatically by the GitHub Actions workflow.
"""

import os
import math
from datetime import datetime, timezone

# ─── Configuration ───────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOPICS = [
    {"dir": "01_Arrays",                     "label": "Arrays",                    "total": 40},
    {"dir": "02_Sorting",                    "label": "Sorting",                   "total": 8},
    {"dir": "03_Binary_Search",              "label": "Binary Search",             "total": 32},
    {"dir": "04_Strings",                    "label": "Strings",                   "total": 25},
    {"dir": "05_Linked_Lists",               "label": "Linked Lists",              "total": 28},
    {"dir": "06_Recursion_and_Backtracking", "label": "Recursion & Backtracking",  "total": 20},
    {"dir": "07_Stacks_and_Queues",          "label": "Stacks & Queues",           "total": 30},
    {"dir": "08_Trees",                      "label": "Trees",                     "total": 50},
    {"dir": "09_Graphs",                     "label": "Graphs",                    "total": 45},
    {"dir": "10_Dynamic_Programming",        "label": "Dynamic Programming",       "total": 55},
]

SOLUTION_EXTENSIONS = {".java", ".py"}
BAR_LENGTH = 20  # number of characters in each progress bar


# ─── Helpers ─────────────────────────────────────────────────────────────────

def count_solutions(directory: str) -> dict:
    """Return {'java': n, 'py': n, 'total': n} for unique problem files."""
    java_count = 0
    py_count = 0
    for root, _, files in os.walk(directory):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext == ".java":
                java_count += 1
            elif ext == ".py":
                py_count += 1
    # Count unique problems: each problem could have both .java and .py
    return {"java": java_count, "py": py_count, "total": max(java_count, py_count)}


def progress_bar(done: int, total: int) -> str:
    """Generate a unicode progress bar like  ████████░░░░░░░░░░░░"""
    if total == 0:
        return "░" * BAR_LENGTH
    ratio = min(done / total, 1.0)
    filled = round(ratio * BAR_LENGTH)
    empty = BAR_LENGTH - filled
    return "█" * filled + "░" * empty


def percentage(done: int, total: int) -> int:
    if total == 0:
        return 0
    return min(math.floor((done / total) * 100), 100)


def status_emoji(pct: int) -> str:
    if pct == 100:
        return "🏆"
    elif pct >= 75:
        return "🔥"
    elif pct >= 50:
        return "⚡"
    elif pct >= 25:
        return "🚀"
    elif pct > 0:
        return "🌱"
    else:
        return "⬜"


# ─── README Generation ──────────────────────────────────────────────────────

def generate_readme() -> str:
    # Gather stats
    stats = []
    grand_solved = 0
    grand_total = 0
    total_java = 0
    total_py = 0

    for topic in TOPICS:
        dir_path = os.path.join(ROOT, topic["dir"])
        counts = count_solutions(dir_path) if os.path.isdir(dir_path) else {"java": 0, "py": 0, "total": 0}
        solved = counts["total"]
        target = topic["total"]
        pct = percentage(solved, target)
        stats.append({
            "label": topic["label"],
            "dir": topic["dir"],
            "solved": solved,
            "target": target,
            "pct": pct,
            "java": counts["java"],
            "py": counts["py"],
            "bar": progress_bar(solved, target),
            "emoji": status_emoji(pct),
        })
        grand_solved += solved
        grand_total += target
        total_java += counts["java"]
        total_py += counts["py"]

    grand_pct = percentage(grand_solved, grand_total)
    now = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    # ── Build Markdown ──

    lines = []

    # Header
    lines.append('<div align="center">\n')
    lines.append("# 🧠 TakeUForward DSA Tracker\n")
    lines.append("**A structured, daily log of my Data Structures & Algorithms journey**\n")
    lines.append(f"*Following the [TakeUForward SDE Sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/) • Solutions in Java & Python*\n")
    lines.append("</div>\n")
    lines.append("---\n")

    # Overall progress hero section
    lines.append('<div align="center">\n')
    lines.append(f"### 📈 Overall Progress: **{grand_solved} / {grand_total}** problems solved ({grand_pct}%)\n")
    lines.append(f"`{progress_bar(grand_solved, grand_total)}` {grand_pct}%\n")
    lines.append("")
    lines.append(f"☕ **Java:** {total_java} &nbsp;│&nbsp; 🐍 **Python:** {total_py} &nbsp;│&nbsp; 📅 **Last Updated:** {now}\n")
    lines.append("</div>\n")
    lines.append("---\n")

    # About
    lines.append("## 📖 About\n")
    lines.append("This repository serves as a **personal reference guide** and a **structured tracking system** for my:\n")
    lines.append("- 🎓 **GATE CS & IT** preparation")
    lines.append("- 🤖 **Machine Learning** engineering readiness")
    lines.append("- 💻 **Software Engineering** technical interviews\n")
    lines.append("Every solution includes detailed complexity analysis, multiple approaches (brute → optimal), and implementations in both **Java** and **Python**.\n")
    lines.append("---\n")

    # Goals
    lines.append("## 🎯 Goals\n")
    lines.append("| Goal | Description |")
    lines.append("| :--- | :--- |")
    lines.append("| 🔁 **Consistency** | Push at least one optimized solution daily |")
    lines.append("| 🧪 **Deep Understanding** | Document Time & Space Complexity for every approach |")
    lines.append("| 🔀 **Versatility** | Translate logic across both Java and Python |")
    lines.append("| 📝 **Documentation** | Maintain clean, well-commented, interview-ready code |\n")
    lines.append("---\n")

    # Progress Table
    lines.append("## 📊 Topic-wise Progress\n")
    lines.append("| Status | Topic | Solved | Progress | Java | Python |")
    lines.append("| :---: | :--- | :---: | :--- | :---: | :---: |")

    for s in stats:
        lines.append(
            f"| {s['emoji']} | **[{s['label']}](./{s['dir']}/)** "
            f"| `{s['solved']:>2} / {s['target']:<2}` "
            f"| `{s['bar']}` {s['pct']}% "
            f"| {s['java']} | {s['py']} |"
        )

    lines.append("")
    lines.append(f"| | **TOTAL** | **`{grand_solved} / {grand_total}`** | `{progress_bar(grand_solved, grand_total)}` **{grand_pct}%** | **{total_java}** | **{total_py}** |")
    lines.append("")

    # Legend
    lines.append("<details>")
    lines.append("<summary>📌 Status Legend</summary>\n")
    lines.append("| Emoji | Meaning |")
    lines.append("| :---: | :--- |")
    lines.append("| ⬜ | Not started (0%) |")
    lines.append("| 🌱 | Just started (1–24%) |")
    lines.append("| 🚀 | Making progress (25–49%) |")
    lines.append("| ⚡ | Halfway there (50–74%) |")
    lines.append("| 🔥 | Almost done (75–99%) |")
    lines.append("| 🏆 | Completed (100%) |\n")
    lines.append("</details>\n")
    lines.append("---\n")

    # Tech Stack
    lines.append("## 🛠️ Tech Stack\n")
    lines.append("| Language | Use Case |")
    lines.append("| :--- | :--- |")
    lines.append("| ☕ **Java** | Primary solutions — industry standard for DSA interviews |")
    lines.append("| 🐍 **Python** | Alternate solutions — concise implementations & ML-ready |\n")
    lines.append("---\n")

    # Folder structure
    lines.append("## 📂 Repository Structure\n")
    lines.append("```")
    lines.append("takeuforward-dsa/")
    lines.append("├── README.md                              ← Auto-updated progress tracker")
    lines.append("├── scripts/")
    lines.append("│   └── update_readme.py                   ← Progress counter script")
    lines.append("├── templates/")
    lines.append("│   └── code_header_template.txt           ← Solution file header")

    for i, topic in enumerate(TOPICS):
        connector = "└──" if i == len(TOPICS) - 1 else "├──"
        lines.append(f"{connector} {topic['dir']}/")

    lines.append("```\n")
    lines.append("---\n")

    # How to use
    lines.append("## 🚀 Getting Started\n")
    lines.append("```bash")
    lines.append("# Clone the repository")
    lines.append("git clone https://github.com/solomon-5A5/takeuforward-dsa.git")
    lines.append("cd takeuforward-dsa")
    lines.append("")
    lines.append("# Manually update progress (or let GitHub Actions handle it)")
    lines.append("python scripts/update_readme.py")
    lines.append("```\n")
    lines.append("---\n")

    # Footer
    lines.append('<div align="center">\n')
    lines.append("**Built with discipline by [Solomon Pattapu](https://github.com/solomon-5A5)**\n")
    lines.append(f"*Progress auto-updated on every push via GitHub Actions*\n")
    lines.append("</div>\n")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    readme_path = os.path.join(ROOT, "README.md")
    content = generate_readme()

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ README.md updated successfully!")
    print(f"   Path: {readme_path}")
