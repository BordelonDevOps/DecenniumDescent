// Enhanced Features for Decennium Descent
// Planar integration and showcase features

const PLANAR_AFFINITIES = {
    material: {
        name: "Material Plane",
        description: "Balanced connection to the nexus of existence",
        benefits: [
            "Planar Stability: +1 to all saving throws when on other planes",
            "Cosmic Anchor: Advantage on checks to resist planar effects",
            "Universal Language: Can understand any spoken language for 1 minute, 1/day"
        ],
        mechanics: "Your connection to the Material Plane grants you exceptional stability when traveling between worlds."
    },
    fire: {
        name: "Plane of Fire",
        description: "Attuned to eternal flames and creative destruction",
        benefits: [
            "Fire Resistance 5 (stacks with other resistances)",
            "Flame Touch: Unarmed strikes deal +1 fire damage",
            "Phoenix Resilience: When reduced to 0 HP, regain 1 HP once per long rest"
        ],
        mechanics: "The eternal flames of the Fire Plane burn within you, providing protection and regenerative power."
    },
    water: {
        name: "Plane of Water",
        description: "Connected to infinite oceans and flowing currents",
        benefits: [
            "Aquatic Adaptation: Swim speed equal to walking speed, breathe underwater",
            "Healing Currents: +1 HP when using healing potions or spells",
            "Tide Sense: Advantage on survival checks near bodies of water"
        ],
        mechanics: "The endless seas flow through your spirit, granting mastery over aquatic environments."
    },
    air: {
        name: "Plane of Air",
        description: "Touched by eternal winds and boundless skies",
        benefits: [
            "Wind Walker: Feather fall at will, +10 feet movement speed",
            "Storm Sense: Predict weather changes 24 hours in advance",
            "Lightning Reflexes: +2 to initiative rolls"
        ],
        mechanics: "The eternal winds carry your spirit, granting speed and foresight."
    },
    earth: {
        name: "Plane of Earth",
        description: "Grounded in eternal stone and precious depths",
        benefits: [
            "Stone Skin: +1 natural armor bonus to AC",
            "Earth Sense: Tremorsense 10 feet when touching the ground",
            "Mineral Wealth: Double the value of gems and precious metals you find"
        ],
        mechanics: "The eternal mountains strengthen your body and sharpen your senses for hidden treasures."
    },
    celestial: {
        name: "Celestial Realms",
        description: "Blessed by the upper planes of good",
        benefits: [
            "Divine Favor: +1 to all saving throws against evil creatures",
            "Celestial Guidance: Reroll one ability check per day",
            "Radiant Soul: Resistance to necrotic damage"
        ],
        mechanics: "The light of the upper planes shines within you, providing protection against darkness."
    },
    infernal: {
        name: "Infernal Realms",
        description: "Marked by the lower planes of evil",
        benefits: [
            "Infernal Resilience: Resistance to fire damage",
            "Dark Pact: Once per day, gain advantage on an intimidation check",
            "Hell's Insight: Advantage on checks to detect lies and deception"
        ],
        mechanics: "The fires of the Nine Hells have left their mark, granting you diabolic insight and resilience."
    },
    order: {
        name: "Plane of Order",
        description: "Aligned with cosmic law and mathematical perfection",
        benefits: [
            "Lawful Mind: Immunity to confusion effects",
            "Perfect Calculation: Take 10 on any Intelligence-based check once per day",
            "Axiom Shield: +2 AC against chaotic creatures"
        ],
        mechanics: "The absolute laws of Order flow through you, providing mental clarity and protection from chaos."
    },
    chaos: {
        name: "Plane of Chaos",
        description: "Touched by pure entropy and creative destruction",
        benefits: [
            "Chaotic Surge: Once per day, reroll any d20 and take either result",
            "Entropy Shield: Resistance to force damage",
            "Wild Magic: Random beneficial effect when you roll a natural 20"
        ],
        mechanics: "The unpredictable forces of Chaos infuse your being, granting luck and magical unpredictability."
    },
    life: {
        name: "Plane of Life",
        description: "Connected to the wellspring of all living energy",
        benefits: [
            "Life Force: +1 HP per character level",
            "Natural Healer: Healing spells you cast restore +1 additional HP",
            "Death Ward: Advantage on death saving throws"
        ],
        mechanics: "The eternal cycle of life flows through you, granting vitality and healing power."
    },
    discord: {
        name: "Plane of Discord",
        description: "Attuned to necessary conflict and competition",
        benefits: [
            "Combat Focus: +1 to attack rolls when outnumbered",
            "Tactical Mind: Bonus action to grant ally +2 to next attack",
            "Warrior's Resolve: Advantage on saves against fear when in combat"
        ],
        mechanics: "The eternal struggle sharpens your combat instincts and tactical awareness."
    }
};

const enhancedCharacterState = {
    planarAffinity: null,
    planarBenefits: [],
    showcaseMode: false
};

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    initializeEnhancedFeatures();
});

function initializeEnhancedFeatures() {
    setupPlanarAffinitySelection();
    setupShowcaseFeatures();
    setupCosmologyIntegration();
    setupEnhancedExport();
}

