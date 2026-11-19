/* ==========================================================
   WebtiqAI — Backend Server
   Node.js + Express + OpenAI API

   What it does
   ------------
   1. Serves the website (index.html, demo.html, css, js)
   2. /api/knowledge  - the bot's Knowledge Base (add / list / delete)
   3. /api/chat       - asks OpenAI, answering ONLY from the Knowledge Base
   4. /api/leads      - questions the bot could not answer
   5. /api/contact    - the contact form on the landing page
   6. /api/health     - tells the frontend if the API key is configured

   If no OPENAI_API_KEY is set, the server falls back to a local
   word-matching engine, so the demo always works.
   ========================================================== */

require("dotenv").config();

const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 5000;

const OPENAI_API_KEY = process.env.OPENAI_API_KEY || "";
const OPENAI_MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";
const BUSINESS_NAME = process.env.BUSINESS_NAME || "our business";

/* ---------- MIDDLEWARE ---------- */
app.use(cors());
app.use(express.json({ limit: "100kb" }));

// Serve the website itself (one folder up from /server)
app.use(express.static(path.join(__dirname, "..")));

/* ==========================================================
   SIMPLE JSON FILE DATABASE
   For a mini project a JSON file is enough. In the real
   product this would be PostgreSQL / Supabase.
   ========================================================== */

const DATA_DIR = path.join(__dirname, "data");
const FILES = {
  knowledge: path.join(DATA_DIR, "knowledge.json"),
  leads: path.join(DATA_DIR, "leads.json"),
  messages: path.join(DATA_DIR, "messages.json")
};

function ensureData() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  Object.values(FILES).forEach(function (file) {
    if (!fs.existsSync(file)) fs.writeFileSync(file, "[]", "utf8");
  });
}

function readData(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (err) {
    console.error("Could not read", file, "-", err.message);
    return [];
  }
}

function writeData(file, rows) {
  fs.writeFileSync(file, JSON.stringify(rows, null, 2), "utf8");
}

ensureData();

/* ==========================================================
   OFFLINE FALLBACK ENGINE
   Used when there is no API key, or if OpenAI fails.
   Same scoring idea as the frontend demo.
   ========================================================== */

const STOP_WORDS = ["the", "is", "are", "do", "does", "you", "your", "a", "an",
  "of", "to", "in", "on", "for", "what", "how", "can", "i", "we", "and",
  "me", "my", "it", "at", "with"];

function cleanWords(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter(function (w) { return w.length > 1 && !STOP_WORDS.includes(w); });
}

