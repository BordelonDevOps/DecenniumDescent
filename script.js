// Global state management
const characterState = {
    race: null,
    subrace: null,
    class: null,
    level: 1,
    abilityScores: {
        strength: 10,
        dexterity: 10,
        constitution: 10,
        intelligence: 10,
        wisdom: 10,
        charisma: 10
    },
    abilityMethod: 'point-buy',
    abilityBoosts: {
        strength: 0,
        dexterity: 0,
        constitution: 0,
        intelligence: 0,
        wisdom: 0,
        charisma: 0
    },
    boostsRemaining: 4,
    selectedFeats: [],
    background: null,
    alignment: null,
    characterName: ''
};

// Current step tracking
let currentStep = 'race';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DEBUG: DOM Content Loaded - Initializing application');
    console.log('DEBUG: Initial characterState:', characterState);
    
    initializeCharacterBuilder();
    setupEventListeners();
    initializeTabNavigation();
    updateDisplay();
    
    console.log('DEBUG: Application initialization completed');
});

function initializeCharacterBuilder() {
    // Set up step navigation
    setupStepNavigation();
    
    // Initialize race options
    setupRaceSelection();
    
    // Initialize class options
    setupClassSelection();
    
    // Initialize ability scores
    setupAbilityScores();
    
    // Initialize feat system
    setupFeatSelection();
    
    // Initialize background selection
    setupBackgroundSelection();
    
    // Initialize alignment selection
    setupAlignmentSelection();
    
    // Show first step
    showStep('race');
}

function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            showTab(targetTab);
        });
    });
    
    // Character name input
    const nameInput = document.getElementById('character-name-input');
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            characterState.characterName = this.value;
            updateDisplay();
        });
    }
    
    // Ability method selection
    const methodSelect = document.getElementById('ability-method');
    if (methodSelect) {
        methodSelect.addEventListener('change', function() {
            characterState.abilityMethod = this.value;
            
            // Show/hide roll all button based on method
            const rollAllBtn = document.getElementById('roll-all-btn');
            if (rollAllBtn) {
                rollAllBtn.style.display = this.value === 'random-roll' ? 'inline-block' : 'none';
            }
            
            resetAbilityScores();
            updateDisplay();
        });
    }
    
    // Background selection
    const backgroundSelect = document.getElementById('background-select');
    if (backgroundSelect) {
        backgroundSelect.addEventListener('change', function() {
            characterState.background = this.value;
            updateDisplay();
        });
    }
    
    // Section navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.hasAttribute('data-next')) {
                const nextSection = this.getAttribute('data-next');
                navigateToSection(nextSection);
            } else if (this.hasAttribute('data-prev')) {
                const prevSection = this.getAttribute('data-prev');
                navigateToSection(prevSection);
            }
        });
    });
}

function navigateToSection(sectionName) {
    // Validate current section before moving
    if (!validateCurrentSection()) {
        return;
    }
    
    currentStep = sectionName;
    showStep(sectionName);
    updateDisplay();
}

function validateCurrentSection() {
    switch(currentStep) {
        case 'race':
            if (!characterState.race) {
                alert('Please select a race before continuing.');
                return false;
            }
            if (!characterState.class) {
                alert('Please select a class before continuing.');
                return false;
            }
            break;
        case 'abilities':
            if (characterState.abilityMethod === 'point-buy' && characterState.boostsRemaining > 0) {
                alert('Please allocate all ability boosts before continuing.');
                return false;
            }
            break;
        case 'background':
            if (!characterState.background) {
                alert('Please select a background before continuing.');
                return false;
            }
            break;
        case 'alignment':
            if (!characterState.alignment) {
                alert('Please select an alignment before continuing.');
                return false;
            }
            break;
    }
    return true;
}

function setupStepNavigation() {
    document.querySelectorAll('.step-item').forEach(step => {
        step.addEventListener('click', function() {
            const stepName = this.getAttribute('data-step');
            showStep(stepName);
        });
    });
}

function showStep(stepName) {
    currentStep = stepName;
    
    // Update step navigation
    document.querySelectorAll('.step-item').forEach(step => {
        step.classList.remove('active');
        if (step.getAttribute('data-step') === stepName) {
            step.classList.add('active');
        }
    });
    
    // Update input sections
    document.querySelectorAll('.input-section').forEach(section => {
        section.classList.remove('active');
    });
    
    const activeSection = document.getElementById(`${stepName}-section`);
    if (activeSection) {
        activeSection.classList.add('active');
    }
    
    // Update output sections
    document.querySelectorAll('.output-section').forEach(section => {
        section.classList.remove('active');
    });
    
    const activeOutput = document.getElementById(`${stepName}-output`);
    if (activeOutput) {
        activeOutput.classList.add('active');
    }
    
    updateDisplay();
}

function showTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
        if (content.id === tabName) {
            content.classList.add('active');
        }
    });
    
    // Initialize cosmology viewer when tab is activated
    if (tabName === 'cosmology') {
        setTimeout(() => {
            if (!window.cosmologyViewer) {
                window.cosmologyViewer = new CosmologyViewer('cosmology-canvas');
            }
            // Trigger resize to ensure proper canvas sizing
            if (window.cosmologyViewer && window.cosmologyViewer.resize) {
                window.cosmologyViewer.resize();
            }
        }, 100);
    }
    
    // Dispatch tab change event for other modules
    document.dispatchEvent(new CustomEvent('tabChanged', {
        detail: { tab: tabName }
    }));
}

