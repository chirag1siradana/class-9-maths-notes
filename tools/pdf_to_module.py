#!/usr/bin/env python3
"""
pdf_to_module.py
================
Success Achievers Institute – PDF to Ultra-Premium Coaching Module Converter
Alwar, Rajasthan

Usage
-----
Convert a single PDF:
    python tools/pdf_to_module.py pdfs/class9-maths-ch01-number-systems.pdf

Convert all PDFs in pdfs/ at once:
    python tools/pdf_to_module.py --all

Output is written to modules/<pdf-stem>-module.md
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# PDF text extraction helpers
# ---------------------------------------------------------------------------

def _extract_with_pymupdf(pdf_path: Path) -> str:
    """Extract text from a PDF using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return ""
    text_parts: list[str] = []
    with fitz.open(str(pdf_path)) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)


def _extract_with_pdfminer(pdf_path: Path) -> str:
    """Extract text from a PDF using pdfminer.six (fallback)."""
    try:
        from pdfminer.high_level import extract_text as pm_extract
    except ImportError:
        return ""
    return pm_extract(str(pdf_path))


def extract_pdf_text(pdf_path: Path) -> str:
    """Try PyMuPDF first, fall back to pdfminer.six."""
    text = _extract_with_pymupdf(pdf_path)
    if text.strip():
        return text
    text = _extract_with_pdfminer(pdf_path)
    if text.strip():
        return text
    raise RuntimeError(
        f"Could not extract text from '{pdf_path}'.\n"
        "Make sure pymupdf or pdfminer.six is installed:\n"
        "    pip install -r requirements.txt\n"
        "If the PDF is a scanned image, enable OCR in requirements.txt."
    )


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

CHAPTER_RE = re.compile(r"ch(\d+)", re.IGNORECASE)
CLASS_RE = re.compile(r"class(\d+)", re.IGNORECASE)


def _guess_meta(pdf_path: Path) -> tuple[str, str, str]:
    """
    Guess class number, chapter number, and chapter name from the file name.
    Returns (class_label, chapter_num, chapter_title).
    """
    stem = pdf_path.stem  # e.g. class9-maths-ch01-number-systems
    parts = stem.split("-")

    cls_match = CLASS_RE.search(stem)
    ch_match = CHAPTER_RE.search(stem)

    class_label = cls_match.group(1) if cls_match else "9"
    chapter_num = ch_match.group(1).lstrip("0") if ch_match else "?"

    # Everything after "ch<NN>-" is the chapter name
    ch_idx = next((i for i, p in enumerate(parts) if CHAPTER_RE.fullmatch(p)), None)
    if ch_idx is not None and ch_idx + 1 < len(parts):
        chapter_title = " ".join(p.capitalize() for p in parts[ch_idx + 1 :])
    else:
        chapter_title = stem.replace("-", " ").title()

    return class_label, chapter_num, chapter_title


def _wrap(text: str, width: int = 90) -> str:
    return textwrap.fill(text, width=width)


def _section_lines(raw: str, max_chars: int = 6000) -> list[str]:
    """
    Split raw extracted text into non-empty lines, truncated to max_chars so
    the module stays readable.
    """
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    combined = "\n".join(lines)
    if len(combined) > max_chars:
        combined = combined[:max_chars] + "\n\n_(Content truncated — see full PDF for remainder.)_"
    return combined.splitlines()


# ---------------------------------------------------------------------------
# Module builder
# ---------------------------------------------------------------------------

TAGLINE = "Success Achievers Institute | Better Than Others, No One Can Refute"
MOTIVATION = "Master the concepts, conquer the exams!"
FOOTER = (
    "Success Achievers Institute – Alwar  |  "
    "Premium Concept Notes  |  "
    f"Academic Session 2025–26"
)


def _page_header(class_label: str, chapter_title: str) -> str:
    return f"""\
---

```
╔══════════════════════════════════════════════════════════════════╗
║              SUCCESS ACHIEVERS INSTITUTE                         ║
║          Class {class_label} – Mathematics                                ║
║      Chapter: {chapter_title:<50}║
║  "{TAGLINE[:55]}"  ║
║         "{MOTIVATION}"              ║
╚══════════════════════════════════════════════════════════════════╝
```

---
"""


