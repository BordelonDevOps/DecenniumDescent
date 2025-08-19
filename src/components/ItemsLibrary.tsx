'use client';

import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Search, Package, Hammer, Wrench, X, Coins } from 'lucide-react';
import bestiaryData from '../bestiary_data_full.json';
import CraftingBuilder from './CraftingBuilder';

// Types
interface DroppedItem {
  id: string;
  name: string;
  description: string;
  rarity: string;
  category: string;
  tier: number;
  value: number;
  type: 'dropped';
  dropRate: number;
  quantity: string;
  sourceMonsters: string[];
}

interface CraftedItem {
  id: string;
  name: string;
  description: string;
  rarity: string;
  category: string;
  tier: number;
  value: number;
  type: 'crafted';
  craftingSkill: string;
  craftingTime: string;
  components: string[];
}

type Item = DroppedItem | CraftedItem;

// Mock crafted items data
const generateCraftedItems = (): CraftedItem[] => {
  const craftedItems: CraftedItem[] = [
    {
      id: 'crafted_iron_sword',
      name: 'Iron Sword',
      description: 'A sturdy sword forged from iron ore.',
      rarity: 'Common',
      category: 'Weapon',
      tier: 1,
      value: 50,
      type: 'crafted',
      craftingSkill: 'Blacksmithing',
      craftingTime: '2 hours',
      components: ['Iron Ore x3', 'Coal x2', 'Leather Strip x1']
    },
    {
      id: 'crafted_healing_potion',
      name: 'Healing Potion',
      description: 'A magical potion that restores health.',
      rarity: 'Common',
      category: 'Consumable',
      tier: 1,
      value: 25,
      type: 'crafted',
      craftingSkill: 'Alchemy',
      craftingTime: '30 minutes',
      components: ['Healing Herb x2', 'Pure Water x1', 'Glass Vial x1']
    }
  ];
  return craftedItems;
};

// Extract dropped items from bestiary data
const extractDroppedItems = (): DroppedItem[] => {
  const droppedItems: DroppedItem[] = [];
  
  bestiaryData.forEach((monster: any) => {
    if (monster.loot) {
      // Process tier 1 loot
      if (monster.loot.tier1 && monster.loot.tier1.drop !== 'None' && monster.loot.tier1.drop !== 'nan' && monster.loot.tier1.drop !== null && monster.loot.tier1.drop !== undefined) {
        const existingItem = droppedItems.find(item => 
          item.name.toLowerCase() === monster.loot.tier1.drop.toLowerCase()
        );
        
        if (!existingItem) {
          droppedItems.push({
            id: `dropped_${monster.loot.tier1.drop.replace(/\s+/g, '_')}`,
            name: monster.loot.tier1.drop,
            description: `A common drop from various creatures in ${monster.zoneFound}.`,
            rarity: 'Common',
            category: 'Material',
            tier: 1,
            value: (monster.loot.tier1.value && monster.loot.tier1.value !== 'nan') ? parseInt(monster.loot.tier1.value) || 1 : 1,
            type: 'dropped',
            dropRate: (monster.loot.tier1.rate && monster.loot.tier1.rate !== 'nan') ? Math.round(parseFloat(monster.loot.tier1.rate) * 100) : 0,
            quantity: '1-3',
            sourceMonsters: [monster.name]
          });
        } else {
          if (!existingItem.sourceMonsters.includes(monster.name)) {
            existingItem.sourceMonsters.push(monster.name);
          }
        }
      }
      
      // Process tier 2 loot
      if (monster.loot.tier2 && monster.loot.tier2.drop !== 'None' && monster.loot.tier2.drop !== 'nan' && monster.loot.tier2.drop !== null && monster.loot.tier2.drop !== undefined) {
        const existingItem = droppedItems.find(item => 
          item.name.toLowerCase() === monster.loot.tier2.drop.toLowerCase()
        );
        
        if (!existingItem) {
          droppedItems.push({
            id: `dropped_${monster.loot.tier2.drop.replace(/\s+/g, '_')}`,
            name: monster.loot.tier2.drop,
            description: `An uncommon drop from creatures in ${monster.zoneFound}.`,
            rarity: 'Uncommon',
            category: 'Material',
            tier: 2,
            value: (monster.loot.tier2.value && monster.loot.tier2.value !== 'nan') ? parseInt(monster.loot.tier2.value) || 5 : 5,
            type: 'dropped',
            dropRate: (monster.loot.tier2.rate && monster.loot.tier2.rate !== 'nan') ? Math.round(parseFloat(monster.loot.tier2.rate) * 100) : 0,
            quantity: '1-2',
            sourceMonsters: [monster.name]
          });
        } else {
          if (!existingItem.sourceMonsters.includes(monster.name)) {
            existingItem.sourceMonsters.push(monster.name);
          }
        }
      }
      
      // Process tier 3 loot
      if (monster.loot.tier3 && monster.loot.tier3.drop !== 'None' && monster.loot.tier3.drop !== 'nan' && monster.loot.tier3.drop !== null && monster.loot.tier3.drop !== undefined) {
        const existingItem = droppedItems.find(item => 
          item.name.toLowerCase() === monster.loot.tier3.drop.toLowerCase()
        );
        
        if (!existingItem) {
          droppedItems.push({
            id: `dropped_${monster.loot.tier3.drop.replace(/\s+/g, '_')}`,
            name: monster.loot.tier3.drop,
            description: `A rare drop from powerful creatures in ${monster.zoneFound}.`,
            rarity: 'Rare',
            category: 'Material',
            tier: 3,
            value: (monster.loot.tier3.value && monster.loot.tier3.value !== 'nan') ? parseInt(monster.loot.tier3.value) || 15 : 15,
            type: 'dropped',
            dropRate: (monster.loot.tier3.rate && monster.loot.tier3.rate !== 'nan') ? Math.round(parseFloat(monster.loot.tier3.rate) * 100) : 0,
            quantity: '1',
            sourceMonsters: [monster.name]
          });
        } else {
          if (!existingItem.sourceMonsters.includes(monster.name)) {
            existingItem.sourceMonsters.push(monster.name);
          }
        }
      }
    }
  });
  
  return droppedItems;
};

