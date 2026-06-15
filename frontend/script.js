// Track game state elements
let rollCount = 0; 
const maxRolls = 4;
let totalPayout = 0; // Tracks the visual payout score tracker

/**
 * 1. "Roll" the dice
 * Handles the visual presentation, removes a side from each die, and updates history sequentially.
 * @param {number} result - The final sum value passed to the UI
 */
function roll(result) {
    if (rollCount >= maxRolls) return;

    const dice1 = document.getElementById('dice1');
    const dice2 = document.getElementById('dice2');

    // Trigger the CSS shake animation
    dice1.classList.add('rolling');
    dice2.classList.add('rolling');

    // Wait for animation loop to finish before updating values
    setTimeout(() => {
        dice1.classList.remove('rolling');
        dice2.classList.remove('rolling');

        // Reveal the final sum (but keep dice bodies blank)
        document.getElementById('current-sum').innerText = result;

        // Visually strip away one side element indicator from BOTH dice
        const d1Sides = document.querySelectorAll('#dice1-sides span');
        const d2Sides = document.querySelectorAll('#dice2-sides span');
        if (d1Sides[rollCount] && d2Sides[rollCount]) {
            d1Sides[rollCount].classList.add('removed');
            d2Sides[rollCount].classList.add('removed');
        }

        // Place the result directly into its fixed chronological slot
        document.getElementById(`slot-${rollCount}`).innerText = result;

        // Increment tracking step
        rollCount++;

        // State Check: When 4 rolls are completed, invert button access states
        if (rollCount === maxRolls) {
            document.getElementById('roll-btn').disabled = true;
            document.getElementById('guess-btn').disabled = false;
        }

    }, 500); 
}

/**
 * 2. Guess Submission & Mock API Call
 * Handles the player's final input guess parameter, makes a mock call, and outputs the result.
 * @param {number} playerGuess - The value parsed from user input
 */
function guess(playerGuess) {
    console.log(`[Mock API] Sent final player guess: ${playerGuess}`);
    
    // Lock the guess button down completely now that it's being used
    document.getElementById('guess-btn').disabled = true;

    // Simulate 1-second network latency
    setTimeout(() => {
        const mockRolledSum = Math.floor(Math.random() * 11) + 2;
        console.log(`[Mock API] Response received. Result rolled: ${mockRolledSum}`);
        
        // Show final outcome in the centerpiece display area
        document.getElementById('current-sum').innerText = mockRolledSum;
        
        // Example logic adjustment: adjust total payout if they got it right
        if (playerGuess === mockRolledSum) {
            totalPayout += 100; // Mock rewards value
            document.getElementById('payout-amount').innerText = totalPayout;
        }

        console.log("Game completed. Max rolls reached and single guess finalized.");
    }, 1000);
}

/**
 * UI Event Handler - Guess Submission
 */
function handleGuessSubmit() {
    const inputElement = document.getElementById('guess-input');
    const value = parseInt(inputElement.value);

    if (isNaN(value) || value < 2 || value > 12) {
        alert("Please enter a valid guess between 2 and 12!");
        return;
    }

    guess(value);
    inputElement.value = ''; 
    inputElement.disabled = true; // Turn off input field since game is concluded
}

/**
 * UI Event Handler - Direct Roll
 */
function handleDirectRoll() {
    if (rollCount < maxRolls) {
        const randomSum = Math.floor(Math.random() * 11) + 2;
        roll(randomSum);
    }
}

/**
 * 3. Game Reset Function (Not in active use yet)
 * Restores core state elements, clears historical slots, and resets physical dice dots.
 */
function reset() {
    // Reset trackers back to step zero
    rollCount = 0;

    // Clear main numerical displays
    document.getElementById('current-sum').innerText = '-';

    // Enable/Disable control mechanisms back to standard start configuration
    document.getElementById('roll-btn').disabled = false;
    document.getElementById('guess-btn').disabled = true;
    
    const inputField = document.getElementById('guess-input');
    inputField.disabled = false;
    inputField.value = '';

    // Reconstruct history display fields back to default empty markers
    for (let i = 0; i < maxRolls; i++) {
        document.getElementById(`slot-${i}`).innerText = '-';
    }

    // Un-dim all physical dice layout dot items
    const allRemovedDots = document.querySelectorAll('.sides-tracker span.removed');
    allRemovedDots.forEach(dot => {
        dot.classList.remove('removed');
    });

    console.log("[System] Game environment cleaned and reset.");
}