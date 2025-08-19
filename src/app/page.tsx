"use client";

import { useState } from "react";
import Header from "@/components/Header";
import CharacterBuilder from "@/components/CharacterBuilder";
import SpellsLibrary from "@/components/SpellsLibrary";
import MonstersLibrary from "@/components/MonstersLibrary";
import ItemsLibrary from "@/components/ItemsLibrary";
import DungeonGuide from "@/components/DungeonGuide";

export default function Home() {
  const [activeTab, setActiveTab] = useState("characters");

  const renderContent = () => {
    switch (activeTab) {
      case "characters":
        return <CharacterBuilder />;
      case "spells":
        return <SpellsLibrary />;
      case "monsters":
        return <MonstersLibrary />;
      case "items":
        return <ItemsLibrary />;
      case "dungeon-guide":
        return <DungeonGuide />;
      case "encounters":
        return <div className="p-8 text-white text-center">Encounters content coming soon...</div>;
      case "generators":
        return <div className="p-8 text-white text-center">Generators content coming soon...</div>;
      case "my-content":
        return <div className="p-8 text-white text-center">Explore Cosmology coming soon...</div>;
      default:
        return <CharacterBuilder />;
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      {renderContent()}
    </main>
  );
}
