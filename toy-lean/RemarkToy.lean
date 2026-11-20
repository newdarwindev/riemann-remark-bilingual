import Lean

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
