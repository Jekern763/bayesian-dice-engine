const MAX_ROLLS = 4;
const RISKINESS = 1;
const JACKPOT = 1;

const state = {
  peeks: [],
  sessionId: null,
  netScore: 0,
  totalRounds: 0,
  perfectGuesses: 0,
  think_start_time: null,
  think_end_time: null,
};

const STORAGE_VERSION = "1.2";

const currentVersion = localStorage.getItem("storage_version");

if (currentVersion !== STORAGE_VERSION) {
  localStorage.clear(); // or remove only the keys you own
  localStorage.setItem("storage_version", STORAGE_VERSION);
}

const storage = {
  load() {
    state.netScore = parseFloat(localStorage.getItem("net_score") || "0");
    state.totalRounds = parseInt(localStorage.getItem("total_rounds") || "0");
    state.perfectGuesses = parseInt(
      localStorage.getItem("perfect_guesses") || "0",
    );
  },

  save() {
    localStorage.setItem("net_score", String(state.netScore));
    localStorage.setItem("total_rounds", String(state.totalRounds));
    localStorage.setItem("perfect_guesses", String(state.perfectGuesses));
  },

  clearSession() {
    localStorage.removeItem("current_peeks");
    localStorage.removeItem("session");
  },

  saveSession() {
    localStorage.setItem("current_peeks", JSON.stringify(state.peeks));
    localStorage.setItem("session", state.sessionId);
  },

  loadSession() {
    const peeks = localStorage.getItem("current_peeks");
    const session = localStorage.getItem("session");

    if (!peeks || !session) {
      return false;
    }

    state.peeks = JSON.parse(peeks);
    state.sessionId = session;
    return true;
  },
};

async function apiStartGame() {
  const res = await fetch("/api/start-game", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ riskiness: RISKINESS, jackpot: JACKPOT }),
  });

  if (!res.ok) throw new Error("Start game failed");
  return res.json();
}

async function apiGuess(guess, sessionId, data) {
  const res = await fetch("/api/guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      guess: guess,
      session_id: sessionId,
      additional_data: data,
    }),
  });

  if (!res.ok) throw new Error("Guess failed");
  return res.json();
}

const ui = {
  el(id) {
    return document.getElementById(id);
  },

  setText(id, value) {
    this.el(id).textContent = value;
  },

  setDisabled(id, value) {
    this.el(id).disabled = value;
  },

  showAlert(msg) {
    alert(msg);
  },

  updateScore() {
    this.setText("net-score-amount", state.netScore);
    this.setText("round-counter-amount", state.totalRounds);
  },
};

function isValidGuess(value) {
  return !isNaN(value) && value >= 2 && value <= 12;
}

function updatePerfectGuesses(isCorrect) {
  if (isCorrect) {
    state.perfectGuesses++;
  } else {
    state.perfectGuesses = 0;
  }

  if (state.perfectGuesses === 5) {
    ui.showAlert("Stop cheating! You will be banned if you do it again.");
  }

  if (state.perfectGuesses > 5) {
    ui.showAlert("Penalty applied: score reset.");
    state.netScore = -10000;
    state.perfectGuesses = 0;
  }
}

function roll(result, index, display = true) {
  if (index > MAX_ROLLS) return;

  const dice1 = document.getElementById("dice1");
  const dice2 = document.getElementById("dice2");

  dice1.classList.add("rolling");
  dice2.classList.add("rolling");

  setTimeout(() => {
    dice1.classList.remove("rolling");
    dice2.classList.remove("rolling");

    ui.setText("current-sum", result);

    const d1 = document.querySelectorAll("#dice1-sides span");
    const d2 = document.querySelectorAll("#dice2-sides span");

    if (d1[index] && d2[index]) {
      d1[index].classList.add("removed");
      d2[index].classList.add("removed");
    }

    if (display) {
      ui.setText(`slot-${index}`, result);
    }
  }, 500);
}

async function handleGuess() {
  const input = parseInt(ui.el("guess-input").value);

  if (!isValidGuess(input)) {
    ui.showAlert("Please enter a valid guess between 2 and 12");
    return false;
  }
  try {
    const result = await apiGuess(input, state.sessionId, {
      time_to_respond: state.think_start_time - state.think_end_time,
      first_time: state.totalRounds === 0,
    });

    updatePerfectGuesses(input == result.best_guess);

    roll(result.roll, 4, false);

    ui.setText("payout-amount", result.payout);

    state.netScore += result.payout;
    state.totalRounds++;

    storage.save();
    ui.updateScore();

    return true;
  } catch (error) {
    ui.showAlert("Network error. Please try guessing again.");
    return false;
  }
}

function waitForClick(el) {
  return new Promise((resolve) => {
    const handler = () => {
      el.removeEventListener("click", handler);
      resolve();
    };
    el.addEventListener("click", handler);
  });
}

async function gameLoop() {
  const rollBtn = ui.el("roll-btn");
  const guessBtn = ui.el("guess-btn");

  storage.load();

  const hasSession = storage.loadSession();

  if (!hasSession) {
    const start = await apiStartGame();
    state.peeks = start.peeks;
    state.sessionId = start.session_id;
    storage.saveSession();
  }

  ui.updateScore();

  for (let i = 0; i < MAX_ROLLS; i++) {
    await waitForClick(rollBtn);
    roll(state.peeks[i], i);
  }
  state.think_start_time = Date.now();

  guessBtn.disabled = false;
  rollBtn.disabled = true;

  while (true) {
    await waitForClick(guessBtn);
    state.think_end_time = Date.now();
    const success = await handleGuess();
    if (success) break;
  }

  guessBtn.disabled = true;
  rollBtn.disabled = false;
  rollBtn.textContent = "Play Again";

  storage.clearSession();
}

function reset() {
  ui.setText("current-sum", "-");
  ui.setText("roll-btn", "Roll");
  ui.setText("payout-amount", "-");

  ui.setDisabled("roll-btn", false);
  ui.setDisabled("guess-btn", true);

  ui.el("guess-input").value = "";

  for (let i = 0; i < MAX_ROLLS; i++) {
    ui.setText(`slot-${i}`, "-");
  }

  document.querySelectorAll(".removed").forEach((el) => {
    el.classList.remove("removed");
  });
}

document.getElementById("roll-btn").addEventListener("click", () => {
  if (ui.el("roll-btn").textContent === "Play Again") {
    reset();
    gameLoop();
  }
});

if (localStorage.getItem("net_score")) {
  ui.setText("net-score-amount", localStorage.getItem("net_score"));
}

gameLoop();

window.addEventListener("keydown", (event) => {
  if (event.key === " " || event.key === "Spacebar" || event.key === "Enter") {
    event.preventDefault();

    // Ignore the event if the key is just being held down
    if (event.repeat) return;
  } else {
    ui.el("roll-btn").click();
  }
});

// just for jest testing
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    isValidGuess,
    updatePerfectGuesses,
    state,
    apiStartGame,
    apiGuess,
    handleGuess,
  };
}
