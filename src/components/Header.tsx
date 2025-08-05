import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Search } from "lucide-react";

export default function Header() {
  return (
    <div className="fantasy-header min-h-[300px] relative">
      {/* Top Bar */}
      <div className="flex justify-between items-center p-4 relative z-10">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <img
            src="https://ext.same-assets.com/804965517/997730296.svg"
            alt="Dungeon Master's Vault"
            className="w-12 h-12"
          />
          <div>
            <div className="text-2xl font-bold text-white">DUNGEON</div>
            <div className="text-lg text-amber-400">MASTER'S VAULT</div>
          </div>
        </div>

        {/* Search and Login */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              type="text"
              placeholder="search"
              className="pl-10 bg-black/30 border-gray-600 text-white placeholder:text-gray-400 w-64"
            />
          </div>
          <Button variant="outline" className="text-white border-white hover:bg-white/10">
            LOGIN
          </Button>
        </div>
      </div>

      {/* Patron Banner */}
      <div className="absolute top-16 left-4 z-10">
        <Button className="bg-red-600 hover:bg-red-700 text-white text-sm px-3 py-1">
          BECOME A PATRON
        </Button>
      </div>

      {/* Social Icons */}
      <div className="absolute top-20 left-4 flex gap-2 mt-12 z-10">
        <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center text-white text-xs">f</div>
        <div className="w-8 h-8 bg-blue-400 rounded flex items-center justify-center text-white text-xs">t</div>
        <div className="w-8 h-8 bg-indigo-600 rounded flex items-center justify-center text-white text-xs">d</div>
      </div>

      {/* Navigation Bar */}
      <div className="absolute bottom-0 left-0 right-0 bg-black/40 backdrop-blur-sm z-10">
        <div className="flex justify-center">
          <div className="flex">
            {/* Characters */}
            <div className="flex flex-col items-center p-4 bg-amber-600 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/2515025706.svg" className="nav-icon" alt="Characters" />
              <span className="text-xs font-semibold">CHARACTERS</span>
            </div>

            {/* Spells */}
            <div className="flex flex-col items-center p-4 hover:bg-white/10 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/886694642.svg" className="nav-icon" alt="Spells" />
              <span className="text-xs font-semibold">SPELLS</span>
            </div>

            {/* Monsters */}
            <div className="flex flex-col items-center p-4 hover:bg-white/10 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/4083733308.svg" className="nav-icon" alt="Monsters" />
              <span className="text-xs font-semibold">MONSTERS</span>
            </div>

            {/* Items */}
            <div className="flex flex-col items-center p-4 hover:bg-white/10 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/3602014741.svg" className="nav-icon" alt="Items" />
              <span className="text-xs font-semibold">ITEMS</span>
            </div>

            {/* Encounters */}
            <div className="flex flex-col items-center p-4 hover:bg-white/10 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/1180557428.svg" className="nav-icon" alt="Encounters" />
              <span className="text-xs font-semibold">ENCOUNTERS</span>
            </div>

            {/* Generators */}
            <div className="flex flex-col items-center p-4 hover:bg-white/10 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/1737277130.svg" className="nav-icon" alt="Generators" />
              <span className="text-xs font-semibold">GENERATORS</span>
            </div>

            {/* My Content */}
            <div className="flex flex-col items-center p-4 hover:bg-white/10 text-white cursor-pointer">
              <img src="https://ext.same-assets.com/804965517/4077409613.svg" className="nav-icon" alt="My Content" />
              <span className="text-xs font-semibold">MY CONTENT</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
