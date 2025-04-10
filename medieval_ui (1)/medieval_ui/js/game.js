/**
 * Game functionality for Medieval Fantasy UI
 * Handles game state, UI updates, and directional control pad
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize game state
    initGameState();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize mini-map
    initMiniMap();
    
    // Initialize chat filters
    initChatFilters();
    
    // Initialize directional control pad
    initDirectionalPad();
    
    // Simulate some combat log entries
    simulateCombatLog();
});

/**
 * Game state object
 */
const gameState = {
    party: [
        { name: 'Sir Gawain', class: 'warrior', life: 80, mana: 60, melee: 90, battleTimer: 75 },
        { name: 'Lady Elara', class: 'cleric', life: 90, mana: 70, melee: 50, battleTimer: 60 },
        { name: 'Magus Thorne', class: 'wizard', life: 60, mana: 90, melee: 30, battleTimer: 85 },
        { name: 'Vex Shadowstep', class: 'rogue', life: 70, mana: 50, melee: 80, battleTimer: 95 },
        { name: 'Lyric Songweaver', class: 'bard', life: 85, mana: 75, melee: 60, battleTimer: 50 },
        { name: 'Willow Oakenheart', class: 'druid', life: 75, mana: 80, melee: 40, battleTimer: 30 }
    ],
    enemy: {
        name: 'Ancient Lich',
        life: 70,
        battleTimer: 40
    },
    activeMember: 0,
    turnOrder: ['Sir Gawain', 'Ancient Lich', 'Lady Elara', 'Vex Shadowstep', 'Magus Thorne', 'Lyric Songweaver', 'Willow Oakenheart'],
    currentTurn: 0,
    playerPosition: {
        x: 5,
        y: 5
    },
    mapSize: 10
};

/**
 * Initialize game state
 */
function initGameState() {
    // Update party member displays
    updatePartyDisplay();
    
    // Update enemy display
    updateEnemyDisplay();
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Battle menu buttons
    const battleButtons = document.querySelectorAll('.battle-btn');
    battleButtons.forEach(button => {
        button.addEventListener('click', handleBattleAction);
    });
    
    // Party member selection
    const partyMembers = document.querySelectorAll('.party-member');
    partyMembers.forEach((member, index) => {
        member.addEventListener('click', () => {
            selectPartyMember(index);
        });
    });
}

/**
 * Handle battle action button clicks
 */
function handleBattleAction(e) {
    const action = e.target.id.replace('-btn', '');
    const activeMember = gameState.party[gameState.activeMember];
    
    let logMessage = '';
    
    switch(action) {
        case 'fight':
            logMessage = `${activeMember.name} strikes ${gameState.enemy.name} with a mighty blow for 15 damage.`;
            gameState.enemy.life = Math.max(0, gameState.enemy.life - 15);
            break;
        case 'magic':
            logMessage = `${activeMember.name} casts Arcane Blast on ${gameState.enemy.name} for 25 damage.`;
            gameState.enemy.life = Math.max(0, gameState.enemy.life - 25);
            gameState.party[gameState.activeMember].mana -= 10;
            break;
        case 'ability':
            logMessage = `${activeMember.name} uses a special ability.`;
            gameState.party[gameState.activeMember].melee -= 20;
            break;
        case 'item':
            logMessage = `${activeMember.name} uses a Healing Potion.`;
            gameState.party[gameState.activeMember].life = Math.min(100, gameState.party[gameState.activeMember].life + 20);
            break;
        case 'search':
            logMessage = `${activeMember.name} searches the area carefully...`;
            setTimeout(() => {
                addLogEntry('Discovered an ancient rune etched into the floor!', 'system');
            }, 1000);
            break;
        case 'flee':
            logMessage = 'The party attempts to retreat from battle...';
            setTimeout(() => {
                addLogEntry('Escape successful! You live to fight another day.', 'system');
            }, 1000);
            break;
    }
    
    // Add log entry
    addLogEntry(logMessage, 'combat');
    
    // Update displays
    updatePartyDisplay();
    updateEnemyDisplay();
    
    // Simulate enemy turn
    if (gameState.enemy.life > 0) {
        setTimeout(() => {
            simulateEnemyTurn();
        }, 1500);
    }
}

/**
 * Simulate enemy turn
 */
function simulateEnemyTurn() {
    // Select random party member to attack
    const targetIndex = Math.floor(Math.random() * gameState.party.length);
    const target = gameState.party[targetIndex];
    
    // Calculate damage
    const damage = Math.floor(Math.random() * 10) + 5;
    
    // Apply damage
    gameState.party[targetIndex].life = Math.max(0, target.life - damage);
    
    // Add log entry
    addLogEntry(`${gameState.enemy.name} unleashes dark magic at ${target.name} for ${damage} damage.`, 'combat');
    
    // Update party display
    updatePartyDisplay();
}

