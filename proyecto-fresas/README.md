# 🍓 Modelamiento del Volumen de una Fresa
**Caso 1 — Modelo 2** | Cálculo Integral I | Universidad de los Llanos

---

## 📋 Descripción

Sistema web que modela el volumen de una fresa usando sólidos de revolución
e integrales definidas.

**Función del Modelo 2:**
```
f(x) = -0.3(x - 1)² + 2,  0 ≤ x ≤ 2.5
```

**Fórmula del volumen:**
```
V = π ∫₀²·⁵ [f(x)]² dx
```

---

## 📁 Estructura del Proyecto

```
proyecto-fresas-calculo/
├── app/
│   ├── app.py              ← Servidor Flask (lógica Python)
│   ├── templates/
│   │   └── index.html      ← Interfaz web (4 paneles)
│   └── static/             ← CSS y JS adicionales (si se agregan)
├── matematicas/
│   └── integral_modelo2.py ← Desarrollo simbólico con SymPy
├── diagramas/              ← Diagrama de flujo en Inkscape (.svg)
├── docs/                   ← Documentación adicional
├── requirements.txt        ← Dependencias Python
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación y Ejecución (Windows)

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/proyecto-fresas-calculo.git
cd proyecto-fresas-calculo
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```
> Verás `(venv)` al inicio de la línea si está activo.

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
cd app
python app.py
```

### 5. Abrir en el navegador
```
http://localhost:5000
```

---

## 🔧 Requisitos

- Python 3.10 o superior
- pip (incluido con Python)
- Navegador moderno (Chrome, Firefox, Edge)

---

## 👥 Grupo

| Nombre | Rol |
|--------|-----|
| — | Desarrollo Python / Flask |
| — | Interfaz HTML / JavaScript |
| — | Informe IEEE / LaTeX |

---

## 📦 Dependencias principales

| Librería | Uso |
|----------|-----|
| Flask | Servidor web |
| NumPy | Cálculo numérico |
| Matplotlib | Gráficas 2D y 3D |
| SciPy | Integración numérica |
| SymPy | Cálculo simbólico (integral paso a paso) |

---

## 📄 Entregables

- [x] Interfaz HTML con 4 paneles
- [x] Backend Python con Flask
- [x] Desarrollo simbólico de la integral
- [ ] Diagrama de flujo (Inkscape)
- [ ] Informe IEEE en LaTeX
- [ ] Prototipo físico del empaque
