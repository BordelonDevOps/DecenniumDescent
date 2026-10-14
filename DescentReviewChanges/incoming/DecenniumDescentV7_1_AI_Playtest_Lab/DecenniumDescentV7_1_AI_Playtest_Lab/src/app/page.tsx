"use client";

import { useState } from "react";
import Header from "@/components/Header";
import CharacterBuilder from "@/components/CharacterBuilder";
import SpellsLibrary from "@/components/SpellsLibrary";
import MonstersLibrary from "@/components/MonstersLibrary";
import ItemsLibrary from "@/components/ItemsLibrary";
import DungeonGuide from "@/components/DungeonGuide";
import EncountersBrowser from "@/components/EncountersBrowser";
import GeneratorsPanel from "@/components/GeneratorsPanel";
import CosmologyViewer from "@/components/CosmologyViewer";
import SessionTracker from "@/components/SessionTracker";
import ExpeditionTracker from "@/components/ExpeditionTracker";

export default function Home() {
  const [activeTab, setActiveTab] = useState("characters");
  const [sessionHandoffTick, setSessionHandoffTick] = useState(0);

  const goToSession = () => {
    setSessionHandoffTick((n) => n + 1);
    setActiveTab("session");
  };

  const renderContent = () => {
    switch (activeTab) {
      case "characters":
        return <CharacterBuilder onOpenLore={() => setActiveTab("my-content")} />;
      case "spells":
        return <SpellsLibrary onLoadSession={goToSession} />;
      case "monsters":
        return <MonstersLibrary onLoadSession={goToSession} />;
      case "items":
        return <ItemsLibrary onLoadSession={goToSession} />;
      case "dungeon-guide":
        return <DungeonGuide />;
      case "encounters":
        return <EncountersBrowser onLoadSession={goToSession} />;
      case "session":
        return <SessionTracker handoffTick={sessionHandoffTick} />;
      case "expedition":
        return <ExpeditionTracker />;
      case "generators":
        return <GeneratorsPanel onLoadSession={goToSession} />;
      case "my-content":
        return <CosmologyViewer />;
      default:
        return <CharacterBuilder onOpenLore={() => setActiveTab("my-content")} />;
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      {renderContent()}
    </main>
  );
}
