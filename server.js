// Decennium Descent Interactive Game Server
// Node.js Express server for hosting the game on port 8500

const express = require('express');
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const cors = require('cors');
const xlsx = require('xlsx');

const app = express();
const PORT = 8500;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use(express.static(__dirname));

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage: storage });

// Ensure uploads directory exists
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

// Game data storage
let gameData = {
    monsters: [],
    materials: [],
    recipes: [],
    characters: [],
    campaigns: [],
    encounters: []
};

// Load game data from Excel files
function loadGameDataFromFiles() {
    try {
        // Load bestiary data
        if (fs.existsSync('final_bestiary.xlsx')) {
            const workbook = xlsx.readFile('final_bestiary.xlsx');
            
            // Load monsters
            if (workbook.SheetNames.includes('Monsters')) {
                const monstersSheet = workbook.Sheets['Monsters'];
                const monstersData = xlsx.utils.sheet_to_json(monstersSheet);
                gameData.monsters = monstersData.map(monster => ({
                    id: monster.Name || 'Unknown',
                    name: monster.Name || 'Unknown',
                    size: monster.Size || 'Medium',
                    type: monster.Type || 'Humanoid',
                    challenge: parseFloat(monster.Challenge) || 0,
                    xp: parseInt(monster.XP) || 0,
                    zone: monster.Zone || 'Unknown',
                    alignment: monster.Alignment || 'Neutral',
                    drops: parseDrops(monster)
                }));
            }
            
            // Load materials from various drop sheets
            const dropSheets = workbook.SheetNames.filter(name => name.includes('Drops'));
            dropSheets.forEach(sheetName => {
                const sheet = workbook.Sheets[sheetName];
                const data = xlsx.utils.sheet_to_json(sheet);
                data.forEach(item => {
                    if (item.Name && !gameData.materials.find(m => m.name === item.Name)) {
                        gameData.materials.push({
                            id: item.Name,
                            name: item.Name,
                            tier: parseInt(item.Tier) || 1,
                            rarity: item.Rarity || 'Common',
                            value: parseFloat(item.Value) || 0,
                            weight: parseFloat(item.Weight) || 0,
                            dropRate: parseFloat(item['Drop Rate']) || 0,
                            quantity: item.Quantity || '1',
                            description: item.Description || '',
                            sources: parseSourceMonsters(item)
                        });
                    }
                });
            });
        }
        
        // Load crafting recipes
        if (fs.existsSync('decennium_descent_crafting_recipes_validated.xlsx')) {
            try {
                const craftingWorkbook = xlsx.readFile('decennium_descent_crafting_recipes_validated.xlsx');
                const recipesSheet = craftingWorkbook.Sheets[craftingWorkbook.SheetNames[0]];
                const recipesData = xlsx.utils.sheet_to_json(recipesSheet);
                gameData.recipes = recipesData.map(recipe => ({
                    id: recipe.Name || Date.now(),
                    name: recipe.Name || 'Unknown Recipe',
                    materials: parseRecipeMaterials(recipe),
                    result: recipe.Result || 'Unknown Item',
                    difficulty: recipe.Difficulty || 'Medium',
                    time: recipe.Time || '1 hour',
                    description: recipe.Description || ''
                }));
            } catch (error) {
                console.log('Could not load crafting recipes:', error.message);
            }
        }
        
        console.log(`Loaded ${gameData.monsters.length} monsters, ${gameData.materials.length} materials, ${gameData.recipes.length} recipes`);
    } catch (error) {
        console.error('Error loading game data:', error);
    }
}

function parseDrops(monster) {
    const drops = {};
    for (let i = 1; i <= 5; i++) {
        const dropKey = `Tier ${i} Drop`;
        const rateKey = `Tier ${i} Rate`;
        const valueKey = `Tier ${i} Value`;
        
        if (monster[dropKey]) {
            drops[`tier${i}`] = {
                item: monster[dropKey],
                rate: parseFloat(monster[rateKey]) || 0,
                value: parseFloat(monster[valueKey]) || 0
            };
        }
    }
    return drops;
}

function parseSourceMonsters(item) {
    const sources = [];
    for (let i = 1; i <= 10; i++) {
        const sourceKey = `Source ${i}`;
        if (item[sourceKey]) {
            sources.push(item[sourceKey]);
        }
    }
    return sources;
}

function parseRecipeMaterials(recipe) {
    const materials = [];
    for (let i = 1; i <= 10; i++) {
        const materialKey = `Material ${i}`;
        const quantityKey = `Quantity ${i}`;
        
        if (recipe[materialKey]) {
            materials.push({
                name: recipe[materialKey],
                quantity: parseInt(recipe[quantityKey]) || 1
            });
        }
    }
    return materials;
}

