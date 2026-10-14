'use client';

import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Search, Package, Hammer, Wrench, X, Coins, Send } from 'lucide-react';
import bestiaryData from '../bestiary_data_full.json';
import craftingRecipes from '@/data/crafting-recipes.json';
import CraftingBuilder from './CraftingBuilder';
import { pushItemHandoff } from '@/lib/session-handoff';

type BestiaryLootTier = {
  drop?: string | null;
  rate?: number | string | null;
  quantity?: string | null;
  value?: number | string | null;
};

type BestiaryMonster = {
  name?: string;
  zoneFound?: string;
  loot?: {
    tier1?: BestiaryLootTier;
    tier2?: BestiaryLootTier;
    tier3?: BestiaryLootTier;
  };
};

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
  difficulty: number;
  effects: string;
  components: string[];
}

type Item = DroppedItem | CraftedItem;

// Crafted catalog from validated workbook ingest
const generateCraftedItems = (): CraftedItem[] => {
  return (craftingRecipes as Array<{
    id: string;
    name: string;
    skill: string;
    craftingTime: string;
    rarity: string;
    difficulty?: number;
    effects?: string;
    components: { name: string }[];
    resultItem?: { name: string; rarity?: string; value?: number; tier?: number; properties?: string[] };
  }>).map((r) => ({
    id: r.id,
    name: r.resultItem?.name || r.name,
    description: r.effects || r.resultItem?.properties?.[0] || `${r.skill} recipe from the Decennium crafting workbook.`,
    rarity: r.rarity || r.resultItem?.rarity || 'Common',
    category: r.skill,
    tier: r.resultItem?.tier || 1,
    value: r.resultItem?.value || 0,
    type: 'crafted' as const,
    craftingSkill: r.skill,
    craftingTime: r.craftingTime || '1 hour',
    difficulty: r.difficulty || 10,
    effects: r.effects || r.resultItem?.properties?.join('; ') || '',
    components: (r.components || []).map((c) => c.name).filter(Boolean),
  }));
};

// Extract dropped items from bestiary data
const extractDroppedItems = (): DroppedItem[] => {
  const droppedItems: DroppedItem[] = [];
  const parseVal = (v: number | string | null | undefined, fallback: number) =>
    v !== undefined && v !== null && v !== 'nan' ? parseInt(String(v)) || fallback : fallback;
  const parseRate = (v: number | string | null | undefined) =>
    v !== undefined && v !== null && v !== 'nan' ? Math.round(parseFloat(String(v)) * 100) : 0;

  const upsert = (
    drop: string,
    tier: number,
    rarity: string,
    description: string,
    value: number,
    dropRate: number,
    quantity: string,
    monsterName: string
  ) => {
    const existingItem = droppedItems.find(
      (item) => item.name.toLowerCase() === drop.toLowerCase()
    );
    if (!existingItem) {
      droppedItems.push({
        id: `dropped_${drop.replace(/\s+/g, '_')}`,
        name: drop,
        description,
        rarity,
        category: 'Material',
        tier,
        value,
        type: 'dropped',
        dropRate,
        quantity,
        sourceMonsters: [monsterName],
      });
    } else if (!existingItem.sourceMonsters.includes(monsterName)) {
      existingItem.sourceMonsters.push(monsterName);
    }
  };

  (bestiaryData as BestiaryMonster[]).forEach((monster) => {
    const loot = monster.loot;
    if (!loot) return;
    const monsterName = monster.name ?? 'Unknown';
    const zone = monster.zoneFound ?? 'the Decennium';

    const tiers: Array<{
      key: 'tier1' | 'tier2' | 'tier3';
      tier: number;
      rarity: string;
      quantity: string;
      fallbackValue: number;
      desc: string;
    }> = [
      { key: 'tier1', tier: 1, rarity: 'Common', quantity: '1-3', fallbackValue: 1, desc: `A common drop from various creatures in ${zone}.` },
      { key: 'tier2', tier: 2, rarity: 'Uncommon', quantity: '1-2', fallbackValue: 5, desc: `An uncommon drop from creatures in ${zone}.` },
      { key: 'tier3', tier: 3, rarity: 'Rare', quantity: '1', fallbackValue: 15, desc: `A rare drop from powerful creatures in ${zone}.` },
    ];

    for (const t of tiers) {
      const entry = loot[t.key];
      const drop = entry?.drop;
      if (!drop || drop === 'None' || drop === 'nan') continue;
      upsert(
        drop,
        t.tier,
        t.rarity,
        t.desc,
        parseVal(entry?.value, t.fallbackValue),
        parseRate(entry?.rate),
        t.quantity,
        monsterName
      );
    }
  });
  
  return droppedItems;
};

