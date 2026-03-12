# Chapter 12: Heron's Formula

## Overview

This chapter introduces Heron's Formula for calculating the area of a triangle when all three sides are known, without needing the height.

---

## Key Concepts

### 12.1 Area of a Triangle – Basic Formula
- Area = ½ × base × height
- Requires knowing the **height**, which may not always be given.

### 12.2 Heron's Formula
When all three sides a, b, c are known:

**Step 1:** Calculate the semi-perimeter:
> s = (a + b + c) / 2

**Step 2:** Apply Heron's Formula:
> Area = √[s(s − a)(s − b)(s − c)]

### 12.3 Application to Quadrilaterals
- Divide the quadrilateral into two triangles using a diagonal.
- Apply Heron's formula to each triangle.
- Total area = sum of both triangle areas.

---

## Important Notes
- Heron's formula works for **any triangle** (scalene, isosceles, equilateral).
- For an **equilateral triangle** with side a: Area = (√3/4)a²

---

## Examples

**Example 1:** Find the area of a triangle with sides 3 cm, 4 cm, 5 cm.
> s = (3 + 4 + 5)/2 = 6
> Area = √[6(6−3)(6−4)(6−5)] = √[6 × 3 × 2 × 1] = √36 = **6 cm²**

**Example 2:** Find the area of an equilateral triangle with side 6 cm.
> Area = (√3/4) × 36 = **9√3 cm²**

**Example 3:** A rhombus has diagonals 24 cm and 10 cm. Find its area.
> Area = ½ × d₁ × d₂ = ½ × 24 × 10 = **120 cm²**
> Alternatively, use Heron's formula on each triangle formed by the diagonal.

---

## Practice Problems

1. Find the area of a triangle with sides 7 cm, 8 cm, 9 cm.
2. A triangular park has sides 120 m, 80 m, 50 m. Find its area.
3. Find the area of an equilateral triangle with perimeter 36 cm.
4. A quadrilateral ABCD has sides AB = 3 cm, BC = 4 cm, CD = 4 cm, DA = 5 cm, and diagonal AC = 5 cm. Find its area.
5. A triangular field has sides 40 m, 24 m, 32 m. Find the cost of planting grass at ₹5 per m².

---

## Summary

- Heron's Formula: Area = √[s(s−a)(s−b)(s−c)], where s = (a+b+c)/2
- Works for any triangle when all three sides are known
- For equilateral triangle: Area = (√3/4)a²
- For quadrilaterals: split into two triangles using a diagonal
