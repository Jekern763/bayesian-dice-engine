/**
 * ============================================================================
 * GAME EXECUTION & LIFECYCLE GUIDE
 * ============================================================================
 * * To run and test these functions manually in your browser console, you can call:
 * 1. handleDirectRoll()  -> Simulates clicking the "Just Roll" button. Call 4 times.
 * 2. roll(8)             -> Directly forces a visual roll animation displaying the sum 8.
 * 3. guess(7)            -> Directly submits a guess of 7 to your mock API.
 * 4. reset()             -> Wipes the board clean so you can play a fresh round.
 * * EXPORTING FOR OTHER SCRIPTS:
 * If your API logic lives in another file, ensure you either link it before this 
 * script in index.html, or export/import these functions globally.
 */

// Track game state elements
let rollCount = 0; 
const maxRolls = 4;
let totalPayout = 0; // Tracks the visual payout score tracker

/**
 * 1. THE VISUAL REVEAL: roll(result)
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
 * 2. API IMPLEMENTATION: guess(playerGuess)
 * Handles the player's final input guess parameter, makes a mock call, and outputs the result.
 * @param {number} playerGuess - The value parsed from user input
 */
function guess(playerGuess) {
    console.log(`[Mock API] Sent final player guess: ${playerGuess}`);
    
    // Lock the guess button down completely now that it's being used
    document.getElementById('guess-btn').disabled = true;

    /* * HOW TO IMPLEMENT YOUR REAL API CALL HERE:
     * ------------------------------------------------------------------------
     * fetch('https://your-api-domain.com/api/guess', {
     * method: 'POST',
     * headers: { 'Content-Type': 'application/json' },
     * body: JSON.stringify({ guess: playerGuess })
     * })
     * .then(response => response.json())
     * .then(data => {
     * // Assuming server returns data object: { rolledSum: 9, payout: 100 }
     * document.getElementById('current-sum').innerText = data.rolledSum;
     * * if (playerGuess === data.rolledSum) {
     * totalPayout += data.payout;
     * document.getElementById('payout-amount').innerText = totalPayout;
     * }
     * })
     * .catch(err => console.error("API error during guess submission:", err));
     */

    // CURRENT MOCK BEHAVIOR (Delete this block when adding real fetch above):
    setTimeout(() => {
        const mockRolledSum = Math.floor(Math.random() * 11) + 2;
        console.log(`[Mock API] Response received. Result rolled: ${mockRolledSum}`);
        
        document.getElementById('current-sum').innerText = mockRolledSum;
        
        if (playerGuess === mockRolledSum) {
            totalPayout += 100; 
            document.getElementById('payout-amount').innerText = totalPayout;
        }
        console.log("Game completed. Max rolls reached and single guess finalized.");
    }, 1000);
}

/**
 * UI Event Handler - Guess Submission Button Click
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
 * 3. API IMPLEMENTATION: handleDirectRoll()
 * UI Event Handler for the "Just Roll" Button.
 */
function handleDirectRoll() {
    if (rollCount >= maxRolls) return;

    /* * HOW TO IMPLEMENT YOUR REAL API CALL HERE:
     * ------------------------------------------------------------------------
     * If you want your server to generate the roll values securely rather than locally:
     * * fetch('https://your-api-domain.com/api/roll-dice')
     * .then(response => response.json())
     * .then(data => {
     * // Assuming server returns data object: { resultSum: 7 }
     * roll(data.resultSum);
     * })
     * .catch(err => console.error("API error getting dice roll:", err));
     */

    // CURRENT MOCK BEHAVIOR (Delete this block when adding real fetch above):
    const randomSum = Math.floor(Math.random() * 11) + 2;
    roll(randomSum);
}

/**
 * 4. SYSTEM RESET: reset()
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