// Race Selection
function setupRaceSelection() {
    // Add event listeners to existing race options
    document.querySelectorAll('.race-option').forEach(raceOption => {
        raceOption.addEventListener('click', function() {
            const raceId = this.getAttribute('data-race');
            const raceName = this.querySelector('.race-name').textContent;
            selectRace(raceId, raceName);
        });
    });
}

function selectRace(raceId, raceName) {
    console.log('DEBUG: selectRace called with:', { raceId, raceName });
    
    characterState.race = { id: raceId, name: raceName };
    characterState.subrace = null; // Reset subrace when race changes
    
    console.log('DEBUG: characterState.race set to:', characterState.race);
    console.log('DEBUG: RACES data for selected race:', RACES[raceId]);
    
    // Update UI
    document.querySelectorAll('.race-option').forEach(option => {
        option.classList.remove('selected');
        if (option.getAttribute('data-race') === raceId) {
            option.classList.add('selected');
        }
    });
    
    // Show subraces if available
    showSubraces(raceId);
    
    updateDisplay();
}

function showSubraces(raceId) {
    console.log('DEBUG: showSubraces called with raceId:', raceId);
    
    const subraceSelection = document.getElementById('subrace-selection');
    const subraceGrid = document.getElementById('subrace-grid');
    
    console.log('DEBUG: subraceSelection element:', subraceSelection);
    console.log('DEBUG: subraceGrid element:', subraceGrid);
    
    if (RACES[raceId] && RACES[raceId].subraces) {
        const subraces = RACES[raceId].subraces;
        console.log('DEBUG: Found subraces for race:', subraces);
        
        // Clear existing subraces
        subraceGrid.innerHTML = '';
        
        // Add subrace options
        Object.keys(subraces).forEach(subraceKey => {
            const subrace = subraces[subraceKey];
            console.log('DEBUG: Creating subrace option for:', { subraceKey, subrace });
            
            const subraceOption = document.createElement('div');
            subraceOption.className = 'variant-option';
            subraceOption.setAttribute('data-subrace', subraceKey);
            subraceOption.textContent = subrace.name;
            
            subraceOption.addEventListener('click', function() {
                selectSubrace(subraceKey, subrace.name);
            });
            
            subraceGrid.appendChild(subraceOption);
        });
        
        subraceSelection.style.display = 'block';
        console.log('DEBUG: Subrace selection shown');
    } else {
        console.log('DEBUG: No subraces found for race:', raceId);
        console.log('DEBUG: RACES[raceId]:', RACES[raceId]);
        console.log('DEBUG: RACES[raceId].subraces:', RACES[raceId] ? RACES[raceId].subraces : 'Race not found');
        
        subraceSelection.style.display = 'none';
        // If no subraces, proceed to class selection
        showClassSelection();
    }
}

function selectSubrace(subraceId, subraceName) {
    console.log('DEBUG: selectSubrace called with:', { subraceId, subraceName });
    
    characterState.subrace = { id: subraceId, name: subraceName };
    
    console.log('DEBUG: characterState.subrace set to:', characterState.subrace);
    console.log('DEBUG: Full characterState:', characterState);
    
    // Update UI
    document.querySelectorAll('.variant-option').forEach(option => {
        option.classList.remove('selected');
        if (option.getAttribute('data-subrace') === subraceId) {
            option.classList.add('selected');
            console.log('DEBUG: Selected subrace option in UI:', option);
        }
    });
    
    // Show class selection after subrace is chosen
    showClassSelection();
    
    updateDisplay();
}



// Class Selection
function setupClassSelection() {
    // Add event listeners to existing class options
    document.querySelectorAll('.class-option').forEach(classOption => {
        classOption.addEventListener('click', function() {
            const classId = this.getAttribute('data-class');
            const className = this.querySelector('.class-name').textContent;
            selectClass(classId, className);
        });
    });
    
    // Level selection
    const levelInput = document.getElementById('character-level');
    if (levelInput) {
        levelInput.addEventListener('change', function() {
            characterState.level = parseInt(this.value) || 1;
            updateDisplay();
        });
    }
}

function selectClass(classId, className) {
    characterState.class = { id: classId, name: className };
    
    // Update UI
    document.querySelectorAll('.class-option').forEach(option => {
        option.classList.remove('selected');
        if (option.getAttribute('data-class') === classId) {
            option.classList.add('selected');
        }
    });
    
    updateDisplay();
}

