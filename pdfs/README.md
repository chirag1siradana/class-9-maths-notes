# 📂 PDF Repository — Success Achievers Institute

This folder is the **PDF Repository** for Class 9 & 10 NCERT chapter PDFs.

The PDFs in this repository are handwritten/scanned NCERT notes.
The `tools/pdf_to_module.py` script reads them using OCR and converts the content
into **Ultra-Premium Coaching Modules** (saved to `modules/`).

---

## 📥 PDFs in This Repository

The following PDFs are stored on the **`main`** branch of this repository:

| File | Chapter | Pages |
|------|---------|-------|
| `01_number_systems_part1.pdf` | Chapter 1: Number Systems | Part 1 |
| `02_number_systems_part2.pdf` | Chapter 1: Number Systems | Part 2 |
| `03_number_systems_part3.pdf` | Chapter 1: Number Systems | Part 3 |
| `04_number_systems_part4.pdf` | Chapter 1: Number Systems | Part 4 |
| `05_number_systems_part5.pdf` | Chapter 1: Number Systems | Part 5 |
| `06_number_systems_part6.pdf` | Chapter 1: Number Systems | Part 6 |
| `07_number_systems_part7.pdf` | Chapter 1: Number Systems | Part 7 |
| `08_number_systems_part8.pdf` | Chapter 1: Number Systems | Part 8 |
| `09_number_systems_part9.pdf` | Chapter 1: Number Systems | Part 9 |
| `10_number_systems_part10.pdf` | Chapter 1: Number Systems | Part 10 |

> **Note:** PDFs are scanned handwritten notes. The tool uses OCR (Tesseract) to read them.

---

## ⚙️ Generating a Module from These PDFs

### Prerequisites

```bash
# Python packages
pip install -r requirements.txt

# System OCR engine (required for handwritten/scanned PDFs)
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-hin   # Linux
brew install tesseract                                                     # macOS
```

### Merge all parts of a chapter and generate the module

```bash
python tools/pdf_to_module.py --chapter number_systems
```

### Convert all chapters at once

```bash
python tools/pdf_to_module.py --all
```

The generated module is saved to `modules/chapter-01-number-systems-module.md`.

---

## 📛 Naming Convention for New PDFs

When adding PDFs for future chapters, use the format:

```
<NN>_<chapter_name>_part<N>.pdf
```

| Example | Chapter |
|---------|---------|
| `01_polynomials_part1.pdf` | Chapter 2: Polynomials |
| `01_coordinate_geometry_part1.pdf` | Chapter 3: Coordinate Geometry |

---

*Success Achievers Institute | Alwar, Rajasthan*
*"Better Than Others, No One Can Refute"*


---

## 📥 How to Add a PDF

1. Download the NCERT chapter PDF (or scan your own notes as a PDF).
2. Rename the file following the naming convention below.
3. Place it in this `pdfs/` folder.
4. Run the extraction tool (see below).

---

## 📛 Naming Convention

Use the format:

```
class<N>-maths-ch<NN>-<short-name>.pdf
```

| Example File Name | Chapter |
|-------------------|---------|
| `class9-maths-ch01-number-systems.pdf` | Class 9 – Chapter 1: Number Systems |
| `class9-maths-ch02-polynomials.pdf` | Class 9 – Chapter 2: Polynomials |
| `class9-maths-ch03-coordinate-geometry.pdf` | Class 9 – Chapter 3: Coordinate Geometry |
| `class9-maths-ch04-linear-equations.pdf` | Class 9 – Chapter 4: Linear Equations |
| `class9-maths-ch05-euclids-geometry.pdf` | Class 9 – Chapter 5: Euclid's Geometry |
| `class9-maths-ch06-lines-angles.pdf` | Class 9 – Chapter 6: Lines and Angles |
| `class9-maths-ch07-triangles.pdf` | Class 9 – Chapter 7: Triangles |
| `class9-maths-ch08-quadrilaterals.pdf` | Class 9 – Chapter 8: Quadrilaterals |
| `class9-maths-ch09-areas.pdf` | Class 9 – Chapter 9: Areas |
| `class9-maths-ch10-circles.pdf` | Class 9 – Chapter 10: Circles |
| `class9-maths-ch11-constructions.pdf` | Class 9 – Chapter 11: Constructions |
| `class9-maths-ch12-herons-formula.pdf` | Class 9 – Chapter 12: Heron's Formula |
| `class9-maths-ch13-surface-volumes.pdf` | Class 9 – Chapter 13: Surface Areas & Volumes |
| `class9-maths-ch14-statistics.pdf` | Class 9 – Chapter 14: Statistics |
| `class9-maths-ch15-probability.pdf` | Class 9 – Chapter 15: Probability |

---

## ⚙️ Running the PDF-to-Module Tool

### Prerequisites

```bash
pip install -r requirements.txt
```

### Convert a single PDF

```bash
python tools/pdf_to_module.py pdfs/class9-maths-ch01-number-systems.pdf
```

The output module will be saved to:

```
modules/class9-maths-ch01-number-systems-module.md
```

### Convert all PDFs in this folder at once

```bash
python tools/pdf_to_module.py --all
```

---

## 📤 Output Location

All generated **Ultra-Premium Coaching Modules** are saved in the `modules/` directory.

Each generated file follows the full Success Achievers Institute format:
- Page header with institute branding
- Concept Boxes (Kota style)
- Memory Tricks
- Board Exam Alerts
- Common Student Mistakes
- Competitive Edge tips
- Gen-Z Hinglish Classroom Dialogues
- Quick Revision Boxes
- MCQs, Assertion-Reasoning, VSA, SA, Case Study, Competency Questions
- Final branding page

---

## 📌 Notes

- PDFs must be text-based (not scanned images) for best extraction results.
- Scanned PDFs may require OCR — install `pytesseract` and `pdf2image` for OCR support.
- The tool works on both Windows and Linux/macOS.

---

*Success Achievers Institute | Alwar, Rajasthan*
*"Better Than Others, No One Can Refute"*
