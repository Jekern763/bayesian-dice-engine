const maxRolls = 4;
let totalPayout = 0;
const riskiness = 8;
const jackpot = 10;
let peeks;
let session_id;

// local storage values: current_peeks to prevent reloading
// current score to show score over history of local storage
// repeat for if it is the users first time
// net_score for total score through sessions
let repeat = localStorage.getItem("repeat") ? true : false;

async function api_start_game() {
  const game_constants = { riskiness: riskiness, jackpot: jackpot };
  try {
    const response = await fetch("/api/start-game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(game_constants),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error during POST request:", error);
  }
}

async function api_guess(guess, session_id) {
  const payload = { guess: guess, session_id: session_id };
  try {
    const response = await fetch("/api/guess", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error during POST request:", error);
  }
}
/**
 * 1. THE VISUAL REVEAL: roll(result)
 * Handles the visual presentation, removes a side from each die, and updates history sequentially.
 * @param {number} result - The final sum value passed to the UI
 */
function roll(result, rollCount, display = true) {
  if (rollCount >= maxRolls) return;

  const dice1 = document.getElementById("dice1");
  const dice2 = document.getElementById("dice2");

  // Trigger the CSS shake animation
  dice1.classList.add("rolling");
  dice2.classList.add("rolling");

  // Wait for animation loop to finish before updating values
  setTimeout(() => {
    dice1.classList.remove("rolling");
    dice2.classList.remove("rolling");

    // Reveal the final sum (but keep dice bodies blank)
    document.getElementById("current-sum").textContent = result;

    // Visually strip away one side element indicator from BOTH dice
    const d1Sides = document.querySelectorAll("#dice1-sides span");
    const d2Sides = document.querySelectorAll("#dice2-sides span");
    if (d1Sides[rollCount] && d2Sides[rollCount]) {
      d1Sides[rollCount].classList.add("removed");
      d2Sides[rollCount].classList.add("removed");
    }

    // Place the result directly into its fixed chronological slot
    if (display) {
      document.getElementById(`slot-${rollCount}`).textContent = result;
    }
  }, 500);
}

/**
 * 2. API IMPLEMENTATION: guess(playerGuess)
 * Handles the player's final input guess parameter, makes a mock call, and outputs the result.
 * @param {number} playerGuess - The value parsed from user input
 */
async function guess(guess, session_id) {
  const api_return = await api_guess(guess, session_id);
  const roll_return = api_return.roll;
  const payout = api_return.payout;
  roll(roll_return, 4, false);
  document.getElementById("payout-amount").textContent = payout;
  document.getElementById("current-sum").textContent = roll_return;

  if (repeat) {
    const current_total = Int(localStorage.getItem("net_score"));
    localStorage.setItem("net_score", String(current_total + payout));
  } else {
    localStorage.setItem("net-score", String(payout));
  }

  document.getElementById("net-score").textContent =
    localStorage.getItem("net_score");

  localStorage.setItem("repeat", "true");

  repeat = true;
}

function ValidateGuessSubmit() {
  const inputElement = document.getElementById("guess-input");
  const value = parseInt(inputElement.value);

  return !isNaN(value) && value >= 2 && value <= 12;
}

/**
 * 4. SYSTEM RESET: reset()
 * Restores core state elements, clears historical slots, and resets physical dice dots.
 */
function reset() {
  // Reset trackers back to step zero
  rollCount = 0;

  document.getElementById("roll-btn").textContent = "Roll";

  // Clear main numerical displays
  document.getElementById("current-sum").textContent = "-";

  // Enable/Disable control mechanisms back to standard start configuration
  document.getElementById("roll-btn").disabled = false;
  document.getElementById("guess-btn").disabled = true;

  const inputField = document.getElementById("guess-input");
  inputField.disabled = false;
  inputField.value = "";

  // Reconstruct history display fields back to default empty markers
  for (let i = 0; i < maxRolls; i++) {
    document.getElementById(`slot-${i}`).textContent = "-";
  }

  // Un-dim all physical dice layout dot items
  const allRemovedDots = document.querySelectorAll(
    ".sides-tracker span.removed",
  );
  allRemovedDots.forEach((dot) => {
    dot.classList.remove("removed");
  });
}

function waitForClick(buttonElement) {
  return new Promise((resolve) => {
    // Inner function handles the click and cleans up after itself
    function listener() {
      buttonElement.removeEventListener("click", listener);
      resolve(); // This unblocks the "await"
    }

    buttonElement.addEventListener("click", listener);
  });
}

async function game_loop() {
  const roll_btn = document.getElementById("roll-btn");
  const guess_btn = document.getElementById("guess-btn");
  const guess_input = document.getElementById("guess-input");
  if (!localStorage.getItem("current_peeks")) {
    const start_game_response = await api_start_game();

    peeks = start_game_response.peeks;
    session_id = start_game_response.session_id;
  } else {
    peeks = localStorage.getItem("current_peeks").split(",");
    ession_id = localStorage.getItem("session");
  }

  for (let i = 0; i <= 3; i++) {
    await waitForClick(roll_btn);
    roll(peeks[i], i);
  }
  guess_btn.disabled = false;
  roll_btn.disabled = true;

  while (true) {
    await waitForClick(document.getElementById("guess-btn"));
    if (ValidateGuessSubmit() === true) {
      guess(guess_input.value, session_id);
      break;
    }
    alert("Please enter a valid guess between 2 and 12");
  }

  guess_btn.disabled = true;
  roll_btn.disabled = false;

  roll_btn.textContent = "Play Again";

  localStorage.removeItem("current_peeks");
  localStorage.removeItem("session");
}

// localStorage.setItem("current_peeks", "");
// localStorage.setItem("session", "");
document.getElementById("roll-btn").addEventListener("click", function () {
  if (document.getElementById("roll-btn").textContent === "Play Again") {
    reset();
    game_loop();
  }
});

game_loop();
