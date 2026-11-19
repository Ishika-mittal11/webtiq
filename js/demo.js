/* ==========================================================
   WebtiqAI — Live Demo JavaScript

   Talks to the backend (server/server.js):
     GET    /api/knowledge          - what the bot knows
     POST   /api/knowledge          - teach it something
     DELETE /api/knowledge/:id      - remove one item
     POST   /api/chat               - ask OpenAI, answering
                                      only from the knowledge
     GET    /api/leads              - unanswered questions

   If the backend is NOT running, everything falls back to
   localStorage + a local matching engine, so the demo always
   works during a presentation.
   ========================================================== */

var kbForm   = document.getElementById("kbForm");
var kbQ      = document.getElementById("kbQ");
var kbA      = document.getElementById("kbA");
var kbError  = document.getElementById("kbError");
var kbList   = document.getElementById("kbList");
var kbCount  = document.getElementById("kbCount");
var kbSample = document.getElementById("kbSample");
var kbClear  = document.getElementById("kbClear");

var demoChat  = document.getElementById("demoChat");
var demoForm  = document.getElementById("demoForm");
var demoInput = document.getElementById("demoInput");
var suggestions = document.getElementById("suggestions");
var leadsBody = document.getElementById("leadsBody");

var STORAGE_KEY = "webtiqai_kb";
var knowledge = [];
var leadCount = 0;

/* ---------- SAMPLE DATA (used in offline mode) ---------- */
var sampleData = [
  { id: 1, q: "What are your opening hours?", a: "We are open Monday to Saturday, 10 AM to 7 PM. Sunday is closed." },
  { id: 2, q: "Do you offer home delivery?",  a: "Yes, we deliver across the city in 2-3 days. Delivery is free on orders above Rs 999." },
  { id: 3, q: "What is your return policy?",  a: "You can return any product within 7 days of delivery, with the original bill." },
  { id: 4, q: "Which payment methods do you accept?", a: "We accept UPI, all major cards, net banking and cash on delivery." },
  { id: 5, q: "Where is your shop located?",  a: "Our shop is at Shop 12, Main Market Road, near the city bus stand." }
];

/* ==========================================================
   OFFLINE STORAGE (only used when the backend is down)
   ========================================================== */
function loadLocal() {
  try {
    var saved = localStorage.getItem(STORAGE_KEY);
    knowledge = saved ? JSON.parse(saved) : [];
  } catch (err) {
    knowledge = [];
  }
}

function saveLocal() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(knowledge));
  } catch (err) {
    // storage blocked - the demo still works for this session
  }
}

/* ==========================================================
   OFFLINE MATCHING ENGINE
   An exact word match scores 2 points, a partial match 1.
   Below 2 points the bot admits it does not know.
   ========================================================== */
var stopWords = ["the", "is", "are", "do", "does", "you", "your", "a", "an",
                 "of", "to", "in", "on", "for", "what", "how", "can", "i",
                 "we", "and", "me", "my", "it", "at", "with"];

function cleanWords(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter(function (word) {
      return word.length > 1 && stopWords.indexOf(word) === -1;
    });
}

function searchKnowledge(question) {
  var askedWords = cleanWords(question);
  var best = null;
  var bestScore = 0;

  knowledge.forEach(function (item) {
    var itemWords = cleanWords(item.q + " " + item.a);
    var score = 0;

    askedWords.forEach(function (word) {
      itemWords.forEach(function (itemWord) {
        if (itemWord === word) score += 2;
        else if (itemWord.indexOf(word) === 0 || word.indexOf(itemWord) === 0) score += 1;
      });
    });

    if (score > bestScore) {
      bestScore = score;
      best = item;
    }
  });

  return bestScore >= 2 ? best : null;
}

/* ==========================================================
   RENDERING
   ========================================================== */
function renderKB() {
  kbList.innerHTML = "";
  kbCount.textContent = knowledge.length + (knowledge.length === 1 ? " item" : " items");

  if (knowledge.length === 0) {
    kbList.innerHTML = '<p class="kb-empty">Nothing taught yet. Add a question and answer, or load the sample data.</p>';
    renderSuggestions();
    return;
  }

  knowledge.forEach(function (item, index) {
    var box = document.createElement("div");
    box.className = "kb-item";

    var title = document.createElement("strong");
    title.textContent = item.q;

    var body = document.createElement("span");
    body.textContent = item.a;

    var del = document.createElement("button");
    del.className = "kb-del";
    del.textContent = "X";
    del.title = "Remove";
    del.addEventListener("click", function () { removeItem(item, index); });

    box.appendChild(title);
    box.appendChild(body);
    box.appendChild(del);
    kbList.appendChild(box);
  });

  renderSuggestions();
}

function renderSuggestions() {
  suggestions.innerHTML = "";
  knowledge.slice(0, 3).forEach(function (item) {
    var chip = document.createElement("button");
    chip.className = "chip";
    chip.type = "button";
    chip.textContent = item.q;
    chip.addEventListener("click", function () {
      demoInput.value = item.q;
      demoForm.dispatchEvent(new Event("submit", { cancelable: true }));
    });
    suggestions.appendChild(chip);
  });
}

/* ==========================================================
   LOADING THE KNOWLEDGE BASE
   ========================================================== */
function loadKnowledge() {
  if (Api.online) {
    return Api.getKnowledge()
      .then(function (rows) {
        knowledge = rows;
        renderKB();
      })
      .catch(function () {
        loadLocal();
        renderKB();
      });
  }

  loadLocal();
  renderKB();
  return Promise.resolve();
}