// Ability Scores
function setupAbilityScores() {
    // Add event listeners to score buttons
    document.querySelectorAll('.score-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const ability = this.getAttribute('data-ability');
            const action = this.getAttribute('data-action');
            const change = action === 'increase' ? 1 : -1;
            changeAbilityScore(ability, change);
        });
    });
    
    // Add event listeners to score inputs
    const scoreInputs = ['str-score', 'dex-score', 'con-score', 'int-score', 'wis-score', 'cha-score'];
    const abilityMap = {
        'str-score': 'strength',
        'dex-score': 'dexterity', 
        'con-score': 'constitution',
        'int-score': 'intelligence',
        'wis-score': 'wisdom',
        'cha-score': 'charisma'
    };
    
    scoreInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            input.addEventListener('change', function() {
                const ability = abilityMap[inputId];
                const value = parseInt(this.value) || 8;
                
                if (characterState.abilityMethod === 'random-roll') {
                    characterState.abilityScores[ability] = Math.max(3, Math.min(18, value));
                } else if (characterState.abilityMethod === 'point-buy') {
                    // PF2e point buy: scores can only be 10 or 12
                    const validScores = [10, 12];
                    const newScore = validScores.includes(value) ? value : 10;
                    characterState.abilityScores[ability] = newScore;
                    characterState.abilityBoosts[ability] = newScore === 12 ? 1 : 0;
                } else {
                    characterState.abilityScores[ability] = Math.max(8, Math.min(15, value));
                }
                updateAbilityScores();
            });
        }
    });
    
    // Add event listener to roll all button
    const rollAllBtn = document.getElementById('roll-all-btn');
    if (rollAllBtn) {
        rollAllBtn.addEventListener('click', function() {
            rollAllAbilityScores();
        });
    }
}

function changeAbilityScore(ability, change) {
    if (characterState.abilityMethod === 'point-buy') {
        const currentBoosts = characterState.abilityBoosts[ability];
        const newBoosts = currentBoosts + change;
        
        // In PF2e, you can only have 0 or 1 boost per ability during character creation
        if (newBoosts >= 0 && newBoosts <= 1) {
            const boostDifference = newBoosts - currentBoosts;
            
            if (characterState.boostsRemaining >= boostDifference) {
                characterState.abilityBoosts[ability] = newBoosts;
                characterState.boostsRemaining -= boostDifference;
                
                // Update the actual ability score (base 10 + 2 per boost)
                characterState.abilityScores[ability] = 10 + (newBoosts * 2);
                updateAbilityScores();
            }
        }
    } else if (characterState.abilityMethod === 'random-roll') {
        // Random roll method allows wider range (3-18)
        const newScore = Math.max(3, Math.min(18, characterState.abilityScores[ability] + change));
        characterState.abilityScores[ability] = newScore;
        updateAbilityScores();
    } else {
        // Standard array or manual (8-15 range)
        const newScore = Math.max(8, Math.min(15, characterState.abilityScores[ability] + change));
        characterState.abilityScores[ability] = newScore;
        updateAbilityScores();
    }
}

function resetAbilityScores() {
    if (characterState.abilityMethod === 'point-buy') {
        // Reset all ability scores to 10 and boosts to 0
        Object.keys(characterState.abilityScores).forEach(ability => {
            characterState.abilityScores[ability] = 10;
            characterState.abilityBoosts[ability] = 0;
        });
        characterState.boostsRemaining = 4;
    } else if (characterState.abilityMethod === 'standard-array') {
        const standardArray = [15, 14, 13, 12, 10, 8];
        const abilities = Object.keys(characterState.abilityScores);
        abilities.forEach((ability, index) => {
            characterState.abilityScores[ability] = standardArray[index] || 10;
        });
    } else if (characterState.abilityMethod === 'random-roll') {
        // Set all scores to 10 initially for random roll method
        Object.keys(characterState.abilityScores).forEach(ability => {
            characterState.abilityScores[ability] = 10;
        });
    }
    updateAbilityScores();
}

function rollAllAbilityScores() {
    if (characterState.abilityMethod === 'random-roll') {
        Object.keys(characterState.abilityScores).forEach(ability => {
            characterState.abilityScores[ability] = rollAbilityScore();
        });
        updateAbilityScores();
        updateDisplay();
    }
}

function updateAbilityScores() {
    const abilityMap = {
        'strength': { input: 'str-score', modifier: 'str-mod' },
        'dexterity': { input: 'dex-score', modifier: 'dex-mod' },
        'constitution': { input: 'con-score', modifier: 'con-mod' },
        'intelligence': { input: 'int-score', modifier: 'int-mod' },
        'wisdom': { input: 'wis-score', modifier: 'wis-mod' },
        'charisma': { input: 'cha-score', modifier: 'cha-mod' }
    };
    
    Object.keys(characterState.abilityScores).forEach(ability => {
        const score = characterState.abilityScores[ability];
        const modifier = Math.floor((score - 10) / 2);
        
        const scoreInput = document.getElementById(abilityMap[ability].input);
        const modifierSpan = document.getElementById(abilityMap[ability].modifier);
        
        if (scoreInput) {
            scoreInput.value = score;
            // Set min/max based on ability method
            if (characterState.abilityMethod === 'random-roll') {
                scoreInput.min = 3;
                scoreInput.max = 18;
            } else if (characterState.abilityMethod === 'point-buy') {
                // PF2e point buy: only 10 or 12 allowed
                scoreInput.min = 10;
                scoreInput.max = 12;
                scoreInput.step = 2;
            } else {
                scoreInput.min = 8;
                scoreInput.max = 15;
            }
        }
        if (modifierSpan) {
            modifierSpan.textContent = modifier >= 0 ? `+${modifier}` : `${modifier}`;
        }
    });
    
    const pointsDisplay = document.getElementById('points-left');
    if (pointsDisplay && characterState.abilityMethod === 'point-buy') {
        pointsDisplay.textContent = characterState.boostsRemaining;
    }
    
    updateDisplay();
}

