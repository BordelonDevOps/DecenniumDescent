"use client";

import React, { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Search, Plus, Minus, Hammer, Sparkles, RotateCcw, Save, Trash2, Beaker } from 'lucide-react';
import bestiaryData from '../bestiary_data_full.json';

// Types
interface CraftingComponent {
  id: string;
  name: string;
  tier: number;
  rarity: string;
  category: string;
  value: number;
  weight: number;
  quantity: number;
  properties: string[];
}

interface CraftingRecipe {
  id: string;
  name: string;
  components: CraftingComponent[];
  skill: string;
  difficulty: number;
  craftingTime: string;
  resultItem: {
    name: string;
    tier: number;
    rarity: string;
    value: number;
    properties: string[];
  };
}

// Extract crafting components from bestiary data
const extractCraftingComponents = (): CraftingComponent[] => {
  const components: CraftingComponent[] = [];
  const processedItems = new Set<string>();
  
  bestiaryData.forEach((monster: any) => {
    ['tier1', 'tier2', 'tier3'].forEach((tierKey, index) => {
      const loot = monster.loot[tierKey];
      if (loot && loot.drop && loot.drop !== 'nan' && !processedItems.has(loot.drop)) {
        processedItems.add(loot.drop);
        
        // Determine category and properties from item name
        const name = loot.drop.toLowerCase();
        let category = 'misc';
        let properties: string[] = [];
        
        if (name.includes('hide') || name.includes('leather')) {
          category = 'hide';
          properties = ['flexible', 'durable', 'armor_component'];
        } else if (name.includes('bone') || name.includes('claw') || name.includes('tooth')) {
          category = 'bone';
          properties = ['sharp', 'hard', 'weapon_component'];
        } else if (name.includes('scale') || name.includes('chitin')) {
          category = 'scale';
          properties = ['protective', 'layered', 'armor_component'];
        } else if (name.includes('essence') || name.includes('spirit')) {
          category = 'essence';
          properties = ['magical', 'volatile', 'enchantment_component'];
        } else if (name.includes('fluid') || name.includes('blood') || name.includes('acid')) {
          category = 'fluid';
          properties = ['liquid', 'reactive', 'potion_component'];
        } else if (name.includes('organ') || name.includes('heart') || name.includes('gland')) {
          category = 'organ';
          properties = ['organic', 'potent', 'alchemical_component'];
        } else if (name.includes('horn') || name.includes('antler')) {
          category = 'horn';
          properties = ['pointed', 'sturdy', 'weapon_component'];
        } else if (name.includes('fiber') || name.includes('silk')) {
          category = 'fiber';
          properties = ['woven', 'light', 'cloth_component'];
        } else if (name.includes('mineral') || name.includes('crystal') || name.includes('gem')) {
          category = 'mineral';
          properties = ['crystalline', 'valuable', 'jewelry_component'];
        } else if (name.includes('powder') || name.includes('dust')) {
          category = 'powder';
          properties = ['fine', 'mixable', 'alchemical_component'];
        } else if (name.includes('plant') || name.includes('leaf') || name.includes('root')) {
          category = 'plant';
          properties = ['natural', 'herbal', 'potion_component'];
        } else if (name.includes('slime') || name.includes('ooze')) {
          category = 'slime';
          properties = ['viscous', 'adhesive', 'binding_component'];
        } else if (name.includes('core')) {
          category = 'core';
          properties = ['concentrated', 'powerful', 'enchantment_component'];
        }
        
        // Determine rarity based on tier
        let rarity = 'Common';
        if (index === 0) rarity = Math.random() > 0.7 ? 'Uncommon' : 'Common';
        else if (index === 1) rarity = Math.random() > 0.5 ? 'Rare' : 'Uncommon';
        else rarity = Math.random() > 0.3 ? 'Epic' : 'Very Rare';
        
        components.push({
          id: `comp_${loot.drop.replace(/\s+/g, '_')}`,
          name: loot.drop,
          tier: index + 1,
          rarity,
          category,
          value: parseInt(loot.value) || 0,
          weight: Math.random() * 2,
          quantity: 1,
          properties
        });
      }
    });
  });
  
  return components;
};