const ItemsLibrary: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dropped' | 'crafted' | 'builder'>('dropped');
  const [searchTerm, setSearchTerm] = useState('');
  const [rarityFilter, setRarityFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [tierFilter, setTierFilter] = useState('all');
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);
  
  const droppedItems = useMemo(() => extractDroppedItems(), []);
  const craftedItems = useMemo(() => generateCraftedItems(), []);
  
  const filteredItems = useMemo(() => {
    let items: Item[] = [];
    
    if (activeTab === 'dropped') {
      items = droppedItems;
    } else if (activeTab === 'crafted') {
      items = craftedItems;
    }
    
    return items.filter(item => {
      const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesRarity = rarityFilter === 'all' || item.rarity === rarityFilter;
      const matchesCategory = categoryFilter === 'all' || item.category === categoryFilter;
      const matchesTier = tierFilter === 'all' || item.tier.toString() === tierFilter;
      
      return matchesSearch && matchesRarity && matchesCategory && matchesTier;
    });
  }, [activeTab, droppedItems, craftedItems, searchTerm, rarityFilter, categoryFilter, tierFilter]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Items Library
          </h1>
          <p className="text-gray-400">
            Discover dropped items and crafting recipes from the world of Decennium Descent
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={(value: string) => setActiveTab(value as 'dropped' | 'crafted' | 'builder')}>
          <TabsList className="grid w-full grid-cols-3 bg-amber-600/20 border border-amber-600/30">
            <TabsTrigger value="dropped" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
              <Package className="w-4 h-4" />
              Dropped Items
            </TabsTrigger>
            <TabsTrigger value="crafted" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
              <Hammer className="w-4 h-4" />
              Crafted Items
            </TabsTrigger>
            <TabsTrigger value="builder" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
              <Wrench className="w-4 h-4" />
              Crafting Builder
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dropped">
            {/* Dropped Items Content */}
          </TabsContent>
          
          <TabsContent value="crafted">
            {/* Crafted Items Content */}
          </TabsContent>
          
          <TabsContent value="builder">
            <CraftingBuilder />
          </TabsContent>
        </Tabs>

        {activeTab !== 'builder' && (
          <div className="mb-6">
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Search items..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-black/30 border-gray-600 text-white placeholder:text-gray-400"
              />
            </div>
            
            <div className="flex flex-wrap gap-4">
              <Select value={rarityFilter} onValueChange={setRarityFilter}>
                <SelectTrigger className="w-48 bg-black/30 border-gray-600 text-white">
                  <SelectValue placeholder="Filter by Rarity" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Rarities</SelectItem>
                  {['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'].map(rarity => (
                    <SelectItem key={rarity} value={rarity}>{rarity}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-48 bg-black/30 border-gray-600 text-white">
                  <SelectValue placeholder="Filter by Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {['Material', 'Weapon', 'Armor', 'Consumable', 'Tool'].map(category => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              <Select value={tierFilter} onValueChange={setTierFilter}>
                <SelectTrigger className="w-48 bg-black/30 border-gray-600 text-white">
                  <SelectValue placeholder="Filter by Tier" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Tiers</SelectItem>
                  {[1, 2, 3, 4, 5].map(tier => (
                    <SelectItem key={tier} value={tier.toString()}>Tier {tier}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        )}

        {activeTab !== 'builder' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 order-2 lg:order-1">
              <div className="mb-4 flex justify-between items-center">
                <h2 className="text-xl font-semibold">
                  {filteredItems.length} {activeTab} items found
                </h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[800px] overflow-y-auto pr-2">
                {filteredItems.map((item) => (
                  <Card 
                    key={item.id} 
                    className={`bg-gray-800 border-gray-700 hover:border-gray-500 transition-colors cursor-pointer ${
                      selectedItem?.id === item.id ? 'border-blue-500 bg-blue-500/10' : ''
                    }`}
                    onClick={() => setSelectedItem(item)}
                  >
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <CardTitle className="text-lg font-bold text-white mb-1">
                            {item.name}
                          </CardTitle>
                          <div className="flex items-center gap-2">
                            <Badge 
                              variant="outline" 
                              className={`${
                                item.rarity === 'Common' ? 'border-gray-500 text-gray-300' :
                                item.rarity === 'Uncommon' ? 'border-green-500 text-green-400' :
                                item.rarity === 'Rare' ? 'border-blue-500 text-blue-400' :
                                item.rarity === 'Epic' ? 'border-purple-500 text-purple-400' :
                                'border-yellow-500 text-yellow-400'
                              }`}
                            >
                              {item.rarity}
                            </Badge>
                            <Badge variant="outline" className="border-gray-600 text-gray-400">
                              Tier {item.tier}
                            </Badge>
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Category:</span>
                          <span className="text-gray-300 capitalize">{item.category}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-400">Value:</span>
                          <div className="flex items-center gap-1">
                            <Coins className="w-3 h-3 text-yellow-500" />
                            <span className="text-yellow-500">{item.value}</span>
                          </div>
                        </div>
                        
                        {item.type === 'dropped' && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Drop Rate:</span>
                            <span className="text-gray-300">{(item as DroppedItem).dropRate}%</span>
                          </div>
                        )}
                        
                        {item.type === 'crafted' && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Skill:</span>
                            <span className="text-gray-300">{(item as CraftedItem).craftingSkill}</span>
                          </div>
                        )}
                      </div>
                      <div className="mt-3">
                        <p className="text-gray-300 text-sm line-clamp-2">
                          {item.description}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            <div className="lg:col-span-1 order-1 lg:order-2">
              {selectedItem ? (
                <Card className="bg-gray-800 border-gray-700 sticky top-4">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-xl font-bold text-white">
                          {selectedItem.name}
                        </CardTitle>
                        <div className="flex items-center gap-2 mt-2">
                          <Badge 
                            variant="outline" 
                            className={`${
                              selectedItem.rarity === 'Common' ? 'border-gray-500 text-gray-300' :
                              selectedItem.rarity === 'Uncommon' ? 'border-green-500 text-green-400' :
                              selectedItem.rarity === 'Rare' ? 'border-blue-500 text-blue-400' :
                              selectedItem.rarity === 'Epic' ? 'border-purple-500 text-purple-400' :
                              'border-yellow-500 text-yellow-400'
                            }`}
                          >
                            {selectedItem.rarity}
                          </Badge>
                          <Badge variant="outline" className="border-gray-600 text-gray-400">
                            Tier {selectedItem.tier}
                          </Badge>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setSelectedItem(null)}
                        className="text-gray-400 hover:text-white"
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold text-white mb-2">Description</h4>
                        <p className="text-gray-300 text-sm">{selectedItem.description}</p>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Coins className="w-4 h-4 text-yellow-500" />
                        <span className="text-yellow-500 font-semibold">{selectedItem.value} gold</span>
                      </div>
                      
                      {selectedItem.type === 'dropped' && (
                        <>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <span className="text-sm text-gray-400">Drop Rate</span>
                              <p className="text-white">{(selectedItem as DroppedItem).dropRate}%</p>
                            </div>
                            <div>
                              <span className="text-sm text-gray-400">Quantity</span>
                              <p className="text-white">{(selectedItem as DroppedItem).quantity}</p>
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="font-semibold text-white mb-2">Source Monsters</h4>
                            <div className="flex flex-wrap gap-1">
                              {(selectedItem as DroppedItem).sourceMonsters.map((monster, index) => (
                                <Badge key={index} variant="outline" className="text-xs border-gray-600 text-gray-300">
                                  {monster}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </>
                      )}
                      
                      {selectedItem.type === 'crafted' && (
                        <>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <span className="text-sm text-gray-400">Crafting Skill</span>
                              <p className="text-white">{(selectedItem as CraftedItem).craftingSkill}</p>
                            </div>
                            <div>
                              <span className="text-sm text-gray-400">Crafting Time</span>
                              <p className="text-white">{(selectedItem as CraftedItem).craftingTime}</p>
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="font-semibold text-white mb-2">Required Components</h4>
                            <div className="space-y-1">
                              {(selectedItem as CraftedItem).components.map((component, index) => (
                                <div key={index} className="text-sm text-gray-300 flex items-center gap-2">
                                  <Wrench className="w-3 h-3 text-gray-400" />
                                  {component}
                                </div>
                              ))}
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="flex items-center justify-center h-64">
                    <div className="text-center text-gray-400">
                      <Package className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p>Select an item to view details</p>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ItemsLibrary;