/**
 * @jest-environment jsdom
 */

// Declare a variable to hold our exported game object
let game;

beforeEach(() => {
  // 1. Set up the DOM
  document.body.innerHTML = `
    <button id="roll-btn">Roll</button>
    <button id="guess-btn">Guess</button>
    <input id="guess-input" value="7" />
    <div id="dice1"></div>
    <div id="dice2"></div>
    <div id="dice1-sides"><span></span><span></span><span></span><span></span><span></span></div>
    <div id="dice2-sides"><span></span><span></span><span></span><span></span><span></span></div>
    <div id="current-sum"></div>
    <div id="slot-0"></div><div id="slot-1"></div><div id="slot-2"></div><div id="slot-3"></div><div id="slot-4"></div>
    <div id="net-score-amount"></div>
    <div id="round-counter-amount"></div>
    <div id="payout-amount"></div>
  `;

  // 2. Mock fetch with a default safe response
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      peeks: [2, 3, 4, 5],
      session_id: "initial-session",
      payout: 0,
      best_guess: 7,
    }),
  });

  global.alert = jest.fn();
  localStorage.clear();

  // 3. Load the script fresh before EVERY test and assign it to our game variable
  game = require("../src/script");
});

afterEach(() => {
  jest.resetModules(); // Clears Node's cache so the script re-runs clean next time
  jest.clearAllMocks();
});

describe("Gamblint Game Script Tests", () => {
  // --- 1. TESTING UTILITY FUNCTIONS ---
  describe("isValidGuess()", () => {
    it("should accept valid dice sums between 2 and 12", () => {
      // Use the 'game' object prefix to call your functions!
      expect(game.isValidGuess(2)).toBe(true);
      expect(game.isValidGuess(7)).toBe(true);
      expect(game.isValidGuess(12)).toBe(true);
    });

    it("should reject numbers outside the dice range or non-numbers", () => {
      expect(game.isValidGuess(1)).toBe(false);
      expect(game.isValidGuess(13)).toBe(false);
      expect(game.isValidGuess(NaN)).toBe(false);
    });
  });

  // --- 2. TESTING STATE LOGIC & ANTI-CHEAT ---
  describe("updatePerfectGuesses()", () => {
    it("should warning-alert the user on the 5th consecutive perfect guess", () => {
      // Access your game state fields using game.state
      game.state.perfectGuesses = 4;

      game.updatePerfectGuesses(true);

      expect(game.state.perfectGuesses).toBe(5);
      expect(global.alert).toHaveBeenCalledWith(
        "Stop cheating! You will be banned if you do it again.",
      );
    });

    it("should penalize the player and reset score on more than 5 perfect guesses", () => {
      game.state.perfectGuesses = 5;
      game.state.netScore = 500;

      game.updatePerfectGuesses(true);

      expect(game.state.netScore).toBe(-10000);
      expect(game.state.perfectGuesses).toBe(0);
      expect(global.alert).toHaveBeenCalledWith(
        "Penalty applied: score reset.",
      );
    });

    it("should reset the streak counter to 0 if a guess is incorrect", () => {
      game.state.perfectGuesses = 3;

      game.updatePerfectGuesses(false);

      expect(game.state.perfectGuesses).toBe(0);
    });
  });

  // --- 3. TESTING API FUNCTIONS DIRECTLY ---
  describe("API Functions via Fetch", () => {
    it("should parse payload correctly on apiStartGame success", async () => {
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ peeks: [3, 4, 5, 6], session_id: "mock-id" }),
      });

      const data = await game.apiStartGame();

      expect(data.session_id).toBe("mock-id");
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/start-game",
        expect.any(Object),
      );
    });

    it("should throw an error if apiGuess fails network-side", async () => {
      global.fetch.mockResolvedValue({ ok: false });

      await expect(game.apiGuess(7, "id", {})).rejects.toThrow("Guess failed");
    });
  });

  // --- 4. TESTING THE ORCHESTRATOR ---
  describe("handleGuess()", () => {
    it("should process correct payouts and increment variables on guess success", async () => {
      game.state.sessionId = "test-session";
      game.state.netScore = 0;
      game.state.totalRounds = 0;

      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({
          best_guess: 7,
          roll: 7,
          payout: 100,
        }),
      });

      const success = await game.handleGuess();

      expect(success).toBe(true);
      expect(game.state.netScore).toBe(100);
      expect(game.state.totalRounds).toBe(1);
    });

    it("should catch exceptions gracefully and return false if the API errors out", async () => {
      global.fetch.mockResolvedValue({ ok: false }); // Force fetch failure

      const success = await game.handleGuess();

      expect(success).toBe(false);
      expect(global.alert).toHaveBeenCalledWith(
        "Network error. Please try guessing again.",
      );
    });
  });
});
