export default function Footer() {
  return (
    <footer className="bg-background border-t border-border py-8 px-6 text-sm text-gray-400">
      <div className="max-w-7xl mx-auto">
        <div className="mb-4">
          <p className="mb-2">
            Icons made by Lorc, Caduceus, and Delapouite. Available on{" "}
            <a href="http://game-icons.net" className="text-amber-400 hover:text-amber-300">
              http://game-icons.net
            </a>
          </p>
          <p className="mb-4">
            Artwork provided by the talented Sandra. Available on{" "}
            <a href="https://www.deviantart.com/sandara" className="text-amber-400 hover:text-amber-300">
              Deviantart
            </a>
          </p>
        </div>

        <div className="flex flex-wrap gap-4 mb-4">
          <a href="#" className="text-amber-400 hover:text-amber-300">
            Support this site on Patreon
          </a>
          <a href="#" className="text-amber-400 hover:text-amber-300">
            Help
          </a>
          <a href="#" className="text-amber-400 hover:text-amber-300">
            Feedback/Bug Reports
          </a>
          <a href="#" className="text-amber-400 hover:text-amber-300">
            Terms of Use
          </a>
          <a href="#" className="text-amber-400 hover:text-amber-300">
            Privacy Policy
          </a>
          <a href="#" className="text-amber-400 hover:text-amber-300">
            Cookie Policy
          </a>
        </div>

        <div className="border-t border-border pt-4">
          <p className="mb-2">
            © 2025{" "}
            <a href="#" className="text-amber-400 hover:text-amber-300">
              www.dungeonmastersvault.com
            </a>
          </p>
          <p className="mb-2">
            This site is based on{" "}
            <a href="#" className="text-amber-400 hover:text-amber-300">
              the 5e SRD-OGL 5.1
            </a>{" "}
            - Wizards of the Coast, Dungeons & Dragons, D&D, and their logos are trademarks of Wizards of the Coast LLC in the United States and other countries. © 2025 Wizards. All Rights Reserved.
          </p>
          <p className="mb-2">
            DungeonMastersVault.com is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC.
          </p>
          <p className="text-xs">
            Version v2.5.0.26 (01-14-2025) Mihel the Dragonslayer edition
          </p>
          <p className="text-xs mt-2">272829303132333435</p>
        </div>
      </div>
    </footer>
  );
}
