/**
 * Script unificado — Proyecto Fresas (Cálculo Integral)
 * 
 * Secciones:
 *   1. Navegación (header, menú móvil, scroll suave, sección activa)
 *   2. Panel Entradas (slider ↔ input, botón confirmar → /api/volumen)
 *   3. Panel Simulación (botones → /api/graficar, /api/solido, /api/integral)
 */

document.addEventListener('DOMContentLoaded', () => {

    /* =========================================================
       1. NAVEGACIÓN
       ========================================================= */

    const header   = document.getElementById('header');
    const menuToggle = document.getElementById('menuToggle');
    const navMenu  = document.getElementById('navMenu');
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    // Header scroll effect
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 100);
    });

    // Mobile menu toggle
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }

    // Smooth scroll + close mobile menu
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const target   = document.getElementById(targetId);
            if (target) {
                const offset = header.offsetHeight;
                window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });
    });

    // Highlight active section on scroll
    function updateActiveNav() {
        const scrollPos = window.scrollY + 120;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(l => {
                    l.classList.toggle('active', l.getAttribute('href') === '#' + id);
                });
            }
        });
    }
    window.addEventListener('scroll', updateActiveNav);

    /* =========================================================
       2. PANEL DE ENTRADAS
       ========================================================= */

    const slider   = document.getElementById('cantidad_rango');
    const numInput = document.getElementById('cantidad_num');

    if (slider && numInput) {
        // Sync slider → number
        slider.addEventListener('input', () => { numInput.value = slider.value; });

        // Sync number → slider (con clamp 0–10000)
        numInput.addEventListener('input', () => {
            let val = parseInt(numInput.value);
            if (isNaN(val) || val < 0) { val = 0; numInput.value = 0; }
            if (val > 10000)           { val = 10000; numInput.value = 10000; }
            slider.value = val;
        });
    }

    // Botón CONFIRMAR → calcular volumen
    const btnConfirmar = document.getElementById('btn-confirmar');
    const confirmMsg   = document.getElementById('confirm-msg');

    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', async () => {
            const cantidad = parseInt(numInput.value);
            btnConfirmar.textContent = 'Calculando...';
            try {
                const res  = await fetch('/api/volumen', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cantidad })
                });
                const data = await res.json();

                // Llenar Panel 4 — Resultados
                document.getElementById('panel-resultados').style.opacity = '1';
                document.getElementById('msg-run-volumen').style.display = 'none';
                document.getElementById('r-vol1').innerText = data.volumen_fresa + ' u³';
                document.getElementById('r-volt').innerText = data.volumen_total + ' u³';
                document.getElementById('r-dim').innerText  =
                    `${data.caja_dimensiones.largo} × ${data.caja_dimensiones.ancho} × ${data.caja_dimensiones.alto} u`;
                document.getElementById('r-area').innerText = data.area_optimizada + ' u²';

                // Feedback visual
                btnConfirmar.textContent = '✓ Confirmado';
                btnConfirmar.classList.add('confirmed');
                confirmMsg.textContent = `Cantidad confirmada: ${cantidad} fresas. Revisa los resultados abajo.`;
            } catch (err) {
                console.error(err);
                btnConfirmar.textContent = 'Error — Reintentar';
            }
        });
    }

    /* =========================================================
       3. PANEL DE SIMULACIÓN
       ========================================================= */

    /** Muestra solo un resultado a la vez en la columna derecha */
    function showOnlyResult(targetId) {
        document.querySelectorAll('#sim-output-area .sim-result')
            .forEach(r => r.style.display = 'none');

        const target = document.getElementById(targetId);
        if (target) target.style.display = 'block';

        // Marcar botón activo
        document.querySelectorAll('.sim-btn')
            .forEach(b => b.classList.remove('active-btn'));
        const active = document.querySelector(`.sim-btn[data-target="${targetId}"]`);
        if (active) active.classList.add('active-btn');
    }

    // 1. Graficar función 2D
    const btnGraficar = document.getElementById('btn-graficar');
    if (btnGraficar) {
        btnGraficar.addEventListener('click', async () => {
            showOnlyResult('res-graficar');
            document.getElementById('img-graficar').src = '';
            try {
                const res  = await fetch('/api/graficar', { method: 'POST' });
                const data = await res.json();
                document.getElementById('img-graficar').src =
                    `data:image/png;base64,${data.grafica_2d}`;
            } catch (err) { console.error(err); }
        });
    }

    // 2. Sólido de revolución 3D (renderizado por Three.js en scene3d.js)
    const btnSolido = document.getElementById('btn-solido');
    if (btnSolido) {
        btnSolido.addEventListener('click', () => {
            showOnlyResult('res-solido');
            // La escena 3D se inicializa desde scene3d.js
        });
    }

    // 3. Integral analítica (SymPy)
    const btnIntegral = document.getElementById('btn-integral');
    if (btnIntegral) {
        btnIntegral.addEventListener('click', async () => {
            showOnlyResult('res-integral');
            document.getElementById('math-exp').innerText = 'Calculando...';
            try {
                const res  = await fetch('/api/integral', { method: 'POST' });
                const data = await res.json();

                document.getElementById('math-exp').innerText   = `$$${data.funcion_cuadrado}$$`;
                document.getElementById('math-indef').innerText = `$$${data.integral_indefinida}$$`;
                document.getElementById('math-res').innerText   =
                    `$$${data.resultado_exacto} \\approx ${data.resultado_decimal}$$`;

                // Re-renderizar MathJax
                if (window.MathJax) {
                    MathJax.typesetPromise([document.getElementById('res-integral')]);
                }
            } catch (err) { console.error(err); }
        });
    }
});
