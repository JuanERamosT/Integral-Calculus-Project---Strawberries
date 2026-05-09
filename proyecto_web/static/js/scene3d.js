/**
 * scene3d.js — Sólido de Revolución Interactivo con Three.js
 *
 * Usa LatheGeometry para rotar el perfil y = -0.3(x-1)³ + 2
 * alrededor del eje X, generando el sólido exacto.
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Modelo matemático: y = -0.3(x-1)³ + 2 para 0 ≤ x ≤ 2.5
function fresaRadius(x) {
    return -0.3 * Math.pow(x - 1, 3) + 2;
}

let scene, camera, renderer, controls, animationId;

/** Crea la escena 3D dentro del contenedor dado */
function initScene(container) {
    // Limpiar si ya existía
    if (renderer) {
        cancelAnimationFrame(animationId);
        renderer.dispose();
        container.innerHTML = '';
    }

    const width  = container.clientWidth;
    const height = container.clientHeight;

    // ─── Escena ───
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0a);

    // ─── Cámara ───
    camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.set(4, 3, 5);
    camera.lookAt(1.25, 0, 0);

    // ─── Renderer ───
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // ─── Controles (arrastrar para rotar, scroll para zoom) ───
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.target.set(1.25, 0, 0);
    controls.minDistance = 2;
    controls.maxDistance = 15;
    controls.update();

    // ─── Generar perfil 2D ───
    // LatheGeometry rota puntos alrededor del eje Y.
    // Nuestro modelo tiene x como longitud y y como radio.
    // Mapeamos: Three.Y ← nuestro x,  Three.X ← nuestro y(x)
    const segments = 200;
    const profilePoints = [];

    // Punta inferior (cerrar la forma)
    profilePoints.push(new THREE.Vector2(0, 0));

    for (let i = 0; i <= segments; i++) {
        const x = (i / segments) * 2.5;
        const y = fresaRadius(x);
        profilePoints.push(new THREE.Vector2(y, x));  // (radio, altura)
    }

    // Punta superior (cerrar la forma)
    profilePoints.push(new THREE.Vector2(0, 2.5));

    // ─── Geometría: Sólido de Revolución ───
    const latheSegments = 64;
    const geometry = new THREE.LatheGeometry(profilePoints, latheSegments);

    // Rotar para que el eje de revolución sea horizontal (eje X)
    geometry.rotateZ(-Math.PI / 2);

    // ─── Material con gradiente tipo fresa ───
    const material = new THREE.MeshPhysicalMaterial({
        color: 0xff1493,           // Rosa fuerte
        metalness: 0.1,
        roughness: 0.4,
        clearcoat: 0.3,
        clearcoatRoughness: 0.2,
        side: THREE.DoubleSide,
    });

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // ─── Wireframe superpuesto (para ver la estructura) ───
    const wireMaterial = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        wireframe: true,
        transparent: true,
        opacity: 0.08,
    });
    const wireMesh = new THREE.Mesh(geometry.clone(), wireMaterial);
    scene.add(wireMesh);

    // ─── Eje de revolución (línea punteada) ───
    const axisPoints = [
        new THREE.Vector3(-0.5, 0, 0),
        new THREE.Vector3(3.0, 0, 0),
    ];
    const axisGeom = new THREE.BufferGeometry().setFromPoints(axisPoints);
    const axisMat  = new THREE.LineBasicMaterial({ color: 0xff3333, linewidth: 2 });
    const axisLine = new THREE.Line(axisGeom, axisMat);
    scene.add(axisLine);

    // ─── Luces ───
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    const pointLight = new THREE.PointLight(0x9945ff, 0.6, 20);
    pointLight.position.set(-3, 2, 3);
    scene.add(pointLight);

    const cyanLight = new THREE.PointLight(0x00ffff, 0.4, 20);
    cyanLight.position.set(3, -2, -3);
    scene.add(cyanLight);

    // ─── Cuadrícula de referencia ───
    const gridHelper = new THREE.GridHelper(6, 12, 0x333333, 0x222222);
    gridHelper.position.y = -2.5;
    scene.add(gridHelper);

    // ─── Redimensionar ───
    const resizeObserver = new ResizeObserver(() => {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    });
    resizeObserver.observe(container);

    // ─── Loop de animación ───
    function animate() {
        animationId = requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
}

// ─── Escuchar el botón "Modelar Sólido (3D)" ───
const btnSolido = document.getElementById('btn-solido');
if (btnSolido) {
    btnSolido.addEventListener('click', () => {
        // Esperar un frame para que el contenedor sea visible
        requestAnimationFrame(() => {
            const container = document.getElementById('threejs-container');
            if (container) {
                initScene(container);
            }
        });
    });
}