const ItemsLibrary: React.FC<{ onLoadSession?: () => void }> = ({ onLoadSession }) => {
  const [activeTab, setActiveTab] = useState<'dropped' | 'crafted' | 'builder'>('dropped');
  const [searchTerm, setSearchTerm] = useState('');
  const [rarityFilter, setRarityFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [tierFilter, setTierFilter] = useState('all');
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);

  const previewItemInSession = (item: Item) => {
    pushItemHandoff({
      name: item.name,
      rarity: item.rarity,
      category: item.category,
      tier: item.tier,
      description: item.description,
      source: item.type === 'crafted' ? 'items-crafted' : 'items-dropped',
    });
    onLoadSession?.();
  };
  
  const droppedItems = useMemo(() => extractDroppedItems(), []);
  const craftedItems = useMemo(() => generateCraftedItems(), []);

  const categoryOptions = useMemo(() => {
    const items = activeTab === 'crafted' ? craftedItems : droppedItems;
    return [...new Set(items.map((item) => item.category))].sort();
  }, [activeTab, droppedItems, craftedItems]);

  const rarityOptions = useMemo(() => {
    const items = activeTab === 'crafted' ? craftedItems : droppedItems;
    return [...new Set(items.map((item) => item.rarity))].sort();
  }, [activeTab, droppedItems, craftedItems]);
  
  const filteredItems = useMemo(() => {
    let items: Item[] = [];
    
    if (activeTab === 'dropped') {
      items = droppedItems;
    } else if (activeTab === 'crafted') {
      items = craftedItems;
    }
    
    const q = searchTerm.trim().toLowerCase();
    return items.filter(item => {
      const searchHaystack = [
        item.name,
        item.description,
        item.type === 'crafted' ? (item as CraftedItem).craftingSkill : '',
        item.type === 'crafted' ? (item as CraftedItem).effects : '',
        ...(item.type === 'crafted' ? (item as CraftedItem).components : []),
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();
      const matchesSearch = !q || searchHaystack.includes(q);
      const matchesRarity = rarityFilter === 'all' || item.rarity === rarityFilter;
      const matchesCategory = categoryFilter === 'all' || item.category === categoryFilter;
      const matchesTier = tierFilter === 'all' || item.tier.toString() === tierFilter;
      
      return matchesSearch && matchesRarity && matchesCategory && matchesTier;
    });
  }, [activeTab, droppedItems, craftedItems, searchTerm, rarityFilter, categoryFilter, tierFilter]);

  const hasActiveFilters =
    searchTerm.trim() !== '' ||
    rarityFilter !== 'all' ||
    categoryFilter !== 'all' ||
    tierFilter !== 'all';

  const clearFilters = () => {
    setSearchTerm('');
    setRarityFilter('all');
    setCategoryFilter('all');
    setTierFilter('all');
  };

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

        <Tabs value={activeTab} onValueChange={(value: string) => {
          setActiveTab(value as 'dropped' | 'crafted' | 'builder');
          setSearchTerm('');
          setRarityFilter('all');
          setCategoryFilter('all');
          setTierFilter('all');
          setSelectedItem(null);
        }}>
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
                  {rarityOptions.map(rarity => (
                    <SelectItem key={rarity} value={rarity}>{rarity}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-48 bg-black/30 border-gray-600 text-white">
                  <SelectValue placeholder={activeTab === 'crafted' ? 'Filter by Skill' : 'Filter by Category'} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{activeTab === 'crafted' ? 'All Skills' : 'All Categories'}</SelectItem>
                  {categoryOptions.map(category => (
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
              <div className="mb-4 flex flex-wrap justify-between items-center gap-2">
                <h2 className="text-xl font-semibold">
                  {filteredItems.length} {activeTab} items found
                  {hasActiveFilters ? ' (filtered)' : ''}
                </h2>
                {hasActiveFilters && (
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={clearFilters}
                    className="h-7 text-xs text-gray-300"
                  >
                    Clear filters
                  </Button>
                )}
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[800px] overflow-y-auto pr-2">
                {filteredItems.length > 0 ? (
                  filteredItems.map((item) => (
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
                            <>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Skill / DC:</span>
                                <span className="text-gray-300">{(item as CraftedItem).craftingSkill} · DC {(item as CraftedItem).difficulty}</span>
                              </div>
                              {(item as CraftedItem).effects && (
                                <div className="text-xs text-purple-300/90 line-clamp-2">{(item as CraftedItem).effects}</div>
                              )}
                            </>
                          )}
                        </div>
                        <div className="mt-3">
                          <p className="text-gray-300 text-sm line-clamp-2">
                            {item.description}
                          </p>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                ) : (
                  <Card className="md:col-span-2 bg-gray-800/70 border-dashed border-gray-600">
                    <CardContent className="flex min-h-56 flex-col items-center justify-center gap-3 p-6 text-center">
                      <Package className="w-10 h-10 text-amber-300/60" />
                      <div>
                        <p className="font-medium text-gray-100">No {activeTab} items match these filters</p>
                        <p className="mt-1 text-sm text-gray-400">
                          Try a different search or reset the active filters.
                        </p>
                      </div>
                      {hasActiveFilters && (
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={clearFilters}
                          className="border-amber-600/50 text-amber-200 hover:bg-amber-900/30"
                        >
                          Clear all filters
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                )}
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

                      <Button
                        variant="outline"
                        size="sm"
                        className="border-teal-600/50 text-teal-200 hover:bg-teal-900/40"
                        onClick={() => previewItemInSession(selectedItem)}
                      >
                        <Send className="w-3 h-3 mr-1" />
                        Preview in Session
                      </Button>
                      <p className="text-[10px] leading-snug text-gray-400">
                        Sends item reference to Session only; the Director resolves acquisition, use, and inventory.
                      </p>
                      
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
                              <span className="text-sm text-gray-400">Craft DC</span>
                              <p className="text-orange-400 font-semibold">{(selectedItem as CraftedItem).difficulty}</p>
                            </div>
                            <div>
                              <span className="text-sm text-gray-400">Crafting Time</span>
                              <p className="text-white">{(selectedItem as CraftedItem).craftingTime}</p>
                            </div>
                            <div>
                              <span className="text-sm text-gray-400">Result Value</span>
                              <p className="text-yellow-500">{(selectedItem as CraftedItem).value} gold</p>
                            </div>
                          </div>

                          {(selectedItem as CraftedItem).effects && (
                            <div>
                              <h4 className="font-semibold text-white mb-2">Effects</h4>
                              <p className="text-sm text-purple-200/90">{(selectedItem as CraftedItem).effects}</p>
                            </div>
                          )}

                          <div>
                            <h4 className="font-semibold text-white mb-2">Ingredients ({(selectedItem as CraftedItem).components.length})</h4>
                            <div className="space-y-1 max-h-48 overflow-y-auto">
                              {(selectedItem as CraftedItem).components.map((component, index) => (
                                <div key={index} className="text-sm text-gray-300 flex items-center gap-2">
                                  <Wrench className="w-3 h-3 text-gray-400 shrink-0" />
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