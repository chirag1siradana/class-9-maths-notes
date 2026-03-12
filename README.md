# Class 9 Maths Notes — Success Achievers Institute

**Success Achievers Institute, Alwar, Rajasthan**
*"Better Than Others, No One Can Refute"*

Detailed notes for Class 9 Mathematics covering all 15 chapters of the NCERT syllabus.

> 🆕 **Ultra-Premium Coaching Modules** are now generated directly from the original PDF notes
> using OCR. See the [`modules/`](modules/) directory for the full Kota-style coaching content.

---

## 🏆 Ultra-Premium Coaching Modules (Generated from PDFs)

| Chapter | Module File | Source PDFs |
|---------|-------------|-------------|
| Chapter 1: Number Systems | [chapter-01-number-systems-module.md](modules/chapter-01-number-systems-module.md) | Parts 1–10 (10 PDFs) |

Each module contains:
- Kota-style **Concept Boxes**
- **Memory Tricks** (mnemonics)
- **Gen-Z Hinglish Classroom Dialogues**
- **Board Exam Alerts** & **Common Mistakes**
- **Competitive Edge** tips for JEE/NEET foundation
- **Quick Revision Sheet** & **Formula Sheet**
- **Board Exam Smart Answer** formats
- **10 MCQs**, **5 Assertion–Reasoning**, **5 VSA**, **5 SA**, **3 Case Studies**, **5 Competency Questions**
- Success Achievers Institute branding throughout

### ➕ Generate a Module from PDFs

```bash
# Prerequisites
pip install -r requirements.txt
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-hin

# Generate Chapter 1 module from the 10 PDF parts
python tools/pdf_to_module.py --chapter number_systems

# Generate all chapters at once
python tools/pdf_to_module.py --all
```

See [`pdfs/README.md`](pdfs/README.md) for full instructions.

---

## 📚 Chapters (Starter Notes)

| # | Chapter | File |
|---|---------|------|
| 1 | Number Systems | [chapter-01-number-systems.md](chapters/chapter-01-number-systems.md) |
| 2 | Polynomials | [chapter-02-polynomials.md](chapters/chapter-02-polynomials.md) |
| 3 | Coordinate Geometry | [chapter-03-coordinate-geometry.md](chapters/chapter-03-coordinate-geometry.md) |
| 4 | Linear Equations in Two Variables | [chapter-04-linear-equations-two-variables.md](chapters/chapter-04-linear-equations-two-variables.md) |
| 5 | Introduction to Euclid's Geometry | [chapter-05-euclids-geometry.md](chapters/chapter-05-euclids-geometry.md) |
| 6 | Lines and Angles | [chapter-06-lines-and-angles.md](chapters/chapter-06-lines-and-angles.md) |
| 7 | Triangles | [chapter-07-triangles.md](chapters/chapter-07-triangles.md) |
| 8 | Quadrilaterals | [chapter-08-quadrilaterals.md](chapters/chapter-08-quadrilaterals.md) |
| 9 | Areas of Parallelograms and Triangles | [chapter-09-areas-parallelograms-triangles.md](chapters/chapter-09-areas-parallelograms-triangles.md) |
| 10 | Circles | [chapter-10-circles.md](chapters/chapter-10-circles.md) |
| 11 | Constructions | [chapter-11-constructions.md](chapters/chapter-11-constructions.md) |
| 12 | Heron's Formula | [chapter-12-herons-formula.md](chapters/chapter-12-herons-formula.md) |
| 13 | Surface Areas and Volumes | [chapter-13-surface-areas-volumes.md](chapters/chapter-13-surface-areas-volumes.md) |
| 14 | Statistics | [chapter-14-statistics.md](chapters/chapter-14-statistics.md) |
| 15 | Probability | [chapter-15-probability.md](chapters/chapter-15-probability.md) |

---

## 🧠 Concepts

| File | Description |
|------|-------------|
| [concepts-overview.md](concepts/concepts-overview.md) | Bird's-eye view of all key concepts across all chapters |
| [formulas-reference.md](concepts/formulas-reference.md) | Consolidated formula sheet for quick reference |

---

## 📝 Notes

| File | Description |
|------|-------------|
| [study-notes-template.md](notes/study-notes-template.md) | Blank template to fill in while studying each chapter |
| [revision-notes.md](notes/revision-notes.md) | Quick-revision summaries for all 15 chapters |

---

## 📁 Repository Structure

```
class-9-maths-notes/
├── README.md
├── .gitignore
├── requirements.txt              ← Python dependencies for PDF tool
├── pdfs/
│   ├── README.md                 ← PDF usage guide
│   ├── 01_number_systems_part1.pdf  ← Source PDFs (on main branch)
│   └── ... (10 parts total)
├── tools/
│   └── pdf_to_module.py          ← OCR + module generator script
├── modules/
│   └── chapter-01-number-systems-module.md  ← Generated premium modules
├── chapters/                     ← Starter chapter notes
│   ├── chapter-01-number-systems.md
│   ├── chapter-02-polynomials.md
│   └── ... (15 chapters)
├── concepts/
│   ├── concepts-overview.md
│   └── formulas-reference.md
└── notes/
    ├── study-notes-template.md
    └── revision-notes.md
```