// Routes

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API Routes

// Get all monsters
app.get('/api/monsters', (req, res) => {
    const { search, challenge, type, size } = req.query;
    let filteredMonsters = [...gameData.monsters];
    
    if (search) {
        const searchLower = search.toLowerCase();
        filteredMonsters = filteredMonsters.filter(monster => 
            monster.name.toLowerCase().includes(searchLower) ||
            monster.type.toLowerCase().includes(searchLower) ||
            monster.zone.toLowerCase().includes(searchLower)
        );
    }
    
    if (challenge) {
        const cr = parseFloat(challenge);
        filteredMonsters = filteredMonsters.filter(monster => monster.challenge === cr);
    }
    
    if (type) {
        filteredMonsters = filteredMonsters.filter(monster => 
            monster.type.toLowerCase() === type.toLowerCase()
        );
    }
    
    if (size) {
        filteredMonsters = filteredMonsters.filter(monster => 
            monster.size.toLowerCase() === size.toLowerCase()
        );
    }
    
    res.json(filteredMonsters);
});

// Get specific monster
app.get('/api/monsters/:id', (req, res) => {
    const monster = gameData.monsters.find(m => m.id === req.params.id);
    if (monster) {
        res.json(monster);
    } else {
        res.status(404).json({ error: 'Monster not found' });
    }
});

// Get all materials
app.get('/api/materials', (req, res) => {
    const { search, tier, rarity } = req.query;
    let filteredMaterials = [...gameData.materials];
    
    if (search) {
        const searchLower = search.toLowerCase();
        filteredMaterials = filteredMaterials.filter(material => 
            material.name.toLowerCase().includes(searchLower) ||
            material.description.toLowerCase().includes(searchLower)
        );
    }
    
    if (tier) {
        filteredMaterials = filteredMaterials.filter(material => material.tier === parseInt(tier));
    }
    
    if (rarity) {
        filteredMaterials = filteredMaterials.filter(material => 
            material.rarity.toLowerCase() === rarity.toLowerCase()
        );
    }
    
    res.json(filteredMaterials);
});

// Get all recipes
app.get('/api/recipes', (req, res) => {
    const { search, difficulty } = req.query;
    let filteredRecipes = [...gameData.recipes];
    
    if (search) {
        const searchLower = search.toLowerCase();
        filteredRecipes = filteredRecipes.filter(recipe => 
            recipe.name.toLowerCase().includes(searchLower) ||
            recipe.result.toLowerCase().includes(searchLower)
        );
    }
    
    if (difficulty) {
        filteredRecipes = filteredRecipes.filter(recipe => 
            recipe.difficulty.toLowerCase() === difficulty.toLowerCase()
        );
    }
    
    res.json(filteredRecipes);
});

// Character management
app.get('/api/characters', (req, res) => {
    res.json(gameData.characters);
});

app.post('/api/characters', (req, res) => {
    const character = {
        id: Date.now().toString(),
        ...req.body,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };
    
    gameData.characters.push(character);
    res.status(201).json(character);
});

app.put('/api/characters/:id', (req, res) => {
    const characterIndex = gameData.characters.findIndex(c => c.id === req.params.id);
    if (characterIndex !== -1) {
        gameData.characters[characterIndex] = {
            ...gameData.characters[characterIndex],
            ...req.body,
            updatedAt: new Date().toISOString()
        };
        res.json(gameData.characters[characterIndex]);
    } else {
        res.status(404).json({ error: 'Character not found' });
    }
});

app.delete('/api/characters/:id', (req, res) => {
    const characterIndex = gameData.characters.findIndex(c => c.id === req.params.id);
    if (characterIndex !== -1) {
        gameData.characters.splice(characterIndex, 1);
        res.status(204).send();
    } else {
        res.status(404).json({ error: 'Character not found' });
    }
});

// Campaign management
app.get('/api/campaigns', (req, res) => {
    res.json(gameData.campaigns);
});

app.post('/api/campaigns', (req, res) => {
    const campaign = {
        id: Date.now().toString(),
        ...req.body,
        createdAt: new Date().toISOString(),
        sessions: [],
        characters: []
    };
    
    gameData.campaigns.push(campaign);
    res.status(201).json(campaign);
});