// Feat Selection
function setupFeatSelection() {
    // Load feats from game-data.js and organize by category
    window.featsData = {
        all: [],
        general: [],
        combat: [],
        magic: [],
        skill: []
    };
    
    // Convert FEATS object to categorized arrays
    if (typeof FEATS !== 'undefined') {
        Object.keys(FEATS).forEach(featKey => {
            const feat = {
                name: FEATS[featKey].name,
                description: FEATS[featKey].description,
                effect: FEATS[featKey].effect,
                prerequisite: FEATS[featKey].prerequisite || "None",
                type: FEATS[featKey].type || "general"
            };
            
            // Add to all feats
            window.featsData.all.push(feat);
            
            // Add to specific category
            const category = feat.type;
            if (window.featsData[category]) {
                window.featsData[category].push(feat);
            } else {
                window.featsData.general.push(feat);
            }
        });
    }
    
    setupFeatCategories();
    setupFeatSearch();
    displayFeats('all');
}

function setupFeatCategories() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            // Display feats for selected category
            const category = button.dataset.category;
            displayFeats(category);
            // Clear search when switching categories
            const searchInput = document.getElementById('feat-search');
            if (searchInput) {
                searchInput.value = '';
            }
        });
    });
}

function setupFeatSearch() {
    const searchInput = document.getElementById('feat-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            filterFeats(searchTerm);
        });
    }
}

function displayFeats(category) {
    const featGrid = document.querySelector('.feat-grid');
    if (!featGrid || !window.featsData[category]) return;
    
    featGrid.innerHTML = '';
    
    window.featsData[category].forEach(feat => {
        const featItem = document.createElement('div');
        featItem.className = 'feat-item';
        featItem.setAttribute('data-feat-name', feat.name);
        
        featItem.innerHTML = `
            <div class="feat-name">${feat.name}</div>
            <div class="feat-description">${feat.description}</div>
        `;
        
        featItem.addEventListener('click', function() {
            toggleFeatSelection(feat);
        });
        
        // Check if feat is already selected
        if (characterState.selectedFeats.some(f => f.name === feat.name)) {
            featItem.classList.add('selected');
        }
        
        featGrid.appendChild(featItem);
    });
}

function toggleFeatSelection(feat) {
    const existingIndex = characterState.selectedFeats.findIndex(f => f.name === feat.name);
    
    if (existingIndex >= 0) {
        // Remove feat
        characterState.selectedFeats.splice(existingIndex, 1);
    } else {
        // Add feat
        characterState.selectedFeats.push(feat);
    }
    
    // Update UI
    const featItem = document.querySelector(`[data-feat-name="${feat.name}"]`);
    if (featItem) {
        featItem.classList.toggle('selected');
    }
    
    updateDisplay();
}

