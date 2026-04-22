"""
integral_modelo2.py
Desarrollo simbólico completo de la integral del Modelo 2
f(x) = -0.3(x-1)^2 + 2, 0 <= x <= 2.5

Ejecutar con: python matematicas/integral_modelo2.py
"""

import sympy as sp

x = sp.Symbol('x')

print("=" * 60)
print("DESARROLLO SIMBÓLICO — CASO 1, MODELO 2")
print("=" * 60)

# PASO 1
fx = sp.Rational(-3, 10) * (x - 1)**2 + 2
print(f"\nPASO 1 — Función del modelo:")
print(f"  f(x) = {fx}")
print(f"  f(x) expandida = {sp.expand(fx)}")

# PASO 2
fx2 = sp.expand(fx**2)
print(f"\nPASO 2 — [f(x)]^2:")
print(f"  [f(x)]^2 = {fx2}")

# PASO 3
print(f"\nPASO 3 — Integral a resolver:")
print(f"  V = π ∫₀²·⁵ [{sp.expand(fx)}]² dx")

# PASO 4
antiderivada = sp.integrate(fx2, x)
print(f"\nPASO 4 — Antiderivada F(x):")
print(f"  F(x) = {antiderivada}")

# PASO 5
resultado = sp.integrate(sp.pi * fx2, (x, 0, sp.Rational(5, 2)))
print(f"\nPASO 5 — Resultado exacto:")
print(f"  V = π·F(2.5) - π·F(0)")
print(f"  V = {resultado}")
print(f"  V ≈ {float(resultado):.4f} cm³")

# VERIFICACIÓN NUMÉRICA
from scipy import integrate
import numpy as np

def f_num(x):
    return -0.3 * (x - 1)**2 + 2

vol_num, err = integrate.quad(lambda x: np.pi * f_num(x)**2, 0, 2.5)
print(f"\nVERIFICACIÓN NUMÉRICA (scipy):")
print(f"  V ≈ {vol_num:.4f} cm³  (error estimado: {err:.2e})")
print(f"\n  ✓ Coincidencia: {abs(float(resultado) - vol_num) < 1e-6}")
print("=" * 60)