// Encounter generation
app.post('/api/encounters/generate', (req, res) => {
    const { partyLevel, partySize, difficulty, environment } = req.body;
    
    // Simple encounter generation logic
    const targetCR = calculateTargetCR(partyLevel, partySize, difficulty);
    const availableMonsters = gameData.monsters.filter(monster => 
        monster.challenge >= targetCR * 0.5 && monster.challenge <= targetCR * 2
    );
    
    if (environment) {
        availableMonsters = availableMonsters.filter(monster => 
            monster.zone.toLowerCase().includes(environment.toLowerCase())
        );
    }
    
    const encounter = generateEncounter(availableMonsters, targetCR);
    
    res.json({
        targetCR,
        actualCR: encounter.totalCR,
        monsters: encounter.monsters,
        xpReward: encounter.totalXP
    });
});

function calculateTargetCR(partyLevel, partySize, difficulty) {
    const baseCR = partyLevel;
    const sizeMultiplier = partySize / 4; // Assuming 4-person party as baseline
    const difficultyMultiplier = {
        'easy': 0.5,
        'medium': 0.75,
        'hard': 1.0,
        'deadly': 1.5
    }[difficulty] || 1.0;
    
    return baseCR * sizeMultiplier * difficultyMultiplier;
}

function generateEncounter(availableMonsters, targetCR) {
    if (availableMonsters.length === 0) {
        return { monsters: [], totalCR: 0, totalXP: 0 };
    }
    
    const encounter = {
        monsters: [],
        totalCR: 0,
        totalXP: 0
    };
    
    // Simple algorithm: try to get close to target CR
    let remainingCR = targetCR;
    
    while (remainingCR > 0.25 && encounter.monsters.length < 8) {
        const suitableMonsters = availableMonsters.filter(monster => 
            monster.challenge <= remainingCR
        );
        
        if (suitableMonsters.length === 0) break;
        
        const randomMonster = suitableMonsters[Math.floor(Math.random() * suitableMonsters.length)];
        encounter.monsters.push({
            ...randomMonster,
            quantity: 1
        });
        
        encounter.totalCR += randomMonster.challenge;
        encounter.totalXP += randomMonster.xp;
        remainingCR -= randomMonster.challenge;
    }
    
    return encounter;
}

// Dice rolling API
app.post('/api/dice/roll', (req, res) => {
    const { sides, count = 1, modifier = 0 } = req.body;
    
    if (!sides || sides < 2) {
        return res.status(400).json({ error: 'Invalid dice sides' });
    }
    
    const rolls = [];
    let total = modifier;
    
    for (let i = 0; i < count; i++) {
        const roll = Math.floor(Math.random() * sides) + 1;
        rolls.push(roll);
        total += roll;
    }
    
    res.json({
        rolls,
        total,
        modifier,
        dice: `${count}d${sides}${modifier !== 0 ? (modifier >= 0 ? '+' : '') + modifier : ''}`
    });
});

// File upload for character import/export
app.post('/api/characters/import', upload.single('characterFile'), (req, res) => {
    try {
        const fileContent = fs.readFileSync(req.file.path, 'utf8');
        const character = JSON.parse(fileContent);
        
        character.id = Date.now().toString();
        character.importedAt = new Date().toISOString();
        
        gameData.characters.push(character);
        
        // Clean up uploaded file
        fs.unlinkSync(req.file.path);
        
        res.status(201).json(character);
    } catch (error) {
        res.status(400).json({ error: 'Invalid character file' });
    }
});

app.get('/api/characters/:id/export', (req, res) => {
    const character = gameData.characters.find(c => c.id === req.params.id);
    if (character) {
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Content-Disposition', `attachment; filename="${character.name || 'character'}.json"`);
        res.send(JSON.stringify(character, null, 2));
    } else {
        res.status(404).json({ error: 'Character not found' });
    }
});

// Game statistics
app.get('/api/stats', (req, res) => {
    res.json({
        monsters: gameData.monsters.length,
        materials: gameData.materials.length,
        recipes: gameData.recipes.length,
        characters: gameData.characters.length,
        campaigns: gameData.campaigns.length,
        averageMonsterCR: gameData.monsters.length > 0 ? 
            gameData.monsters.reduce((sum, m) => sum + m.challenge, 0) / gameData.monsters.length : 0,
        materialsByTier: gameData.materials.reduce((acc, material) => {
            acc[material.tier] = (acc[material.tier] || 0) + 1;
            return acc;
        }, {})
    });
});

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Server error:', error);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Load game data on startup
loadGameDataFromFiles();

// Start server
app.listen(PORT, () => {
    console.log(`🎲 Decennium Descent Interactive Game Server running on http://localhost:${PORT}`);
    console.log(`📊 Loaded game data: ${gameData.monsters.length} monsters, ${gameData.materials.length} materials, ${gameData.recipes.length} recipes`);
    console.log('🚀 Ready for epic adventures!');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Decennium Descent server...');
    process.exit(0);
});

module.exports = app;