/* ---------- TEACH THE BOT ---------- */
kbForm.addEventListener("submit", function (e) {
  e.preventDefault();
  kbError.textContent = "";

  var question = kbQ.value.trim();
  var answer = kbA.value.trim();

  if (question.length < 5) {
    kbError.textContent = "The question should be at least 5 characters.";
    return;
  }
  if (answer.length < 5) {
    kbError.textContent = "The answer should be at least 5 characters.";
    return;
  }

  function afterAdd() {
    kbQ.value = "";
    kbA.value = "";
    kbQ.focus();
    renderKB();
    addBubble(demoChat, "bot", 'Learned it! You can now ask me: "' + question + '"');
  }

  if (Api.online) {
    Api.addKnowledge(question, answer)
      .then(function (item) {
        knowledge.push(item);
        afterAdd();
      })
      .catch(function (err) {
        kbError.textContent = err.message;
      });
  } else {
    knowledge.push({ id: Date.now(), q: question, a: answer });
    saveLocal();
    afterAdd();
  }
});

/* ---------- REMOVE ONE ITEM ---------- */
function removeItem(item, index) {
  if (Api.online && item.id) {
    Api.deleteKnowledge(item.id)
      .then(function () {
        knowledge = knowledge.filter(function (row) { return row.id !== item.id; });
        renderKB();
      })
      .catch(function (err) { kbError.textContent = err.message; });
  } else {
    knowledge.splice(index, 1);
    saveLocal();
    renderKB();
  }
}

/* ---------- SAMPLE DATA ---------- */
kbSample.addEventListener("click", function () {
  if (Api.online) {
    Api.loadSample().then(function (rows) {
      knowledge = rows;
      renderKB();
      addBubble(demoChat, "bot", "I just learned 5 sample answers. Try asking me about delivery, timings or returns.");
    });
  } else {
    knowledge = sampleData.slice();
    saveLocal();
    renderKB();
    addBubble(demoChat, "bot", "I just learned 5 sample answers. Try asking me about delivery, timings or returns.");
  }
});

/* ---------- CLEAR EVERYTHING ---------- */
kbClear.addEventListener("click", function () {
  if (Api.online) {
    Api.clearKnowledge().then(function () {
      knowledge = [];
      renderKB();
      addBubble(demoChat, "bot", "My knowledge base is empty now. Teach me something new.");
    });
  } else {
    knowledge = [];
    saveLocal();
    renderKB();
    addBubble(demoChat, "bot", "My knowledge base is empty now. Teach me something new.");
  }
});

/* ==========================================================
   CHAT
   ========================================================== */
demoForm.addEventListener("submit", function (e) {
  e.preventDefault();

  var question = demoInput.value.trim();
  if (question === "") return;

  addBubble(demoChat, "user", question);
  demoInput.value = "";

  var dots = showTyping(demoChat);

  /* ----- Backend path: the real OpenAI answer ----- */
  if (Api.online) {
    Api.chat(question)
      .then(function (data) {
        dots.remove();
        addBubble(demoChat, "bot", data.reply, data.source ? 'Source: "' + data.source + '"' : null);
        if (!data.answered && data.mode !== "empty") addLeadRow(question);
      })
      .catch(function (err) {
        dots.remove();
        addBubble(demoChat, "bot", "Could not reach the server: " + err.message);
      });
    return;
  }

  /* ----- Offline path: matching inside the browser ----- */
  setTimeout(function () {
    dots.remove();

    if (knowledge.length === 0) {
      addBubble(demoChat, "bot", "I have not been taught anything yet. Add a question and answer on the left, or click 'Load sample data'.");
      return;
    }

    var match = searchKnowledge(question);

    if (match) {
      addBubble(demoChat, "bot", match.a, 'Source: "' + match.q + '"');
    } else {
      addBubble(demoChat, "bot", "Sorry, I could not find that in my content. I will not guess an answer. Our team will get back to you - I have saved your question.");
      addLeadRow(question);
    }
  }, 800);
});

/* ==========================================================
   LEADS TABLE
   ========================================================== */
function addLeadRow(question, timeString) {
  leadCount++;

  var empty = leadsBody.querySelector(".empty-row");
  if (empty) empty.remove();

  var now = timeString ? new Date(timeString) : new Date();
  var time = now.getHours() + ":" + String(now.getMinutes()).padStart(2, "0");

  var row = document.createElement("tr");
  row.innerHTML =
    "<td>" + leadCount + "</td>" +
    "<td></td>" +
    '<td><span class="status-new">New lead</span></td>' +
    "<td>" + time + "</td>";
  row.children[1].textContent = question;   // safe text, no HTML injection

  leadsBody.appendChild(row);
}

function loadLeads() {
  if (!Api.online) return;
  Api.getLeads().then(function (rows) {
    rows.forEach(function (lead) { addLeadRow(lead.question, lead.time); });
  }).catch(function () { /* ignore */ });
}

/* ==========================================================
   START
   Wait for the health check in api.js, then load everything.
   ========================================================== */
Api.checkHealth().then(function () {
  paintApiStatus();
  loadKnowledge();
  loadLeads();

  var where = Api.online
    ? (Api.aiEnabled
        ? "I am connected to the backend and answering with OpenAI."
        : "I am connected to the backend, but no API key is set, so I am using word matching.")
    : "The backend is not running, so I am working inside your browser.";

  addBubble(demoChat, "bot", "Hi! I am your bot. Teach me on the left, then ask me anything here. I only answer from what you taught me.");
  addBubble(demoChat, "bot", where);
});