function setupPlanarAffinitySelection() {
    const planarOptions = document.querySelectorAll('.planar-option');
    planarOptions.forEach(option => {
        option.addEventListener('click', function() {
            const planeType = this.getAttribute('data-plane');
            selectPlanarAffinity(planeType);
        });
    });
}

function selectPlanarAffinity(planeType) {
    enhancedCharacterState.planarAffinity = planeType;
    
    document.querySelectorAll('.planar-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    const selectedOption = document.querySelector(`[data-plane="${planeType}"]`);
    if (selectedOption) {
        selectedOption.classList.add('selected');
    }
    
    updatePlanarBenefits(planeType);
}

function updatePlanarBenefits(planeType) {
    const benefitsDiv = document.getElementById('planar-benefits');
    if (benefitsDiv && PLANAR_AFFINITIES[planeType]) {
        const affinity = PLANAR_AFFINITIES[planeType];
        
        benefitsDiv.innerHTML = `
            <h4>Planar Benefits: ${affinity.name}</h4>
            <p class="affinity-description">${affinity.description}</p>
            <div class="benefits-list">
                <h5>Mechanical Benefits:</h5>
                <ul>
                    ${affinity.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
                </ul>
            </div>
            <p class="mechanics-note"><strong>Note:</strong> ${affinity.mechanics}</p>
        `;
        
        enhancedCharacterState.planarBenefits = affinity.benefits;
    }
}

function setupShowcaseFeatures() {
    const showcaseToggle = document.createElement('div');
    showcaseToggle.className = 'showcase-toggle';
    showcaseToggle.innerHTML = `
        <button id="showcase-mode-btn" class="showcase-btn">
            🎭 Showcase Mode
        </button>
    `;
    document.body.appendChild(showcaseToggle);
    
    document.getElementById('showcase-mode-btn').addEventListener('click', toggleShowcaseMode);
}

function toggleShowcaseMode() {
    enhancedCharacterState.showcaseMode = !enhancedCharacterState.showcaseMode;
    const btn = document.getElementById('showcase-mode-btn');
    
    if (enhancedCharacterState.showcaseMode) {
        btn.textContent = '🎮 Game Mode';
        btn.classList.add('active');
        populateShowcaseCharacter();
        showNotification('Showcase Mode: Displaying sample character for demonstration', 'info');
    } else {
        btn.textContent = '🎭 Showcase Mode';
        btn.classList.remove('active');
        resetCharacterCreation();
        showNotification('Game Mode: Ready for character creation', 'info');
    }
}

function populateShowcaseCharacter() {
    if (typeof characterState !== 'undefined') {
        characterState.characterName = 'Aeliana Starweaver';
        characterState.race = { id: 'elf', name: 'Elf' };
        characterState.class = { id: 'wizard', name: 'Wizard' };
        characterState.level = 8;
        characterState.abilityScores = {
            strength: 10,
            dexterity: 14,
            constitution: 13,
            intelligence: 18,
            wisdom: 12,
            charisma: 15
        };
        characterState.background = 'sage';
        characterState.alignment = 'Lawful Good';
        enhancedCharacterState.planarAffinity = 'celestial';
        
        characterState.selectedFeats = [
            { name: 'Elemental Adept', description: 'Mastery over elemental magic' },
            { name: 'Celestial Blessing', description: 'Blessed by celestial powers' }
        ];
        
        if (typeof updateDisplay === 'function') {
            updateDisplay();
        }
    }
}

function resetCharacterCreation() {
    if (typeof characterState !== 'undefined') {
        Object.keys(characterState).forEach(key => {
            if (key === 'abilityScores') {
                characterState[key] = {
                    strength: 10, dexterity: 10, constitution: 10,
                    intelligence: 10, wisdom: 10, charisma: 10
                };
            } else if (key === 'selectedFeats') {
                characterState[key] = [];
            } else if (key === 'level') {
                characterState[key] = 1;
            } else {
                characterState[key] = null;
            }
        });
        
        enhancedCharacterState.planarAffinity = null;
        enhancedCharacterState.planarBenefits = [];
        
        if (typeof updateDisplay === 'function') {
            updateDisplay();
        }
    }
}

function setupCosmologyIntegration() {
    document.addEventListener('planeSelected', function(event) {
        const planeData = event.detail;
        if (document.getElementById('character-creation').classList.contains('active')) {
            showPlaneIntegrationSuggestion(planeData);
        }
    });
    
    document.addEventListener('tabChanged', function(event) {
        if (event.detail.tab === 'cosmology') {
            setTimeout(() => {
                if (window.initializeCosmologyViewer) {
                    window.initializeCosmologyViewer();
                }
            }, 100);
        }
    });
}

function showPlaneIntegrationSuggestion(planeData) {
    const suggestion = document.createElement('div');
    suggestion.className = 'plane-suggestion';
    suggestion.innerHTML = `
        <div class="suggestion-content">
            <h4>Planar Connection Discovered!</h4>
            <p>You've explored <strong>${planeData.plane}</strong> in the cosmology viewer.</p>
            <p>Consider this plane for your character's background or planar affinity.</p>
            <button onclick="applyPlaneToCharacter('${planeData.type}')">Apply to Character</button>
            <button onclick="dismissSuggestion()">Dismiss</button>
        </div>
    `;
    
    document.body.appendChild(suggestion);
    setTimeout(() => suggestion.classList.add('show'), 100);
}

function applyPlaneToCharacter(planeType) {
    const planeMapping = {
        'elemental': 'fire',
        'celestial': 'celestial',
        'infernal': 'infernal',
        'primordial': 'order',
        'material': 'material'
    };
    
    const affinityType = planeMapping[planeType] || 'material';
    selectPlanarAffinity(affinityType);
    dismissSuggestion();
}

function dismissSuggestion() {
    const suggestion = document.querySelector('.plane-suggestion');
    if (suggestion) {
        suggestion.remove();
    }
}

function setupEnhancedExport() {
    const exportJsonBtn = document.getElementById('export-json');
    const exportPdfBtn = document.getElementById('export-pdf');
    const saveCharacterBtn = document.getElementById('save-character');
    
    if (exportJsonBtn) {
        exportJsonBtn.addEventListener('click', exportCharacterJSON);
    }
    
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', generateCharacterPDF);
    }
    
    if (saveCharacterBtn) {
        saveCharacterBtn.addEventListener('click', saveCharacterToGallery);
    }
}