def _page_footer() -> str:
    return f"\n> 📌 _{FOOTER}_\n\n---\n"


def _concept_box(name: str, explanation: str, formula: str = "", example: str = "") -> str:
    parts = [
        "```",
        "┌─────────────────────────────────────────┐",
        f"│  📘 CONCEPT BOX: {name:<23}│",
        "├─────────────────────────────────────────┤",
        f"│  {_wrap(explanation, 41):<41}│",
    ]
    if formula:
        parts.append(f"│  Formula : {formula:<30}│")
    if example:
        parts.append(f"│  Example : {example:<30}│")
    parts += [
        "└─────────────────────────────────────────┘",
        "```",
        "",
    ]
    return "\n".join(parts)


def _memory_trick(trick: str) -> str:
    return f"""\
> 🧠 **MEMORY TRICK:**
> {trick}
"""


def _board_exam_alert(tip: str) -> str:
    return f"""\
> ⚠️ **BOARD EXAM ALERT:**
> {tip}
"""


def _common_mistake(mistake: str) -> str:
    return f"""\
> ❌ **COMMON STUDENT MISTAKE:**
> {mistake}
"""


def _competitive_edge(tip: str) -> str:
    return f"""\
> 🏆 **COMPETITIVE EDGE (JEE/NEET Foundation):**
> {tip}
"""


def _brand_line() -> str:
    return (
        "\n> 💡 *At Success Achievers Institute, we focus on concept mastery, "
        "not rote learning.*\n"
    )


def _classroom_dialogue(teacher: str, student: str, teacher2: str = "") -> str:
    lines = [
        "```",
        "🎓 CLASSROOM MOMENT",
        f"  Teacher : \"{teacher}\"",
        f"  Student : \"{student}\"",
    ]
    if teacher2:
        lines.append(f"  Teacher : \"{teacher2}\"")
    lines += ["```", ""]
    return "\n".join(lines)


def _quick_revision_box(points: list[str], formulas: list[str]) -> str:
    lines = [
        "---",
        "### 📋 QUICK REVISION BOX",
        "",
        "**Key Points:**",
    ]
    for p in points:
        lines.append(f"- {p}")
    lines += ["", "**Key Formulas:**"]
    for f in formulas:
        lines.append(f"- {f}")
    lines += ["", "---", ""]
    return "\n".join(lines)


def _smart_board_answer(topic: str, definition: str, formula: str, explanation: str) -> str:
    return f"""\
#### ✍️ SMART BOARD ANSWER: {topic}

| Part | Content |
|------|---------|
| **Definition** | {definition} |
| **Formula** | {formula} |
| **Explanation** | {explanation} |
| **Diagram** | _(Draw the relevant figure with all labels)_ |

"""


def _mcqs(chapter_title: str, items: list[tuple[str, list[str], str]]) -> str:
    lines = [
        "---",
        "## 📝 MCQs (Multiple Choice Questions)",
        "",
        f"*Chapter: {chapter_title}*",
        "",
    ]
    for i, (q, opts, ans) in enumerate(items, 1):
        lines.append(f"**Q{i}.** {q}")
        for opt in opts:
            lines.append(f"   {opt}")
        lines.append(f"   **Answer:** {ans}")
        lines.append("")
    return "\n".join(lines)


def _assertion_reasoning(items: list[tuple[str, str, str]]) -> str:
    lines = [
        "---",
        "## 🔍 Assertion–Reasoning Questions",
        "",
        "**Instructions:** Choose the correct option:",
        "- (A) Both Assertion and Reason are true; Reason is the correct explanation of Assertion.",
        "- (B) Both are true; Reason is NOT the correct explanation.",
        "- (C) Assertion is true; Reason is false.",
        "- (D) Assertion is false; Reason is true.",
        "",
    ]
    for i, (assertion, reason, answer) in enumerate(items, 1):
        lines += [
            f"**Q{i}.**",
            f"  **Assertion (A):** {assertion}",
            f"  **Reason (R):** {reason}",
            f"  **Answer:** {answer}",
            "",
        ]
    return "\n".join(lines)


