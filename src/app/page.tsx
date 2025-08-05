import Header from "@/components/Header";
import CharacterBuilder from "@/components/CharacterBuilder";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <Header />
      <CharacterBuilder />
    </main>
  );
}
