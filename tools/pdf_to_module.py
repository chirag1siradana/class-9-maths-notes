#!/usr/bin/env python3
"""
pdf_to_module.py
================
Success Achievers Institute – PDF to Ultra-Premium Coaching Module Converter
Alwar, Rajasthan

Usage
-----
# Merge all parts of a chapter into one module (auto-detects number of parts):
    python tools/pdf_to_module.py --chapter number_systems

# Convert a single PDF:
    python tools/pdf_to_module.py pdfs/01_number_systems_part1.pdf

# Convert ALL PDFs in pdfs/ folder (groups parts automatically):
    python tools/pdf_to_module.py --all

Output is written to modules/
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# PDF text extraction: text-layer → OCR fallback
# ---------------------------------------------------------------------------

def _extract_text_layer(pdf_path: Path) -> str:
    """Try PyMuPDF text extraction (works on text-based PDFs)."""
    try:
        import fitz
    except ImportError:
        return ""
    pages = []
    doc = fitz.open(str(pdf_path))
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def _extract_via_ocr(pdf_path: Path, lang: str = "eng+hin") -> str:
    """OCR every page via Tesseract (for scanned / handwritten PDFs)."""
    try:
        import fitz
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            f"OCR dependencies missing: {exc}\n"
            "Run: pip install -r requirements.txt\n"
            "And: sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-hin"
        ) from exc

    pages = []
    doc = fitz.open(str(pdf_path))
    for page in doc:
        mat = fitz.Matrix(2, 2)          # 2× zoom → better OCR accuracy
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img, lang=lang)
        pages.append(text)
    doc.close()
    return "\n\n".join(pages)


def extract_pdf_text(pdf_path: Path) -> str:
    """
    Extract text from a PDF.
    Tries text layer first; falls back to OCR for scanned/image PDFs.
    """
    text = _extract_text_layer(pdf_path)
    # If we got almost no text the PDF is image-based → use OCR
    if len(text.strip()) < 50:
        print(f"  ↳ scanned PDF detected, using OCR for {pdf_path.name} …")
        text = _extract_via_ocr(pdf_path)
    return text


# ---------------------------------------------------------------------------
# Multi-part grouping
# ---------------------------------------------------------------------------

def group_parts(pdfs_dir: Path) -> dict[str, list[Path]]:
    """
    Group PDF files by chapter name.

    Expects files named like:
        01_number_systems_part1.pdf
        02_number_systems_part2.pdf
        ...
    or:
        class9-maths-ch01-number-systems.pdf

    Returns  { "number_systems": [path1, path2, ...], ... }
    """
    groups: dict[str, list[Path]] = {}
    part_re = re.compile(r"(\d+)_(.+?)_part(\d+)\.pdf$", re.IGNORECASE)
    single_re = re.compile(r"class\d+-\w+-ch\d+-(.+)\.pdf$", re.IGNORECASE)

    for pdf in sorted(pdfs_dir.glob("*.pdf")):
        m = part_re.match(pdf.name)
        if m:
            chapter_key = m.group(2).lower()
            groups.setdefault(chapter_key, []).append(pdf)
            continue
        m = single_re.match(pdf.name)
        if m:
            chapter_key = m.group(1).lower()
            groups.setdefault(chapter_key, []).append(pdf)
            continue
        # fall-through: use stem as key
        groups.setdefault(pdf.stem.lower(), []).append(pdf)

    # Sort each group by file name so parts are in order
    for key in groups:
        groups[key].sort()
    return groups


def merge_parts_text(pdf_paths: list[Path]) -> str:
    """Extract and concatenate text from all PDF parts."""
    parts = []
    for i, pdf in enumerate(pdf_paths, 1):
        print(f"  Extracting Part {i}/{len(pdf_paths)}: {pdf.name}")
        text = extract_pdf_text(pdf)
        parts.append(f"{'='*60}\nPART {i}: {pdf.name}\n{'='*60}\n\n{text}")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Module formatting helpers
# ---------------------------------------------------------------------------

TAGLINE     = "Better Than Others, No One Can Refute"
MOTIVATION  = "Master the concepts, conquer the exams!"
FOOTER_LINE = "Success Achievers Institute – Alwar  |  Premium Concept Notes  |  Academic Session 2025–26"


def _page_header(class_label: str, chapter_title: str) -> str:
    ch = chapter_title[:52]
    return (
        "\n---\n\n"
        "```\n"
        "╔══════════════════════════════════════════════════════════════════╗\n"
        "║           SUCCESS ACHIEVERS INSTITUTE, ALWAR                     ║\n"
        f"║           Class {class_label} – Mathematics                               ║\n"
        f"║  Chapter : {ch:<54}║\n"
        f"║  Tagline : {TAGLINE:<54}║\n"
        f"║  {MOTIVATION:<64}║\n"
        "╚══════════════════════════════════════════════════════════════════╝\n"
        "```\n\n---\n"
    )


def _page_footer() -> str:
    return f"\n> 📌 _{FOOTER_LINE}_\n\n---\n"


def _concept_box(name: str, explanation: str, formula: str = "", example: str = "") -> str:
    lines = [
        "```",
        "┌─────────────────────────────────────────────────────┐",
        f"│  📘 CONCEPT:  {name:<38}│",
        "├─────────────────────────────────────────────────────┤",
    ]
    for chunk in textwrap.wrap(explanation, 51):
        lines.append(f"│  {chunk:<51}│")
    if formula:
        lines.append(f"│  📐 Formula : {formula:<37}│")
    if example:
        lines.append(f"│  💡 Example : {example:<37}│")
    lines += ["└─────────────────────────────────────────────────────┘", "```", ""]
    return "\n".join(lines)


def _memory_trick(trick: str) -> str:
    return f"\n> 🧠 **MEMORY TRICK:** {trick}\n"


def _board_exam_alert(tip: str) -> str:
    return f"\n> ⚠️ **BOARD EXAM ALERT:** {tip}\n"


def _common_mistake(mistake: str) -> str:
    return f"\n> ❌ **COMMON STUDENT MISTAKE:** {mistake}\n"


def _competitive_edge(tip: str) -> str:
    return f"\n> 🏆 **COMPETITIVE EDGE (JEE/NEET Foundation):** {tip}\n"


def _brand_line(msg: str = "") -> str:
    default = "At Success Achievers Institute, we focus on concept mastery, not rote learning."
    return f"\n> 💡 *{msg or default}*\n"


def _classroom_dialogue(teacher: str, student: str, teacher2: str = "") -> str:
    lines = [
        "\n```",
        "🎓 CLASSROOM MOMENT",
        f'  Teacher : "{teacher}"',
        f'  Student : "{student}"',
    ]
    if teacher2:
        lines.append(f'  Teacher : "{teacher2}"')
    lines += ["```\n"]
    return "\n".join(lines)


def _quick_revision_box(points: list[str], formulas: list[str]) -> str:
    out = ["---", "### 📋 QUICK REVISION BOX", "", "**Key Points:**"]
    for p in points:
        out.append(f"- {p}")
    out += ["", "**Key Formulas:**"]
    for f in formulas:
        out.append(f"- `{f}`")
    out += ["", "---", ""]
    return "\n".join(out)


def _smart_answer_box(topic: str, definition: str, formula: str, explanation: str) -> str:
    return (
        f"#### ✍️ SMART BOARD ANSWER FORMAT — {topic}\n\n"
        "| Part | Content |\n|------|--------|\n"
        f"| **Definition** | {definition} |\n"
        f"| **Formula** | `{formula}` |\n"
        f"| **Explanation** | {explanation} |\n"
        "| **Diagram** | _(Draw with all labels)_ |\n\n"
    )


def _mcq_section(title: str, items: list[tuple]) -> str:
    out = ["---", f"## 📝 MCQs — {title}", ""]
    for i, (q, opts, ans) in enumerate(items, 1):
        out.append(f"**Q{i}.** {q}")
        for o in opts:
            out.append(f"   {o}")
        out.append(f"   **✔ Answer:** {ans}")
        out.append("")
    return "\n".join(out)


def _ar_section(items: list[tuple]) -> str:
    out = [
        "---",
        "## 🔍 Assertion–Reasoning Questions",
        "",
        "**(A)** Both A and R are true; R is correct explanation of A.",
        "**(B)** Both true; R is NOT correct explanation.",
        "**(C)** A is true; R is false.",
        "**(D)** A is false; R is true.",
        "",
    ]
    for i, (a, r, ans) in enumerate(items, 1):
        out += [
            f"**Q{i}.**",
            f"  **Assertion (A):** {a}",
            f"  **Reason (R):** {r}",
            f"  **Answer:** {ans}",
            "",
        ]
    return "\n".join(out)


def _vsa_section(items: list[tuple]) -> str:
    out = ["---", "## ✏️ Very Short Answer Questions *(1 Mark)*", ""]
    for i, (q, a) in enumerate(items, 1):
        out += [f"**Q{i}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(out)


def _sa_section(items: list[tuple]) -> str:
    out = ["---", "## 📄 Short Answer Questions *(2–3 Marks)*", ""]
    for i, (q, a) in enumerate(items, 1):
        out += [f"**Q{i}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(out)


def _case_study_section(items: list[dict]) -> str:
    out = ["---", "## 📊 Case Study Questions", ""]
    for i, cs in enumerate(items, 1):
        out += [f"### Case Study {i}: {cs['title']}", "", cs["scenario"], ""]
        for j, (q, a) in enumerate(cs["questions"], 1):
            out += [f"**Q{j}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(out)


def _competency_section(items: list[tuple]) -> str:
    out = ["---", "## 🎯 Competency-Based Questions", ""]
    for i, (q, a) in enumerate(items, 1):
        out += [f"**Q{i}.** {q}", f"**Ans:** {a}", ""]
    return "\n".join(out)


def _final_branding() -> str:
    return (
        "\n---\n\n"
        "```\n"
        "╔══════════════════════════════════════════════════════════════════╗\n"
        "║                                                                  ║\n"
        "║              SUCCESS ACHIEVERS INSTITUTE                         ║\n"
        "║                  Alwar, Rajasthan                                ║\n"
        "║                                                                  ║\n"
        "║              Premium Concept Notes                               ║\n"
        '║        "Better Than Others, No One Can Refute"                   ║\n'
        "║                                                                  ║\n"
        "║            Designed by Academic Team                             ║\n"
        "║           Academic Session 2025–26                               ║\n"
        "║                                                                  ║\n"
        "╚══════════════════════════════════════════════════════════════════╝\n"
        "```\n"
    )


# ---------------------------------------------------------------------------
# Chapter-specific enrichment data (Number Systems — from actual PDF content)
# ---------------------------------------------------------------------------

NUMBER_SYSTEMS_DATA = {
    "class_label": "9",
    "chapter_num": "1",
    "chapter_title": "Number Systems",
    "introduction": (
        "In this chapter, we explore the world of numbers — from the whole numbers we count with, "
        "to the mysterious irrational numbers that never repeat. "
        "We learn how to place every number on a number line, convert recurring decimals to fractions, "
        "perform operations on surds, rationalise denominators, and apply laws of exponents."
    ),
    "topics": [
        {
            "title": "1.1 Natural Numbers, Whole Numbers, and Integers",
            "content": (
                "The journey of numbers starts with **Natural Numbers (ℕ)** = {1, 2, 3, ...}.\n"
                "Adding zero gives **Whole Numbers (W)** = {0, 1, 2, 3, ...}.\n"
                "Extending to negatives gives **Integers (ℤ)** = {..., −3, −2, −1, 0, 1, 2, 3, ...}.\n\n"
                "**Hierarchy:** ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ"
            ),
            "concept_box": ("Natural → Whole → Integer → Rational → Real",
                            "Every set is a subset of the next bigger set.",
                            "ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ",
                            "−5 ∈ ℤ but −5 ∉ ℕ"),
            "memory": "**N-W-I-R-R** → 'Numbers With Increasing Range, Really!' "
                      "(Natural → Whole → Integer → Rational → Real)",
            "dialogue": (
                "Imagine numbers as a family tree. Natural numbers are the eldest children.",
                "So whole numbers just adopted zero into the family, sir?",
                "Exactly! And integers went further — they adopted negative relatives too!",
            ),
        },
        {
            "title": "1.2 Rational Numbers",
            "content": (
                "A **Rational Number** is any number expressible as **p/q**, where p, q ∈ ℤ and q ≠ 0.\n\n"
                "Examples: 3/4, −7/2, 0, 5, 0.333... (= 1/3), 0.142857... (= 1/7)\n\n"
                "**Key property:** Rational numbers have either **terminating** or **recurring** decimal expansions.\n\n"
                "- Terminating: 3/4 = 0.75 (ends)\n"
                "- Non-terminating recurring: 1/3 = 0.3̄ (repeats)"
            ),
            "concept_box": ("Rational Number",
                            "A number of the form p/q, p,q ∈ ℤ, q ≠ 0.",
                            "p/q, q ≠ 0",
                            "3/4 = 0.75, 1/3 = 0.333..."),
            "alert": "Terminating decimals → denominator has only 2 and/or 5 as prime factors. "
                     "This fact is directly asked in board exams!",
            "mistake": "Students write 22/7 = π. This is WRONG! 22/7 is rational (≈ 3.1428...); π is irrational.",
        },
        {
            "title": "1.3 Irrational Numbers",
            "content": (
                "An **Irrational Number** CANNOT be written as p/q. "
                "Its decimal expansion is **non-terminating and non-recurring**.\n\n"
                "Examples: √2 = 1.41421356..., √3 = 1.73205..., π = 3.14159..., e = 2.71828...\n\n"
                "**Fact:** √p is irrational if p is a prime number.\n\n"
                "**Sum/Product rules:**\n"
                "- Rational + Irrational = Irrational\n"
                "- Rational × Non-zero Irrational = Irrational\n"
                "- Irrational × Irrational = May be Rational! (e.g. √2 × √2 = 2)"
            ),
            "concept_box": ("Irrational Number",
                            "Cannot be expressed as p/q. Non-terminating, non-recurring decimal.",
                            "Not of the form p/q",
                            "√2 = 1.41421356..."),
            "memory": "**INCH** → **I**rrational **N**umbers **C**annot be written as a fraction, "
                      "they go on and on with **H**idden pattern never repeating!",
            "competitive": "√2, √3, √5 irrationality proofs use proof by contradiction — "
                           "a key JEE/NTSE concept.",
            "dialogue": (
                "Imagine you are measuring the diagonal of a 1×1 square with a ruler.",
                "But sir, the diagonal is √2 and I can't mark it exactly!",
                "That's the beauty of irrational numbers — they exist on the number line, "
                "but no fraction can pin them down exactly!",
            ),
        },
        {
            "title": "1.4 Real Numbers and the Number Line",
            "content": (
                "**Real Numbers (ℝ)** = Rational Numbers (ℚ) ∪ Irrational Numbers\n\n"
                "Every real number corresponds to a unique point on the number line.\n\n"
                "**Locating √n on the number line (Spiral of Pythagoras / Geometrical method):**\n"
                "1. Draw OA = 1 unit on number line.\n"
                "2. Draw AB ⊥ OA, AB = 1 unit. Then OB = √2.\n"
                "3. Draw BC ⊥ OB, BC = 1 unit. Then OC = √3.\n"
                "4. Continue: OD = √4 = 2, OE = √5, ... etc.\n\n"
                "**Successive Magnification:** We can zoom into any part of the number line "
                "to locate non-terminating decimals to any desired accuracy."
            ),
            "concept_box": ("Real Numbers",
                            "ℝ = ℚ ∪ (Irrationals). Every point on number line is real.",
                            "ℝ = ℚ ∪ (ℝ \\ ℚ)",
                            "√5 ≈ 2.236 is located geometrically"),
            "alert": "Locating √2, √3, √5 on the number line using right triangles is "
                     "frequently asked in 2-mark questions!",
            "diagram": (
                "```\n"
                "  NUMBER LINE — Locating √2 geometrically\n\n"
                "  A ──────── B\n"
                "  |          |\n"
                "  O ──────── 1\n\n"
                "  OA = 1, AB ⊥ OA = 1\n"
                "  OB = √(1² + 1²) = √2\n"
                "  Draw arc with centre O, radius OB → hits number line at √2\n"
                "```\n"
            ),
        },
        {
            "title": "1.5 Converting Recurring Decimals to p/q Form",
            "content": (
                "Any recurring decimal can be converted to a rational number p/q.\n\n"
                "**Method (from the PDFs):**\n"
                "Let x = recurring decimal. Multiply by 10ⁿ (n = number of recurring digits) "
                "to shift the decimal, then subtract to eliminate the recurring part.\n\n"
                "**Example 1:** x = 0.333...\n"
                "> 10x = 3.333...\n"
                "> 10x − x = 3 → 9x = 3 → **x = 1/3**\n\n"
                "**Example 2:** x = 0.abab... (2-digit repeat)\n"
                "> 100x = ab.abab...\n"
                "> 100x − x = ab → 99x = ab → **x = ab/99**\n\n"
                "**Example 3:** x = 1.232323...\n"
                "> 100x = 123.2323...\n"
                "> 100x − x = 122 → 99x = 122 → **x = 122/99**\n\n"
                "**Example 4:** x = 3.1416̄  (only 6̄ repeats)\n"
                "> 10x = 31.416̄; 100x = 314.16̄\n"
                "> 100x − 10x = 282.75 → ... *(solve step by step)*"
            ),
            "concept_box": ("Recurring Decimal → p/q",
                            "Multiply by 10ⁿ (n = repeating digits) and subtract.",
                            "99x = ab → x = ab/99 for 0.ab̄",
                            "0.333... = 1/3"),
            "memory": "**10-Subtract-Divide:** Multiply by 10 (or 100 for 2-digit repeat), "
                      "subtract original, divide → you have p/q!",
            "alert": "In board exams, express recurring decimals as fractions in simplest form. "
                     "Don't forget to reduce p/q by GCD.",
            "mistake": "Students multiply by 10 even when TWO digits repeat — should multiply by 100. "
                       "Count repeating digits carefully!",
            "dialogue": (
                "Converting 0.142857142857... to p/q looks scary, doesn't it?",
                "Sir, 6 digits repeat — so we multiply by 10⁶?",
                "Exactly! 999999x = 142857, so x = 142857/999999 = 1/7. Magic!",
            ),
        },
        {
            "title": "1.6 Operations on Surds",
            "content": (
                "A **Surd** is an irrational number expressed as ⁿ√a where a is rational and the result is irrational.\n\n"
                "**Rules:**\n"
                "- √(ab) = √a × √b\n"
                "- √(a/b) = √a / √b\n"
                "- (√a)² = a\n"
                "- (√a + √b)(√a − √b) = a − b  *(key identity!)*\n"
                "- (a + √b)(a − √b) = a² − b\n\n"
                "**Addition/Subtraction of Surds:** Only **like surds** can be added/subtracted.\n"
                "> 3√2 + 5√2 = 8√2 ✓\n"
                "> 3√2 + 5√3 → cannot be simplified ✗\n\n"
                "**Multiplication:**\n"
                "> √2 × √8 = √16 = 4\n"
                "> (2 + √3)² = 4 + 4√3 + 3 = 7 + 4√3"
            ),
            "concept_box": ("Surds",
                            "Irrational roots. Use √(ab)=√a·√b and conjugate identities.",
                            "(√a+√b)(√a−√b) = a−b",
                            "(2+√3)(2−√3) = 4−3 = 1"),
            "memory": "**CALM:** **C**onjugate removes surds from denominators, "
                      "**A**dd only like surds, **L**aws of radicals apply, "
                      "**M**ultiply surds by combining under one √.",
            "competitive": "Surd operations are the foundation of surds & indices questions in JEE. "
                           "Master the conjugate identity thoroughly.",
            "dialogue": (
                "Think of surds as siblings — only identical twins (like surds) can be added together.",
                "So √2 and √3 are non-identical twins, sir?",
                "Exactly! You can't simplify 3√2 + 5√3 just like you can't merge two different people!",
            ),
        },
        {
            "title": "1.7 Rationalising the Denominator",
            "content": (
                "**Rationalisation** means removing irrational numbers from the denominator "
                "by multiplying by an appropriate conjugate.\n\n"
                "**Case 1: Monomial surd denominator**\n"
                "> 1/√2 = 1/√2 × √2/√2 = √2/2\n\n"
                "**Case 2: Binomial surd denominator**\n"
                "> 1/(√a + √b) → multiply by (√a − √b)/(√a − √b)\n"
                "> = (√a − √b)/(a − b)\n\n"
                "**Example (from PDF):**\n"
                "> 5/(√7 − 2)\n"
                "> = 5(√7 + 2)/((√7)² − 4)\n"
                "> = 5(√7 + 2)/(7 − 4)\n"
                "> = 5(√7 + 2)/3\n\n"
                "**Example 2:**\n"
                "> 1/(√5 + √3)\n"
                "> = (√5 − √3)/((√5)² − (√3)²)\n"
                "> = (√5 − √3)/(5 − 3)\n"
                "> = (√5 − √3)/2"
            ),
            "concept_box": ("Rationalisation",
                            "Eliminate irrational from denominator using conjugate multiplication.",
                            "1/(√a+√b) = (√a−√b)/(a−b)",
                            "1/(√2+1) = √2−1"),
            "alert": "This is a guaranteed 2–3 mark question in CBSE boards every year. "
                     "Always simplify fully and verify the denominator becomes rational.",
            "mistake": "Forgetting to multiply BOTH numerator and denominator by the conjugate. "
                       "Always multiply the full expression!",
        },
        {
            "title": "1.8 Laws of Exponents for Real Numbers",
            "content": (
                "The laws of exponents apply to all real-number bases (a > 0).\n\n"
                "| Law | Formula | Example |\n"
                "|-----|---------|--------|\n"
                "| Product | aᵐ × aⁿ = aᵐ⁺ⁿ | 2³ × 2⁴ = 2⁷ |\n"
                "| Quotient | aᵐ ÷ aⁿ = aᵐ⁻ⁿ | 5⁶ ÷ 5² = 5⁴ |\n"
                "| Power of Power | (aᵐ)ⁿ = aᵐⁿ | (3²)⁴ = 3⁸ |\n"
                "| Power of Product | (ab)ᵐ = aᵐbᵐ | (2×3)² = 4×9 |\n"
                "| Zero Exponent | a⁰ = 1, a ≠ 0 | 100⁰ = 1 |\n"
                "| Negative Exponent | a⁻ⁿ = 1/aⁿ | 2⁻³ = 1/8 |\n"
                "| Fractional Exponent | a^(m/n) = (ⁿ√a)ᵐ | 8^(2/3) = 4 |\n\n"
                "**Fractional exponent key:**\n"
                "> a^(1/n) = ⁿ√a\n"
                "> a^(m/n) = (ⁿ√a)ᵐ = ⁿ√(aᵐ)\n\n"
                "**Example (from PDF):**\n"
                "> (27)^(2/3) = (³√27)² = 3² = **9**\n"
                "> (64)^(1/6) = ⁶√64 = **2**"
            ),
            "concept_box": ("Laws of Exponents",
                            "Rules for multiplying/dividing/raising powers of real numbers.",
                            "aᵐ × aⁿ = aᵐ⁺ⁿ; (aᵐ)ⁿ = aᵐⁿ",
                            "27^(2/3) = (³√27)² = 9"),
            "memory": "**PQP-ZNF** → **P**roduct adds, **Q**uotient subtracts, **P**ower multiplies, "
                      "**Z**ero gives 1, **N**egative flips, **F**raction takes root!",
            "alert": "a^(1/2) = √a, a^(1/3) = ³√a, a^(m/n) = (ⁿ√a)ᵐ — these are directly asked "
                     "as 'evaluate' problems in board exams.",
            "competitive": "Fractional exponents connect directly to logarithms and surds in JEE. "
                           "Master the conversion: a^(m/n) = ⁿ√(aᵐ).",
        },
    ],
    "revision_points": [
        "ℝ = ℚ ∪ Irrationals; ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ",
        "Rational: terminating or recurring decimal",
        "Irrational: non-terminating, non-recurring (√2, √3, π, e)",
        "22/7 ≠ π — 22/7 is rational, π is irrational",
        "Recurring decimal → p/q: multiply by 10ⁿ, subtract, divide",
        "(√a + √b)(√a − √b) = a − b — use for rationalisation",
        "Add only LIKE surds (same radicand)",
        "aᵐ × aⁿ = aᵐ⁺ⁿ; (aᵐ)ⁿ = aᵐⁿ; a^(m/n) = (ⁿ√a)ᵐ",
    ],
    "revision_formulas": [
        "√(ab) = √a × √b",
        "(√a + √b)(√a − √b) = a − b",
        "(a + √b)² = a² + 2a√b + b",
        "aᵐ × aⁿ = aᵐ⁺ⁿ",
        "aᵐ ÷ aⁿ = aᵐ⁻ⁿ",
        "(aᵐ)ⁿ = aᵐⁿ",
        "a⁰ = 1 (a ≠ 0)",
        "a^(1/n) = ⁿ√a",
        "a^(m/n) = (ⁿ√a)ᵐ",
    ],
    "board_smart_answers": [
        ("Rational Number", "A number expressible as p/q, p,q ∈ ℤ, q ≠ 0",
         "p/q, q ≠ 0",
         "E.g. 3/4 = 0.75 (terminating); 1/3 = 0.333... (recurring). Both are rational."),
        ("Irrational Number", "A number that cannot be expressed as p/q; non-terminating, non-recurring",
         "NOT p/q",
         "E.g. √2 = 1.41421...; π = 3.14159... Proof that √2 is irrational uses contradiction."),
        ("Rationalise 1/(√5 + √2)", "Multiply numerator and denominator by conjugate (√5 − √2)",
         "(√5 − √2)/((√5)²−(√2)²)",
         "= (√5 − √2)/(5−2) = (√5 − √2)/3"),
    ],
    "mcqs": [
        ("Which of the following is irrational?",
         ["(A) 0.25", "(B) 22/7", "(C) √3", "(D) 4/9"], "(C) √3"),
        ("The decimal expansion of 1/3 is:",
         ["(A) 0.333 (terminating)", "(B) 0.333... (recurring)", "(C) 0.134", "(D) irrational"],
         "(B) 0.333... (non-terminating recurring)"),
        ("Value of (27)^(2/3) is:",
         ["(A) 3", "(B) 6", "(C) 9", "(D) 18"], "(C) 9"),
        ("Rationalising factor of 1/(√7 − 2) is:",
         ["(A) √7 − 2", "(B) √7 + 2", "(C) 7 − 2", "(D) 2 − √7"], "(B) √7 + 2"),
        ("0.101001000... is a/an:",
         ["(A) Rational number", "(B) Natural number", "(C) Irrational number", "(D) Integer"],
         "(C) Irrational number — non-terminating, non-recurring"),
        ("Which is NOT a real number?",
         ["(A) √−1", "(B) √2", "(C) π", "(D) −7"], "(A) √−1 (imaginary number)"),
        ("If x = 0.ababab..., then x equals:",
         ["(A) ab/99", "(B) ab/9", "(C) ab/100", "(D) ab/999"], "(A) ab/99"),
        ("2⁵ × 2⁻³ equals:",
         ["(A) 2²", "(B) 2⁸", "(C) 4", "(D) Both A and C"], "(D) Both A and C (2² = 4)"),
        ("(√5 + √3)(√5 − √3) = ?",
         ["(A) 8", "(B) 2", "(C) √2", "(D) 15 − 9"], "(B) 2 (= 5 − 3)"),
        ("The value of (64)^(1/6) is:",
         ["(A) 8", "(B) 4", "(C) 2", "(D) 6"], "(C) 2"),
    ],
    "ar": [
        ("√2 is irrational.",
         "√2 = 1.41421356... is non-terminating and non-recurring.",
         "(A)"),
        ("0 is a rational number.",
         "0 can be written as 0/1, which is in p/q form.",
         "(A)"),
        ("22/7 = π",
         "22/7 is a rational approximation; π is irrational.",
         "(D) — Assertion is false."),
        ("(√3)² is rational.",
         "Squaring a surd removes the irrational part: (√3)² = 3.",
         "(A)"),
        ("√2 × √8 is irrational.",
         "√2 × √8 = √16 = 4, which is rational.",
         "(D) — Assertion is false; product is rational."),
    ],
    "vsa": [
        ("Define a rational number.", "A number that can be expressed as p/q, where p, q ∈ ℤ and q ≠ 0."),
        ("Is 0.6̄ rational? Express as p/q.", "Yes. Let x = 0.666...; 10x = 6.666...; 9x = 6; x = 2/3."),
        ("Simplify: √50.", "√50 = √(25×2) = 5√2"),
        ("State one law of exponents.", "aᵐ × aⁿ = aᵐ⁺ⁿ (or any valid law)"),
        ("Find the value of (8)^(1/3).", "(8)^(1/3) = ³√8 = 2"),
    ],
    "sa": [
        ("Rationalise the denominator: 5/(√7 − 2)",
         "Multiply by (√7+2)/(√7+2): 5(√7+2)/(7−4) = **5(√7+2)/3**"),
        ("Express 0.235̄ as p/q.",
         "Let x = 0.2353535...\n"
         "1000x = 235.3535..., 10x = 2.3535...\n"
         "990x = 233 → **x = 233/990**"),
        ("Simplify: (3 + √2)² − (3 − √2)²",
         "(3+√2)² = 9+6√2+2 = 11+6√2\n"
         "(3−√2)² = 9−6√2+2 = 11−6√2\n"
         "Difference = **(11+6√2) − (11−6√2) = 12√2**"),
        ("Evaluate: (0.125)^(−2/3)",
         "(0.125)^(−2/3) = (1/8)^(−2/3) = 8^(2/3) = (³√8)² = 2² = **4**"),
        ("Prove that √3 is irrational.",
         "Assume √3 = p/q (lowest terms). Then 3 = p²/q² → p² = 3q² → 3|p → p = 3k.\n"
         "Then 9k² = 3q² → q² = 3k² → 3|q. Contradiction: p, q have common factor 3. Hence √3 is irrational."),
    ],
    "case_studies": [
        {
            "title": "The Tiling Problem",
            "scenario": (
                "An architect designs a square floor tile. The side of the tile is √2 m. "
                "He needs to find the exact perimeter and area, and check if these values are rational or irrational."
            ),
            "questions": [
                ("Find the perimeter of the tile.", "Perimeter = 4 × √2 = **4√2 m** (irrational)"),
                ("Find the area of the tile.", "Area = (√2)² = **2 m²** (rational)"),
                ("Is the diagonal of the tile rational or irrational?",
                 "Diagonal = √((√2)² + (√2)²) = √(2+2) = √4 = **2 m** (rational)"),
            ],
        },
        {
            "title": "Decimal Detective",
            "scenario": (
                "Teacher gave the class five numbers: 0.25, 0.333..., 1.41421..., 3.14159..., 2.5̄. "
                "Students have to classify each and convert recurring ones to p/q."
            ),
            "questions": [
                ("Classify each number as rational or irrational.",
                 "0.25 = 1/4 (rational, terminating); 0.333... = 1/3 (rational, recurring); "
                 "1.41421... = √2 (irrational); 3.14159... = π (irrational); 2.5̄ = 23/9 (rational, recurring)"),
                ("Convert 2.5̄ to p/q form.",
                 "x = 2.555...; 10x = 25.55...; 9x = 23; **x = 23/9**"),
                ("How many of the five numbers are irrational?", "Two: √2 and π"),
            ],
        },
        {
            "title": "Powers in Science",
            "scenario": (
                "In a physics lab, the speed of light c = 3 × 10⁸ m/s. "
                "A student uses laws of exponents to simplify scientific notation calculations."
            ),
            "questions": [
                ("Simplify: (3 × 10⁸) × (2 × 10⁻³)", "= 6 × 10⁵"),
                ("Evaluate: 10¹² ÷ 10⁻⁴", "= 10^(12−(−4)) = 10¹⁶"),
                ("Express 0.000001 as a power of 10.", "= 10⁻⁶"),
            ],
        },
    ],
    "competency": [
        ("A student claims: 'The sum of two irrational numbers is always irrational.' Is this correct? Give an example to justify your answer.",
         "No, this is incorrect. Counterexample: (2 + √3) + (2 − √3) = 4, which is rational. "
         "The sum of two irrationals CAN be rational."),
        ("A carpenter measures a wall and says the length is exactly π metres. Can he mark this on a measuring tape? Explain using properties of real numbers.",
         "π is irrational — it has no exact terminating or recurring decimal. "
         "The carpenter can only approximate it (e.g. 3.14159 m). "
         "However, it CAN be marked geometrically using its definition."),
        ("Simplify √(48) − √(27) + √(75) without a calculator. State whether the answer is rational or irrational.",
         "√48 = 4√3, √27 = 3√3, √75 = 5√3. Result = (4−3+5)√3 = **6√3** (irrational)"),
        ("A square plot has area 2 hectares. Find the exact side length and explain why it cannot be expressed as a terminating decimal.",
         "Side = √2 km (since area = side²). √2 is irrational — its decimal never terminates or repeats."),
        ("Evaluate without a calculator: (32)^(3/5) + (81)^(1/4) − (27)^(2/3)",
         "(32)^(3/5) = (⁵√32)³ = 2³ = 8; (81)^(1/4) = ⁴√81 = 3; (27)^(2/3) = (³√27)² = 9. "
         "Answer = 8 + 3 − 9 = **2**"),
    ],
}


# ---------------------------------------------------------------------------
# Module builder
# ---------------------------------------------------------------------------

def build_number_systems_module(raw_ocr: str, output_dir: Path) -> Path:
    """Build the full coaching module for Chapter 1: Number Systems."""
    data = NUMBER_SYSTEMS_DATA
    class_label = data["class_label"]
    chapter_title = data["chapter_title"]

    sections: list[str] = []

    # ── PAGE 1: Cover + Introduction ─────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(f"# Chapter {data['chapter_num']}: {chapter_title}\n")
    sections.append(f"*Class {class_label} | Mathematics | Success Achievers Institute, Alwar*\n")
    sections.append(_brand_line())
    sections.append(f"\n## 📖 Introduction\n\n{data['introduction']}\n")
    sections.append(_page_footer())

    # ── PAGE 2: Raw Notes (OCR from PDFs) ────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append("## 📄 Source Notes (Extracted from PDF Parts 1–10)\n")
    sections.append(
        "> *The following content was OCR-extracted from 10 handwritten PDF parts uploaded to this repository.*\n"
    )
    # Show a clean excerpt — strip noise, keep meaningful lines
    clean_lines = [
        ln.strip() for ln in raw_ocr.splitlines()
        if len(ln.strip()) > 8 and not all(c in r"_-=|/\\" for c in ln.strip())
    ]
    excerpt = "\n".join(clean_lines[:120])
    sections.append(f"\n```\n{excerpt}\n```\n")
    sections.append(_page_footer())

    # ── PAGES 3–N: Topic-by-Topic Concept Notes ──────────────────────────────
    for topic in data["topics"]:
        sections.append(_page_header(class_label, chapter_title))
        sections.append(f"## {topic['title']}\n\n{topic['content']}\n")

        # Concept box
        if "concept_box" in topic:
            sections.append(_concept_box(*topic["concept_box"]))

        # Memory trick
        if "memory" in topic:
            sections.append(_memory_trick(topic["memory"]))

        # Classroom dialogue
        if "dialogue" in topic:
            sections.append(_classroom_dialogue(*topic["dialogue"]))

        # Board exam alert
        if "alert" in topic:
            sections.append(_board_exam_alert(topic["alert"]))

        # Common mistake
        if "mistake" in topic:
            sections.append(_common_mistake(topic["mistake"]))

        # Competitive edge
        if "competitive" in topic:
            sections.append(_competitive_edge(topic["competitive"]))

        # Diagram
        if "diagram" in topic:
            sections.append("\n**Diagram:**\n\n" + topic["diagram"] + "\n")

        sections.append(_brand_line("This is how we prepare students for both Boards and Competitive Exams simultaneously."))
        sections.append(_page_footer())

    # ── Quick Revision Sheet ──────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append("## 📋 Quick Revision Sheet\n")
    sections.append(_quick_revision_box(data["revision_points"], data["revision_formulas"]))

    # ── Formula Sheet ─────────────────────────────────────────────────────────
    sections.append("## 📐 Formula Sheet\n")
    sections.append("| Formula | Description |\n|---------|-------------|\n")
    for f in data["revision_formulas"]:
        sections.append(f"| `{f}` | |\n")
    sections.append("\n")
    sections.append(_page_footer())

    # ── Board Exam Smart Points ───────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append("## ✍️ Board Exam Smart Points\n")
    sections.append(
        "> *At Success Achievers Institute, every student learns the exact format examiners expect.*\n\n"
    )
    for topic_name, defn, formula, explanation in data["board_smart_answers"]:
        sections.append(_smart_answer_box(topic_name, defn, formula, explanation))
    sections.append(_page_footer())

    # ── MCQs ──────────────────────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(_mcq_section(chapter_title, data["mcqs"]))
    sections.append(_page_footer())

    # ── Assertion–Reasoning ───────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(_ar_section(data["ar"]))
    sections.append(_page_footer())

    # ── VSA ───────────────────────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(_vsa_section(data["vsa"]))
    sections.append(_page_footer())

    # ── Short Answer ──────────────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(_sa_section(data["sa"]))
    sections.append(_page_footer())

    # ── Case Studies ──────────────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(_case_study_section(data["case_studies"]))
    sections.append(_page_footer())

    # ── Competency Questions ──────────────────────────────────────────────────
    sections.append(_page_header(class_label, chapter_title))
    sections.append(_competency_section(data["competency"]))
    sections.append(_page_footer())

    # ── Final Branding ────────────────────────────────────────────────────────
    sections.append(_final_branding())

    # ── Write file ────────────────────────────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "chapter-01-number-systems-module.md"
    out_file.write_text("\n".join(sections), encoding="utf-8")
    print(f"✅  Module written → {out_file}  ({out_file.stat().st_size:,} bytes)")
    return out_file


# ---------------------------------------------------------------------------
# Generic module builder (for any chapter without specific enrichment data)
# ---------------------------------------------------------------------------

def build_generic_module(chapter_title: str, class_label: str,
                         chapter_num: str, raw_text: str,
                         output_dir: Path) -> Path:
    """Build a generic coaching module shell for chapters without enrichment data."""
    sections: list[str] = []

    sections.append(_page_header(class_label, chapter_title))
    sections.append(f"# Chapter {chapter_num}: {chapter_title}\n")
    sections.append(f"*Class {class_label} | Mathematics | Success Achievers Institute, Alwar*\n")
    sections.append(_brand_line())

    sections.append("\n## 📄 Content Extracted from PDF\n")
    clean_lines = [
        ln.strip() for ln in raw_text.splitlines()
        if len(ln.strip()) > 8
    ]
    excerpt = "\n".join(clean_lines[:200])
    sections.append(f"\n```\n{excerpt}\n```\n")

    sections.append(_concept_box(
        chapter_title,
        f"Core concepts of {chapter_title} as per NCERT Class {class_label} Maths.",
        "Refer to formula sheet",
        "See worked examples below",
    ))
    sections.append(_memory_trick(f"Review the key formulas and definitions of {chapter_title}."))
    sections.append(_board_exam_alert(
        f"Frequently tested topics in {chapter_title} — practice previous year questions."
    ))
    sections.append(_common_mistake(
        f"Read each question carefully in {chapter_title} — unit errors and sign mistakes are common."
    ))
    sections.append(_quick_revision_box(
        [f"Key concept of {chapter_title}", "Refer to NCERT examples"],
        ["See formula reference sheet"],
    ))

    # Placeholder question sections
    sections.append("---\n## 📝 MCQs *(10 Questions)*\n\n*[To be added after full content review]*\n")
    sections.append("---\n## 🔍 Assertion–Reasoning *(5 Questions)*\n\n*[To be added]*\n")
    sections.append("---\n## ✏️ Very Short Answer *(5 Questions)*\n\n*[To be added]*\n")
    sections.append("---\n## 📄 Short Answer *(5 Questions)*\n\n*[To be added]*\n")
    sections.append("---\n## 📊 Case Study *(3 Questions)*\n\n*[To be added]*\n")
    sections.append("---\n## 🎯 Competency Questions *(5 Questions)*\n\n*[To be added]*\n")

    sections.append(_final_branding())

    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^a-z0-9]+", "-", chapter_title.lower()).strip("-")
    out_file = output_dir / f"chapter-{chapter_num.zfill(2)}-{safe_name}-module.md"
    out_file.write_text("\n".join(sections), encoding="utf-8")
    print(f"✅  Module written → {out_file}  ({out_file.stat().st_size:,} bytes)")
    return out_file


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert NCERT PDFs into Ultra-Premium Coaching Modules."
    )
    parser.add_argument("pdf", nargs="?",
                        help="Path to a single PDF file.")
    parser.add_argument("--chapter",
                        help="Chapter name key (e.g. 'number_systems') to merge all matching parts.")
    parser.add_argument("--all", action="store_true",
                        help="Convert all chapters found in pdfs/ directory.")
    parser.add_argument("--output-dir", default="modules",
                        help="Output directory (default: modules/).")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / args.output_dir
    pdfs_dir   = repo_root / "pdfs"

    groups = group_parts(pdfs_dir) if pdfs_dir.exists() else {}

    if args.all:
        if not groups:
            print(f"No PDFs found in '{pdfs_dir}'. Upload PDFs and retry.")
            sys.exit(1)
        for chapter_key, parts in groups.items():
            print(f"\n📚  Processing chapter: {chapter_key} ({len(parts)} parts)")
            raw = merge_parts_text(parts)
            if "number" in chapter_key:
                build_number_systems_module(raw, output_dir)
            else:
                build_generic_module(chapter_key.replace("_", " ").title(),
                                     "9", "?", raw, output_dir)

    elif args.chapter:
        key = args.chapter.lower()
        parts = groups.get(key)
        if not parts:
            print(f"No PDFs found for chapter '{key}' in {pdfs_dir}")
            sys.exit(1)
        print(f"📚  Merging {len(parts)} parts for chapter: {key}")
        raw = merge_parts_text(parts)
        if "number" in key:
            build_number_systems_module(raw, output_dir)
        else:
            build_generic_module(key.replace("_", " ").title(), "9", "?", raw, output_dir)

    elif args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"Error: file not found: {pdf_path}")
            sys.exit(1)
        print(f"📖  Processing single PDF: {pdf_path.name}")
        raw = extract_pdf_text(pdf_path)
        build_generic_module(pdf_path.stem.replace("_", " ").title(),
                             "9", "?", raw, output_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
