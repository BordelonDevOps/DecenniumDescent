'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Button } from './ui/button';
import { 
  Castle, 
  Shield, 
  Sword, 
  Users, 
  ArrowUp, 
  ArrowDown, 
  RotateCcw, 
  AlertTriangle,
  Crown,
  Coins,
  Hammer,
  Heart,
  MapPin
} from 'lucide-react';

interface SafeHaven {
  id: string;
  name: string;
  tier: number;
  floor: number;
  services: string[];
  description: string;
  rarity: 'Common' | 'Rare' | 'Legendary';
  tradingDifficulty: 'Easy' | 'Moderate' | 'Hard' | 'Extreme';
}

interface DungeonTier {
  tier: number;
  floors: string;
  gateWarden: string;
  difficulty: string;
  safeHavens: SafeHaven[];
  description: string;
}

const DungeonGuide: React.FC = () => {
  const [selectedTier, setSelectedTier] = useState<number>(1);
  const [activeTab, setActiveTab] = useState<'overview' | 'tiers' | 'mechanics'>('overview');

  const dungeonTiers: DungeonTier[] = [
    {
      tier: 1,
      floors: '1-10',
      gateWarden: 'The Iron Sentinel',
      difficulty: 'Novice',
      description: 'The upper reaches where most adventurers begin their descent.',
      safeHavens: [
        {
          id: 'haven_1_5',
          name: 'Emberfall Outpost',
          tier: 1,
          floor: 5,
          services: ['Rest', 'Basic Trading', 'Party Management', 'Resurrection'],
          description: 'A well-established settlement with full amenities.',
          rarity: 'Common',
          tradingDifficulty: 'Easy'
        },
        {
          id: 'haven_1_8',
          name: 'Wayward Inn',
          tier: 1,
          floor: 8,
          services: ['Rest', 'Trading', 'Crafting Supplies'],
          description: 'A cozy inn run by retired adventurers.',
          rarity: 'Common',
          tradingDifficulty: 'Easy'
        }
      ]
    },
    {
      tier: 2,
      floors: '11-20',
      gateWarden: 'Voidclaw Behemoth',
      difficulty: 'Apprentice',
      description: 'Deeper chambers where the dungeon\'s true nature begins to show.',
      safeHavens: [
        {
          id: 'haven_2_15',
          name: 'Crystalwatch Sanctuary',
          tier: 2,
          floor: 15,
          services: ['Rest', 'Advanced Trading', 'Enchanting', 'Party Management'],
          description: 'A sanctuary built around natural crystal formations.',
          rarity: 'Common',
          tradingDifficulty: 'Moderate'
        }
      ]
    },
    {
      tier: 3,
      floors: '21-30',
      gateWarden: 'Shadowmere the Eternal',
      difficulty: 'Journeyman',
      description: 'The depths where reality begins to warp and shift.',
      safeHavens: [
        {
          id: 'haven_3_25',
          name: 'The Gilded Refuge',
          tier: 3,
          floor: 25,
          services: ['Rest', 'Rare Trading', 'Master Crafting', 'Resurrection'],
          description: 'An opulent haven maintained by wealthy merchant guilds.',
          rarity: 'Rare',
          tradingDifficulty: 'Hard'
        },
        {
          id: 'haven_3_28',
          name: 'Whisperwind Camp',
          tier: 3,
          floor: 28,
          services: ['Rest', 'Information Trading'],
          description: 'A small camp where knowledge is the primary currency.',
          rarity: 'Rare',
          tradingDifficulty: 'Hard'
        }
      ]
    },
    {
      tier: 4,
      floors: '31-40',
      gateWarden: 'Archon Maleficus',
      difficulty: 'Expert',
      description: 'The abyss where few dare to tread and fewer return.',
      safeHavens: [
        {
          id: 'haven_4_35',
          name: 'The Last Light',
          tier: 4,
          floor: 35,
          services: ['Rest', 'Legendary Trading', 'Soul Binding'],
          description: 'A beacon of hope in the crushing darkness below.',
          rarity: 'Legendary',
          tradingDifficulty: 'Extreme'
        }
      ]
    },
    {
      tier: 5,
      floors: '41-50',
      gateWarden: 'The Void Incarnate',
      difficulty: 'Master',
      description: 'The deepest known levels where reality itself breaks down.',
      safeHavens: [
        {
          id: 'haven_5_45',
          name: 'Terminus Station',
          tier: 5,
          floor: 45,
          services: ['Rest', 'Artifact Trading', 'Planar Crafting'],
          description: 'The final outpost before the ultimate depths.',
          rarity: 'Legendary',
          tradingDifficulty: 'Extreme'
        }
      ]
    }
  ];

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'Common': return 'bg-gray-500';
      case 'Rare': return 'bg-blue-500';
      case 'Legendary': return 'bg-purple-500';
      default: return 'bg-gray-500';
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'text-green-400';
      case 'Moderate': return 'text-yellow-400';
      case 'Hard': return 'text-orange-400';
      case 'Extreme': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-amber-400">Dungeon Guide</h2>
        <p className="text-amber-200/80 max-w-2xl mx-auto">
          Knowledge passed down through generations of adventurers. The Dungeon shifts every decade, 
          but these truths remain constant.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={(value: string) => setActiveTab(value as 'overview' | 'tiers' | 'mechanics')}>
        <TabsList className="grid w-full grid-cols-3 bg-amber-600/20 border border-amber-600/30">
          <TabsTrigger value="overview" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <MapPin className="w-4 h-4 mr-2" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="tiers" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <Castle className="w-4 h-4 mr-2" />
            Tier Details
          </TabsTrigger>
          <TabsTrigger value="mechanics" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <Shield className="w-4 h-4 mr-2" />
            Mechanics
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400 flex items-center gap-2">
                <Castle className="w-5 h-5" />
                The Eternal Dungeon
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-amber-300">Core Principles</h3>
                  <ul className="space-y-2 text-amber-100/80">
                    <li className="flex items-start gap-2">
                      <RotateCcw className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Dungeon reshapes every 10 years</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ArrowDown className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Descent is permanent past Gate Wardens</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ArrowUp className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Free movement within conquered tiers</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <AlertTriangle className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Evacuation resets progress to Tier 1</span>
                    </li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-amber-300">Safe Haven System</h3>
                  <ul className="space-y-2 text-amber-100/80">
                    <li className="flex items-start gap-2">
                      <Users className="w-4 h-4 mt-1 text-amber-400" />
                      <span>1-2 havens per tier (10 floors)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <Coins className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Trading difficulty increases with depth</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <Hammer className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Crafting and resupply opportunities</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <Heart className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Resurrection services (when available)</span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-5 gap-4">
            {dungeonTiers.map((tier) => (
              <Card 
                key={tier.tier} 
                className={`bg-slate-800/50 border-amber-600/30 cursor-pointer transition-all hover:border-amber-400/50 ${
                  selectedTier === tier.tier ? 'ring-2 ring-amber-400/50' : ''
                }`}
                onClick={() => setSelectedTier(tier.tier)}
              >
                <CardHeader className="pb-2">
                  <CardTitle className="text-amber-400 text-center">
                    Tier {tier.tier}
                  </CardTitle>
                  <p className="text-xs text-amber-200/60 text-center">
                    Floors {tier.floors}
                  </p>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="text-center space-y-2">
                    <Badge className={`${getRarityColor('Common')} text-white text-xs`}>
                      {tier.difficulty}
                    </Badge>
                    <p className="text-xs text-amber-100/70">
                      {tier.safeHavens.length} Safe Haven{tier.safeHavens.length !== 1 ? 's' : ''}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="tiers" className="space-y-4">
          {dungeonTiers.find(t => t.tier === selectedTier) && (
            <Card className="bg-slate-800/50 border-amber-600/30">
              <CardHeader>
                <CardTitle className="text-amber-400 flex items-center gap-2">
                  <Crown className="w-5 h-5" />
                  Tier {selectedTier} - Floors {dungeonTiers.find(t => t.tier === selectedTier)?.floors}
                </CardTitle>
                <p className="text-amber-200/80">
                  {dungeonTiers.find(t => t.tier === selectedTier)?.description}
                </p>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-4 p-3 bg-slate-700/50 rounded-lg">
                  <Sword className="w-5 h-5 text-red-400" />
                  <div>
                    <p className="font-semibold text-amber-300">Gate Warden</p>
                    <p className="text-amber-100/80">{dungeonTiers.find(t => t.tier === selectedTier)?.gateWarden}</p>
                  </div>
                </div>

                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-amber-300">Safe Havens</h3>
                  <div className="grid gap-4">
                    {dungeonTiers.find(t => t.tier === selectedTier)?.safeHavens.map((haven) => (
                      <Card key={haven.id} className="bg-slate-700/50 border-amber-600/20">
                        <CardHeader className="pb-2">
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-amber-300 text-lg">{haven.name}</CardTitle>
                            <div className="flex gap-2">
                              <Badge className={`${getRarityColor(haven.rarity)} text-white text-xs`}>
                                {haven.rarity}
                              </Badge>
                              <Badge className={`bg-slate-600 text-xs ${getDifficultyColor(haven.tradingDifficulty)}`}>
                                {haven.tradingDifficulty} Trading
                              </Badge>
                            </div>
                          </div>
                          <p className="text-sm text-amber-200/60">Floor {haven.floor}</p>
                        </CardHeader>
                        <CardContent>
                          <p className="text-amber-100/80 mb-3">{haven.description}</p>
                          <div className="flex flex-wrap gap-2">
                            {haven.services.map((service, index) => (
                              <Badge key={index} className="bg-amber-600/20 text-amber-300 text-xs">
                                {service}
                              </Badge>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="mechanics" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="bg-slate-800/50 border-amber-600/30">
              <CardHeader>
                <CardTitle className="text-amber-400 flex items-center gap-2">
                  <ArrowDown className="w-5 h-5" />
                  Progression Rules
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <h4 className="font-semibold text-amber-300">Gate Warden System</h4>
                  <p className="text-amber-100/80 text-sm">
                    Each tier is guarded by a powerful Gate Warden. Defeating them grants permanent access to the next tier.
                  </p>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold text-amber-300">One-Way Descent</h4>
                  <p className="text-amber-100/80 text-sm">
                    Once you progress past a Gate Warden, you cannot ascend beyond your highest conquered tier without evacuation.
                  </p>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold text-amber-300">Free Movement</h4>
                  <p className="text-amber-100/80 text-sm">
                    Within conquered tiers, adventurers can move freely between floors and safe havens.
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 border-amber-600/30">
              <CardHeader>
                <CardTitle className="text-amber-400 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5" />
                  Emergency Systems
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <h4 className="font-semibold text-amber-300">Evacuation Protocols</h4>
                  <p className="text-amber-100/80 text-sm">
                    Emergency teleportation returns you to Tier 1's safe haven, but all Gate Warden progress is reset.
                  </p>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold text-amber-300">Decennial Reset</h4>
                  <p className="text-amber-100/80 text-sm">
                    Every 10 years, the Dungeon reshapes completely. Only the safe havens in Tiers 1-5 remain constant.
                  </p>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold text-amber-300">Knowledge Preservation</h4>
                  <p className="text-amber-100/80 text-sm">
                    Information about safe havens, trading routes, and survival strategies is passed down between generations.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400 flex items-center gap-2">
                <Coins className="w-5 h-5" />
                Trading & Economy
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-4 gap-4">
                <div className="text-center space-y-2">
                  <div className="text-green-400 font-semibold">Easy Trading</div>
                  <p className="text-xs text-amber-100/70">Tiers 1-2</p>
                  <p className="text-xs text-amber-100/60">Standard prices, full services</p>
                </div>
                <div className="text-center space-y-2">
                  <div className="text-yellow-400 font-semibold">Moderate Trading</div>
                  <p className="text-xs text-amber-100/70">Tier 2-3</p>
                  <p className="text-xs text-amber-100/60">Higher prices, limited stock</p>
                </div>
                <div className="text-center space-y-2">
                  <div className="text-orange-400 font-semibold">Hard Trading</div>
                  <p className="text-xs text-amber-100/70">Tier 3-4</p>
                  <p className="text-xs text-amber-100/60">Premium prices, rare items</p>
                </div>
                <div className="text-center space-y-2">
                  <div className="text-red-400 font-semibold">Extreme Trading</div>
                  <p className="text-xs text-amber-100/70">Tier 4-5</p>
                  <p className="text-xs text-amber-100/60">Barter only, legendary items</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DungeonGuide;