function exportCharacterJSON() {
    const completeCharacter = {
        ...(typeof characterState !== 'undefined' ? characterState : {}),
        ...enhancedCharacterState,
        exportDate: new Date().toISOString(),
        systemVersion: "Decennium Descent v1.0"
    };
    
    const dataStr = JSON.stringify(completeCharacter, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${(typeof characterState !== 'undefined' && characterState.characterName) || 'character'}_decennium_descent.json`;
    link.click();
    
    URL.revokeObjectURL(url);
}

function generateCharacterPDF() {
    const printWindow = window.open('', '_blank');
    const characterSheet = generatePrintableSheet();
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>${(typeof characterState !== 'undefined' && characterState.characterName) || 'Character'} - Decennium Descent</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; color: #333; }
                .header { text-align: center; border-bottom: 2px solid #4fc3f7; padding-bottom: 20px; }
                .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
                .stat-item { padding: 10px; background: #f5f5f5; border-radius: 3px; }
                .planar-benefits { background: #e3f2fd; }
                @media print { body { margin: 0; } }
            </style>
        </head>
        <body>${characterSheet}</body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}

function generatePrintableSheet() {
    const character = typeof characterState !== 'undefined' ? characterState : {};
    const planarAffinity = enhancedCharacterState.planarAffinity ? 
        PLANAR_AFFINITIES[enhancedCharacterState.planarAffinity] : null;
    
    return `
        <div class="header">
            <h1>${character.characterName || 'Unnamed Character'}</h1>
            <h2>Decennium Descent Character Sheet</h2>
        </div>
        
        <div class="section">
            <h3>Basic Information</h3>
            <div class="stat-grid">
                <div class="stat-item"><strong>Race:</strong> ${character.race ? character.race.name : 'Not selected'}</div>
                <div class="stat-item"><strong>Class:</strong> ${character.class ? character.class.name : 'Not selected'}</div>
                <div class="stat-item"><strong>Level:</strong> ${character.level || 1}</div>
                <div class="stat-item"><strong>Background:</strong> ${character.background || 'Not selected'}</div>
                <div class="stat-item"><strong>Alignment:</strong> ${character.alignment || 'Not selected'}</div>
                <div class="stat-item"><strong>Planar Affinity:</strong> ${planarAffinity ? planarAffinity.name : 'None'}</div>
            </div>
        </div>
        
        ${planarAffinity ? `
        <div class="section planar-benefits">
            <h3>Planar Affinity: ${planarAffinity.name}</h3>
            <p>${planarAffinity.description}</p>
            <h4>Benefits:</h4>
            <ul>
                ${planarAffinity.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
            </ul>
            <p><em>${planarAffinity.mechanics}</em></p>
        </div>
        ` : ''}
        
        <div class="section">
            <p><em>Generated by Decennium Descent Character Creator - ${new Date().toLocaleDateString()}</em></p>
        </div>
    `;
}

function saveCharacterToGallery() {
    const character = {
        ...(typeof characterState !== 'undefined' ? characterState : {}),
        ...enhancedCharacterState,
        id: Date.now().toString(),
        createdAt: new Date().toISOString()
    };
    
    let savedCharacters = JSON.parse(localStorage.getItem('decenniumCharacters') || '[]');
    savedCharacters.push(character);
    localStorage.setItem('decenniumCharacters', JSON.stringify(savedCharacters));
    
    showNotification('Character saved to gallery!', 'success');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => notification.classList.add('show'), 100);
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

window.enhancedCharacterState = enhancedCharacterState;
window.PLANAR_AFFINITIES = PLANAR_AFFINITIES;