function filterFeats(searchTerm) {
    document.querySelectorAll('.feat-item').forEach(item => {
        const featName = item.querySelector('.feat-name').textContent.toLowerCase();
        const featDesc = item.querySelector('.feat-description').textContent.toLowerCase();
        
        if (featName.includes(searchTerm) || featDesc.includes(searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Background Selection
function setupBackgroundSelection() {
    const backgrounds = [
        { name: 'Acolyte', id: 'acolyte' },
        { name: 'Criminal', id: 'criminal' },
        { name: 'Folk Hero', id: 'folk-hero' },
        { name: 'Noble', id: 'noble' },
        { name: 'Sage', id: 'sage' },
        { name: 'Soldier', id: 'soldier' }
    ];
    
    const backgroundSelect = document.getElementById('background-select');
    if (backgroundSelect) {
        backgroundSelect.innerHTML = '<option value="">Select Background...</option>';
        backgrounds.forEach(bg => {
            const option = document.createElement('option');
            option.value = bg.id;
            option.textContent = bg.name;
            backgroundSelect.appendChild(option);
        });
    }
}

// Alignment Selection
function setupAlignmentSelection() {
    const alignments = [
        'Lawful Good', 'Neutral Good', 'Chaotic Good',
        'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
        'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'
    ];
    
    const alignmentGrid = document.querySelector('.alignment-grid');
    if (alignmentGrid) {
        alignmentGrid.innerHTML = '';
        alignments.forEach(alignment => {
            const alignmentOption = document.createElement('div');
            alignmentOption.className = 'alignment-option';
            alignmentOption.setAttribute('data-alignment', alignment);
            alignmentOption.textContent = alignment;
            
            alignmentOption.addEventListener('click', function() {
                selectAlignment(alignment);
            });
            
            alignmentGrid.appendChild(alignmentOption);
        });
    }
}

function selectAlignment(alignment) {
    characterState.alignment = alignment;
    
    // Update UI
    document.querySelectorAll('.alignment-option').forEach(option => {
        option.classList.remove('selected');
        if (option.getAttribute('data-alignment') === alignment) {
            option.classList.add('selected');
        }
    });
    
    updateDisplay();
}

// Display Updates
function updateDisplay() {
    console.log('DEBUG: updateDisplay called');
    console.log('DEBUG: Current characterState:', JSON.stringify(characterState, null, 2));
    
    updateRaceOutput();
    updateClassOutput();
    updateQualifyingFeats();
    updateSelectedFeats();
    updateBackgroundOutput();
    updateAlignmentOutput();
    updateCharacterSummary();
    updateFinalStats();
    
    console.log('DEBUG: updateDisplay completed');
}

function updateRaceOutput() {
    console.log('DEBUG: updateRaceOutput called');
    console.log('DEBUG: characterState in updateRaceOutput:', characterState);
    
    const raceDetails = document.querySelector('#race-output .race-details');
    console.log('DEBUG: raceDetails element:', raceDetails);
    
    if (raceDetails) {
        if (characterState.race) {
            console.log('DEBUG: Race selected:', characterState.race);
            const raceData = RACES[characterState.race.id];
            console.log('DEBUG: Race data found:', raceData);
            
            if (raceData) {
                let output = `
                    <h4>${raceData.name}</h4>
                    <p class="race-description">${raceData.description}</p>
                    
                    <div class="race-stats">
                        <p><strong>Size:</strong> ${raceData.size}</p>
                        <p><strong>Speed:</strong> ${raceData.speed} feet</p>
                        ${raceData.swimSpeed ? `<p><strong>Swim Speed:</strong> ${raceData.swimSpeed} feet</p>` : ''}
                        <p><strong>Languages:</strong> ${raceData.languages.join(', ')}</p>
                    </div>
                    
                    <div class="ability-increases">
                        <h5>Ability Score Increases</h5>
                        <ul>
                `;
                
                // Display base ability score increases
                Object.entries(raceData.abilityScoreIncrease).forEach(([ability, increase]) => {
                    output += `<li>${ability.charAt(0).toUpperCase() + ability.slice(1)}: +${increase}</li>`;
                });
                
                output += `
                        </ul>
                    </div>
                    
                    <div class="racial-traits">
                        <h5>Racial Traits</h5>
                        <ul>
                `;
                
                // Display racial traits
                raceData.traits.forEach(trait => {
                    output += `<li>${trait}</li>`;
                });
                
                output += `
                        </ul>
                    </div>
                `;
                
                // Display subrace information if selected
                console.log('DEBUG: Checking subrace - characterState.subrace:', characterState.subrace);
                console.log('DEBUG: raceData.subraces:', raceData.subraces);
                
                if (characterState.subrace && raceData.subraces && raceData.subraces[characterState.subrace.id]) {
                    const subraceData = raceData.subraces[characterState.subrace.id];
                    console.log('DEBUG: Subrace data found:', subraceData);
                    
                    output += `
                        <div class="subrace-info">
                            <h5>${subraceData.name}</h5>
                            <p class="subrace-description">${subraceData.description}</p>
                    `;
                    
                    // Subrace ability score increases
                    if (subraceData.abilityScoreIncrease) {
                        output += `
                            <div class="subrace-abilities">
                                <strong>Additional Ability Increases:</strong>
                                <ul>
                        `;
                        Object.entries(subraceData.abilityScoreIncrease).forEach(([ability, increase]) => {
                            output += `<li>${ability.charAt(0).toUpperCase() + ability.slice(1)}: +${increase}</li>`;
                        });
                        output += `</ul></div>`;
                    }
                    
                    // Subrace traits
                    if (subraceData.traits) {
                        output += `
                            <div class="subrace-traits">
                                <strong>Subrace Traits:</strong>
                                <ul>
                        `;
                        subraceData.traits.forEach(trait => {
                            output += `<li>${trait}</li>`;
                        });
                        output += `</ul></div>`;
                    }
                    
                    // Damage resistance
                    if (subraceData.damageResistance) {
                        output += `<p><strong>Damage Resistance:</strong> ${subraceData.damageResistance}</p>`;
                    }
                    
                    // Breath weapon
                    if (subraceData.breathWeapon) {
                        output += `<p><strong>Breath Weapon:</strong> ${subraceData.breathWeapon}</p>`;
                    }
                    
                    output += `</div>`;
                } else {
                    console.log('DEBUG: No subrace to display or subrace data not found');
                    if (characterState.subrace) {
                        console.log('DEBUG: Subrace exists but data missing for:', characterState.subrace.id);
                    }
                }
                
                console.log('DEBUG: Final output HTML:', output);
                raceDetails.innerHTML = output;
            } else {
                console.log('DEBUG: Race data not found for:', characterState.race.id);
                raceDetails.innerHTML = `<h4>${characterState.race.name}</h4><p>Race data not found.</p>`;
            }
        } else {
            console.log('DEBUG: No race selected');
            raceDetails.innerHTML = '<p>Select a race to see its details and traits.</p>';
        }
    } else {
        console.log('DEBUG: raceDetails element not found');
    }
}

function updateClassOutput() {
    const classDetails = document.querySelector('#class-output .class-details');
    if (classDetails) {
        if (characterState.class) {
            const classData = CLASSES[characterState.class.id];
            if (classData) {
                let html = `
                    <div class="class-description">
                        <h4>${characterState.class.name} (Level ${characterState.level})</h4>
                        <p>${classData.description}</p>
                    </div>
                    <div class="class-stats">
                        <p><strong>Hit Die:</strong> d${classData.hitDie}</p>
                        <p><strong>Primary Ability:</strong> ${classData.primaryAbility.join(' and ')}</p>
                        <p><strong>Saving Throws:</strong> ${classData.savingThrows.join(', ')}</p>
                    </div>
                    <div class="class-proficiencies">
                        <p><strong>Armor:</strong> ${classData.armorProficiency ? classData.armorProficiency.join(', ') : 'None'}</p>
                        <p><strong>Weapons:</strong> ${classData.weaponProficiency ? classData.weaponProficiency.join(', ') : 'None'}</p>
                        <p><strong>Skills:</strong> Choose ${classData.skillChoices || 0} from ${classData.skillList.includes('Any') ? 'any skills' : classData.skillList.join(', ')}</p>
                    </div>
                `;
                
                if (classData.spellcasting) {
                    html += `
                        <div class="class-spellcasting">
                            <p><strong>Spellcasting:</strong> ${classData.spellcasting.ability}-based spellcaster</p>
                        </div>
                    `;
                }
                
                if (classData.features && classData.features[1]) {
                    html += `
                        <div class="class-features">
                            <p><strong>1st Level Features:</strong> ${classData.features[1].join(', ')}</p>
                        </div>
                    `;
                }
                
                classDetails.innerHTML = html;
            } else {
                classDetails.innerHTML = `
                    <h4>${characterState.class.name} (Level ${characterState.level})</h4>
                    <p>Class details not available.</p>
                `;
            }
        } else {
            classDetails.innerHTML = '<p>Select a class to see its features and proficiencies.</p>';
        }
    }
}

function updateQualifyingFeats() {
    const qualifyingFeats = document.querySelector('#abilities-output .qualifying-feats');
    if (qualifyingFeats) {
        const qualifiedFeats = getQualifyingFeats();
        
        if (qualifiedFeats.length > 0) {
            qualifyingFeats.innerHTML = `
                <h4>Qualifying Feats</h4>
                ${qualifiedFeats.map(feat => `
                    <div class="qualifying-feat">
                        <div class="qualifying-feat-name">${feat.name}</div>
                        <div class="qualifying-feat-desc">${feat.description}</div>
                    </div>
                `).join('')}
            `;
        } else {
            qualifyingFeats.innerHTML = '<h4>Qualifying Feats</h4><p>Set your ability scores to see which feats you qualify for.</p>';
        }
    }
}

function updateSelectedFeats() {
    const selectedFeats = document.querySelector('#feats-output .selected-feats');
    if (selectedFeats) {
        if (characterState.selectedFeats.length > 0) {
            selectedFeats.innerHTML = `
                <h4>Selected Feats</h4>
                ${characterState.selectedFeats.map(feat => `
                    <div class="selected-feat">
                        <div class="selected-feat-name">${feat.name}</div>
                        <div class="selected-feat-desc">${feat.effect}</div>
                        <button class="remove-feat" onclick="removeFeat('${feat.name}')">×</button>
                    </div>
                `).join('')}
            `;
        } else {
            selectedFeats.innerHTML = '<h4>Selected Feats</h4><p>No feats selected yet. Choose feats from the left panel.</p>';
        }
    }
}

function updateBackgroundOutput() {
    const backgroundDetails = document.querySelector('#background-output .background-details');
    if (backgroundDetails) {
        if (characterState.background) {
            backgroundDetails.innerHTML = `
                <h4>${getBackgroundName(characterState.background)}</h4>
                <p><strong>Skill Proficiencies:</strong> ${getBackgroundSkills(characterState.background)}</p>
                <p><strong>Languages:</strong> ${getBackgroundLanguages(characterState.background)}</p>
                <p><strong>Equipment:</strong> ${getBackgroundEquipment(characterState.background)}</p>
                <p><strong>Feature:</strong> ${getBackgroundFeature(characterState.background)}</p>
            `;
        } else {
            backgroundDetails.innerHTML = '<p>Select a background to see its benefits and features.</p>';
        }
    }
}

function updateAlignmentOutput() {
    const alignmentEffects = document.querySelector('#alignment-output .alignment-effects');
    if (alignmentEffects) {
        if (characterState.alignment) {
            alignmentEffects.innerHTML = `
                <h4>${characterState.alignment}</h4>
                <p><strong>Moral Compass:</strong> ${getAlignmentDescription(characterState.alignment)}</p>
                <p><strong>Roleplay Guidelines:</strong> ${getAlignmentRoleplay(characterState.alignment)}</p>
                <p><strong>Divine Relations:</strong> ${getAlignmentDivine(characterState.alignment)}</p>
            `;
        } else {
            alignmentEffects.innerHTML = '<p>Select an alignment to see how it affects your character.</p>';
        }
    }
}

function updateCharacterSummary() {
    const characterOverview = document.querySelector('#summary-output .character-overview');
    if (characterOverview) {
        let raceDisplay = 'Not selected';
        if (characterState.race) {
            raceDisplay = characterState.race.name;
            if (characterState.subrace) {
                raceDisplay += ` (${characterState.subrace.name})`;
            }
        }
        
        characterOverview.innerHTML = `
            <h4>Character Overview</h4>
            <p><strong>Name:</strong> ${characterState.characterName || 'Unnamed Character'}</p>
            <p><strong>Race:</strong> ${raceDisplay}</p>
            <p><strong>Class:</strong> ${characterState.class ? `${characterState.class.name} (Level ${characterState.level})` : 'Not selected'}</p>
            <p><strong>Background:</strong> ${characterState.background ? getBackgroundName(characterState.background) : 'Not selected'}</p>
            <p><strong>Alignment:</strong> ${characterState.alignment || 'Not selected'}</p>
            <p><strong>Selected Feats:</strong> ${characterState.selectedFeats.length > 0 ? characterState.selectedFeats.map(f => f.name).join(', ') : 'None'}</p>
        `;
    }
}

function updateFinalStats() {
    const completeSheet = document.querySelector('#final-output .complete-sheet');
    if (completeSheet) {
        const hp = calculateHP();
        const ac = calculateAC();
        const initiative = getAbilityModifier('dexterity');
        
        completeSheet.innerHTML = `
            <div class="stat-group">
                <h4>Core Stats</h4>
                <div class="stat-item">
                    <span class="stat-label">Armor Class</span>
                    <span class="stat-value">${ac}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Hit Points</span>
                    <span class="stat-value">${hp}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Initiative</span>
                    <span class="stat-value">${initiative >= 0 ? '+' : ''}${initiative}</span>
                </div>
            </div>
            
            <div class="stat-group">
                <h4>Ability Scores</h4>
                ${Object.entries(characterState.abilityScores).map(([ability, score]) => {
                    const modifier = getAbilityModifier(ability);
                    return `
                        <div class="stat-item">
                            <span class="stat-label">${ability.charAt(0).toUpperCase() + ability.slice(1)}</span>
                            <span class="stat-value">${score} (${modifier >= 0 ? '+' : ''}${modifier})</span>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }
}

// Helper Functions
function getQualifyingFeats() {
    const qualifiedFeats = [];
    
    // Check all feats for prerequisites
    Object.values(window.featsData || {}).forEach(category => {
        category.forEach(feat => {
            if (meetsPrerequisites(feat)) {
                qualifiedFeats.push(feat);
            }
        });
    });
    
    return qualifiedFeats;
}

function meetsPrerequisites(feat) {
    if (!feat.prerequisite || feat.prerequisite === 'None') return true;
    
    // Simple prerequisite checking
    if (feat.prerequisite.includes('Strength 13')) {
        return characterState.abilityScores.strength >= 13;
    }
    if (feat.prerequisite.includes('Dexterity 13')) {
        return characterState.abilityScores.dexterity >= 13;
    }
    if (feat.prerequisite.includes('Intelligence or Wisdom 13')) {
        return characterState.abilityScores.intelligence >= 13 || characterState.abilityScores.wisdom >= 13;
    }
    
    return true;
}

function removeFeat(featName) {
    const index = characterState.selectedFeats.findIndex(f => f.name === featName);
    if (index >= 0) {
        characterState.selectedFeats.splice(index, 1);
        
        // Update feat item UI
        const featItem = document.querySelector(`[data-feat-name="${featName}"]`);
        if (featItem) {
            featItem.classList.remove('selected');
        }
        
        updateDisplay();
    }
}

function getAbilityModifier(ability) {
    return Math.floor((characterState.abilityScores[ability] - 10) / 2);
}

function calculateHP() {
    if (!characterState.class) return 10;
    
    const hitDie = getClassHitDie(characterState.class.id);
    const conModifier = getAbilityModifier('constitution');
    
    // First level gets max hit die + con modifier
    // Additional levels get average of hit die + con modifier
    const firstLevelHP = hitDie + conModifier;
    const additionalLevels = characterState.level - 1;
    const averageHitDie = Math.floor(hitDie / 2) + 1;
    const additionalHP = additionalLevels * (averageHitDie + conModifier);
    
    return Math.max(1, firstLevelHP + additionalHP);
}

function calculateAC() {
    // Base AC (10 + Dex modifier)
    return 10 + getAbilityModifier('dexterity');
}

function getClassHitDie(classId) {
    if (CLASSES[classId] && CLASSES[classId].hitDie) {
        return CLASSES[classId].hitDie;
    }
    return 8;
}

function getClassPrimaryAbility(classId) {
    if (CLASSES[classId] && CLASSES[classId].primaryAbility) {
        return CLASSES[classId].primaryAbility.join(' and ');
    }
    return 'Varies';
}

function getClassSavingThrows(classId) {
    if (CLASSES[classId] && CLASSES[classId].savingThrows) {
        return CLASSES[classId].savingThrows.join(', ');
    }
    return 'Varies';
}

function getClassSkills(classId) {
    if (CLASSES[classId] && CLASSES[classId].skillList) {
        if (CLASSES[classId].skillList.includes('Any')) {
            return `Choose ${CLASSES[classId].skillChoices || 'any'} skills of your choice`;
        }
        return CLASSES[classId].skillList.join(', ');
    }
    return 'Varies';
}

function getBackgroundName(backgroundId) {
    const names = {
        'acolyte': 'Acolyte', 'criminal': 'Criminal', 'folk-hero': 'Folk Hero',
        'noble': 'Noble', 'sage': 'Sage', 'soldier': 'Soldier'
    };
    return names[backgroundId] || backgroundId;
}

function getBackgroundSkills(backgroundId) {
    const skills = {
        'acolyte': 'Insight, Religion',
        'criminal': 'Deception, Stealth',
        'folk-hero': 'Animal Handling, Survival',
        'noble': 'History, Persuasion',
        'sage': 'Arcana, History',
        'soldier': 'Athletics, Intimidation'
    };
    return skills[backgroundId] || 'Varies';
}

function getBackgroundLanguages(backgroundId) {
    const languages = {
        'acolyte': 'Two of your choice',
        'criminal': 'One of your choice',
        'folk-hero': 'One of your choice',
        'noble': 'One of your choice',
        'sage': 'Two of your choice',
        'soldier': 'One of your choice'
    };
    return languages[backgroundId] || 'Varies';
}

function getBackgroundEquipment(backgroundId) {
    const equipment = {
        'acolyte': 'Holy symbol, prayer book, incense, vestments, common clothes, belt pouch with 15 gp',
        'criminal': 'Crowbar, dark common clothes with hood, belt pouch with 15 gp',
        'folk-hero': 'Artisan tools, shovel, iron pot, common clothes, belt pouch with 10 gp',
        'noble': 'Fine clothes, signet ring, scroll of pedigree, purse with 25 gp',
        'sage': 'Bottle of black ink, quill, small knife, letter from colleague, common clothes, belt pouch with 10 gp',
        'soldier': 'Insignia of rank, trophy, deck of cards, common clothes, belt pouch with 10 gp'
    };
    return equipment[backgroundId] || 'Varies';
}

function getBackgroundFeature(backgroundId) {
    const features = {
        'acolyte': 'Shelter of the Faithful',
        'criminal': 'Criminal Contact',
        'folk-hero': 'Rustic Hospitality',
        'noble': 'Position of Privilege',
        'sage': 'Researcher',
        'soldier': 'Military Rank'
    };
    return features[backgroundId] || 'Varies';
}

function getAlignmentDescription(alignment) {
    const descriptions = {
        'Lawful Good': 'Acts with compassion and honor, always trying to do the right thing.',
        'Neutral Good': 'Does good without bias for or against order.',
        'Chaotic Good': 'Acts as conscience directs, with little regard for expectations.',
        'Lawful Neutral': 'Acts in accordance with law, tradition, or personal codes.',
        'True Neutral': 'Prefers to steer clear of moral questions and doesn\'t take sides.',
        'Chaotic Neutral': 'Follows whims, holding personal freedom above all else.',
        'Lawful Evil': 'Methodically takes what they want within the limits of a code.',
        'Neutral Evil': 'Does whatever they can get away with, without compassion or qualms.',
        'Chaotic Evil': 'Acts with arbitrary violence, spurred by greed, hatred, or bloodlust.'
    };
    return descriptions[alignment] || 'Unknown alignment';
}

function getAlignmentRoleplay(alignment) {
    const roleplay = {
        'Lawful Good': 'Upholds justice, protects the innocent, keeps promises.',
        'Neutral Good': 'Helps others when possible, avoids unnecessary harm.',
        'Chaotic Good': 'Rebels against unjust authority, values freedom and kindness.',
        'Lawful Neutral': 'Follows rules and traditions, maintains order.',
        'True Neutral': 'Seeks balance, avoids extremes, adapts to situations.',
        'Chaotic Neutral': 'Unpredictable, values personal freedom above all.',
        'Lawful Evil': 'Uses rules and hierarchy to gain power and control.',
        'Neutral Evil': 'Selfish and cruel, but not necessarily destructive.',
        'Chaotic Evil': 'Destructive and violent, spreads misery and chaos.'
    };
    return roleplay[alignment] || 'Varies';
}

function getAlignmentDivine(alignment) {
    const divine = {
        'Lawful Good': 'Favored by celestials and good deities.',
        'Neutral Good': 'Welcomed by most good-aligned divine beings.',
        'Chaotic Good': 'Appreciated by freedom-loving celestials.',
        'Lawful Neutral': 'Respected by lawful deities regardless of moral stance.',
        'True Neutral': 'Maintains balance between all divine forces.',
        'Chaotic Neutral': 'Unpredictable relationship with divine beings.',
        'Lawful Evil': 'May serve devils or lawful evil deities.',
        'Neutral Evil': 'Attracts attention from evil entities.',
        'Chaotic Evil': 'Favored by demons and chaotic evil deities.'
    };
    return divine[alignment] || 'Varies';
}

// Enhanced Tab Navigation for Cosmology Integration
function initializeTabNavigation() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            showTab(targetTab);
        });
    });
}