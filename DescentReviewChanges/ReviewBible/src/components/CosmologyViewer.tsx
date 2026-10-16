"use client";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import lore from "@/data/cosmology-lore.json";
import { DirectorCosmologyNotes, PlayerCosmologyNotes } from "./CosmologyReadingNotes";

type PlaneInfo = {
  name: string;
  summary: string;
  color: string;
};

type WorldSection = {
  id: string;
  title: string;
  bullets: string[];
  subsections?: string[];
  draft?: boolean;
  draftNote?: string;
};

type FirstSongSection = {
  id: string;
  title: string;
  body: string;
  draft?: boolean;
  draftNote?: string;
};

const PLANES: PlaneInfo[] = lore.planes as PlaneInfo[];
const WORLD_SECTIONS = (lore.worldSections ?? []) as WorldSection[];
const FIRST_SONG_SECTIONS = (lore.firstSongSections ?? []) as FirstSongSection[];
const DRAFT_EXTRACT_NOTICE =
  "Draft extract — marked sections preserve an overnight extract or presentation batch and remain pending source or author review.";

const GLOSSARY_TERMS = [
  {
    term: "Calan'thir",
    summary:
      "Architect of the Spiral; melodic weaver at the First Seal. In Umbrin exile lore (draft), he and the First Choir banished Umbrin forebears from ordered light.",
  },
  {
    term: "First Choir",
    summary:
      "Divine chorus of the Spiral age — Celestial rites and ordered song. Shunned and exiled the Umbrin in companion draft canon (Obsidian Burn).",
  },
  {
    term: "Umbra",
    summary:
      "Primordial abyssal depth paired with Lumina at creation; source of the Obsidian Thread. Umbrin derive their demonym from Umbra — not the same as Umbrin PCs.",
  },
  {
    term: "Lumina",
    summary:
      "Primordial radiant counterpart to Umbra; ordered light and song. Calan'thir's Spiral calibration aligns with bounded Lumina.",
  },
  {
    term: "Umbrin",
    summary:
      "Obsidian-skinned elves of The Murk — exiled by Calan'thir and the First Choir; Murkish language; perverse Umbra cults vs Choir orthodoxy.",
  },
] as const;

