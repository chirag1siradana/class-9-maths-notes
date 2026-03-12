# Chapter 1: Number Systems – Study Notes

> Class 9 NCERT Maths

---

## 1. Types of Numbers

| Type | Symbol | Description | Examples |
|------|--------|-------------|----------|
| **Natural Numbers** | ℕ | Counting numbers starting from 1 | 1, 2, 3, 4, … |
| **Whole Numbers** | W | Natural numbers + 0 | 0, 1, 2, 3, … |
| **Integers** | ℤ | Whole numbers + negative numbers | …, −2, −1, 0, 1, 2, … |
| **Rational Numbers** | ℚ | Numbers of the form p/q (q ≠ 0), where p and q are integers | ½, −3, 0.75, 0.333… |
| **Irrational Numbers** | | Numbers that **cannot** be expressed as p/q | √2, √3, π |
| **Real Numbers** | ℝ | All rational and irrational numbers | Every point on the number line |

### Number Set Hierarchy

```
ℕ ⊂ W ⊂ ℤ ⊂ ℚ ⊂ ℝ
```

Every natural number is a whole number, every whole number is an integer, every integer is a rational number, and every rational number is a real number. Irrational numbers are also real numbers but are **not** rational.

---

## 2. Rational Numbers

A number **r** is rational if it can be written as **p/q**, where p and q are integers and **q ≠ 0**.

### Key Properties

- Every integer n can be written as n/1, so every integer is rational.
- Between any two rational numbers, there are **infinitely many** rational numbers.
- Decimal expansion of a rational number is either **terminating** or **non-terminating repeating**.

### Decimal Expansions

| Type | Description | Example |
|------|-------------|---------|
| Terminating | Finite number of decimal digits | 7/8 = 0.875 |
| Non-terminating repeating | A block of digits repeats forever | 1/3 = 0.333… = 0.3̄ |

**Tip:** A rational number p/q (in lowest terms) has a terminating decimal if and only if the prime factorisation of q contains **only** 2s and/or 5s.

---

## 3. Irrational Numbers

A number is **irrational** if it **cannot** be expressed in the form p/q.

### Examples

- √2, √3, √5, √6, √7, √8, √10, …
- π (pi) ≈ 3.14159…
- 0.1010010001… (non-terminating, non-repeating)

### Key Fact

> √p is irrational for every prime number p.

### Proof that √2 is irrational (by contradiction)

1. Assume √2 = a/b where a, b are co-prime integers (b ≠ 0).
2. Then 2 = a²/b², so a² = 2b².
3. This means a² is even, so a is even. Write a = 2c.
4. Then 4c² = 2b², so b² = 2c², meaning b is also even.
5. But a and b are both even — contradicts the assumption they are co-prime.
6. Therefore, √2 is irrational. ∎

---

## 4. Real Numbers and the Number Line

- Every real number corresponds to a **unique point** on the number line, and vice versa.
- Irrational numbers can be located on the number line using geometric constructions (e.g., using the Pythagorean theorem to plot √2).

### Locating √2 on the Number Line

1. Draw a unit square (side = 1) on the number line starting at 0.
2. The diagonal of this square has length √(1² + 1²) = √2.
3. Use a compass centred at 0 with radius = diagonal to mark √2 on the line.

---

## 5. Operations on Real Numbers

### Properties

- The **sum** or **difference** of a rational and an irrational number is **irrational**.
  - Example: 2 + √3 is irrational
- The **product** or **quotient** of a non-zero rational and an irrational number is **irrational**.
  - Example: 7√5 is irrational
- The sum, difference, product, or quotient of two irrationals may be rational or irrational.
  - Example: √2 × √2 = 2 (rational); √2 + √3 (irrational)

---

## 6. Laws of Exponents for Real Numbers

For positive real numbers **a** and **b**, and rational exponents **m** and **n**:

| Law | Expression |
|-----|------------|
| Product of powers | aᵐ × aⁿ = aᵐ⁺ⁿ |
| Quotient of powers | aᵐ ÷ aⁿ = aᵐ⁻ⁿ |
| Power of a power | (aᵐ)ⁿ = aᵐⁿ |
| Product to a power | (ab)ⁿ = aⁿ bⁿ |
| Zero exponent | a⁰ = 1 |
| Negative exponent | a⁻ⁿ = 1/aⁿ |

### Rational Exponents and Radicals

- a^(1/n) = ⁿ√a (the nth root of a)
- a^(m/n) = (ⁿ√a)ᵐ = ⁿ√(aᵐ)

**Examples:**

- 8^(1/3) = ³√8 = 2
- 27^(2/3) = (³√27)² = 3² = 9

---

## 7. Rationalising the Denominator

To remove surds from the denominator, multiply numerator and denominator by the **conjugate** or appropriate surd.

### Common Identities Used

- (a + b)(a − b) = a² − b²
- (√a + √b)(√a − √b) = a − b

### Examples

| Expression | Rationalised Form |
|------------|-------------------|
| 1/√2 | √2/2 |
| 1/(√3 + √2) | √3 − √2 |
| 1/(√5 − √3) | (√5 + √3)/2 |

**Worked Example:**

```
  1/(√5 − √3)
= 1/(√5 − √3) × (√5 + √3)/(√5 + √3)
= (√5 + √3) / (5 − 3)
= (√5 + √3) / 2
```

---

## 8. Important Formulas at a Glance

| # | Formula / Identity |
|---|-------------------|
| 1 | aᵐ × aⁿ = aᵐ⁺ⁿ |
| 2 | aᵐ ÷ aⁿ = aᵐ⁻ⁿ |
| 3 | (aᵐ)ⁿ = aᵐⁿ |
| 4 | a^(1/n) = ⁿ√a |
| 5 | a^(m/n) = ⁿ√(aᵐ) |
| 6 | (√a + √b)(√a − √b) = a − b |
| 7 | (a + b)² = a² + 2ab + b² |
| 8 | (a − b)² = a² − 2ab + b² |

---

## 9. Common Mistakes to Avoid

1. **√(a + b) ≠ √a + √b** — Square root does not distribute over addition.
2. **Forgetting q ≠ 0** when writing rational numbers as p/q.
3. Confusing **non-terminating repeating** (rational) with **non-terminating non-repeating** (irrational).
4. Not simplifying the surd before rationalising.
5. Writing √4 = ±2 — by convention, √4 = 2 (the positive root).

---

## 10. Practice Questions

1. Is √(4/9) rational or irrational? Justify.
2. Find five rational numbers between 3/5 and 4/5.
3. Represent √9.3 on the number line.
4. Rationalise the denominator of 1/(2 + √3).
5. Simplify: (3^(1/3))⁴ × (3^(1/3))⁵.
6. Prove that √5 is irrational.
7. Express 0.4̄7̄ (0.474747…) in the form p/q.
8. Simplify: 2^(2/3) × 2^(1/3).

### Answers (Brief)

1. √(4/9) = 2/3 → **Rational**
2. 31/50, 32/50, 33/50, 34/50, 35/50 (or simplify)
3. Use successive magnification on the number line
4. 1/(2 + √3) = (2 − √3)/(4 − 3) = **2 − √3**
5. 3^(4/3) × 3^(5/3) = 3^(9/3) = 3³ = **27**
6. Proof by contradiction (see Section 3)
7. Let x = 0.474747…; 100x = 47.474747…; 99x = 47; x = **47/99**
8. 2^(2/3) × 2^(1/3) = 2^(3/3) = 2¹ = **2**