function matchLocally(question, knowledge) {
  const askedWords = cleanWords(question);
  let best = null;
  let bestScore = 0;

  knowledge.forEach(function (item) {
    const itemWords = cleanWords(item.q + " " + item.a);
    let score = 0;

    askedWords.forEach(function (word) {
      itemWords.forEach(function (itemWord) {
        if (itemWord === word) score += 2;
        else if (itemWord.startsWith(word) || word.startsWith(itemWord)) score += 1;
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
   OPENAI CALL
   Uses the Chat Completions API over plain fetch
   (built into Node 18+), so there is no extra SDK to install.
   ========================================================== */

async function askOpenAI(question, knowledge) {
  const content = knowledge
    .map(function (item, i) { return (i + 1) + ". Q: " + item.q + "\n   A: " + item.a; })
    .join("\n");

  const systemPrompt =
    "You are the website support assistant for " + BUSINESS_NAME + ".\n" +
    "Answer ONLY using the content below. Never invent facts, prices or policies.\n" +
    "If the answer is not in the content, reply with exactly: NO_ANSWER\n" +
    "Keep answers short (1-3 sentences) and friendly. Reply in the language the visitor used.\n\n" +
    "--- CONTENT ---\n" + content;

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + OPENAI_API_KEY
    },
    body: JSON.stringify({
      model: OPENAI_MODEL,
      temperature: 0.2,
      max_tokens: 200,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: question }
      ]
    })
  });

  if (!response.ok) {
    const details = await response.text();
    throw new Error("OpenAI returned " + response.status + ": " + details.slice(0, 200));
  }

  const data = await response.json();
  return (data.choices[0].message.content || "").trim();
}

/* ==========================================================
   ROUTES
   ========================================================== */

/* ---------- HEALTH ---------- */
app.get("/api/health", function (req, res) {
  res.json({
    status: "ok",
    aiEnabled: OPENAI_API_KEY !== "",
    model: OPENAI_API_KEY ? OPENAI_MODEL : "offline-matching",
    knowledgeItems: readData(FILES.knowledge).length
  });
});

/* ---------- KNOWLEDGE BASE ---------- */

// List everything the bot knows
app.get("/api/knowledge", function (req, res) {
  res.json(readData(FILES.knowledge));
});

// Teach the bot something new
app.post("/api/knowledge", function (req, res) {
  const q = String(req.body.q || "").trim();
  const a = String(req.body.a || "").trim();

  if (q.length < 5 || a.length < 5) {
    return res.status(400).json({ error: "Both the question and the answer need at least 5 characters." });
  }
  if (q.length > 300 || a.length > 2000) {
    return res.status(400).json({ error: "That is too long for one knowledge item." });
  }

  const knowledge = readData(FILES.knowledge);
  const item = { id: Date.now(), q: q, a: a, createdAt: new Date().toISOString() };

  knowledge.push(item);
  writeData(FILES.knowledge, knowledge);

  res.status(201).json(item);
});

// Forget one item
app.delete("/api/knowledge/:id", function (req, res) {
  const id = Number(req.params.id);
  const knowledge = readData(FILES.knowledge);
  const left = knowledge.filter(function (item) { return item.id !== id; });

  if (left.length === knowledge.length) {
    return res.status(404).json({ error: "That item was not found." });
  }

  writeData(FILES.knowledge, left);
  res.json({ deleted: id });
});

// Forget everything
app.delete("/api/knowledge", function (req, res) {
  writeData(FILES.knowledge, []);
  res.json({ cleared: true });
});

// Load the 5 sample answers
app.post("/api/knowledge/sample", function (req, res) {
  const samples = [
    { q: "What are your opening hours?", a: "We are open Monday to Saturday, 10 AM to 7 PM. Sunday is closed." },
    { q: "Do you offer home delivery?", a: "Yes, we deliver across the city in 2-3 days. Delivery is free on orders above Rs 999." },
    { q: "What is your return policy?", a: "You can return any product within 7 days of delivery, with the original bill." },
    { q: "Which payment methods do you accept?", a: "We accept UPI, all major cards, net banking and cash on delivery." },
    { q: "Where is your shop located?", a: "Our shop is at Shop 12, Main Market Road, near the city bus stand." }
  ];

  const rows = samples.map(function (s, i) {
    return { id: Date.now() + i, q: s.q, a: s.a, createdAt: new Date().toISOString() };
  });

  writeData(FILES.knowledge, rows);
  res.status(201).json(rows);
});

/* ---------- CHAT ---------- */
app.post("/api/chat", async function (req, res) {
  const message = String(req.body.message || "").trim();

  if (message === "") {
    return res.status(400).json({ error: "Please type a question." });
  }
  if (message.length > 500) {
    return res.status(400).json({ error: "That question is too long." });
  }

  const knowledge = readData(FILES.knowledge);

  if (knowledge.length === 0) {
    return res.json({
      reply: "I have not been taught anything yet. Add a question and answer in the Knowledge Base first.",
      answered: false,
      source: null,
      mode: "empty"
    });
  }

  // ----- Path A: OpenAI -----
  if (OPENAI_API_KEY) {
    try {
      const answer = await askOpenAI(message, knowledge);

      if (answer.includes("NO_ANSWER")) {
        saveLead(message);
        return res.json({
          reply: "Sorry, I could not find that in my content, and I will not guess. Our team will get back to you - I have saved your question.",
          answered: false,
          source: null,
          mode: "ai"
        });
      }

      // Show which knowledge item is closest, as the "source"
      const closest = matchLocally(message, knowledge);

      return res.json({
        reply: answer,
        answered: true,
        source: closest ? closest.q : null,
        mode: "ai"
      });

    } catch (err) {
      console.error("OpenAI failed, using offline matching -", err.message);
      // falls through to Path B so the demo never breaks
    }
  }

  // ----- Path B: offline matching -----
  const match = matchLocally(message, knowledge);

  if (match) {
    return res.json({
      reply: match.a,
      answered: true,
      source: match.q,
      mode: "offline"
    });
  }

  saveLead(message);
  res.json({
    reply: "Sorry, I could not find that in my content. I will not guess an answer. Our team will get back to you - I have saved your question.",
    answered: false,
    source: null,
    mode: "offline"
  });
});

/* ==========================================================
   SITE ASSISTANT
   The floating chat button on the landing page. It answers
   about WebtiqAI itself, so it has its own fixed content and
   never touches the business Knowledge Base.
   ========================================================== */

// The extra words in each question are there on purpose: the offline
// matching engine uses them as keywords when there is no API key.
const SITE_KNOWLEDGE = [
  { q: "Hi hello hey namaste greeting", a: "Hello! I am the WebtiqAI assistant. Ask me about pricing, setup or features." },
  { q: "What is WebtiqAI and how does it work?", a: "WebtiqAI is an AI chatbot for business websites. It learns from your own content and answers your visitors 24 hours a day." },
  { q: "How much does it cost? Price, pricing, plans, charges, rupees", a: "There are 3 plans: Starter is free, Growth is Rs 999 per month and Business is Rs 2499 per month. Yearly billing saves 20%." },
  { q: "Is there a free plan, free trial or demo to try?", a: "Yes, the Starter plan is free and includes 100 chats a month. You can also try the live demo page right now." },
  { q: "How do I install, setup, integrate or add the code to my website?", a: "Setup takes about 3 minutes: add your website, train the bot, then paste one script tag before the closing body tag." },
  { q: "How do I train or teach the bot? Knowledge base, content, learning", a: "You paste your FAQs, services, prices and policies into the Knowledge Base. The bot answers only from that content." },
  { q: "Which languages are supported? Hindi, English, multilingual", a: "The bot replies in the visitor's own language and supports over 40 languages." },
  { q: "What happens when the bot cannot answer? Leads, human team, agent, contact", a: "It says so honestly, offers your human team, and collects the visitor's name and email as a lead." },
  { q: "Which websites or platforms does it work on? WordPress, Shopify, Wix, HTML", a: "Any website where you can add a script tag - WordPress, Shopify, Wix, Webflow or a plain HTML site." },
  { q: "Is my data safe, secure and private?", a: "Your content is only used to answer your visitors. You can delete anything from the Knowledge Base at any time." },
  { q: "What support and working hours do you offer? 24/7 help", a: "The bot answers 24/7. Our human support team replies within 24 hours." }
];

app.post("/api/site-chat", async function (req, res) {
  const message = String(req.body.message || "").trim();

  if (message === "" || message.length > 500) {
    return res.status(400).json({ error: "Please type a shorter question." });
  }

  if (OPENAI_API_KEY) {
    try {
      const answer = await askOpenAI(message, SITE_KNOWLEDGE);
      if (!answer.includes("NO_ANSWER")) {
        return res.json({ reply: answer, answered: true, mode: "ai" });
      }
      return res.json({
        reply: "I could not find that in my content. Please use the contact form below the FAQ section and our team will reply.",
        answered: false,
        mode: "ai"
      });
    } catch (err) {
      console.error("OpenAI failed on site-chat -", err.message);
    }
  }

  const match = matchLocally(message, SITE_KNOWLEDGE);
  res.json({
    reply: match
      ? match.a
      : "I could not find that in my content. Please use the contact form below the FAQ section and our team will reply.",
    answered: Boolean(match),
    mode: "offline"
  });
});

/* ---------- LEADS ---------- */
function saveLead(question) {
  const leads = readData(FILES.leads);
  leads.push({
    id: Date.now(),
    question: question,
    status: "New lead",
    time: new Date().toISOString()
  });
  writeData(FILES.leads, leads);
}

app.get("/api/leads", function (req, res) {
  res.json(readData(FILES.leads));
});

app.delete("/api/leads", function (req, res) {
  writeData(FILES.leads, []);
  res.json({ cleared: true });
});

/* ---------- CONTACT FORM ---------- */
app.post("/api/contact", function (req, res) {
  const name = String(req.body.name || "").trim();
  const email = String(req.body.email || "").trim();
  const website = String(req.body.website || "").trim();
  const message = String(req.body.message || "").trim();

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  if (name.length < 3) return res.status(400).json({ error: "Please enter your name." });
  if (!emailPattern.test(email)) return res.status(400).json({ error: "Please enter a valid email address." });
  if (website.length < 4) return res.status(400).json({ error: "Please enter your website." });
  if (message.length < 10) return res.status(400).json({ error: "Please write a longer message." });

  const messages = readData(FILES.messages);
  messages.push({
    id: Date.now(),
    name: name,
    email: email,
    website: website,
    message: message,
    time: new Date().toISOString()
  });
  writeData(FILES.messages, messages);

  res.status(201).json({ ok: true, message: "Thank you! We will reply within 24 hours." });
});

app.get("/api/messages", function (req, res) {
  res.json(readData(FILES.messages));
});

/* ---------- START ---------- */
app.listen(PORT, function () {
  console.log("");
  console.log("  WebtiqAI backend is running");
  console.log("  ----------------------------------------");
  console.log("  Website : http://localhost:" + PORT);
  console.log("  Demo    : http://localhost:" + PORT + "/demo.html");
  console.log("  API     : http://localhost:" + PORT + "/api/health");
  console.log("  AI mode : " + (OPENAI_API_KEY
    ? "OpenAI (" + OPENAI_MODEL + ")"
    : "OFFLINE matching - add OPENAI_API_KEY in server/.env to enable AI"));
  console.log("");
});