// Generate crafting recipes based on component combinations
const generateRecipes = (components: CraftingComponent[]): CraftingRecipe[] => {
  const recipes: CraftingRecipe[] = [];
  const skills = ['Blacksmithing', 'Leatherworking', 'Alchemy', 'Enchanting', 'Tailoring', 'Jewelcrafting', 'Carpentry', 'Cooking'];
  
  // Generate recipes for different item types
  const recipeTemplates = [
    {
      name: 'Weapon',
      requiredProperties: ['weapon_component', 'sharp'],
      skill: 'Blacksmithing',
      baseValue: 100
    },
    {
      name: 'Armor',
      requiredProperties: ['armor_component', 'protective'],
      skill: 'Leatherworking',
      baseValue: 80
    },
    {
      name: 'Potion',
      requiredProperties: ['potion_component', 'liquid'],
      skill: 'Alchemy',
      baseValue: 50
    },
    {
      name: 'Enchanted Item',
      requiredProperties: ['enchantment_component', 'magical'],
      skill: 'Enchanting',
      baseValue: 150
    },
    {
      name: 'Jewelry',
      requiredProperties: ['jewelry_component', 'valuable'],
      skill: 'Jewelcrafting',
      baseValue: 200
    }
  ];
  
  recipeTemplates.forEach((template, templateIndex) => {
    // Find components that match the template requirements
    const matchingComponents = components.filter(comp => 
      template.requiredProperties.some(prop => comp.properties.includes(prop))
    );
    
    // Create recipes with 2-4 components
    for (let recipeCount = 0; recipeCount < 20; recipeCount++) {
      const numComponents = Math.floor(Math.random() * 3) + 2; // 2-4 components
      const selectedComponents: CraftingComponent[] = [];
      
      for (let i = 0; i < numComponents; i++) {
        const randomComponent = matchingComponents[Math.floor(Math.random() * matchingComponents.length)];
        if (randomComponent && !selectedComponents.find(c => c.id === randomComponent.id)) {
          selectedComponents.push({
            ...randomComponent,
            quantity: Math.floor(Math.random() * 3) + 1
          });
        }
      }
      
      if (selectedComponents.length >= 2) {
        const avgTier = selectedComponents.reduce((sum, comp) => sum + comp.tier, 0) / selectedComponents.length;
        const totalValue = selectedComponents.reduce((sum, comp) => sum + (comp.value * comp.quantity), 0);
        
        let resultRarity = 'Common';
        if (avgTier >= 3) resultRarity = 'Epic';
        else if (avgTier >= 2.5) resultRarity = 'Very Rare';
        else if (avgTier >= 2) resultRarity = 'Rare';
        else if (avgTier >= 1.5) resultRarity = 'Uncommon';
        
        recipes.push({
          id: `recipe_${templateIndex}_${recipeCount}`,
          name: `${template.name} Recipe ${recipeCount + 1}`,
          components: selectedComponents,
          skill: template.skill,
          difficulty: Math.floor(avgTier * 10) + Math.floor(Math.random() * 20),
          craftingTime: `${Math.floor(avgTier * 30) + Math.floor(Math.random() * 60)} minutes`,
          resultItem: {
            name: `Crafted ${template.name} (T${Math.floor(avgTier)})`,
            tier: Math.floor(avgTier),
            rarity: resultRarity,
            value: Math.floor(totalValue * 1.5),
            properties: [...new Set(selectedComponents.flatMap(c => c.properties))]
          }
        });
      }
    }
  });
  
  return recipes;
};