def _vsa(items: list[tuple[str, str]]) -> str:
    lines = ["---", "## ✏️ Very Short Answer Questions (1 Mark)", ""]
    for i, (q, a) in enumerate(items, 1):
        lines += [f"**Q{i}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(lines)


def _sa(items: list[tuple[str, str]]) -> str:
    lines = ["---", "## 📄 Short Answer Questions (2–3 Marks)", ""]
    for i, (q, a) in enumerate(items, 1):
        lines += [f"**Q{i}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(lines)


def _case_study(items: list[dict]) -> str:
    lines = ["---", "## 📊 Case Study Questions", ""]
    for i, cs in enumerate(items, 1):
        lines += [
            f"### Case Study {i}: {cs['title']}",
            "",
            cs["scenario"],
            "",
        ]
        for j, (q, a) in enumerate(cs["questions"], 1):
            lines += [f"**Q{j}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(lines)


def _competency(items: list[tuple[str, str]]) -> str:
    lines = ["---", "## 🎯 Competency-Based Questions", ""]
    for i, (q, a) in enumerate(items, 1):
        lines += [f"**Q{i}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(lines)


def _branding_page() -> str:
    return f"""
---

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              SUCCESS ACHIEVERS INSTITUTE                         ║
║                  Alwar, Rajasthan                                ║
║                                                                  ║
║              Premium Concept Notes                               ║
║        "Better Than Others, No One Can Refute"                   ║
║                                                                  ║
║              Designed by Academic Team                           ║
║           Academic Session 2025–26                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```
"""


# ---------------------------------------------------------------------------
# Chapter-specific enrichment data
# ---------------------------------------------------------------------------
# Each entry provides the rich coaching content that cannot be automatically
# extracted from raw PDF text — concept boxes, dialogues, MCQs, etc.
# Keys are lowercase chapter-title fragments matched against the PDF file name.
# ---------------------------------------------------------------------------

CHAPTER_DATA: dict[str, dict] = {
    "number": {
        "concepts": [
            ("Real Numbers", "Every number on the number line is real. Real = Rational ∪ Irrational.", "ℝ = ℚ ∪ (ℝ\\ℚ)", "√2 ∈ ℝ but √2 ∉ ℚ"),
            ("Rational Numbers", "Expressible as p/q, p,q ∈ ℤ, q ≠ 0.", "p/q, q ≠ 0", "3/4, −7, 0.333..."),
            ("Irrational Numbers", "Non-terminating and non-repeating decimals.", "Cannot be written as p/q", "√2 = 1.41421..."),
            ("Laws of Exponents", "Rules governing powers of real numbers.", "aᵐ × aⁿ = aᵐ⁺ⁿ; (aᵐ)ⁿ = aᵐⁿ", "(2³)² = 2⁶ = 64"),
        ],
        "memory": "**RILE** → **R**ational numbers **I**nclude fractions, **L**ong decimals repeat, **I**rrational decimals **E**nd never!",
        "alert": "Rationalization of denominators is asked almost every year. Always multiply by the conjugate.",
        "mistake": "Students often say 22/7 = π. It is only an approximation! π is irrational; 22/7 is rational.",
        "competitive": "Laws of exponents are directly used in JEE logarithm and surds problems.",
        "dialogue": (
            "Imagine rational numbers are well-behaved students who always sit in proper rows.",
            "So, sir, irrational numbers are the rebels who never follow a pattern?",
            "Exactly! That's why their decimal expansion never repeats and never terminates!",
        ),
        "revision_points": [
            "Real Numbers = Rational + Irrational",
            "Rational → terminating or recurring decimals",
            "Irrational → non-terminating, non-recurring",
            "Rationalise by multiplying conjugate",
            "a⁰ = 1 for any a ≠ 0",
        ],
        "revision_formulas": [
            "(√a + √b)(√a − √b) = a − b",
            "aᵐ × aⁿ = aᵐ⁺ⁿ",
            "(aᵐ)ⁿ = aᵐⁿ",
            "a^(1/n) = ⁿ√a",
        ],
        "mcqs": [
            ("Which of the following is irrational?", ["(A) 0.25", "(B) 22/7", "(C) √3", "(D) 4/9"], "(C) √3"),
            ("Value of (27)^(2/3) is:", ["(A) 3", "(B) 6", "(C) 9", "(D) 18"], "(C) 9"),
            ("Rationalising factor of 1/(√5 + 2) is:", ["(A) √5 − 2", "(B) √5 + 2", "(C) 2 − √5", "(D) None"], "(A) √5 − 2"),
            ("2⁵ × 2⁻³ equals:", ["(A) 2²", "(B) 2⁸", "(C) 4⁻¹", "(D) 2"], "(A) 2²"),
            ("Which is NOT a real number?", ["(A) √−1", "(B) √2", "(C) π", "(D) 0"], "(A) √−1 (it is imaginary)"),
            ("0.101001000... is:", ["(A) Rational", "(B) Irrational", "(C) Integer", "(D) Whole number"], "(B) Irrational"),
            ("Value of (64)^(1/6) is:", ["(A) 2", "(B) 4", "(C) 8", "(D) 6"], "(A) 2"),
            ("If a = 2, b = 3, then (√a + √b)(√a − √b) =", ["(A) 5", "(B) −1", "(C) 1", "(D) 6"], "(B) −1"),
            ("Every rational number is:", ["(A) Natural", "(B) Integer", "(C) Real", "(D) Irrational"], "(C) Real"),
            ("Which decimal is rational?", ["(A) 0.101001...", "(B) π", "(C) 0.333...", "(D) √7"], "(C) 0.333..."),
        ],
        "ar": [
            ("√2 is irrational.", "√2 cannot be expressed in p/q form.", "(A)"),
            ("0 is a rational number.", "0 = 0/1, which is in p/q form.", "(A)"),
            ("All integers are rational.", "Integers can be written as n/1.", "(A)"),
            ("22/7 = π", "22/7 is a rational approximation of π.", "(D) Assertion is false; 22/7 ≠ π exactly."),
            ("(√3)² = 3 is rational.", "Squaring an irrational can give a rational.", "(A)"),
        ],
        "vsa": [
            ("Define irrational number.", "A number that cannot be written as p/q, q ≠ 0, with non-terminating non-repeating decimal expansion."),
            ("Is 0.6̄ rational?", "Yes. 0.6̄ = 6/9 = 2/3."),
            ("Simplify: (√5)².", "5"),
            ("State: product of two irrationals.", "May be rational or irrational. e.g. √2 × √2 = 2 (rational)."),
            ("Write a between 2 and 3.", "Any value such as 2.5 or √5 ≈ 2.236."),
        ],
        "sa": [
            ("Rationalise the denominator: 5/(√7 − 2).", "Multiply by (√7 + 2)/(√7 + 2): 5(√7 + 2)/(7 − 4) = 5(√7 + 2)/3."),
            ("Simplify (2 + √3)².", "4 + 4√3 + 3 = 7 + 4√3."),
            ("Express 0.4̄7̄ as p/q.", "Let x = 0.474747... → 100x = 47.4747... → 99x = 47 → x = 47/99."),
            ("Evaluate: (8/27)^(−2/3).", "= (27/8)^(2/3) = (3/2)² = 9/4."),
            ("Locate √5 on the number line.", "Draw right triangle with legs 2 and 1; hypotenuse = √5. Mark on number line."),
        ],
        "case_studies": [
            {
                "title": "The Number Line Journey",
                "scenario": (
                    "Aryan's teacher asked him to classify numbers and place them on a number line. "
                    "Aryan found the following numbers: 3/4, √7, −2, 0.121221222..., 22/7, π."
                ),
                "questions": [
                    ("Which numbers are rational?", "3/4, −2, 22/7 are rational."),
                    ("Which are irrational?", "√7, 0.121221222..., π are irrational."),
                    ("Is 22/7 = π?", "No. 22/7 is rational (≈ 3.1428...) and π is irrational (≈ 3.14159...)."),
                ],
            },
            {
                "title": "Laws of Exponents in Science",
                "scenario": (
                    "A science teacher explained that the speed of light is 3 × 10⁸ m/s and "
                    "the charge of an electron is 1.6 × 10⁻¹⁹ C. She asked students to apply exponent laws."
                ),
                "questions": [
                    ("Simplify: (3 × 10⁸) × (2 × 10⁻³).", "= 6 × 10⁵"),
                    ("Simplify: 10⁸ ÷ 10⁻¹⁹.", "= 10²⁷"),
                    ("Express 0.000001 in scientific notation.", "= 10⁻⁶"),
                ],
            },
            {
                "title": "Rationalisation in Architecture",
                "scenario": (
                    "An architect found the diagonal of a square tile is √50 cm. "
                    "He needed to rationalise expressions to find exact dimensions."
                ),
                "questions": [
                    ("Simplify √50.", "√50 = 5√2"),
                    ("Rationalise 10/√2.", "= 10√2/2 = 5√2"),
                    ("If side = 5 cm, find area and diagonal.", "Area = 25 cm²; Diagonal = 5√2 cm."),
                ],
            },
        ],
        "competency": [
            ("A carpenter needs to cut a piece of wood into √3 m lengths. Is √3 rational or irrational? How would you help him measure it precisely?", "√3 is irrational. Use geometric construction: draw a right triangle with legs 1 m and √2 m (itself a hypotenuse of a 1–1 right triangle); the hypotenuse = √3."),
            ("Two students argue: Priya says π = 22/7; Raj says π ≠ 22/7. Who is right and why?", "Raj is correct. π is irrational (non-terminating, non-repeating), while 22/7 is rational. 22/7 is only an approximation."),
            ("A scientist writes mass of a proton = 1.67 × 10⁻²⁷ kg. Express this without scientific notation.", "0.00000000000000000000000000167 kg"),
            ("Simplify √(48) − √(27) and state whether the result is rational or irrational.", "4√3 − 3√3 = √3, which is irrational."),
            ("Without a calculator, prove that 7 + √2 is irrational.", "Assume 7 + √2 = p/q (rational). Then √2 = p/q − 7 = (p − 7q)/q, which is rational — contradiction. Hence 7 + √2 is irrational."),
        ],
    },
    "polynomial": {
        "concepts": [
            ("Polynomial", "An algebraic expression with non-negative integer powers of a variable.", "aₙxⁿ + ... + a₁x + a₀", "3x² − 2x + 1"),
            ("Degree", "Highest power of the variable in the polynomial.", "Degree = highest exponent", "Degree of 4x³ − x is 3"),
            ("Zero of Polynomial", "Value of x where p(x) = 0.", "p(c) = 0 ⟹ c is a zero", "p(x) = x−2; zero is x = 2"),
            ("Factor Theorem", "If p(a) = 0 then (x−a) is a factor of p(x).", "p(a) = 0 ⟺ (x−a) | p(x)", "p(2) = 0 ⟹ (x−2) is a factor"),
        ],
        "memory": "**RIFLE** → **R**emainder **I**s **F**ound by **L**etting x = that value (Remainder Theorem).",
        "alert": "In board exams, students are often asked to factorise cubic polynomials using Factor Theorem + long division.",
        "mistake": "Degree of a zero polynomial is undefined — NOT zero. Don't confuse the zero polynomial with a constant.",
        "competitive": "Polynomial identities like a³ + b³ + c³ − 3abc are directly asked in JEE Mains.",
        "dialogue": (
            "A polynomial is like a recipe. Each term is an ingredient.",
            "So, sir, the degree is how many of the 'strongest' ingredient we have?",
            "Brilliant! And finding the zero means figuring out what input gives us an empty dish — output zero!",
        ),
        "revision_points": [
            "Degree determines polynomial type",
            "Remainder Theorem: p(a) is the remainder when p(x) ÷ (x−a)",
            "Factor Theorem: (x−a) is factor ⟺ p(a) = 0",
            "Linear → 1 zero; Quadratic → up to 2 zeros; Cubic → up to 3 zeros",
        ],
        "revision_formulas": [
            "(a+b)² = a²+2ab+b²",
            "(a−b)² = a²−2ab+b²",
            "a²−b² = (a+b)(a−b)",
            "(a+b)³ = a³+3a²b+3ab²+b³",
            "a³+b³+c³−3abc = (a+b+c)(a²+b²+c²−ab−bc−ca)",
        ],
        "mcqs": [
            ("The zero of p(x) = 3x − 6 is:", ["(A) 6", "(B) 2", "(C) −2", "(D) 3"], "(B) 2"),
            ("Degree of 5 is:", ["(A) 1", "(B) 0", "(C) 5", "(D) Undefined"], "(B) 0"),
            ("If p(x) = x² − 5x + 6, then p(2) =", ["(A) 0", "(B) 4", "(C) −4", "(D) 2"], "(A) 0"),
            ("(x + 2) is a factor of x³ + kx + 4 if k =", ["(A) 6", "(B) −6", "(C) 2", "(D) −2"], "(A) 6"),
            ("Factorise: x² − 5x + 6", ["(A) (x−2)(x−3)", "(B) (x+2)(x+3)", "(C) (x−1)(x−6)", "(D) (x−2)(x+3)"], "(A) (x−2)(x−3)"),
            ("(a+b)³ − (a−b)³ =", ["(A) 2b³", "(B) 2(3a²b+b³)", "(C) 6a²b+2b³", "(D) Both B and C"], "(D) Both B and C"),
            ("Remainder when x³ − 2x + 1 is divided by (x−1):", ["(A) 0", "(B) 1", "(C) −1", "(D) 2"], "(A) 0"),
            ("Which is a polynomial?", ["(A) x + 1/x", "(B) √x + 1", "(C) 3x² − 2x + 1", "(D) x^(1/2)"], "(C) 3x² − 2x + 1"),
            ("Zero of 2x + 4 is:", ["(A) 2", "(B) −2", "(C) 4", "(D) −4"], "(B) −2"),
            ("(a³ + b³) = ?", ["(A) (a+b)³", "(B) (a+b)(a²−ab+b²)", "(C) (a−b)(a²+ab+b²)", "(D) a³−b³"], "(B) (a+b)(a²−ab+b²)"),
        ],
        "ar": [
            ("p(x) = x² − 1 has two zeros: 1 and −1.", "At x=1: 1−1=0; at x=−1: 1−1=0.", "(A)"),
            ("Every linear polynomial has exactly one zero.", "A linear polynomial ax+b = 0 gives x = −b/a, a unique value.", "(A)"),
            ("(x−2) is a factor of x³ − 8.", "p(2) = 8 − 8 = 0 by Factor Theorem.", "(A)"),
            ("Degree of a zero polynomial is 0.", "Degree of zero polynomial is undefined, not 0.", "(D)"),
            ("x² + 1 has no real zeros.", "x² + 1 = 0 gives x² = −1, no real solution.", "(A)"),
        ],
        "vsa": [
            ("What is the degree of 4x³ − 2x + 7?", "3"),
            ("Find zero of p(x) = 5x − 10.", "x = 2"),
            ("State the Remainder Theorem.", "When p(x) is divided by (x−a), remainder = p(a)."),
            ("Expand: (a+b)².", "a² + 2ab + b²"),
            ("Is x² + 1 a polynomial? State its degree.", "Yes. Degree = 2."),
        ],
        "sa": [
            ("Factorise: x³ − 23x² + 142x − 120.", "Try p(1) = 0: 1−23+142−120 = 0 ✓. So (x−1) is factor. Divide: (x−1)(x²−22x+120) = (x−1)(x−10)(x−12)."),
            ("Using Remainder Theorem, find remainder: p(x) = x³ − 6x² + 2x − 4 divided by (x−3).", "p(3) = 27 − 54 + 6 − 4 = −25."),
            ("Expand: (2x + 3y)³.", "8x³ + 36x²y + 54xy² + 27y³"),
            ("Factorise: 8a³ + b³ + 12a²b + 6ab².", "= (2a + b)³"),
            ("If p(x) = x³ + 3x² + 3x + 1, find p(−1).", "p(−1) = −1+3−3+1 = 0. So (x+1) is a factor."),
        ],
        "case_studies": [
            {
                "title": "The Polynomial Gardener",
                "scenario": (
                    "Meena designs a rectangular garden where length = (x+3) m and breadth = (x−2) m. "
                    "She represents the area as a polynomial."
                ),
                "questions": [
                    ("Express area as a polynomial.", "Area = (x+3)(x−2) = x² + x − 6"),
                    ("Find area when x = 5 m.", "25 + 5 − 6 = 24 m²"),
                    ("For what x does the area become 0?", "x² + x − 6 = 0 → (x+3)(x−2) = 0 → x = 2 (taking positive value)."),
                ],
            },
            {
                "title": "Factorisation in Construction",
                "scenario": "A builder represents the volume of a box as V(x) = x³ − 6x² + 11x − 6.",
                "questions": [
                    ("Check if (x−1) is a factor.", "V(1) = 1 − 6 + 11 − 6 = 0. Yes."),
                    ("Factorise V(x) completely.", "(x−1)(x−2)(x−3)"),
                    ("Find x if V = 0.", "x = 1, 2, or 3"),
                ],
            },
            {
                "title": "Remainder in Real Life",
                "scenario": "A teacher divides students into groups. Total students = p(x) = 2x² − 3x + 1 and each group has (x−1) students.",
                "questions": [
                    ("Find the remainder using Remainder Theorem.", "p(1) = 2 − 3 + 1 = 0. No student is left out."),
                    ("Is (x−1) a factor of p(x)?", "Yes, since p(1) = 0."),
                    ("Factorise p(x).", "(x−1)(2x−1)"),
                ],
            },
        ],
        "competency": [
            ("A shopkeeper earns p(x) = x² + 5x + 6 rupees when he sells x items. Find the price per item if he sold (x+2) items.", "p(x)/(x+2) = (x+2)(x+3)/(x+2) = (x+3). Price per item = (x+3) rupees."),
            ("The volume of a cuboid is x³ − 7x + 6. Factorise to find its dimensions.", "p(1) = 0 → (x−1) is factor. x³−7x+6 = (x−1)(x²+x−6) = (x−1)(x+3)(x−2). Dimensions: (x−1), (x−2), (x+3)."),
            ("Priya says the zero of p(x) = x² is x = 1. Is she correct?", "No. p(0) = 0, so zero is x = 0."),
            ("A chemist uses polynomial 2x² − 8 to represent concentration. At what x is concentration zero?", "2x² − 8 = 0 → x² = 4 → x = 2 (positive value)."),
            ("Simplify: (a+b+c)² − (a²+b²+c²). What does this equal?", "2(ab + bc + ca)"),
        ],
    },
}


def _get_chapter_data(chapter_title: str) -> dict:
    """Match chapter title to enrichment data."""
    title_lower = chapter_title.lower()
    for key, data in CHAPTER_DATA.items():
        if key in title_lower:
            return data
    return {}


# ---------------------------------------------------------------------------
# Module generator
# ---------------------------------------------------------------------------

def generate_module(pdf_path: Path, output_dir: Path) -> Path:
    """Read a PDF and write a premium coaching module markdown file."""
    print(f"📖  Reading: {pdf_path.name} ...")
    raw_text = extract_pdf_text(pdf_path)

    class_label, chapter_num, chapter_title = _guess_meta(pdf_path)
    data = _get_chapter_data(chapter_title)

    lines: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────────
    lines.append(_page_header(class_label, chapter_title))
    lines.append(f"# Chapter {chapter_num}: {chapter_title}\n")
    lines.append(f"*Class {class_label} | Mathematics | Success Achievers Institute*\n")
    lines.append(_brand_line())

    # ── Extracted content ────────────────────────────────────────────────────
    lines.append("---\n## 📖 Content Extracted from PDF\n")
    content_lines = _section_lines(raw_text)
    # Format the extracted text neatly
    for ln in content_lines:
        lines.append(ln)
    lines.append("\n")
    lines.append(_page_footer())

    # ── Concept Boxes ────────────────────────────────────────────────────────
    lines.append(_page_header(class_label, chapter_title))
    lines.append("## 📘 Concept Boxes\n")
    if data.get("concepts"):
        for name, explanation, formula, example in data["concepts"]:
            lines.append(_concept_box(name, explanation, formula, example))
    else:
        lines.append(_concept_box(
            chapter_title,
            f"Core concepts of {chapter_title} as per NCERT Class {class_label}.",
            "Refer to chapter formulas",
            "See worked examples below",
        ))

    # ── Memory Trick ─────────────────────────────────────────────────────────
    if data.get("memory"):
        lines.append(_memory_trick(data["memory"]))

    # ── Classroom Dialogue ───────────────────────────────────────────────────
    if data.get("dialogue"):
        lines.append(_classroom_dialogue(*data["dialogue"]))

    # ── Board Exam Alert ─────────────────────────────────────────────────────
    if data.get("alert"):
        lines.append(_board_exam_alert(data["alert"]))

    # ── Common Mistake ───────────────────────────────────────────────────────
    if data.get("mistake"):
        lines.append(_common_mistake(data["mistake"]))

    # ── Competitive Edge ─────────────────────────────────────────────────────
    if data.get("competitive"):
        lines.append(_competitive_edge(data["competitive"]))

    lines.append(_brand_line())
    lines.append(_page_footer())

    # ── Quick Revision Box ───────────────────────────────────────────────────
    lines.append(_page_header(class_label, chapter_title))
    lines.append("## 📋 Quick Revision Sheet\n")
    if data.get("revision_points") and data.get("revision_formulas"):
        lines.append(_quick_revision_box(data["revision_points"], data["revision_formulas"]))
    else:
        lines.append(_quick_revision_box(
            [f"Review key concepts of {chapter_title}"],
            ["See formula sheet in concepts/formulas-reference.md"],
        ))

    # ── Smart Board Answer Template ──────────────────────────────────────────
    lines.append("## ✍️ Board Exam Smart Answer Format\n")
    lines.append(_smart_board_answer(
        chapter_title,
        f"[Write definition of the asked concept from {chapter_title}]",
        "[State the relevant formula]",
        "[Explain step-by-step with clear working]",
    ))
    lines.append(_page_footer())

    # ── Practice Questions ───────────────────────────────────────────────────
    lines.append(_page_header(class_label, chapter_title))

    if data.get("mcqs"):
        lines.append(_mcqs(chapter_title, data["mcqs"]))

    if data.get("ar"):
        lines.append(_assertion_reasoning(data["ar"]))

    if data.get("vsa"):
        lines.append(_vsa(data["vsa"]))

    if data.get("sa"):
        lines.append(_sa(data["sa"]))

    if data.get("case_studies"):
        lines.append(_case_study(data["case_studies"]))

    if data.get("competency"):
        lines.append(_competency(data["competency"]))

    lines.append(_page_footer())

    # ── Final Branding Page ──────────────────────────────────────────────────
    lines.append(_branding_page())

    # ── Write output ─────────────────────────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{pdf_path.stem}-module.md"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅  Module written: {out_file}")
    return out_file


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert NCERT chapter PDFs into Ultra-Premium Coaching Modules."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        help="Path to a single PDF file (e.g. pdfs/class9-maths-ch01-number-systems.pdf)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert ALL PDFs found in the pdfs/ directory.",
    )
    parser.add_argument(
        "--output-dir",
        default="modules",
        help="Directory where generated modules are saved (default: modules/).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / args.output_dir

    if args.all:
        pdfs_dir = repo_root / "pdfs"
        pdfs = sorted(pdfs_dir.glob("*.pdf"))
        if not pdfs:
            print(
                f"No PDF files found in '{pdfs_dir}'.\n"
                "Upload NCERT chapter PDFs there first — see pdfs/README.md for instructions."
            )
            sys.exit(1)
        for pdf in pdfs:
            generate_module(pdf, output_dir)
    elif args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"Error: file not found: {pdf_path}")
            sys.exit(1)
        generate_module(pdf_path, output_dir)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
