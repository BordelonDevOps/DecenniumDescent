"use client";

import { useState } from "react";
import Header from "@/components/Header";
import CharacterBuilder from "@/components/CharacterBuilder";
import SpellsLibrary from "@/components/SpellsLibrary";

export default function Home() {
  const [activeTab, setActiveTab] = useState("characters");

  const renderContent = () => {
    switch (activeTab) {
      case "characters":
        return <CharacterBuilder />;
      case "spells":
        return <SpellsLibrary />;
      case "monsters":
        return <div className="p-8 text-white text-center">Monsters content coming soon...</div>;
      case "items":
        return <div className="p-8 text-white text-center">Items content coming soon...</div>;
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