/**
 * Select a party member
 */
function selectPartyMember(index) {
    gameState.activeMember = index;
    
    // Update visual selection
    const partyMembers = document.querySelectorAll('.party-member');
    partyMembers.forEach((member, i) => {
        if (i === index) {
            member.style.borderColor = '#ffd700';
            member.style.boxShadow = '0 0 10px rgba(255, 215, 0, 0.5)';
        } else {
            member.style.borderColor = '#8e6b3d';
            member.style.boxShadow = 'none';
        }
    });
    
    // Add log entry
    addLogEntry(`Selected ${gameState.party[index].name}.`, 'system');
}

/**
 * Update party member displays
 */
function updatePartyDisplay() {
    const partyMembers = document.querySelectorAll('.party-member');
    
    gameState.party.forEach((member, index) => {
        if (index < partyMembers.length) {
            const memberElement = partyMembers[index];
            
            // Update name
            const nameElement = memberElement.querySelector('.member-name');
            if (nameElement) nameElement.textContent = member.name;
            
            // Update bars
            const lifeFill = memberElement.querySelector('.life-bar');
            const manaFill = memberElement.querySelector('.mana-bar');
            const meleeFill = memberElement.querySelector('.melee-bar');
            const battleFill = memberElement.querySelector('.battle-timer');
            
            if (lifeFill) lifeFill.style.width = `${member.life}%`;
            if (manaFill) manaFill.style.width = `${member.mana}%`;
            if (meleeFill) meleeFill.style.width = `${member.melee}%`;
            if (battleFill) {
                battleFill.style.width = `${member.battleTimer}%`;
                if (member.battleTimer >= 100) {
                    battleFill.classList.add('ready');
                } else {
                    battleFill.classList.remove('ready');
                }
            }
        }
    });
}

/**
 * Update enemy display
 */
function updateEnemyDisplay() {
    const enemyName = document.querySelector('#enemy-area .enemy-name');
    const lifeFill = document.querySelector('#enemy-area .life-bar');
    const battleFill = document.querySelector('#enemy-area .battle-timer');
    
    if (enemyName) enemyName.textContent = gameState.enemy.name;
    if (lifeFill) lifeFill.style.width = `${gameState.enemy.life}%`;
    if (battleFill) {
        battleFill.style.width = `${gameState.enemy.battleTimer}%`;
        if (gameState.enemy.battleTimer >= 100) {
            battleFill.classList.add('ready');
        } else {
            battleFill.classList.remove('ready');
        }
    }
}

/**
 * Add entry to combat log
 */
function addLogEntry(text, type = 'system') {
    const logEntries = document.querySelector('.log-entries');
    if (!logEntries) return;
    
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = text;
    
    // Add to top of log
    logEntries.insertBefore(entry, logEntries.firstChild);
    
    // Limit number of entries
    if (logEntries.children.length > 50) {
        logEntries.removeChild(logEntries.lastChild);
    }
}

/**
 * Initialize chat log filters
 */
function initChatFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const filter = button.getAttribute('data-filter');
            filterLogEntries(filter);
        });
    });
}

/**
 * Filter log entries based on selected filter
 */
function filterLogEntries(filter) {
    const logEntries = document.querySelectorAll('.log-entry');
    
    logEntries.forEach(entry => {
        if (filter === 'all') {
            entry.style.display = 'block';
        } else {
            if (entry.classList.contains(filter)) {
                entry.style.display = 'block';
            } else {
                entry.style.display = 'none';
            }
        }
    });
}

/**
 * Initialize mini-map
 */
function initMiniMap() {
    const mapContainer = document.querySelector('.map-container');
    if (!mapContainer) return;
    
    // Create a grid map
    const mapSize = gameState.mapSize;
    const grid = document.createElement('div');
    grid.className = 'map-grid';
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = `repeat(${mapSize}, 1fr)`;
    grid.style.gridTemplateRows = `repeat(${mapSize}, 1fr)`;
    grid.style.gap = '1px';
    grid.style.height = '100%';
    
    for (let y = 0; y < mapSize; y++) {
        for (let x = 0; x < mapSize; x++) {
            const cell = document.createElement('div');
            cell.className = 'map-cell';
            cell.dataset.x = x;
            cell.dataset.y = y;
            
            // Add some random walls
            if (Math.random() < 0.2) {
                cell.classList.add('wall');
            }
            
            // Add player position
            if (x === gameState.playerPosition.x && y === gameState.playerPosition.y) {
                cell.classList.add('player');
            }
            
            grid.appendChild(cell);
        }
    }
    
    mapContainer.appendChild(grid);
}

/**
 * Update player position on the map
 */
