#!/usr/bin/env python3
"""
Dynamically scans each topic folder, counts .java and .py solution files,
and regenerates README.md with live progress bars and stats.

Aligned with: Striver's SDE Sheet — Top 191 Coding Interview Problems

Run manually:   python scripts/update_readme.py
Or via CI:       Triggered automatically by the GitHub Actions workflow.
"""

import os
import math
from datetime import datetime, timezone

# ─── Configuration ───────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Striver's SDE Sheet — 191 problems across 13 broad categories
TOPICS = [
    {
        "dir": "01_Arrays",
        "label": "Arrays",
        "total": 24,
        "sections": [
            {
                "name": "Arrays",
                "problems": [
                    ("Set Matrix Zeroes", "Medium"),
                    ("Pascal's Triangle I", "Easy"),
                    ("Next Permutation", "Medium"),
                    ("Kadane's Algorithm", "Medium"),
                    ("Sort an array of 0's 1's and 2's", "Medium"),
                    ("Stock Buy and Sell", "Medium"),
                ],
            },
            {
                "name": "Arrays Part-II",
                "problems": [
                    ("Rotate matrix by 90 degrees", "Medium"),
                    ("Merge Overlapping Subintervals", "Medium"),
                    ("Merge two sorted arrays without extra space", "Medium"),
                    ("Find the Duplicate Number", "Medium"),
                    ("Find the repeating and missing number", "Hard"),
                    ("Inversion of Array (Pre-req: Merge Sort)", "Hard"),
                ],
            },
            {
                "name": "Arrays Part-III",
                "problems": [
                    ("Search in a 2D matrix", "Hard"),
                    ("Pow(x, n)", "Easy"),
                    ("Majority Element-I", "Easy"),
                    ("Majority Element-II", "Hard"),
                    ("Grid unique paths", "Medium"),
                    ("Reverse Pairs", "Hard"),
                ],
            },
            {
                "name": "Arrays Part-IV",
                "problems": [
                    ("Two Sum", "Easy"),
                    ("4 Sum", "Medium"),
                    ("Longest Consecutive Sequence in an Array", "Medium"),
                    ("Largest Subarray with K sum", "Medium"),
                    ("Count subarrays with given xor K", "Hard"),
                    ("Longest Substring Without Repeating Characters", "Medium"),
                ],
            },
        ],
    },
    {
        "dir": "02_Linked_List",
        "label": "Linked List",
        "total": 18,
        "sections": [
            {
                "name": "Linked List",
                "problems": [
                    ("Reverse a LL", "Medium"),
                    ("Find Middle of Linked List", "Easy"),
                    ("Merge two Sorted Lists", "Hard"),
                    ("Remove Nth node from the back of the LL", "Medium"),
                    ("Add two numbers as LinkedList", "Medium"),
                    ("Delete Node in a Linked List O(1)", "Medium"),
                ],
            },
            {
                "name": "Linked List Part-II",
                "problems": [
                    ("Find the intersection point of Y LL", "Medium"),
                    ("Detect a loop in LL", "Medium"),
                    ("Reverse LL in group of given size K", "Hard"),
                    ("Check if LL is palindrome or not", "Medium"),
                    ("Find the starting point in LL", "Medium"),
                    ("Flattening of LL", "Hard"),
                ],
            },
            {
                "name": "Linked List and Arrays",
                "problems": [
                    ("Rotate a LL", "Hard"),
                    ("Clone a LL with random and next pointer", "Hard"),
                    ("3 Sum", "Medium"),
                    ("Trapping Rainwater", "Hard"),
                    ("Remove duplicates from sorted array", "Easy"),
                    ("Maximum Consecutive Ones", "Easy"),
                ],
            },
        ],
    },
    {
        "dir": "03_Greedy",
        "label": "Greedy Algorithm",
        "total": 6,
        "sections": [
            {
                "name": "Greedy Algorithm",
                "problems": [
                    ("N meetings in one room", "Medium"),
                    ("Minimum number of platforms required for a railway", "Medium"),
                    ("Job sequencing Problem", "Medium"),
                    ("Fractional Knapsack", "Medium"),
                    ("Minimum coins", "Hard"),
                    ("Assign Cookies", "Easy"),
                ],
            },
        ],
    },
    {
        "dir": "04_Recursion_and_Backtracking",
        "label": "Recursion & Backtracking",
        "total": 12,
        "sections": [
            {
                "name": "Recursion",
                "problems": [
                    ("Subset Sums", "Hard"),
                    ("Subsets II", "Medium"),
                    ("Combination Sum", "Medium"),
                    ("Combination Sum II", "Medium"),
                    ("Palindrome partitioning", "Hard"),
                    ("Permutation Sequence", "Medium"),
                ],
            },
            {
                "name": "Recursion and Backtracking",
                "problems": [
                    ("Permutations of a String", "Medium"),
                    ("N Queen", "Hard"),
                    ("Sudoku Solver", "Hard"),
                    ("M Coloring Problem", "Hard"),
                    ("Rat in a Maze", "Hard"),
                    ("Word Break (print all ways)", "Medium"),
                ],
            },
        ],
    },
    {
        "dir": "05_Binary_Search",
        "label": "Binary Search",
        "total": 8,
        "sections": [
            {
                "name": "Binary Search",
                "problems": [
                    ("The N-th root of an integer", "Medium"),
                    ("Matrix Median", "Hard"),
                    ("Single element in sorted array", "Medium"),
                    ("Search element in a sorted and rotated array", "Medium"),
                    ("Median of 2 sorted arrays", "Hard"),
                    ("Kth element of 2 sorted arrays", "Medium"),
                    ("Allocate Minimum Number of Pages", "Hard"),
                    ("Aggressive Cows", "Hard"),
                ],
            },
        ],
    },
    {
        "dir": "06_Heaps",
        "label": "Heaps",
        "total": 6,
        "sections": [
            {
                "name": "Heaps",
                "problems": [
                    ("Implement Max Heap", "Medium"),
                    ("K-th Largest element in an array", "Medium"),
                    ("Maximum Sum Combination", "Hard"),
                    ("Find Median from Data Stream", "Hard"),
                    ("Merge K Sorted Arrays", "Medium"),
                    ("Top K Frequent Elements", "Medium"),
                ],
            },
        ],
    },
    {
        "dir": "07_Stacks_and_Queues",
        "label": "Stack & Queue",
        "total": 17,
        "sections": [
            {
                "name": "Stack and Queue",
                "problems": [
                    ("Implement Stack using Arrays", "Easy"),
                    ("Implement Queue using Arrays", "Easy"),
                    ("Implement Stack using Queue (single queue)", "Easy"),
                    ("Implement Queue using Stack", "Easy"),
                    ("Balanced Parenthesis", "Easy"),
                    ("Next Greater Element", "Medium"),
                    ("Sort a Stack", "Medium"),
                ],
            },
            {
                "name": "Stack and Queue Part-II",
                "problems": [
                    ("Next Smaller Element", "Medium"),
                    ("LRU Cache", "Medium"),
                    ("LFU Cache", "Hard"),
                    ("Largest rectangle in a histogram", "Hard"),
                    ("Sliding Window Maximum", "Hard"),
                    ("Implement Min Stack", "Hard"),
                    ("Rotten Oranges", "Medium"),
                    ("Stock span problem", "Hard"),
                    ("Maximum of Minimums for Every Window Size", "Medium"),
                    ("Celebrity Problem", "Hard"),
                ],
            },
        ],
    },
    {
        "dir": "08_Strings",
        "label": "Strings",
        "total": 12,
        "sections": [
            {
                "name": "String",
                "problems": [
                    ("Reverse every word in a string", "Medium"),
                    ("Longest Palindrome in a string", "Medium"),
                    ("Roman to Integer", "Medium"),
                    ("Implement ATOI/STRSTR", "Medium"),
                    ("Longest Common Prefix", "Easy"),
                    ("Rabin Karp Algorithm", "Hard"),
                ],
            },
            {
                "name": "String Part-II",
                "problems": [
                    ("Z function", "Hard"),
                    ("KMP Algorithm or LPS array", "Hard"),
                    ("Minimum insertions to make string palindrome", "Hard"),
                    ("Valid Anagram", "Easy"),
                    ("Count and say", "Hard"),
                    ("Compare version numbers", "Medium"),
                ],
            },
        ],
    },
    {
        "dir": "09_Binary_Tree",
        "label": "Binary Tree",
        "total": 33,
        "sections": [
            {
                "name": "Binary Tree",
                "problems": [
                    ("Inorder Traversal", "Easy"),
                    ("Preorder Traversal", "Easy"),
                    ("Postorder Traversal", "Easy"),
                    ("Morris Inorder Traversal", "Hard"),
                    ("Morris Preorder Traversal", "Hard"),
                    ("Right/Left View of BT", "Medium"),
                    ("Bottom view of BT", "Medium"),
                    ("Top View of BT", "Medium"),
                    ("Pre, Post, Inorder in one traversal", "Easy"),
                    ("Vertical Order Traversal", "Medium"),
                    ("Print root to leaf path in BT", "Medium"),
                    ("Maximum Width of BT", "Medium"),
                ],
            },
            {
                "name": "Binary Tree Part-II",
                "problems": [
                    ("Level Order Traversal", "Easy"),
                    ("Maximum Depth in BT", "Medium"),
                    ("Diameter of Binary Tree", "Easy"),
                    ("Check for balanced binary tree", "Medium"),
                    ("LCA in BT", "Hard"),
                    ("Check if two trees are identical or not", "Medium"),
                    ("Zig Zag or Spiral Traversal", "Medium"),
                    ("Boundary Traversal", "Medium"),
                ],
            },
            {
                "name": "Binary Tree Part-III",
                "problems": [
                    ("Maximum path sum", "Medium"),
                    ("Construct a BT from Preorder and Inorder", "Hard"),
                    ("Construct a BT from Postorder and Inorder", "Hard"),
                    ("Symmetric Binary Tree", "Medium"),
                    ("Flatten Binary Tree to Linked List", "Medium"),
                    ("Check for symmetrical BTs", "Medium"),
                    ("Children Sum Property in Binary Tree", "Medium"),
                ],
            },
            {
                "name": "Binary Trees [Miscellaneous]",
                "problems": [
                    ("Binary Tree to Doubly Linked List", "Medium"),
                    ("Find Median in a Stream", "Medium"),
                    ("Kth largest element in a stream of running integers", "Hard"),
                    ("Distinct Numbers in Each Subarray", "Medium"),
                    ("K-th largest element in an unsorted array", "Medium"),
                    ("Flood-fill Algorithm", "Medium"),
                ],
            },
        ],
    },
    {
        "dir": "10_BST",
        "label": "Binary Search Tree",
        "total": 15,
        "sections": [
            {
                "name": "Binary Search Tree",
                "problems": [
                    ("Populating Next Right Pointers in Each Node", "Medium"),
                    ("Search in BST", "Easy"),
                    ("Construct BST from given keys", "Easy"),
                    ("Construct a BST from a preorder traversal", "Medium"),
                    ("Check if a tree is a BST or not", "Medium"),
                    ("LCA in BST", "Medium"),
                    ("Inorder successor and predecessor in BST", "Medium"),
                ],
            },
            {
                "name": "Binary Search Tree Part-II",
                "problems": [
                    ("Floor in a BST", "Easy"),
                    ("Ceil in a BST", "Easy"),
                    ("Find K-th smallest element in BST", "Medium"),
                    ("Kth Smallest and Largest element in BST", "Medium"),
                    ("Two sum in BST", "Hard"),
                    ("BST iterator", "Hard"),
                    ("Size of the largest BST in a Binary Tree", "Hard"),
                    ("Serialize and De-serialize BT", "Hard"),
                ],
            },
        ],
    },
    {
        "dir": "11_Graphs",
        "label": "Graphs",
        "total": 18,
        "sections": [
            {
                "name": "Graph",
                "problems": [
                    ("Clone Graph", "Medium"),
                    ("DFS", "Medium"),
                    ("Traversal Techniques", "Medium"),
                    ("Detect A cycle in Undirected Graph using BFS", "Hard"),
                    ("Detect A cycle in Undirected Graph using DFS", "Hard"),
                    ("Detect A cycle in a Directed Graph using DFS", "Hard"),
                    ("Detect A cycle in a Directed Graph using BFS", "Hard"),
                    ("Topological Sort BFS", "Hard"),
                    ("Topological Sort DFS", "Hard"),
                    ("Number of islands", "Medium"),
                    ("Bipartite graph", "Hard"),
                    ("Bipartite Check using DFS", "Hard"),
                ],
            },
            {
                "name": "Graph Part-II",
                "problems": [
                    ("Strongly Connected Component (Kosaraju's algo)", "Hard"),
                    ("Dijkstra's algorithm", "Hard"),
                    ("Bellman ford algorithm", "Hard"),
                    ("Floyd Warshall Algorithm", "Hard"),
                    ("MST using Prim's Algo", "Hard"),
                    ("MST using Kruskal's Algo", "Hard"),
                ],
            },
        ],
    },
    {
        "dir": "12_Dynamic_Programming",
        "label": "Dynamic Programming",
        "total": 15,
        "sections": [
            {
                "name": "Dynamic Programming",
                "problems": [
                    ("Max Product Subarray", "Hard"),
                    ("Longest Increasing Subsequence", "Medium"),
                    ("Longest common subsequence", "Hard"),
                    ("0 and 1 Knapsack", "Hard"),
                    ("Edit distance", "Hard"),
                    ("Maximum Sum Increasing Subsequence", "Medium"),
                    ("Matrix chain multiplication", "Hard"),
                ],
            },
            {
                "name": "Dynamic Programming Part-II",
                "problems": [
                    ("Minimum sum path in the matrix", "Medium"),
                    ("Coin change II", "Hard"),
                    ("Subset sum equals to target", "Hard"),
                    ("Rod cutting problem", "Hard"),
                    ("Super Egg Drop", "Medium"),
                    ("Word Break", "Medium"),
                    ("Palindrome Partitioning (MCM Variation)", "Hard"),
                    ("Maximum Profit in Job Scheduling", "Medium"),
                ],
            },
        ],
    },
    {
        "dir": "13_Trie",
        "label": "Trie",
        "total": 7,
        "sections": [
            {
                "name": "Trie",
                "problems": [
                    ("Trie Implementation and Operations", "Hard"),
                    ("Trie Implementation and Advanced Operations", "Hard"),
                    ("Longest Word with All Prefixes", "Medium"),
                    ("Number of distinct substrings in a string", "Medium"),
                    ("Power Set (this is very important)", "Medium"),
                    ("Maximum XOR of two numbers in an array", "Hard"),
                    ("Maximum Xor with an element from an array", "Hard"),
                ],
            },
        ],
    },
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


def difficulty_badge(diff: str) -> str:
    colors = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
    return colors.get(diff, "⚪")


# ─── README Generation ──────────────────────────────────────────────────────

def generate_readme() -> str:
    # Gather stats
    stats = []
    grand_solved = 0
    grand_total = 0
    total_java = 0
    total_py = 0
    total_easy = 0
    total_medium = 0
    total_hard = 0

    for topic in TOPICS:
        dir_path = os.path.join(ROOT, topic["dir"])
        counts = count_solutions(dir_path) if os.path.isdir(dir_path) else {"java": 0, "py": 0, "total": 0}
        solved = counts["total"]
        target = topic["total"]
        pct = percentage(solved, target)

        # Count difficulty distribution
        easy = medium = hard = 0
        for section in topic.get("sections", []):
            for _, diff in section["problems"]:
                if diff == "Easy":
                    easy += 1
                elif diff == "Medium":
                    medium += 1
                elif diff == "Hard":
                    hard += 1

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
            "easy": easy,
            "medium": medium,
            "hard": hard,
            "sections": topic.get("sections", []),
        })
        grand_solved += solved
        grand_total += target
        total_java += counts["java"]
        total_py += counts["py"]
        total_easy += easy
        total_medium += medium
        total_hard += hard

    grand_pct = percentage(grand_solved, grand_total)
    now = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    # ── Build Markdown ──

    lines = []

    # Header
    lines.append('<div align="center">\n')
    lines.append("# 🧠 Striver's SDE Sheet — DSA Tracker\n")
    lines.append("**A structured, daily log of my problem-solving journey through the top 191 coding interview questions**\n")
    lines.append("*Following [Striver's SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/) • Solutions in Java & Python*\n")
    lines.append("</div>\n")
    lines.append("---\n")

    # Overall progress hero section
    lines.append('<div align="center">\n')
    lines.append(f"### 📈 Overall Progress: **{grand_solved} / {grand_total}** problems solved ({grand_pct}%)\n")
    lines.append(f"`{progress_bar(grand_solved, grand_total)}` {grand_pct}%\n")
    lines.append("")
    lines.append(f"☕ **Java:** {total_java} &nbsp;│&nbsp; 🐍 **Python:** {total_py} &nbsp;│&nbsp; 📅 **Last Updated:** {now}\n")
    lines.append(f"🟢 Easy: {total_easy} &nbsp;│&nbsp; 🟡 Medium: {total_medium} &nbsp;│&nbsp; 🔴 Hard: {total_hard}\n")
    lines.append("</div>\n")
    lines.append("---\n")

    # About
    lines.append("## 📖 About\n")
    lines.append("This repository tracks my progress through **Striver's SDE Sheet** — a curated set of **191 must-do problems** from companies like Google, Amazon, Microsoft, Facebook, Flipkart, and more.\n")
    lines.append("It serves as a **personal reference guide** and a **structured tracking system** for my:\n")
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

    # ── Full Problem Checklist ──
    lines.append("## 📋 Full Problem Checklist\n")

    for s in stats:
        lines.append(f"### {s['emoji']} {s['label']}  —  `{s['solved']} / {s['target']}`\n")

        for section in s["sections"]:
            lines.append(f"<details>")
            lines.append(f"<summary><b>{section['name']}</b> ({len(section['problems'])} problems)</summary>\n")
            lines.append("| # | Problem | Difficulty |")
            lines.append("| :---: | :--- | :---: |")

            for idx, (problem, diff) in enumerate(section["problems"], 1):
                badge = difficulty_badge(diff)
                lines.append(f"| {idx} | {problem} | {badge} {diff} |")

            lines.append("\n</details>\n")

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
    lines.append("*Progress auto-updated on every push via GitHub Actions*\n")
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
