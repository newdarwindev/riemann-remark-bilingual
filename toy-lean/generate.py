"""Generate an original finite Lean teaching corpus; no upstream proof inputs."""
from itertools import product
from pathlib import Path
import sys

BASE = """import Lean

namespace RemarkToy

def determinant (a b c d : Int) := a * d - b * c
def square (n : Nat) := n * n
def towerStep (base level scale : Nat) := base ^ level * scale
def thetaMoment (n : Nat) := (List.range (n + 1)).foldl (fun a k => a + k * k) 0
def periodTotal (a b c n : Nat) := n * (a + b + c)
def residue (base n : Nat) := n % base

theorem determinantDiagonal (a d : Int) : determinant a 0 0 d = a * d := by
  simp [determinant]

theorem towerNesting (b level n : Nat) :
    towerStep b level n = b ^ level * n := rfl

theorem periodZero (a b c : Nat) : periodTotal a b c 0 = 0 := by
  simp [periodTotal]

end RemarkToy
"""
def determinant():
    for a, b, c, d in product(range(-5, 6), range(-5, 6), range(-4, 5), range(-4, 5)):
        yield f"determinant ({a}) ({b}) ({c}) ({d}) = ({a*d-b*c} : Int)"

def positivity():
    for a, b, c in product(range(1, 19), repeat=3):
        yield f"0 < square {a} + square {b} + square {c}"

def towers():
    for b, k, n in product(range(2, 17), range(1, 9), range(1, 25)):
        yield f"towerStep {b} {k} {n} % ({b} ^ {k}) = 0"

def theta():
    for n, w, x in product(range(1, 21), range(1, 16), range(10)):
        v = sum(k*k for k in range(n+1))
        yield f"{w} * thetaMoment {n} + {x} = {w*v+x}"

def periods():
    for a,b,c,n in product(range(6), range(6), range(6), range(1,16)):
        yield f"periodTotal {a} {b} {c} {n} / {n} = {a+b+c}"

def congruences():
    for b, q, r in product(range(2, 29), range(1, 14), range(8)):
        yield f"residue {b} ({q} * {b} + {r}) = {r%b}"

SECTIONS = [
 ("01_Determinants", "Signed 2-by-2 determinants on small integer matrices.", determinant),
 ("02_Positivity", "Positive sums of three squares of positive naturals.", positivity),
 ("03_Towers", "A power divides each corresponding scaled tower step.", towers),
 ("04_ThetaMoments", "Finite weighted square moments, not analytic theta identities.", theta),
 ("05_PeriodAverages", "A length-three pattern repeated whole periods.", periods),
 ("06_Congruences", "Residue normalization after adding a modulus multiple.", congruences),
]

def main(out):
    out.mkdir(parents=True, exist_ok=True)
    (out / "RemarkToy.lean").write_text(BASE, encoding="utf-8")
    for name, description, cases in SECTIONS:
        body = [f"import RemarkToy\n\n-- {description}\nopen RemarkToy\n"]
        for i, case in enumerate(cases()):
            if i >= 2600:
                break
            body.append(f"theorem case_{i:04d} : {case} := by decide\n")
        # Modules have disjoint namespaces when loaded together.
        head, *proofs = body
        text = head + f"\nnamespace Toy{name}\n" + "".join(proofs)
        (out / f"{name}.lean").write_text(text + f"end Toy{name}\n", encoding="utf-8")

if __name__ == "__main__":
    main(Path(sys.argv[1]))