function updatePlayerPosition() {
    const cells = document.querySelectorAll('.map-cell');
    
    cells.forEach(cell => {
        const x = parseInt(cell.dataset.x);
        const y = parseInt(cell.dataset.y);
        
        if (x === gameState.playerPosition.x && y === gameState.playerPosition.y) {
            cell.classList.add('player');
        } else {
            cell.classList.remove('player');
        }
    });
    
    // Add log entry about movement
    addLogEntry(`Moved to position [${gameState.playerPosition.x}, ${gameState.playerPosition.y}].`, 'system');
}

/**
 * Initialize directional control pad
 */
function initDirectionalPad() {
    const upButton = document.querySelector('.d-pad-up');
    const rightButton = document.querySelector('.d-pad-right');
    const downButton = document.querySelector('.d-pad-down');
    const leftButton = document.querySelector('.d-pad-left');
    const centerButton = document.querySelector('.d-pad-center');
    
    // Up button
    upButton.addEventListener('click', () => {
        movePlayer(0, -1);
    });
    
    // Right button
    rightButton.addEventListener('click', () => {
        movePlayer(1, 0);
    });
    
    // Down button
    downButton.addEventListener('click', () => {
        movePlayer(0, 1);
    });
    
    // Left button
    leftButton.addEventListener('click', () => {
        movePlayer(-1, 0);
    });
    
    // Center button (interact)
    centerButton.addEventListener('click', () => {
        interactWithEnvironment();
    });
    
    // Keyboard controls
    document.addEventListener('keydown', (e) => {
        switch(e.key) {
            case 'ArrowUp':
            case 'w':
                movePlayer(0, -1);
                break;
            case 'ArrowRight':
            case 'd':
                movePlayer(1, 0);
                break;
            case 'ArrowDown':
            case 's':
                movePlayer(0, 1);
                break;
            case 'ArrowLeft':
            case 'a':
                movePlayer(-1, 0);
                break;
            case ' ':
            case 'Enter':
                interactWithEnvironment();
                break;
        }
    });
}

/**
 * Move player on the map
 */
function movePlayer(dx, dy) {
    // Calculate new position
    const newX = gameState.playerPosition.x + dx;
    const newY = gameState.playerPosition.y + dy;
    
    // Check boundaries
    if (newX >= 0 && newX < gameState.mapSize && newY >= 0 && newY < gameState.mapSize) {
        // Check if the cell is a wall
        const cells = document.querySelectorAll('.map-cell');
        let isWall = false;
        
        cells.forEach(cell => {
            const x = parseInt(cell.dataset.x);
            const y = parseInt(cell.dataset.y);
            
            if (x === newX && y === newY && cell.classList.contains('wall')) {
                isWall = true;
            }
        });
        
        if (!isWall) {
            // Update player position
            gameState.playerPosition.x = newX;
            gameState.playerPosition.y = newY;
            
            // Update map display
            updatePlayerPosition();
            
            // Random encounter check (10% chance)
            if (Math.random() < 0.1) {
                addLogEntry('A monster approaches!', 'system');
                // Could trigger combat here
            }
        } else {
            addLogEntry('Your path is blocked.', 'system');
        }
    } else {
        addLogEntry('You cannot move in that direction.', 'system');
    }
}

/**
 * Interact with the environment
 */
function interactWithEnvironment() {
    // Check if there's something to interact with at the current position
    const x = gameState.playerPosition.x;
    const y = gameState.playerPosition.y;
    
    // Random chance to find something (30%)
    if (Math.random() < 0.3) {
        const items = [
            'a small health potion',
            'a rusty key',
            'a mysterious scroll',
            'a gold coin',
            'a strange rune',
            'an old map fragment'
        ];
        
        const randomItem = items[Math.floor(Math.random() * items.length)];
        addLogEntry(`You found ${randomItem}!`, 'system');
    } else {
        addLogEntry('There is nothing of interest here.', 'system');
    }
}

/**
 * Simulate combat log entries
 */
function simulateCombatLog() {
    // Add initial entries
    addLogEntry('You enter the ancient crypt, torches flickering on the walls.', 'system');
    
    setTimeout(() => {
        addLogEntry('A skeletal lich materializes before you!', 'system');
    }, 1000);
    
    setTimeout(() => {
        addLogEntry('Prepare for battle!', 'system');
    }, 2000);
}

/**
 * Simulate battle timer progress
 */
function simulateBattleTimers() {
    // Update party battle timers
    gameState.party.forEach((member, index) => {
        member.battleTimer += Math.random() * 5 + 5;
        if (member.battleTimer > 100) {
            member.battleTimer = 100;
        }
    });
    
    // Update enemy battle timer
    gameState.enemy.battleTimer += Math.random() * 5 + 5;
    if (gameState.enemy.battleTimer > 100) {
        gameState.enemy.battleTimer = 100;
    }
    
    // Update displays
    updatePartyDisplay();
    updateEnemyDisplay();
}

// Simulate battle timer progress every second
setInterval(simulateBattleTimers, 1000);