const CraftingBuilder: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedComponents, setSelectedComponents] = useState<CraftingComponent[]>([]);
  const [craftingSkill, setCraftingSkill] = useState<string>('Blacksmithing');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [tierFilter, setTierFilter] = useState<string>('all');
  const [testResult, setTestResult] = useState<CraftingRecipe | null>(null);
  
  // Generate components and recipes
  const availableComponents = useMemo(() => extractCraftingComponents(), []);
  const allRecipes = useMemo(() => generateRecipes(availableComponents), [availableComponents]);
  
  // Get unique filter values
  const categories = [...new Set(availableComponents.map(comp => comp.category))].sort();
  const tiers = [...new Set(availableComponents.map(comp => comp.tier))].sort((a, b) => a - b);
  const skills = ['Blacksmithing', 'Leatherworking', 'Alchemy', 'Enchanting', 'Tailoring', 'Jewelcrafting', 'Carpentry', 'Cooking'];
  
  // Filter components
  const filteredComponents = useMemo(() => {
    return availableComponents.filter(comp => {
      const matchesSearch = comp.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = categoryFilter === 'all' || comp.category === categoryFilter;
      const matchesTier = tierFilter === 'all' || comp.tier.toString() === tierFilter;
      
      return matchesSearch && matchesCategory && matchesTier;
    });
  }, [availableComponents, searchTerm, categoryFilter, tierFilter]);
  
  const addComponent = (component: CraftingComponent) => {
    const existing = selectedComponents.find(c => c.id === component.id);
    if (existing) {
      setSelectedComponents(prev => 
        prev.map(c => c.id === component.id ? { ...c, quantity: c.quantity + 1 } : c)
      );
    } else {
      setSelectedComponents(prev => [...prev, { ...component, quantity: 1 }]);
    }
  };
  
  const removeComponent = (componentId: string) => {
    setSelectedComponents(prev => prev.filter(c => c.id !== componentId));
  };
  
  const updateQuantity = (componentId: string, quantity: number) => {
    if (quantity <= 0) {
      removeComponent(componentId);
    } else {
      setSelectedComponents(prev => 
        prev.map(c => c.id === componentId ? { ...c, quantity } : c)
      );
    }
  };
  
  const testCrafting = () => {
    if (selectedComponents.length < 2) {
      alert('You need at least 2 components to craft an item!');
      return;
    }
    
    const avgTier = selectedComponents.reduce((sum, comp) => sum + comp.tier, 0) / selectedComponents.length;
    const totalValue = selectedComponents.reduce((sum, comp) => sum + (comp.value * comp.quantity), 0);
    const allProperties = [...new Set(selectedComponents.flatMap(c => c.properties))];
    
    let resultRarity = 'Common';
    if (avgTier >= 3) resultRarity = 'Epic';
    else if (avgTier >= 2.5) resultRarity = 'Very Rare';
    else if (avgTier >= 2) resultRarity = 'Rare';
    else if (avgTier >= 1.5) resultRarity = 'Uncommon';
    
    // Determine item type based on properties
    let itemType = 'Miscellaneous Item';
    if (allProperties.includes('weapon_component')) itemType = 'Weapon';
    else if (allProperties.includes('armor_component')) itemType = 'Armor';
    else if (allProperties.includes('potion_component')) itemType = 'Potion';
    else if (allProperties.includes('enchantment_component')) itemType = 'Enchanted Item';
    else if (allProperties.includes('jewelry_component')) itemType = 'Jewelry';
    
    const testRecipe: CraftingRecipe = {
      id: 'test_recipe',
      name: `Custom ${itemType} Recipe`,
      components: selectedComponents,
      skill: craftingSkill,
      difficulty: Math.floor(avgTier * 10) + Math.floor(Math.random() * 20),
      craftingTime: `${Math.floor(avgTier * 30) + Math.floor(Math.random() * 60)} minutes`,
      resultItem: {
        name: `Crafted ${itemType} (T${Math.floor(avgTier)})`,
        tier: Math.floor(avgTier),
        rarity: resultRarity,
        value: Math.floor(totalValue * 1.5),
        properties: allProperties
      }
    };
    
    setTestResult(testRecipe);
  };
  
  const clearComponents = () => {
    setSelectedComponents([]);
    setTestResult(null);
  };
  
  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'Common': return 'bg-gray-500';
      case 'Uncommon': return 'bg-green-500';
      case 'Rare': return 'bg-blue-500';
      case 'Very Rare': return 'bg-purple-500';
      case 'Epic': return 'bg-orange-500';
      case 'Legendary': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };
  
  const getTierColor = (tier: number) => {
    const colors = ['bg-gray-600', 'bg-green-600', 'bg-blue-600', 'bg-purple-600', 'bg-orange-600', 'bg-red-600'];
    return colors[tier - 1] || 'bg-gray-600';
  };
  
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-center bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
            Crafting Item Builder
          </h1>
          <p className="text-gray-400 text-center">
            Test combinations of crafting components to create new items
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Components Library */}
          <div className="lg:col-span-2">
            <Card className="bg-gray-800 border-gray-700 mb-6">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Beaker className="w-5 h-5" />
                  Crafting Components Library
                </CardTitle>
              </CardHeader>
              <CardContent>
                {/* Search and Filters */}
                <div className="space-y-4 mb-6">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <Input
                      type="text"
                      placeholder="Search components..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 bg-gray-700 border-gray-600 text-white"
                    />
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                      <SelectTrigger className="bg-gray-700 border-gray-600">
                        <SelectValue placeholder="Filter by Category" />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-700 border-gray-600">
                        <SelectItem value="all">All Categories</SelectItem>
                        {categories.map(category => (
                          <SelectItem key={category} value={category}>
                            {category.charAt(0).toUpperCase() + category.slice(1)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    
                    <Select value={tierFilter} onValueChange={setTierFilter}>
                      <SelectTrigger className="bg-gray-700 border-gray-600">
                        <SelectValue placeholder="Filter by Tier" />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-700 border-gray-600">
                        <SelectItem value="all">All Tiers</SelectItem>
                        {tiers.map(tier => (
                          <SelectItem key={tier} value={tier.toString()}>Tier {tier}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                {/* Components Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto pr-2">
                  {filteredComponents.map((component) => (
                    <Card
                      key={component.id}
                      className="bg-gray-700 border-gray-600 hover:bg-gray-650 transition-all cursor-pointer"
                      onClick={() => addComponent(component)}
                    >
                      <CardContent className="p-3">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-semibold text-sm text-white">{component.name}</h3>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              addComponent(component);
                            }}
                            className="text-green-400 hover:text-green-300 p-1 h-auto"
                          >
                            <Plus className="w-3 h-3" />
                          </Button>
                        </div>
                        <div className="flex gap-1 flex-wrap mb-2">
                          <Badge className={`${getRarityColor(component.rarity)} text-white text-xs`}>
                            {component.rarity}
                          </Badge>
                          <Badge className={`${getTierColor(component.tier)} text-white text-xs`}>
                            T{component.tier}
                          </Badge>
                          <Badge variant="outline" className="border-gray-500 text-gray-300 text-xs">
                            {component.category}
                          </Badge>
                        </div>
                        <div className="text-xs text-gray-400">
                          Value: {component.value}g | Weight: {component.weight.toFixed(1)} lbs
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
          
          {/* Crafting Workbench */}
          <div>
            <Card className="bg-gray-800 border-gray-700 mb-6">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Hammer className="w-5 h-5" />
                  Crafting Workbench
                </CardTitle>
              </CardHeader>
              <CardContent>
                {/* Crafting Skill Selection */}
                <div className="mb-4">
                  <label className="text-sm text-gray-400 mb-2 block">Crafting Skill</label>
                  <Select value={craftingSkill} onValueChange={setCraftingSkill}>
                    <SelectTrigger className="bg-gray-700 border-gray-600">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-700 border-gray-600">
                      {skills.map(skill => (
                        <SelectItem key={skill} value={skill}>{skill}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                {/* Selected Components */}
                <div className="mb-4">
                  <label className="text-sm text-gray-400 mb-2 block">Selected Components ({selectedComponents.length})</label>
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {selectedComponents.length === 0 ? (
                      <div className="text-center text-gray-500 py-4">
                        <Sparkles className="w-8 h-8 mx-auto mb-2 opacity-50" />
                        <p className="text-sm">Add components to start crafting</p>
                      </div>
                    ) : (
                      selectedComponents.map((component) => (
                        <div key={component.id} className="bg-gray-700 p-2 rounded flex items-center justify-between">
                          <div className="flex-1">
                            <div className="text-sm font-medium text-white">{component.name}</div>
                            <div className="text-xs text-gray-400">
                              {component.category} | T{component.tier} | {component.value}g
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => updateQuantity(component.id, component.quantity - 1)}
                              className="text-red-400 hover:text-red-300 p-1 h-auto"
                            >
                              <Minus className="w-3 h-3" />
                            </Button>
                            <span className="text-sm text-white min-w-[20px] text-center">{component.quantity}</span>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => updateQuantity(component.id, component.quantity + 1)}
                              className="text-green-400 hover:text-green-300 p-1 h-auto"
                            >
                              <Plus className="w-3 h-3" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => removeComponent(component.id)}
                              className="text-red-400 hover:text-red-300 p-1 h-auto ml-2"
                            >
                              <Trash2 className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
                
                {/* Action Buttons */}
                <div className="space-y-2">
                  <Button
                    onClick={testCrafting}
                    disabled={selectedComponents.length < 2}
                    className="w-full bg-purple-600 hover:bg-purple-700 text-white"
                  >
                    <Hammer className="w-4 h-4 mr-2" />
                    Test Crafting
                  </Button>
                  <Button
                    onClick={clearComponents}
                    variant="outline"
                    className="w-full border-gray-600 text-gray-300 hover:bg-gray-700"
                  >
                    <RotateCcw className="w-4 h-4 mr-2" />
                    Clear All
                  </Button>
                </div>
              </CardContent>
            </Card>
            
            {/* Crafting Result */}
            {testResult && (
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-yellow-400" />
                    Crafting Result
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h3 className="font-semibold text-white mb-2">{testResult.resultItem.name}</h3>
                      <div className="flex gap-2 flex-wrap mb-3">
                        <Badge className={`${getRarityColor(testResult.resultItem.rarity)} text-white`}>
                          {testResult.resultItem.rarity}
                        </Badge>
                        <Badge className={`${getTierColor(testResult.resultItem.tier)} text-white`}>
                          Tier {testResult.resultItem.tier}
                        </Badge>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-400">Value:</span>
                        <div className="text-yellow-400">{testResult.resultItem.value}g</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Difficulty:</span>
                        <div className="text-orange-400">{testResult.difficulty}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Skill:</span>
                        <div className="text-purple-400">{testResult.skill}</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Time:</span>
                        <div className="text-blue-400">{testResult.craftingTime}</div>
                      </div>
                    </div>
                    
                    <div>
                      <span className="text-gray-400 text-sm">Properties:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {testResult.resultItem.properties.map((prop, index) => (
                          <Badge key={index} variant="outline" className="border-gray-600 text-gray-300 text-xs">
                            {prop.replace('_', ' ')}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CraftingBuilder;