// Cosmology Viewer for Decennium Descent
class CosmologyViewer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = {
            isDragging: false,
            previousMouse: { x: 0, y: 0 },
            rotation: { x: 0.2, y: 0 },
            distance: 120
        };
        this.celestialObjects = [];
        this.orbitalGroups = [];
        this.animationPaused = false;
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.init();
    }

    init() {
        this.setupScene();
        this.setupLighting();
        this.createCosmology();
        this.setupInteractions();
        this.animate();
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.canvas.clientWidth / this.canvas.clientHeight, 0.1, 2000);
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.setClearColor(0x000000, 1);
        this.createStarfield();
        this.createOrbitRings();
    }

    createStarfield() {
        const starGeometry = new THREE.BufferGeometry();
        const starVertices = [];
        for (let i = 0; i < 10000; i++) {
            const x = (Math.random() - 0.5) * 4000;
            const y = (Math.random() - 0.5) * 4000;
            const z = (Math.random() - 0.5) * 4000;
            starVertices.push(x, y, z);
        }
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
        const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2, transparent: true, opacity: 0.8 });
        this.stars = new THREE.Points(starGeometry, starMaterial);
        this.scene.add(this.stars);
    }

    createOrbitRings() {
        const rings = [
            { radius: 25, color: 0xff6600, opacity: 0.05 },
            { radius: 30, color: 0x3399ff, opacity: 0.05 },
            { radius: 35, color: 0xffffff, opacity: 0.03 },
            { radius: 28, color: 0x8b4513, opacity: 0.05 },
            { radius: 45, color: 0xffd700, opacity: 0.08 },
            { radius: 55, color: 0xffd700, opacity: 0.06 },
            { radius: 60, color: 0xcc66ff, opacity: 0.04 },
            { radius: 65, color: 0xcc66ff, opacity: 0.04 }
        ];
        rings.forEach(ring => {
            const ringGeometry = new THREE.RingGeometry(ring.radius - 0.5, ring.radius + 0.5, 64);
            const ringMaterial = new THREE.MeshBasicMaterial({ color: ring.color, transparent: true, opacity: ring.opacity, side: THREE.DoubleSide });
            const ringMesh = new THREE.Mesh(ringGeometry, ringMaterial);
            ringMesh.rotation.x = Math.PI / 2;
            this.scene.add(ringMesh);
        });
    }

    setupLighting() {
        const ambientLight = new THREE.AmbientLight(0x404080, 0.4);
        this.scene.add(ambientLight);
        const centralLight = new THREE.PointLight(0x4fc3f7, 2, 200);
        centralLight.position.set(0, 0, 0);
        this.scene.add(centralLight);
        const celestialLight = new THREE.PointLight(0xffd700, 1.5, 150);
        celestialLight.position.set(0, 50, 0);
        this.scene.add(celestialLight);
    }

    createCosmology() {
        // Material Plane
        this.createPlanarBody({ name: "Material Plane", color: 0x4fc3f7, radius: 4.0, position: { x: 0, y: 0, z: 0 }, description: "The nexus of all existence" });
        
        // Elemental Ring
        const elementals = [
            { name: "Plane of Fire", color: 0xff6b35, radius: 2.2, orbitRadius: 25, speed: 0.0064 },
            { name: "Plane of Water", color: 0x29b6f6, radius: 2.2, orbitRadius: 30, speed: 0.0048 },
            { name: "Plane of Air", color: 0xe1f5fe, radius: 2.2, orbitRadius: 35, speed: 0.0056 },
            { name: "Plane of Earth", color: 0x8d6e63, radius: 2.2, orbitRadius: 28, speed: 0.004 }
        ];
        elementals.forEach(realm => this.createPlanarBody(realm));
        
        // Throne and Nessus
        this.createPlanarBody({ name: "Throne of Accord", color: 0xffffcc, radius: 3.5, position: { x: 0, y: 25, z: 0 }, description: "Seat of divine justice" });
        this.createPlanarBody({ name: "Nessus", color: 0x4e0000, radius: 3.2, position: { x: 0, y: -25, z: 0 }, description: "Deepest hell" });
    }

    createPlanarBody(config) {
        const geometry = new THREE.SphereGeometry(config.radius, 32, 32);
        const material = new THREE.MeshStandardMaterial({ color: config.color, emissive: config.color, emissiveIntensity: 0.3 });
        const body = new THREE.Mesh(geometry, material);
        body.userData = { name: config.name, description: config.description };
        
        const glowGeometry = new THREE.SphereGeometry(config.radius * 1.4, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({ color: config.color, transparent: true, opacity: 0.15 });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        
        const group = new THREE.Group();
        group.add(body);
        group.add(glow);
        this.celestialObjects.push(body);

        if (config.position) {
            group.position.set(config.position.x, config.position.y, config.position.z);
            this.scene.add(group);
        } else if (config.orbitRadius) {
            const orbitGroup = new THREE.Group();
            group.position.set(config.orbitRadius, 0, 0);
            orbitGroup.add(group);
            this.scene.add(orbitGroup);
            this.orbitalGroups.push({ group: orbitGroup, speed: config.speed || 0.001, angle: 0 });
        }
    }

    setupInteractions() {
        this.canvas.addEventListener('mousedown', () => { this.controls.isDragging = true; });
        this.canvas.addEventListener('mouseup', () => { this.controls.isDragging = false; });
        this.canvas.addEventListener('mousemove', (e) => {
            if (this.controls.isDragging) {
                const deltaX = e.clientX - this.controls.previousMouse.x;
                const deltaY = e.clientY - this.controls.previousMouse.y;
                this.controls.rotation.y -= deltaX * 0.005;
                this.controls.rotation.x -= deltaY * 0.005;
                this.controls.rotation.x = Math.max(-Math.PI/3, Math.min(Math.PI/3, this.controls.rotation.x));
            }
            this.controls.previousMouse = { x: e.clientX, y: e.clientY };
        });
        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            this.controls.distance += e.deltaY * 0.1;
            this.controls.distance = Math.max(40, Math.min(300, this.controls.distance));
        });
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (!this.animationPaused) {
            this.orbitalGroups.forEach(orb => {
                orb.angle += orb.speed;
                orb.group.rotation.y = orb.angle;
            });
            if (this.stars) {
                this.stars.rotation.y += 0.0002;
                this.stars.rotation.x += 0.0001;
            }
        }

        this.camera.position.x = this.controls.distance * Math.sin(this.controls.rotation.y) * Math.cos(this.controls.rotation.x);
        this.camera.position.y = this.controls.distance * Math.sin(this.controls.rotation.x);
        this.camera.position.z = this.controls.distance * Math.cos(this.controls.rotation.y) * Math.cos(this.controls.rotation.x);
        this.camera.lookAt(0, 0, 0);

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
    }
}

window.CosmologyViewer = CosmologyViewer;