export default function CosmologyViewer() {
  const [showSourceReference, setShowSourceReference] = useState(false);

  if (showSourceReference) {
    return (
      <div>
        <Card className="m-6 bg-slate-900/70 border-amber-600/30">
          <CardHeader>
            <CardTitle className="text-amber-300">Director / source reference</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <DirectorCosmologyNotes />
            <Button variant="outline" onClick={() => setShowSourceReference(false)}>
              Return to player cosmology
            </Button>
          </CardContent>
        </Card>
        <OriginalCosmologyReference />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader>
          <CardTitle className="text-amber-300">Cosmology</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
          <PlayerCosmologyNotes />
          <div className="border-t border-amber-600/30 pt-4 space-y-3">
            <p className="text-sm text-amber-100/70">
              The original cosmology reader contains Director material and story
              revelations. Open it deliberately when you want to consult those sources.
            </p>
            <Button variant="outline" onClick={() => setShowSourceReference(true)}>
              Open Director / source reference
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function OriginalCosmologyReference() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [selected, setSelected] = useState<PlaneInfo>(PLANES[0]);
  const [paused, setPaused] = useState(false);
  const pausedRef = useRef(false);
  const [loreTab, setLoreTab] = useState<"song" | "world">("song");
  const [worldSectionId, setWorldSectionId] = useState(WORLD_SECTIONS[0]?.id ?? "I-VI");
  const [songChapterId, setSongChapterId] = useState(FIRST_SONG_SECTIONS[0]?.id ?? "I");
  const activeWorldSection =
    WORLD_SECTIONS.find((s) => s.id === worldSectionId) ?? WORLD_SECTIONS[0];
  const activeSongSection =
    FIRST_SONG_SECTIONS.find((s) => s.id === songChapterId) ?? FIRST_SONG_SECTIONS[0];

  useEffect(() => {
    pausedRef.current = paused;
  }, [paused]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 2000);
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setClearColor(0x000000, 1);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const controls = {
      dragging: false,
      prev: { x: 0, y: 0 },
      rotation: { x: 0.25, y: 0.4 },
      distance: 110,
    };

    const starGeo = new THREE.BufferGeometry();
    const starVerts: number[] = [];
    for (let i = 0; i < 6000; i++) {
      starVerts.push((Math.random() - 0.5) * 3500, (Math.random() - 0.5) * 3500, (Math.random() - 0.5) * 3500);
    }
    starGeo.setAttribute("position", new THREE.Float32BufferAttribute(starVerts, 3));
    const stars = new THREE.Points(
      starGeo,
      new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, transparent: true, opacity: 0.75 })
    );
    scene.add(stars);

    scene.add(new THREE.AmbientLight(0x404080, 0.45));
    const centerLight = new THREE.PointLight(0x4fc3f7, 2, 220);
    scene.add(centerLight);
    const throneLight = new THREE.PointLight(0xffd700, 1.4, 160);
    throneLight.position.set(0, 50, 0);
    scene.add(throneLight);

    const celestial: THREE.Object3D[] = [];
    const orbitals: { group: THREE.Group; speed: number; angle: number }[] = [];

    const addBody = (cfg: {
      name: string;
      color: number;
      radius: number;
      position?: { x: number; y: number; z: number };
      orbitRadius?: number;
      speed?: number;
      description?: string;
    }) => {
      const mat = new THREE.MeshStandardMaterial({
        color: cfg.color,
        emissive: cfg.color,
        emissiveIntensity: 0.28,
      });
      const body = new THREE.Mesh(new THREE.SphereGeometry(cfg.radius, 28, 28), mat);
      body.userData = { name: cfg.name, description: cfg.description };
      const glow = new THREE.Mesh(
        new THREE.SphereGeometry(cfg.radius * 1.35, 14, 14),
        new THREE.MeshBasicMaterial({ color: cfg.color, transparent: true, opacity: 0.14 })
      );
      const group = new THREE.Group();
      group.add(body);
      group.add(glow);
      celestial.push(body);

      if (cfg.position) {
        group.position.set(cfg.position.x, cfg.position.y, cfg.position.z);
        scene.add(group);
      } else if (cfg.orbitRadius != null) {
        const orbit = new THREE.Group();
        group.position.set(cfg.orbitRadius, 0, 0);
        orbit.add(group);
        scene.add(orbit);
        orbitals.push({ group: orbit, speed: cfg.speed ?? 0.004, angle: Math.random() * Math.PI * 2 });
      }
    };

    addBody({
      name: "Material Plane",
      color: 0x4fc3f7,
      radius: 4,
      position: { x: 0, y: 0, z: 0 },
      description: "The nexus of all existence",
    });
    addBody({ name: "Plane of Fire", color: 0xff6b35, radius: 2.1, orbitRadius: 25, speed: 0.0064 });
    addBody({ name: "Plane of Water", color: 0x29b6f6, radius: 2.1, orbitRadius: 30, speed: 0.0048 });
    addBody({ name: "Plane of Air", color: 0xe1f5fe, radius: 2.1, orbitRadius: 35, speed: 0.0056 });
    addBody({ name: "Plane of Earth", color: 0x8d6e63, radius: 2.1, orbitRadius: 28, speed: 0.004 });
    addBody({
      name: "Throne of Accord",
      color: 0xffffcc,
      radius: 3.3,
      position: { x: 0, y: 25, z: 0 },
      description: "Seat of divine justice",
    });
    addBody({
      name: "Nessus",
      color: 0x4e0000,
      radius: 3,
      position: { x: 0, y: -25, z: 0 },
      description: "Deepest hell",
    });

    const rings = [
      { radius: 25, color: 0xff6600 },
      { radius: 30, color: 0x3399ff },
      { radius: 35, color: 0xffffff },
      { radius: 28, color: 0x8b4513 },
      { radius: 45, color: 0xffd700 },
    ];
    for (const ring of rings) {
      const mesh = new THREE.Mesh(
        new THREE.RingGeometry(ring.radius - 0.4, ring.radius + 0.4, 64),
        new THREE.MeshBasicMaterial({
          color: ring.color,
          transparent: true,
          opacity: 0.06,
          side: THREE.DoubleSide,
        })
      );
      mesh.rotation.x = Math.PI / 2;
      scene.add(mesh);
    }

    const resize = () => {
      const parent = canvas.parentElement;
      const w = parent?.clientWidth || 800;
      const h = Math.max(420, parent?.clientHeight || 520);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h, false);
    };
    resize();

    const onDown = (e: PointerEvent) => {
      controls.dragging = true;
      controls.prev = { x: e.clientX, y: e.clientY };
    };
    const onUp = () => {
      controls.dragging = false;
    };
    const onMove = (e: PointerEvent) => {
      if (!controls.dragging) return;
      controls.rotation.y -= (e.clientX - controls.prev.x) * 0.005;
      controls.rotation.x -= (e.clientY - controls.prev.y) * 0.005;
      controls.rotation.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, controls.rotation.x));
      controls.prev = { x: e.clientX, y: e.clientY };
    };
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      controls.distance = Math.max(40, Math.min(280, controls.distance + e.deltaY * 0.08));
    };
    const onClick = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);
      const hits = raycaster.intersectObjects(celestial, false);
      if (hits[0]) {
        const name = String(hits[0].object.userData.name || "");
        const plane = PLANES.find((p) => p.name === name);
        if (plane) setSelected(plane);
      }
    };

    canvas.addEventListener("pointerdown", onDown);
    window.addEventListener("pointerup", onUp);
    window.addEventListener("pointermove", onMove);
    canvas.addEventListener("wheel", onWheel, { passive: false });
    canvas.addEventListener("click", onClick);
    window.addEventListener("resize", resize);

    let raf = 0;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      if (!pausedRef.current) {
        for (const orb of orbitals) {
          orb.angle += orb.speed;
          orb.group.rotation.y = orb.angle;
        }
        stars.rotation.y += 0.00015;
      }
      camera.position.x =
        controls.distance * Math.sin(controls.rotation.y) * Math.cos(controls.rotation.x);
      camera.position.y = controls.distance * Math.sin(controls.rotation.x);
      camera.position.z =
        controls.distance * Math.cos(controls.rotation.y) * Math.cos(controls.rotation.x);
      camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(raf);
      canvas.removeEventListener("pointerdown", onDown);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointermove", onMove);
      canvas.removeEventListener("wheel", onWheel);
      canvas.removeEventListener("click", onClick);
      window.removeEventListener("resize", resize);
      renderer.dispose();
      starGeo.dispose();
    };
  }, []);

  return (
    <div className="p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-amber-400">{lore.title}</h1>
        <p className="text-amber-100/70 max-w-3xl mx-auto text-sm">
          Drag to orbit, scroll to zoom, click a sphere to inspect a plane. This is Aethel&apos;s Weave —
          not a shipping 3D client, just enough presence to feel the world.
        </p>
      </div>

      <div className="grid lg:grid-cols-12 gap-4">
        <Card className="lg:col-span-8 bg-black/60 border-amber-600/30 overflow-hidden">
          <CardContent className="p-0 relative min-h-[480px]">
            <canvas ref={canvasRef} className="w-full h-[480px] block cursor-grab active:cursor-grabbing" />
            <div className="absolute top-3 right-3 flex gap-2">
              <Button size="sm" variant="secondary" onClick={() => setPaused((p) => !p)}>
                {paused ? "Resume" : "Pause"}
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="lg:col-span-4 space-y-4">
          <Card className="bg-slate-900/70 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-300 text-lg">{selected.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-amber-50/80 leading-relaxed">{selected.summary}</p>
              <div className="flex flex-wrap gap-2">
                {PLANES.map((p) => (
                  <Badge
                    key={p.name}
                    onClick={() => setSelected(p)}
                    className="cursor-pointer"
                    style={{
                      backgroundColor: selected.name === p.name ? p.color : "transparent",
                      color: selected.name === p.name ? "#111" : p.color,
                      borderColor: p.color,
                    }}
                    variant="outline"
                  >
                    {p.name.replace("Plane of ", "")}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/70 border-amber-600/30">
            <CardHeader className="pb-2">
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant={loreTab === "song" ? "default" : "outline"}
                  onClick={() => setLoreTab("song")}
                >
                  First Song
                </Button>
                <Button
                  size="sm"
                  variant={loreTab === "world" ? "default" : "outline"}
                  onClick={() => setLoreTab("world")}
                >
                  World of Aethel
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {((loreTab === "world" && WORLD_SECTIONS.some((s) => s.draft)) ||
                (loreTab === "song" && FIRST_SONG_SECTIONS.some((s) => s.draft))) && (
                <div className="flex items-start gap-2 rounded border border-amber-600/40 bg-amber-950/20 p-2 text-[10px] leading-snug text-amber-200/80">
                  <Badge
                    variant="outline"
                    className="shrink-0 border-amber-500/50 px-1 py-0 text-[9px] text-amber-300"
                  >
                    Draft extract
                  </Badge>
                  <span>{DRAFT_EXTRACT_NOTICE} Look for † in the section picker.</span>
                </div>
              )}
              {loreTab === "world" && WORLD_SECTIONS.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {WORLD_SECTIONS.map((s) => (
                    <Button
                      key={s.id}
                      size="sm"
                      variant={worldSectionId === s.id ? "default" : "outline"}
                      className="text-[10px] h-7 px-2"
                      onClick={() => setWorldSectionId(s.id)}
                      title={s.title}
                    >
                      {s.id}
                      {s.draft ? " †" : ""}
                    </Button>
                  ))}
                </div>
              )}
              {loreTab === "song" && FIRST_SONG_SECTIONS.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {FIRST_SONG_SECTIONS.map((s) => (
                    <Button
                      key={s.id}
                      size="sm"
                      variant={songChapterId === s.id ? "default" : "outline"}
                      className="text-[10px] h-7 px-2"
                      onClick={() => setSongChapterId(s.id)}
                      title={s.title}
                    >
                      {s.id}
                      {s.draft ? " †" : ""}
                    </Button>
                  ))}
                </div>
              )}
              {loreTab === "song" ? (
                activeSongSection ? (
                  <div className="text-xs text-amber-50/70 leading-relaxed max-h-[280px] overflow-y-auto space-y-2">
                    <p className="text-amber-300 font-medium">{activeSongSection.title}</p>
                    {activeSongSection.draft && (
                      <p className="text-[10px] text-amber-400/90 border border-amber-600/40 rounded p-2 leading-snug">
                        [draft extract]{activeSongSection.draftNote ? ` ${activeSongSection.draftNote}` : ""}
                      </p>
                    )}
                    <p className="whitespace-pre-wrap">{activeSongSection.body}</p>
                  </div>
                ) : (
                  <p className="text-xs text-amber-50/70 leading-relaxed whitespace-pre-wrap max-h-[240px] overflow-y-auto">
                    {lore.firstSong}
                  </p>
                )
              ) : activeWorldSection ? (
                <div className="text-xs text-amber-50/70 leading-relaxed max-h-[280px] overflow-y-auto space-y-2">
                  <p className="text-amber-300 font-medium">{activeWorldSection.title}</p>
                  {activeWorldSection.draft && (
                    <p className="text-[10px] text-amber-400/90 border border-amber-600/40 rounded p-2 leading-snug">
                      {activeWorldSection.id === "XIV"
                        ? "[superseded by Dungeon Guide]"
                        : "[draft extract]"}
                      {activeWorldSection.draftNote ? ` ${activeWorldSection.draftNote}` : ""}
                      {activeWorldSection.id === "XIV" &&
                        " For gate bosses and tier play, use Dungeon Guide / Encounters (`floor-encounters.json`)."}
                    </p>
                  )}
                  <ul className="list-disc pl-4 space-y-1">
                    {activeWorldSection.bullets.map((b) => (
                      <li key={b.slice(0, 40)}>{b}</li>
                    ))}
                  </ul>
                  {activeWorldSection.subsections && activeWorldSection.subsections.length > 0 && (
                    <ul className="list-disc pl-6 space-y-1 text-amber-100/60">
                      {activeWorldSection.subsections.map((b) => (
                        <li key={b.slice(0, 40)}>{b}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ) : (
                <p className="text-xs text-amber-50/70 leading-relaxed whitespace-pre-wrap max-h-[280px] overflow-y-auto">
                  {lore.worldOutline}
                </p>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-900/70 border-amber-600/30">
            <CardHeader className="pb-2">
              <CardTitle className="text-amber-300 text-sm">Key terms</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 max-h-[200px] overflow-y-auto">
              {GLOSSARY_TERMS.map((entry) => (
                <div key={entry.term} className="text-xs border-b border-amber-800/20 pb-2 last:border-0">
                  <span className="text-amber-300 font-medium">{entry.term}</span>
                  <p className="text-amber-50/65 leading-snug mt-0.5">{entry.summary}</p>
                </div>
              ))}
              <p className="text-[10px] text-amber-200/45 pt-1">
                Full glossary: <code className="text-amber-200/60">CONTINUITY_GLOSSARY.md</code>
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
