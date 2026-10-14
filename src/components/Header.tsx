"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Search,
  Users,
  Sparkles,
  Skull,
  Package,
  Castle,
  Map,
  Dices,
  Orbit,
  Swords,
  CircleHelp,
} from "lucide-react";

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const NAV = [
  { id: "characters", label: "CHARACTERS", keywords: "character chargen build sheet race class", Icon: Users },
  { id: "spells", label: "SPELLS", keywords: "spell magic weave arcane", Icon: Sparkles },
  { id: "monsters", label: "MONSTERS", keywords: "monster bestiary creature umbrin", Icon: Skull },
  { id: "items", label: "ITEMS", keywords: "item loot craft recipe gear", Icon: Package },
  { id: "dungeon-guide", label: "DUNGEON GUIDE", keywords: "dungeon tier cycle shardspire gate boss", Icon: Castle },
  { id: "encounters", label: "ENCOUNTERS", keywords: "encounter tier floor haven poi", Icon: Map },
  { id: "session", label: "SESSION", keywords: "session combat initiative resonance rest", Icon: Swords },
  { id: "generators", label: "GENERATORS", keywords: "generator random name people spark", Icon: Dices },
  { id: "my-content", label: "COSMOLOGY", keywords: "cosmology lore world aethel umbra umbrin", Icon: Orbit },
];

export default function Header({ activeTab, setActiveTab }: HeaderProps) {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
      const target = e.target as HTMLElement;
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable) return;
      e.preventDefault();
      searchRef.current?.focus();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const trimmed = query.trim().toLowerCase();

  const matches = useMemo(() => {
    if (!trimmed) return [];
    return NAV.filter(
      (tab) =>
        tab.label.toLowerCase().includes(trimmed) ||
        tab.id.replace(/-/g, " ").includes(trimmed) ||
        tab.keywords.includes(trimmed)
    );
  }, [trimmed]);

  const openTab = (tabId: string) => {
    setActiveTab(tabId);
    setQuery("");
    setFocused(false);
  };

  const handleSubmit = () => {
    if (matches.length > 0) {
      openTab(matches[0].id);
      return;
    }
    if (trimmed) {
      openTab("characters");
    }
  };

  const showDropdown = focused && trimmed.length > 0;

  return (
    <div className="fantasy-header min-h-[200px] md:min-h-[260px] relative">
      <div className="flex justify-between items-center p-4 relative z-10">
        <div>
          <div className="text-2xl font-bold text-white">DECENNIUM&apos;S</div>
          <div className="text-lg text-amber-400">DESCENT</div>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-amber-400/60 w-4 h-4" />
            <Input
              ref={searchRef}
              type="search"
              placeholder="Search tabs… (/ to focus)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => window.setTimeout(() => setFocused(false), 120)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleSubmit();
                }
                if (e.key === "Escape") {
                  setQuery("");
                  setFocused(false);
                  searchRef.current?.blur();
                }
              }}
              aria-label="Search companion tabs"
              className="pl-10 pr-[4.75rem] bg-black/40 border-amber-700/40 text-amber-50 placeholder:text-amber-200/40 w-72"
            />
            <div className="absolute right-8 top-1/2 -translate-y-1/2 group/help">
              <button
                type="button"
                aria-label="Search keyboard shortcuts"
                className="inline-flex items-center justify-center rounded-full text-amber-200/45 hover:text-amber-200/80 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-amber-500/60"
              >
                <CircleHelp className="w-3.5 h-3.5" />
              </button>
              <div
                role="tooltip"
                className="pointer-events-none absolute bottom-full right-0 mb-2 w-44 rounded border border-amber-700/50 bg-black/95 px-2.5 py-2 text-[11px] leading-snug text-amber-100/90 opacity-0 shadow-lg transition-opacity group-hover/help:opacity-100 group-focus-within/help:opacity-100"
              >
                <div className="flex items-center justify-between gap-2">
                  <span>Focus search</span>
                  <kbd className="rounded border border-amber-700/40 bg-black/50 px-1 py-0.5 text-[10px] text-amber-200/60">/</kbd>
                </div>
                <div className="mt-1 flex items-center justify-between gap-2">
                  <span>Clear &amp; blur</span>
                  <kbd className="rounded border border-amber-700/40 bg-black/50 px-1 py-0.5 text-[10px] text-amber-200/60">Esc</kbd>
                </div>
              </div>
            </div>
            <kbd className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 hidden lg:inline-flex items-center rounded border border-amber-700/40 bg-black/50 px-1.5 py-0.5 text-[10px] font-medium text-amber-200/50">
              /
            </kbd>
            {showDropdown && (
              <div className="absolute top-full left-0 right-0 mt-1 rounded-md border border-amber-700/50 bg-black/95 shadow-lg z-50 overflow-hidden">
                {matches.length > 0 ? (
                  matches.map((tab) => (
                    <button
                      key={tab.id}
                      type="button"
                      className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-amber-50 hover:bg-amber-900/40"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={() => openTab(tab.id)}
                    >
                      <tab.Icon className="w-4 h-4 text-amber-400/80 shrink-0" />
                      <span>{tab.label}</span>
                    </button>
                  ))
                ) : (
                  <button
                    type="button"
                    className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-amber-200/70 hover:bg-amber-900/40"
                    onMouseDown={(e) => e.preventDefault()}
                    onClick={() => openTab("characters")}
                  >
                    <Users className="w-4 h-4 text-amber-400/80 shrink-0" />
                    <span>No tab match — open CHARACTERS</span>
                  </button>
                )}
              </div>
            )}
          </div>
          <Button variant="outline" className="text-amber-100 border-amber-700/50 hover:bg-amber-950/50 hidden md:inline-flex">
            Account
          </Button>
        </div>
      </div>

      <div className="absolute top-20 left-4 z-10">
        <div className="text-xs text-amber-200/80 bg-black/40 border border-amber-700/40 rounded px-3 py-1">
          Companion for the table · Aethel
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 bg-black/50 backdrop-blur-sm z-10 overflow-x-auto">
        <div className="flex justify-center min-w-max">
          {NAV.map(({ id, label, Icon }) => (
            <button
              key={id}
              type="button"
              className={`flex flex-col items-center px-3 py-3 text-white min-w-[88px] ${
                activeTab === id ? "bg-amber-600" : "hover:bg-white/10"
              }`}
              onClick={() => setActiveTab(id)}
            >
              <Icon className="w-5 h-5 mb-1 opacity-90" />
              <span className="text-[10px] font-semibold tracking-wide whitespace-nowrap">{label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
