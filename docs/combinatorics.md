# 🔢 Permutations in the Game “Bulls and Cows”

In the game “Bulls and Cows”, the goal is to guess a **secret 4-digit number** made of **unique digits**.  
Order matters, and digits do not repeat.

---

## 📈 Permutation Formula (without repetition):

To generate all possible 4-digit combinations from `n` unique digits (without repetition), the following formula applies:

\[
P(n, k) = \frac{n!}{(n - k)!}
\]

Where:
- `n` — total number of available digits
- `k` — length of the combination (4)
- `!` — factorial (e.g., 4! = 4×3×2×1 = 24)
- **Order matters**
- **No repetition**

---

## ▶️ Examples:

### 🔹 Simplified version (6 digits: 0–5):
$$
P(6, 4) = \frac{6!}{(6 - 4)!} = 6 * 5 * 4 * 3 = 360
$$

$$
P(n, k) = \frac{n!}{(n - k)!}
$$
**Total: 360 possible combinations**

### 🔹 Classic version (10 digits: 0–9):
\[
P(10, 4) = 10 \times 9 \times 8 \times 7 = 5040
\]
**Total: 5040 combinations**

---

## 💡 Conclusion:
- The maximum number of attempts required to guess the number by brute-force = number of permutations
- A strategy using Bulls/Cows feedback reduces the average number of attempts to around 7–8
