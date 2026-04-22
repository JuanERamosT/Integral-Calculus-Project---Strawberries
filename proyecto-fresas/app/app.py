"""
Proyecto: Modelamiento del Volumen de una Fresa
Caso 1 - Modelo 2: f(x) = -0.3(x-1)^2 + 2, 0 <= x <= 2.5
Universidad de los Llanos - Cálculo Integral I
"""

from flask import Flask, render_template, jsonify, request
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin pantalla (necesario en servidor)
import matplotlib.pyplot as plt
from scipy import integrate
import sympy as sp
import base64
import io
import os

app = Flask(__name__)

# ─────────────────────────────────────────────
# MODELO MATEMÁTICO - Modelo 2
# ─────────────────────────────────────────────

def f(x):
    """Función que modela el radio de la fresa en la posición x."""
    return -0.3 * (x - 1)**2 + 2

A = 0      # Límite inferior de integración (cm)
B = 2.5    # Límite superior de integración (cm)


# ─────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graficar_funcion', methods=['POST'])
def graficar_funcion():
    """Grafica f(x) = -0.3(x-1)^2 + 2 en el intervalo [0, 2.5]."""
    x = np.linspace(A, B, 400)
    y = f(x)

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#0f1117')

    ax.plot(x, y, color='#e63946', linewidth=2.5, label=r'$f(x) = -0.3(x-1)^2 + 2$')
    ax.fill_between(x, 0, y, alpha=0.15, color='#e63946')
    ax.axhline(0, color='white', linewidth=0.5, alpha=0.4)
    ax.axvline(0, color='white', linewidth=0.5, alpha=0.4)

    ax.set_xlabel('x (longitud de la fresa, cm)', color='white')
    ax.set_ylabel('f(x) = radio (cm)', color='white')
    ax.set_title('Perfil de la Fresa — Modelo 2', color='white', fontsize=13)
    ax.legend(facecolor='#1a1a2e', edgecolor='#e63946', labelcolor='white')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')

    imagen = _fig_a_base64(fig)
    plt.close(fig)
    return jsonify({'imagen': imagen, 'status': 'ok'})


@app.route('/solido_revolucion', methods=['POST'])
def solido_revolucion():
    """Genera visualización 3D del sólido de revolución."""
    theta = np.linspace(0, 2 * np.pi, 60)
    x_vals = np.linspace(A, B, 80)
    X, T = np.meshgrid(x_vals, theta)
    R = f(X)
    Y = R * np.cos(T)
    Z = R * np.sin(T)

    fig = plt.figure(figsize=(7, 5))
    fig.patch.set_facecolor('#0f1117')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0f1117')

    ax.plot_surface(X, Y, Z, cmap='RdYlGn', alpha=0.85, linewidth=0)
    ax.set_xlabel('x (longitud)', color='white', labelpad=8)
    ax.set_ylabel('y', color='white')
    ax.set_zlabel('z', color='white')
    ax.set_title('Sólido de Revolución — Fresa 3D', color='white')
    ax.tick_params(colors='white')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    imagen = _fig_a_base64(fig)
    plt.close(fig)
    return jsonify({'imagen': imagen, 'status': 'ok'})


@app.route('/calcular_volumen', methods=['POST'])
def calcular_volumen():
    """Calcula el volumen numérico de la fresa con scipy.integrate."""
    datos = request.get_json()
    cantidad = int(datos.get('cantidad', 1))

    # Integrando: π * [f(x)]^2
    integrando = lambda x: np.pi * f(x)**2
    volumen_unitario, error = integrate.quad(integrando, A, B)
    volumen_total = volumen_unitario * cantidad

    return jsonify({
        'volumen_unitario': round(volumen_unitario, 4),
        'volumen_total': round(volumen_total, 4),
        'error_estimado': f'{error:.2e}',
        'cantidad': cantidad,
        'unidades': 'cm³',
        'status': 'ok'
    })


@app.route('/resolver_integral', methods=['POST'])
def resolver_integral():
    """Resuelve la integral simbólicamente paso a paso con SymPy."""
    x = sp.Symbol('x')

    # Definir función simbólica
    fx = sp.Rational(-3, 10) * (x - 1)**2 + 2

    # Expandir f(x)
    fx_expandida = sp.expand(fx)

    # [f(x)]^2
    fx_cuadrado = sp.expand(fx**2)

    # Integrando completo: π * [f(x)]^2
    integrando = sp.pi * fx_cuadrado

    # Antiderivada (integral indefinida)
    antiderivada = sp.integrate(fx_cuadrado, x)

    # Integral definida
    resultado = sp.integrate(sp.pi * fx_cuadrado, (x, 0, sp.Rational(5, 2)))
    resultado_decimal = float(resultado)

    return jsonify({
        'f_x': str(fx_expandida),
        'f_x_cuadrado': str(fx_cuadrado),
        'integrando': str(integrando),
        'antiderivada': str(antiderivada),
        'resultado_exacto': str(resultado),
        'resultado_decimal': round(resultado_decimal, 4),
        'latex_fx': sp.latex(fx),
        'latex_fx2': sp.latex(fx_cuadrado),
        'latex_antiderivada': sp.latex(antiderivada),
        'latex_resultado': sp.latex(resultado),
        'status': 'ok'
    })


@app.route('/diseno_caja', methods=['POST'])
def diseno_caja():
    """Calcula dimensiones sugeridas de la caja y área mínima de material."""
    datos = request.get_json()
    cantidad = int(datos.get('cantidad', 100))

    # Volumen unitario numérico
    integrando = lambda x: np.pi * f(x)**2
    v_unitario, _ = integrate.quad(integrando, A, B)
    v_total = v_unitario * cantidad

    # Dimensiones sugeridas: caja cúbica como aproximación inicial
    lado = v_total ** (1/3)
    largo  = round(lado * 1.5, 2)
    ancho  = round(lado, 2)
    alto   = round(v_total / (largo * ancho), 2)

    # Área de la caja
    area = 2 * (largo * ancho + largo * alto + ancho * alto)

    return jsonify({
        'volumen_unitario': round(v_unitario, 4),
        'volumen_total': round(v_total, 4),
        'largo': largo,
        'ancho': ancho,
        'alto': alto,
        'area_material': round(area, 4),
        'cantidad': cantidad,
        'unidades_volumen': 'cm³',
        'unidades_dimension': 'cm',
        'status': 'ok'
    })


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────

def _fig_a_base64(fig):
    """Convierte figura matplotlib a string base64 para enviar al frontend."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs('app/static/plots', exist_ok=True)
    app.run(debug=True, port=5000)
