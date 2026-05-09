import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
from scipy.integrate import quad
import sympy as sp

app = Flask(__name__)


# ── Modelo matemático ──

def perfil_fresa(x):
    """Modelo 2: y = -0.3(x-1)³ + 2"""
    return -0.3 * (x - 1)**3 + 2

def integrando_volumen(x):
    """π·[f(x)]² — integrando para el volumen por discos"""
    return np.pi * perfil_fresa(x)**2


# ── Utilidad ──

def fig_to_base64(fig):
    """Convierte una figura matplotlib a string base64 PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close(fig)
    return encoded


# ── Rutas ──

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/graficar', methods=['POST'])
def graficar():
    x = np.linspace(0, 2.5, 100)
    y = perfil_fresa(x)

    fig, ax = plt.subplots(figsize=(4, 3.5), facecolor='#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    ax.plot(x, y, color='#00d2ff', linewidth=2)
    ax.set_title('Perfil de la Fresa (Modelo 2)', color='white')
    ax.set_xlabel('x (Longitud)', color='white')
    ax.set_ylabel('y (Radio)', color='white')
    ax.tick_params(colors='white')
    ax.grid(color='#333333', linestyle='--')
    ax.spines['bottom'].set_color('#00d2ff')
    ax.spines['left'].set_color('#00d2ff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return jsonify({'grafica_2d': fig_to_base64(fig)})


@app.route('/api/solido', methods=['POST'])
def solido():
    x = np.linspace(0, 2.5, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    X, THETA = np.meshgrid(x, theta)
    Y = perfil_fresa(X) * np.cos(THETA)
    Z = perfil_fresa(X) * np.sin(THETA)

    fig = plt.figure(figsize=(4, 3.5), facecolor='#1e1e1e')
    ax = fig.add_subplot(111, projection='3d', facecolor='#1e1e1e')
    ax.plot_surface(X, Y, Z, color='#ff007f', alpha=0.8, antialiased=True)
    ax.set_title('Sólido de Revolución (3D)', color='white')
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False
        axis.pane.set_edgecolor('#1e1e1e')
    ax.tick_params(colors='white')

    return jsonify({'grafica_3d': fig_to_base64(fig)})


@app.route('/api/volumen', methods=['POST'])
def volumen():
    cantidad = int(request.json.get('cantidad', 1))

    vol_fresa, _ = quad(integrando_volumen, 0, 2.5)
    vol_total = vol_fresa * cantidad

    # Caja cúbica optimizada
    lado = vol_total ** (1 / 3)
    area = 6 * lado ** 2

    return jsonify({
        'volumen_fresa': round(vol_fresa, 4),
        'volumen_total': round(vol_total, 4),
        'caja_dimensiones': {
            'largo': round(lado, 2),
            'ancho': round(lado, 2),
            'alto':  round(lado, 2)
        },
        'area_optimizada': round(area, 2)
    })


@app.route('/api/integral', methods=['POST'])
def integral():
    x = sp.Symbol('x')
    f = -sp.Rational(3, 10) * (x - 1)**3 + 2
    expr = sp.pi * f**2

    expandida = sp.expand(expr)
    primitiva = sp.integrate(expandida, x)
    resultado = primitiva.subs(x, sp.Rational(5, 2)) - primitiva.subs(x, 0)

    return jsonify({
        'funcion_cuadrado':    sp.latex(expandida),
        'integral_indefinida': sp.latex(primitiva),
        'resultado_exacto':    sp.latex(resultado),
        'resultado_decimal':   str(round(float(resultado.evalf()), 4))
    })


if __name__ == '__main__':
    app.run(debug=True)
