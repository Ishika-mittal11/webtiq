/* =========================================================
   WebtiqAI — Mini Project Presentation
   Built with pptxgenjs. Animations are injected afterwards
   by animate.py (shape names carry the effect plan).

   Shape naming convention used for animation:
     <effect>_<group>__<part>
     effect = fade | fly | zoom | wipe
     shapes whose name starts with "bg" are never animated
   ========================================================= */

const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 inches

/* ---------- THEME ---------- */
const THEME = {
  name: "WebtiqAI",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0B2D6B", // deep navy  (text1)
    lt1: "FFFFFF", // white      (background1)
    dk2: "334155", // slate      (text2)
    lt2: "F2F6FF", // pale blue  (background2)
    accent1: "1D6FE8", // blue
    accent2: "06B6D4", // cyan
    accent3: "7C3AED", // violet
    accent4: "EC4899", // pink
    accent5: "F97316", // orange
    accent6: "10B981", // green
    hlink: "1D6FE8",
    folHlink: "7C3AED",
  },
};
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Ishika Mittal, Nikhil Sharma, Ojasvi Garg";
pres.title = "WebtiqAI - Mini Project Presentation";
pres.subject = "AI chatbot for business websites";

const C = pres.SchemeColor;

/* ---------- palette shortcuts (hex, for options that need hex) ---------- */
const BLUE = "1D6FE8", CYAN = "06B6D4", VIOLET = "7C3AED",
      PINK = "EC4899", ORANGE = "F97316", GREEN = "10B981",
      NAVY = "0B2D6B", SLATE = "475569", MUTED = "64748B",
      CARDLINE = "E2E8F7", RED = "EF4444", AMBER = "F59E0B";

/* ---------- geometry ---------- */
const M = 0.62;                 // page margin
const CW = 13.333 - M * 2;      // content width = 12.09
const TOP = 1.78;               // where content starts

/* fresh shadow object every call (pptxgenjs mutates them) */
const shadow = (blur = 14, offset = 3, opacity = 0.18) => ({
  type: "outer", angle: 90, blur, offset, color: "7C8FB8", opacity,
});

/* ---------- LAYOUTS ---------- */
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { path: "bg/bg_dark.jpg" },
  objects: [],
});

pres.defineSlideMaster({
  title: "CONTENT",
  background: { path: "bg/bg_light.jpg" },
  objects: [
    {
      placeholder: {
        options: { name: "eyebrow", type: "body", x: M, y: 0.44, w: 9, h: 0.3,
          fontSize: 13, bold: true, color: VIOLET, charSpacing: 2, margin: 0, valign: "middle" },
        text: "",
      },
    },
    {
      placeholder: {
        options: { name: "title", type: "title", x: M, y: 0.74, w: 12.0, h: 0.72,
          fontSize: 34, bold: true, color: NAVY, margin: 0, valign: "middle", align: "left" },
        text: "",
      },
    },
    { text: { text: "WebtiqAI", options: { x: M, y: 6.95, w: 3, h: 0.3, fontSize: 10, color: MUTED, margin: 0 } } },
  ],
  slideNumber: { x: 12.5, y: 6.95, w: 0.5, h: 0.3, fontSize: 10, color: MUTED, align: "right" },
});

pres.defineSlideMaster({
  title: "SECTION_DARK",
  background: { path: "bg/bg_section.jpg" },
  objects: [],
});

/* ---------- helpers ---------- */
function card(slide, o) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: o.x, y: o.y, w: o.w, h: o.h, rectRadius: 0.1,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || CARDLINE, width: 1 },
    shadow: shadow(),
    objectName: o.name,
  });
}

function iconBadge(slide, o) {
  const d = o.d || 0.62;
  slide.addShape(pres.ShapeType.ellipse, {
    x: o.x, y: o.y, w: d, h: d, fill: { color: o.color }, objectName: o.name + "__badge",
  });
  slide.addImage({
    path: `icons/${o.icon}.png`,
    x: o.x + d * 0.235, y: o.y + d * 0.235, w: d * 0.53, h: d * 0.53,
    objectName: o.name + "__icon",
  });
}

/* a soft tinted callout with an icon — used at the bottom of several slides */
function callout(slide, o) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: M, y: o.y, w: CW, h: 0.72, rectRadius: 0.1,
    fill: { color: o.fill || "E8F0FF" }, line: { color: o.line || "C7DBFF", width: 1 },
    objectName: o.name + "__box",
  });
  slide.addShape(pres.ShapeType.ellipse, {
    x: M + 0.22, y: o.y + 0.17, w: 0.38, h: 0.38,
    fill: { color: o.color || BLUE }, objectName: o.name + "__dot",
  });
  slide.addImage({
    path: `icons/${o.icon || "target"}.png`,
    x: M + 0.31, y: o.y + 0.26, w: 0.2, h: 0.2, objectName: o.name + "__ic",
  });
  slide.addText(o.text, {
    x: M + 0.74, y: o.y + 0.06, w: CW - 0.95, h: 0.6, fontSize: 13.5, color: NAVY,
    valign: "middle", margin: 0, isTextBox: true, objectName: o.name + "__txt",
  });
}

function slideHead(slide, eyebrow, title) {
  slide.addText(eyebrow, { placeholder: "eyebrow" });
  slide.addText(title, { placeholder: "title" });
}

/* =========================================================
   SECTIONS
   ========================================================= */
pres.addSection({ title: "Opening" });

/* ---------- 1. TITLE ---------- */
{
  const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Opening" });

  s.addShape(pres.ShapeType.ellipse, {
    x: 7.55, y: 0.62, w: 5.3, h: 5.3, fill: { color: "FFFFFF", transparency: 88 },
    line: { color: "FFFFFF", width: 1, transparency: 60 }, objectName: "zoom_ring",
  });
  s.addImage({ path: "img/bot.png", x: 8.05, y: 1.1, w: 4.3, h: 4.25, objectName: "zoom_bot" });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 0.52, w: 0.98, h: 0.98, rectRadius: 0.14, fill: { color: "FFFFFF" },
    objectName: "fade_logo__box",
  });
  s.addImage({ path: "img/logo.png", x: M + 0.07, y: 0.59, w: 0.84, h: 0.84, objectName: "fade_logo__img" });

  s.addText("MINI PROJECT PRESENTATION", {
    x: M, y: 1.95, w: 7, h: 0.3, fontSize: 13.5, bold: true, color: "CFE6FF",
    charSpacing: 3, margin: 0, isTextBox: true, objectName: "fly_eyebrow",
  });
  s.addText("WebtiqAI", {
    x: M - 0.06, y: 2.28, w: 7, h: 1.0, fontSize: 60, bold: true, color: "FFFFFF",
    margin: 0, isTextBox: true, objectName: "fly_title",
  });
  s.addText(
    "An AI chatbot that answers website visitors 24/7 - using only the business's own content, and never an invented fact.",
    { x: M, y: 3.32, w: 6.6, h: 0.95, fontSize: 16, color: "E6F1FF", lineSpacing: 24,
      margin: 0, isTextBox: true, objectName: "fade_sub" }
  );

  s.addText("TEAM", {
    x: M, y: 4.55, w: 3, h: 0.26, fontSize: 12, bold: true, color: "FFD166",
    charSpacing: 3, margin: 0, isTextBox: true, objectName: "fade_teamlabel",
  });
  const team = [
    ["Ishika Mittal", "fly_t1"],
    ["Nikhil Sharma", "fly_t2"],
    ["Ojasvi Garg", "fly_t3"],
  ];
  team.forEach((t, i) => {
    s.addText(t[0], {
      x: M, y: 4.88 + i * 0.42, w: 4, h: 0.38, fontSize: 19, bold: true, color: "FFFFFF",
      margin: 0, isTextBox: true, objectName: t[1],
    });
  });

  s.addNotes(
    "Good morning. We are Ishika, Nikhil and Ojasvi, and our project is WebtiqAI - " +
    "an AI chatbot that a business can train on its own content and embed on its website. " +
    "The whole frontend is plain HTML, CSS and JavaScript, and the backend is Node.js with Express."
  );
}

/* ---------- 2. PROBLEM ---------- */
pres.addSection({ title: "Problem and solution" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Problem and solution" });
  slideHead(s, "THE PROBLEM", "Customer support does not scale");

  const items = [
    { icon: "clock", color: BLUE, t: "Nobody answers at night",
      b: "A small business cannot staff live chat 24 hours. A visitor with one simple question at 11 PM leaves and buys somewhere else." },
    { icon: "ghost", color: PINK, t: "A plain AI invents answers",
      b: "A general chatbot will confidently state a price, an offer or a return policy the business never had. That costs trust." },
    { icon: "code", color: VIOLET, t: "Custom bots need developers",
      b: "Training a bot normally needs machine-learning skills and weeks of work that a shop owner simply does not have." },
  ];
  const w = (CW - 0.7) / 3;
  items.forEach((it, i) => {
    const x = M + i * (w + 0.35);
    const g = `fly_p${i + 1}`;
    card(s, { x, y: TOP, w, h: 3.25, name: g + "__card" });
    iconBadge(s, { x: x + 0.38, y: TOP + 0.38, d: 0.7, color: it.color, icon: it.icon, name: g });
    s.addText(it.t, { x: x + 0.38, y: TOP + 1.25, w: w - 0.76, h: 0.6, fontSize: 18, bold: true,
      color: NAVY, margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(it.b, { x: x + 0.38, y: TOP + 1.9, w: w - 0.76, h: 1.15, fontSize: 13.5, color: SLATE,
      lineSpacing: 19, margin: 0, isTextBox: true, objectName: g + "__b" });
  });

  callout(s, { y: 5.55, name: "fade_cta", icon: "target", color: GREEN, fill: "E6F8F0", line: "B6EBD6",
    text: "Our goal: a support bot that answers only from the business's own content, and can be added to any website in minutes." });

  s.addNotes("Three problems. Support does not scale at night, a general AI hallucinates, and a custom bot is out of reach for a small shop.");
}

/* ---------- 3. SOLUTION ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Problem and solution" });
  slideHead(s, "OUR SOLUTION", "From content to a live chatbot in four steps");

  const steps = [
    { n: "01", t: "Add your content", b: "Paste FAQs, prices, timings and policies into the Knowledge Base.", c: BLUE },
    { n: "02", t: "The server grounds it", b: "Node.js builds a prompt that contains only that content and strict rules.", c: CYAN },
    { n: "03", t: "OpenAI answers", b: "gpt-4o-mini replies from those facts, in the visitor's own language.", c: VIOLET },
    { n: "04", t: "Unknown becomes a lead", b: "If the answer is not there, the bot says so and saves the question.", c: PINK },
  ];
  const w = (CW - 3 * 0.3) / 4;
  steps.forEach((st, i) => {
    const x = M + i * (w + 0.3);
    const g = `fly_s${i + 1}`;
    card(s, { x, y: TOP, w, h: 3.3, name: g + "__card" });
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: TOP + 0.34, w: 0.82, h: 0.82,
      fill: { color: st.c }, objectName: g + "__circle" });
    s.addText(st.n, { x: x + 0.3, y: TOP + 0.34, w: 0.82, h: 0.82, fontSize: 20, bold: true,
      color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: g + "__n" });
    s.addText(st.t, { x: x + 0.3, y: TOP + 1.35, w: w - 0.6, h: 0.56, fontSize: 16.5, bold: true,
      color: NAVY, margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(st.b, { x: x + 0.3, y: TOP + 1.92, w: w - 0.6, h: 1.2, fontSize: 13, color: SLATE,
      lineSpacing: 18, margin: 0, isTextBox: true, objectName: g + "__b" });

    if (i < 3) {
      s.addShape(pres.ShapeType.rightArrow, {
        x: x + w + 0.045, y: TOP + 0.62, w: 0.21, h: 0.26, fill: { color: "9FB6DC" },
        objectName: `fade_arrow${i + 1}`,
      });
    }
  });

  callout(s, { y: 5.55, name: "fade_cta3", icon: "code", color: VIOLET, fill: "F1ECFE", line: "DCCEFB",
    text: "The business never writes code. One script tag is the only thing ever installed on their site." });

  s.addNotes("Four steps: add content, the server grounds it, OpenAI phrases the answer, and anything unknown becomes a lead.");
}

/* ---------- 4. FEATURES ---------- */
pres.addSection({ title: "What we built" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "What we built" });
  slideHead(s, "KEY FEATURES", "What WebtiqAI offers");

  const feats = [
    { icon: "book", c: BLUE, t: "Knowledge Base", b: "Add, view and delete everything the bot knows. Stored on the server as JSON." },
    { icon: "shield", c: CYAN, t: "Grounded answers", b: "Replies come only from trained content. No invented prices or policies." },
    { icon: "check", c: VIOLET, t: "Source citation", b: "Every answer shows the exact knowledge item it was taken from." },
    { icon: "user", c: PINK, t: "Lead capture", b: "A question the bot cannot answer is saved with a timestamp for the team." },
    { icon: "chat", c: ORANGE, t: "Floating chat widget", b: "A site assistant on every page that answers about the product itself." },
    { icon: "zap", c: GREEN, t: "Graceful fallback", b: "Works with no API key - and even with the server switched off." },
  ];
  const w = (CW - 0.7) / 3, h = 1.93;
  feats.forEach((f, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * (w + 0.35), y = TOP + row * (h + 0.26);
    const g = `fly_f${i + 1}`;
    card(s, { x, y, w, h, name: g + "__card" });
    iconBadge(s, { x: x + 0.33, y: y + 0.33, d: 0.62, color: f.c, icon: f.icon, name: g });
    s.addText(f.t, { x: x + 1.08, y: y + 0.36, w: w - 1.4, h: 0.55, fontSize: 16.5, bold: true,
      color: NAVY, valign: "middle", margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(f.b, { x: x + 0.33, y: y + 1.02, w: w - 0.66, h: 0.8, fontSize: 13, color: SLATE,
      lineSpacing: 18, margin: 0, isTextBox: true, objectName: g + "__b" });
  });

  callout(s, { y: 6.05, name: "fade_cta4", icon: "check", color: GREEN, fill: "E6F8F0", line: "B6EBD6",
    text: "Every one of these is working in the project - nothing on this slide is a mock-up." });

  s.addNotes("Six features. The two that matter most are grounded answers with a visible source, and lead capture when it does not know.");
}

/* ---------- 5. TECH STACK ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "What we built" });
  slideHead(s, "TOOLS WE USED", "Technology stack");

  const cols = [
    { icon: "monitor", c: BLUE, t: "Frontend", items: ["HTML5 semantic markup", "CSS Grid + Flexbox", "Vanilla JavaScript (ES6)", "No framework, no build"] },
    { icon: "server", c: CYAN, t: "Backend", items: ["Node.js 18+", "Express 4.x", "REST API, 12 endpoints", "dotenv for secrets"] },
    { icon: "cpu", c: VIOLET, t: "AI", items: ["OpenAI gpt-4o-mini", "Chat Completions API", "Prompt engineering", "temperature 0.2"] },
    { icon: "database", c: PINK, t: "Storage", items: ["JSON file database", "Node fs module", "knowledge / leads / messages", "Created automatically"] },
    { icon: "refresh", c: GREEN, t: "Fallback", items: ["Word-matching engine", "Stop-word filtering", "localStorage mode", "Three operating modes"] },
  ];
  const w = (CW - 4 * 0.28) / 5;
  cols.forEach((col, i) => {
    const x = M + i * (w + 0.28);
    const g = `fly_tc${i + 1}`;
    card(s, { x, y: TOP, w, h: 3.5, name: g + "__card" });
    iconBadge(s, { x: x + (w - 0.62) / 2, y: TOP + 0.3, d: 0.62, color: col.c, icon: col.icon, name: g });
    s.addText(col.t, { x, y: TOP + 1.02, w, h: 0.4, fontSize: 16.5, bold: true, color: NAVY,
      align: "center", margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(
      col.items.map((t, k) => ({ text: t, options: { breakLine: k < col.items.length - 1 } })),
      { x: x + 0.22, y: TOP + 1.5, w: w - 0.44, h: 1.8, fontSize: 12.5, color: SLATE,
        align: "center", lineSpacing: 20, margin: 0, isTextBox: true, objectName: g + "__b" }
    );
  });

  callout(s, { y: 5.75, name: "fade_cta5", icon: "zap", color: ORANGE, fill: "FFF1E4", line: "FBD6B0",
    text: "Only three npm packages: express, cors and dotenv. Everything else is written by hand." });

  s.addNotes("We deliberately avoided React and Bootstrap. The accordion, the chat, the validation - all hand written.");
}

/* ---------- 6. ARCHITECTURE ---------- */
pres.addSection({ title: "How it works" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "How it works" });
  slideHead(s, "HOW IT IS BUILT", "System architecture");

  const boxW = 3.5, boxH = 3.1, y = TOP + 0.22;
  const lanes = [
    { x: M, t: "BROWSER", c: BLUE, items: ["index.html  ·  demo.html", "style.css", "script.js  ·  demo.js", "api.js sends fetch() calls"] },
    { x: M + 4.3, t: "OUR SERVER", c: VIOLET, items: ["Node.js + Express", "12 REST endpoints", "Builds the grounded prompt", "Holds the secret API key"] },
    { x: M + 8.6, t: "EXTERNAL", c: CYAN, items: ["OpenAI gpt-4o-mini", "Chat Completions API", "", "JSON files: knowledge,", "leads, messages"] },
  ];
  lanes.forEach((ln, i) => {
    const g = `fly_a${i + 1}`;
    card(s, { x: ln.x, y, w: boxW, h: boxH, name: g + "__card" });
    s.addShape(pres.ShapeType.roundRect, { x: ln.x, y, w: boxW, h: 0.52, rectRadius: 0.1,
      fill: { color: ln.c }, objectName: g + "__head" });
    s.addText(ln.t, { x: ln.x, y, w: boxW, h: 0.52, fontSize: 13.5, bold: true, color: "FFFFFF",
      align: "center", valign: "middle", charSpacing: 2, margin: 0, isTextBox: true, objectName: g + "__ht" });
    s.addText(
      ln.items.map((t, k) => ({ text: t, options: { breakLine: k < ln.items.length - 1 } })),
      { x: ln.x + 0.28, y: y + 0.78, w: boxW - 0.56, h: 2.1, fontSize: 13, color: SLATE,
        lineSpacing: 22, margin: 0, isTextBox: true, objectName: g + "__b" }
    );
  });

  // arrows between lanes
  [0, 1].forEach((i) => {
    const ax = M + boxW + 0.16 + i * 4.3;
    s.addShape(pres.ShapeType.rightArrow, { x: ax, y: y + 1.15, w: 0.5, h: 0.24,
      fill: { color: BLUE }, objectName: `fade_ar${i}a` });
    s.addShape(pres.ShapeType.leftArrow, { x: ax, y: y + 1.75, w: 0.5, h: 0.24,
      fill: { color: "9FB6DC" }, objectName: `fade_ar${i}b` });
    s.addText(i === 0 ? "question" : "prompt + key", { x: ax - 0.26, y: y + 0.85, w: 1.0, h: 0.26,
      fontSize: 10, color: BLUE, align: "center", margin: 0, isTextBox: true, objectName: `fade_ar${i}t1` });
    s.addText(i === 0 ? "answer" : "reply text", { x: ax - 0.26, y: y + 2.01, w: 1.0, h: 0.26,
      fontSize: 10, color: MUTED, align: "center", margin: 0, isTextBox: true, objectName: `fade_ar${i}t2` });
  });

  callout(s, { y: 5.6, name: "fade_cta6", icon: "lock", color: RED, fill: "FFECEC", line: "FBC9C9",
    text: "The API key never leaves the server. The browser talks only to our own backend - otherwise anyone could read the key with Ctrl+U." });

  s.addNotes("Three layers. The important point is that the browser never calls OpenAI directly, because the key would then be public.");
}

/* ---------- 7. REQUEST LIFECYCLE ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "How it works" });
  slideHead(s, "INSIDE ONE QUESTION", "How an answer is produced");

  const steps = [
    { n: "1", t: "Visitor asks", b: "The submit event fires and preventDefault stops the page reloading.", c: BLUE },
    { n: "2", t: "fetch() to our API", b: "POST /api/chat carries the question as JSON.", c: BLUE },
    { n: "3", t: "Validate and read", b: "Express checks the length, then reads knowledge.json.", c: VIOLET },
    { n: "4", t: "Ground the prompt", b: "Rules plus the whole Knowledge Base become the system prompt.", c: VIOLET },
    { n: "5", t: "OpenAI replies", b: "gpt-4o-mini answers from those facts only.", c: CYAN },
    { n: "6", t: "Show or capture", b: "Answer with its source - or NO_ANSWER becomes a lead.", c: PINK },
  ];
  const w = (CW - 5 * 0.22) / 6;
  steps.forEach((st, i) => {
    const x = M + i * (w + 0.22);
    const g = `fly_l${i + 1}`;
    card(s, { x, y: TOP + 0.35, w, h: 2.45, name: g + "__card" });
    s.addShape(pres.ShapeType.ellipse, { x: x + (w - 0.6) / 2, y: TOP + 0.08, w: 0.6, h: 0.6,
      fill: { color: st.c }, line: { color: "FFFFFF", width: 2 }, objectName: g + "__circle" });
    s.addText(st.n, { x: x + (w - 0.6) / 2, y: TOP + 0.08, w: 0.6, h: 0.6, fontSize: 17, bold: true,
      color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: g + "__n" });
    s.addText(st.t, { x: x + 0.14, y: TOP + 0.82, w: w - 0.28, h: 0.5, fontSize: 14, bold: true,
      color: NAVY, align: "center", margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(st.b, { x: x + 0.14, y: TOP + 1.3, w: w - 0.28, h: 1.4, fontSize: 11.5, color: SLATE,
      align: "center", lineSpacing: 16, margin: 0, isTextBox: true, objectName: g + "__b" });
  });

  callout(s, { y: 5.7, name: "fade_cta7", icon: "target", color: BLUE,
    text: "Six steps, about two seconds: event handling, HTTP, middleware, validation, file read, prompt building, external API, DOM update." });

  s.addNotes("If the examiner says walk me through the project, this is the slide to narrate.");
}

/* ---------- 8. THE CORE IDEA ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "How it works" });
  slideHead(s, "THE CORE IDEA", "Grounding: why it cannot make things up");

  // left: prompt anatomy
  card(s, { x: M, y: TOP, w: 6.55, h: 3.45, name: "fly_pr__card" });
  s.addText("THE SYSTEM PROMPT WE SEND", { x: M + 0.3, y: TOP + 0.22, w: 5.9, h: 0.3, fontSize: 11.5,
    bold: true, color: VIOLET, charSpacing: 2, margin: 0, isTextBox: true, objectName: "fly_pr__h" });

  s.addShape(pres.ShapeType.roundRect, { x: M + 0.3, y: TOP + 0.62, w: 5.95, h: 0.86, rectRadius: 0.08,
    fill: { color: "FFF6DF" }, line: { color: "F3DFA8", width: 1 }, objectName: "fly_pr1__box" });
  s.addText("You are the support assistant for this business.\nAnswer ONLY using the content below. Never invent\nfacts, prices or policies.", {
    x: M + 0.45, y: TOP + 0.68, w: 5.7, h: 0.76, fontSize: 11.5, color: "7A5A17", fontFace: "Consolas",
    lineSpacing: 15, margin: 0, isTextBox: true, objectName: "fly_pr1__t" });

  s.addShape(pres.ShapeType.roundRect, { x: M + 0.3, y: TOP + 1.58, w: 5.95, h: 0.5, rectRadius: 0.08,
    fill: { color: "FFE9E9" }, line: { color: "FBC2C2", width: 1 }, objectName: "fly_pr2__box" });
  s.addText("If the answer is not in the content, reply: NO_ANSWER", {
    x: M + 0.45, y: TOP + 1.63, w: 5.7, h: 0.4, fontSize: 11.5, color: "A32D2D", fontFace: "Consolas",
    valign: "middle", margin: 0, isTextBox: true, objectName: "fly_pr2__t" });

  s.addShape(pres.ShapeType.roundRect, { x: M + 0.3, y: TOP + 2.18, w: 5.95, h: 1.0, rectRadius: 0.08,
    fill: { color: "E6F8F0" }, line: { color: "B6EBD6", width: 1 }, objectName: "fly_pr3__box" });
  s.addText("--- CONTENT ---\n1. Q: Do you offer home delivery?\n   A: Yes, we deliver across the city in 2-3 days.", {
    x: M + 0.45, y: TOP + 2.24, w: 5.7, h: 0.9, fontSize: 11.5, color: "16614A", fontFace: "Consolas",
    lineSpacing: 15, margin: 0, isTextBox: true, objectName: "fly_pr3__t" });

  // right: outcome cards
  const rx = M + 6.95, rw = CW - 6.95;
  card(s, { x: rx, y: TOP, w: rw, h: 1.62, name: "fly_o1__card" });
  iconBadge(s, { x: rx + 0.3, y: TOP + 0.28, d: 0.58, color: GREEN, icon: "check", name: "fly_o1" });
  s.addText("In the content", { x: rx + 1.0, y: TOP + 0.3, w: rw - 1.3, h: 0.5, fontSize: 16, bold: true,
    color: NAVY, valign: "middle", margin: 0, isTextBox: true, objectName: "fly_o1__t" });
  s.addText("The model only rephrases the fact it was given, and the reply shows which knowledge item it came from.", {
    x: rx + 0.3, y: TOP + 0.92, w: rw - 0.6, h: 0.6, fontSize: 13, color: SLATE, lineSpacing: 18,
    margin: 0, isTextBox: true, objectName: "fly_o1__b" });

  card(s, { x: rx, y: TOP + 1.84, w: rw, h: 1.61, name: "fly_o2__card" });
  iconBadge(s, { x: rx + 0.3, y: TOP + 2.12, d: 0.58, color: PINK, icon: "user", name: "fly_o2" });
  s.addText("Not in the content", { x: rx + 1.0, y: TOP + 2.14, w: rw - 1.3, h: 0.5, fontSize: 16, bold: true,
    color: NAVY, valign: "middle", margin: 0, isTextBox: true, objectName: "fly_o2__t" });
  s.addText("The model returns NO_ANSWER. The server detects that word, admits it honestly and saves a lead.", {
    x: rx + 0.3, y: TOP + 2.76, w: rw - 0.6, h: 0.6, fontSize: 13, color: SLATE, lineSpacing: 18,
    margin: 0, isTextBox: true, objectName: "fly_o2__b" });

  callout(s, { y: 5.6, name: "fade_cta8", icon: "search", color: VIOLET, fill: "F1ECFE", line: "DCCEFB",
    text: "This is Retrieval Augmented Generation in its simplest form: retrieve the content first, then let the model phrase the answer." });

  s.addNotes("The model is never asked to know our business. It is handed the facts and asked only to phrase them.");
}

/* ---------- 9. THREE MODES ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "How it works" });
  slideHead(s, "RELIABILITY", "Three operating modes, one working website");

  const modes = [
    { icon: "check", c: GREEN, dot: "22C55E", t: "AI mode", s: "Server on + API key",
      b: "OpenAI answers. Understands meaning, handles other languages and spelling mistakes.", tint: "EAFBF3" },
    { icon: "alert", c: AMBER, dot: "F59E0B", t: "Offline matching", s: "Server on, no key",
      b: "A word-scoring engine on the server answers instead. Knowledge still stored in JSON files.", tint: "FFF8E7" },
    { icon: "wifioff", c: RED, dot: "EF4444", t: "Browser mode", s: "Server stopped",
      b: "Matching runs in JavaScript and the Knowledge Base comes from localStorage.", tint: "FFEFEF" },
  ];
  const w = (CW - 0.7) / 3;
  modes.forEach((m, i) => {
    const x = M + i * (w + 0.35);
    const g = `fly_m${i + 1}`;
    card(s, { x, y: TOP, w, h: 3.0, fill: m.tint, line: "FFFFFF", name: g + "__card" });
    iconBadge(s, { x: x + 0.35, y: TOP + 0.35, d: 0.66, color: m.c, icon: m.icon, name: g });
    s.addText(m.t, { x: x + 1.12, y: TOP + 0.33, w: w - 1.4, h: 0.4, fontSize: 17, bold: true,
      color: NAVY, valign: "middle", margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(m.s, { x: x + 1.12, y: TOP + 0.7, w: w - 1.4, h: 0.3, fontSize: 12, color: m.c,
      bold: true, margin: 0, isTextBox: true, objectName: g + "__s" });
    s.addText(m.b, { x: x + 0.35, y: TOP + 1.3, w: w - 0.7, h: 1.2, fontSize: 13.5, color: SLATE,
      lineSpacing: 19, margin: 0, isTextBox: true, objectName: g + "__b" });
    s.addText("Badge on the page: " + ["green", "yellow", "red"][i], {
      x: x + 0.35, y: TOP + 2.45, w: w - 0.7, h: 0.3, fontSize: 11.5, bold: true, color: MUTED,
      margin: 0, isTextBox: true, objectName: g + "__badge2" });
  });

  callout(s, { y: 5.35, name: "fade_cta9", icon: "refresh", color: BLUE,
    text: "On load the page calls GET /api/health and adapts. A demo that crashes because the Wi-Fi dropped is a bad demo." });

  s.addNotes("Stop the server in front of them if they ask. The site keeps working and the badge turns red.");
}

/* ---------- 10. WALKTHROUGH ---------- */
pres.addSection({ title: "Demo" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Demo" });
  slideHead(s, "PRODUCT WALKTHROUGH", "The landing page and the site assistant");

  card(s, { x: M, y: TOP, w: 7.55, h: 3.95, name: "zoom_w1__card" });
  s.addImage({ path: "img/hero.png", x: M + 0.16, y: TOP + 0.16, w: 7.23, h: 3.4, objectName: "zoom_w1__img" });
  s.addText("Landing page: hero, live stats, features, pricing and FAQ - all hand-built", {
    x: M + 0.16, y: TOP + 3.6, w: 7.23, h: 0.3, fontSize: 12, color: MUTED, align: "center",
    margin: 0, isTextBox: true, objectName: "zoom_w1__cap" });

  const rx = M + 7.9, rw = CW - 7.9;
  card(s, { x: rx, y: TOP, w: rw, h: 3.95, name: "zoom_w2__card" });
  s.addImage({ path: "img/widget.png", x: rx + 0.73, y: TOP + 0.16, w: 2.72, h: 3.35, objectName: "zoom_w2__img" });
  s.addText("The floating assistant answers about WebtiqAI itself", {
    x: rx + 0.16, y: TOP + 3.6, w: rw - 0.32, h: 0.3, fontSize: 12, color: MUTED, align: "center",
    margin: 0, isTextBox: true, objectName: "zoom_w2__cap" });

  callout(s, { y: 6.0, name: "fade_cta10", icon: "chat", color: ORANGE, fill: "FFF1E4", line: "FBD6B0",
    text: "The widget uses a separate endpoint, /api/site-chat, so product questions never mix with the demo business's content." });

  s.addNotes("This is the real page running on localhost:5000. The widget is on every page.");
}

/* ---------- 11. LIVE DEMO ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Demo" });
  slideHead(s, "LIVE DEMO", "Train the bot, then ask it");

  card(s, { x: M, y: TOP, w: 5.05, h: 3.5, name: "zoom_d1__card" });
  s.addImage({ path: "img/kb.png", x: M + 0.15, y: TOP + 0.15, w: 4.75, h: 2.95, objectName: "zoom_d1__img" });
  s.addText("Knowledge Base: what the bot was taught", { x: M + 0.15, y: TOP + 3.14, w: 4.75, h: 0.28,
    fontSize: 12, color: MUTED, align: "center", margin: 0, isTextBox: true, objectName: "zoom_d1__cap" });

  card(s, { x: M + 5.4, y: TOP, w: 5.05, h: 3.5, name: "zoom_d2__card" });
  s.addImage({ path: "img/chat.png", x: M + 5.55, y: TOP + 0.15, w: 4.75, h: 2.95, objectName: "zoom_d2__img" });
  s.addText("The reply, with the source it came from", { x: M + 5.55, y: TOP + 3.14, w: 4.75, h: 0.28,
    fontSize: 12, color: MUTED, align: "center", margin: 0, isTextBox: true, objectName: "zoom_d2__cap" });

  const nx = M + 10.65, nw = CW - 10.65;
  const points = [
    { n: "1", t: "Load the sample\nknowledge", c: BLUE },
    { n: "2", t: "Ask about\ndelivery", c: VIOLET },
    { n: "3", t: "Answer + source\nappear", c: GREEN },
  ];
  points.forEach((p, i) => {
    const g = `fly_n${i + 1}`;
    const y = TOP + 0.12 + i * 1.12;
    s.addShape(pres.ShapeType.ellipse, { x: nx, y, w: 0.46, h: 0.46, fill: { color: p.c }, objectName: g + "__c" });
    s.addText(p.n, { x: nx, y, w: 0.46, h: 0.46, fontSize: 13, bold: true, color: "FFFFFF",
      align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: g + "__n" });
    s.addText(p.t, { x: nx + 0.58, y: y - 0.06, w: nw - 0.58, h: 0.62, fontSize: 12.5, color: NAVY,
      bold: true, lineSpacing: 16, valign: "middle", margin: 0, isTextBox: true, objectName: g + "__t" });
    if (i < 2) {
      s.addShape(pres.ShapeType.line, {
        x: nx + 0.23, y: y + 0.5, w: 0, h: 0.56,
        line: { color: "B9C9E6", width: 1.5, dashType: "sysDot" }, objectName: g + "__ln",
      });
    }
  });

  callout(s, { y: 5.6, name: "fade_cta11", icon: "check", color: GREEN, fill: "E6F8F0", line: "B6EBD6",
    text: "Result: the reply matched the trained policy word for word, and the Source line names the exact item it used." });

  s.addNotes("Demo live if possible: Load sample data, ask about delivery, point at the Source line.");
}

/* ---------- 12. WHEN IT DOES NOT KNOW ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Demo" });
  slideHead(s, "THE HONEST BOT", "What happens when it does not know");

  card(s, { x: M, y: TOP, w: 5.4, h: 3.45, name: "zoom_u1__card" });
  s.addImage({ path: "img/unknown.png", x: M + 0.16, y: TOP + 0.16, w: 5.08, h: 2.9, objectName: "zoom_u1__img" });
  s.addText("Asked: do you sell laptops? - never trained", { x: M + 0.16, y: TOP + 3.1, w: 5.08, h: 0.28,
    fontSize: 12, color: MUTED, align: "center", margin: 0, isTextBox: true, objectName: "zoom_u1__cap" });

  const rx = M + 5.75, rw = CW - 5.75;
  card(s, { x: rx, y: TOP, w: rw, h: 1.72, name: "zoom_u2__card" });
  s.addImage({ path: "img/leads.png", x: rx + 0.2, y: TOP + 0.18, w: 5.95, h: 1.36, objectName: "zoom_u2__img" });

  card(s, { x: rx, y: TOP + 1.93, w: rw, h: 1.52, name: "fly_u3__card" });
  iconBadge(s, { x: rx + 0.3, y: TOP + 2.2, d: 0.56, color: PINK, icon: "trending", name: "fly_u3" });
  s.addText("A refusal is not a failure", { x: rx + 0.98, y: TOP + 2.2, w: rw - 1.3, h: 0.5, fontSize: 16,
    bold: true, color: NAVY, valign: "middle", margin: 0, isTextBox: true, objectName: "fly_u3__t" });
  s.addText("The question is saved as a lead with a timestamp. The owner gets a customer to follow up, and learns exactly which content is missing.", {
    x: rx + 0.3, y: TOP + 2.78, w: rw - 0.6, h: 0.62, fontSize: 13, color: SLATE, lineSpacing: 18,
    margin: 0, isTextBox: true, objectName: "fly_u3__b" });

  callout(s, { y: 5.6, name: "fade_cta12", icon: "shield", color: RED, fill: "FFECEC", line: "FBC9C9",
    text: "A wrong answer costs trust. An honest I do not know costs nothing and creates a sales lead instead." });

  s.addNotes("This is the slide that shows the product thinking, not just the code.");
}

/* ---------- 13. ENGINEERING HIGHLIGHTS ---------- */
pres.addSection({ title: "Closing" });
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Closing" });
  slideHead(s, "ENGINEERING HIGHLIGHTS", "Problems we solved along the way");

  const items = [
    { icon: "key", c: BLUE, t: "Keeping the key secret",
      b: "Calling OpenAI from the browser would expose the API key in the page source. The request goes browser to our server to OpenAI, and the key is read from .env." },
    { icon: "shield", c: VIOLET, t: "Blocking script injection",
      b: "Chat text is user input. Every bubble is filled with textContent instead of innerHTML, so a typed script tag renders as plain text." },
    { icon: "refresh", c: GREEN, t: "Never breaking the demo",
      b: "A health check on load, try/catch around the AI call, and three fallback modes mean a dead key or dead Wi-Fi cannot kill the presentation." },
    { icon: "edit", c: PINK, t: "Making I do not know useful",
      b: "The model is told to reply with the exact word NO_ANSWER. That turns a vague refusal into a signal the code can detect and convert into a lead." },
  ];
  const w = (CW - 0.35) / 2, h = 1.72;
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * (w + 0.35), y = TOP + row * (h + 0.28);
    const g = `fly_e${i + 1}`;
    card(s, { x, y, w, h, name: g + "__card" });
    iconBadge(s, { x: x + 0.32, y: y + 0.3, d: 0.6, color: it.c, icon: it.icon, name: g });
    s.addText(it.t, { x: x + 1.05, y: y + 0.3, w: w - 1.35, h: 0.55, fontSize: 16.5, bold: true,
      color: NAVY, valign: "middle", margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(it.b, { x: x + 0.32, y: y + 0.98, w: w - 0.64, h: 0.68, fontSize: 12.5, color: SLATE,
      lineSpacing: 17, margin: 0, isTextBox: true, objectName: g + "__b" });
  });

  callout(s, { y: 5.6, name: "fade_cta13", icon: "terminal", color: VIOLET, fill: "F1ECFE", line: "DCCEFB",
    text: "Every endpoint was tested with curl before the frontend was connected - health, knowledge, chat, leads, contact and validation." });

  s.addNotes("Pick the key-secrecy one if they ask what was hardest technically.");
}

/* ---------- 14. FUTURE SCOPE ---------- */
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Closing" });
  slideHead(s, "FUTURE SCOPE", "Where we take it next");

  const future = [
    { icon: "login", c: BLUE, t: "Login and multiple businesses", b: "JWT authentication, with an ownerId on every knowledge item." },
    { icon: "database", c: CYAN, t: "A real database", b: "MongoDB or PostgreSQL in place of JSON files - only two functions change." },
    { icon: "search", c: VIOLET, t: "Proper RAG with embeddings", b: "Store vectors and send only the closest chunks instead of the whole Knowledge Base." },
    { icon: "chat", c: PINK, t: "Conversation memory", b: "Send the last few turns so follow-up questions keep their context." },
    { icon: "globe", c: GREEN, t: "A real embeddable widget", b: "Ship widget.js so any customer site can load the chat with one script tag." },
  ];
  const w = 7.5;
  future.forEach((f, i) => {
    const g = `fly_fu${i + 1}`;
    const y = TOP + i * 0.92;
    card(s, { x: M, y, w, h: 0.78, name: g + "__card" });
    iconBadge(s, { x: M + 0.2, y: y + 0.14, d: 0.5, color: f.c, icon: f.icon, name: g });
    s.addText(f.t, { x: M + 0.82, y: y + 0.06, w: 3.0, h: 0.6, fontSize: 14, bold: true, color: NAVY,
      valign: "middle", margin: 0, isTextBox: true, objectName: g + "__t" });
    s.addText(f.b, { x: M + 3.85, y: y + 0.06, w: w - 4.05, h: 0.6, fontSize: 12.5, color: SLATE,
      valign: "middle", margin: 0, isTextBox: true, objectName: g + "__b" });
  });

  s.addShape(pres.ShapeType.ellipse, { x: 9.0, y: TOP + 0.45, w: 3.6, h: 3.6,
    fill: { color: "FFFFFF", transparency: 35 }, line: { color: "D7E3FA", width: 1 }, objectName: "zoom_ring2" });
  s.addImage({ path: "img/bot.png", x: 9.35, y: TOP + 0.8, w: 2.9, h: 2.87, objectName: "zoom_bot2" });

  s.addNotes("Close by saying the architecture was built so none of these needs a rewrite.");
}

/* ---------- 15. THANK YOU ---------- */
{
  const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Closing" });

  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 0.52, w: 0.9, h: 0.9, rectRadius: 0.13, fill: { color: "FFFFFF" }, objectName: "fade_logo2__box",
  });
  s.addImage({ path: "img/logo.png", x: M + 0.06, y: 0.58, w: 0.78, h: 0.78, objectName: "fade_logo2__img" });

  s.addText("Questions?", {
    x: 0, y: 2.35, w: 13.333, h: 1.0, fontSize: 58, bold: true, color: "FFFFFF",
    align: "center", margin: 0, isTextBox: true, objectName: "zoom_q",
  });
  s.addText("Thank you for listening", {
    x: 0, y: 3.42, w: 13.333, h: 0.5, fontSize: 20, color: "DCEBFF", align: "center",
    margin: 0, isTextBox: true, objectName: "fade_ty",
  });

  const names = ["Ishika Mittal", "Nikhil Sharma", "Ojasvi Garg"];
  const cw2 = 3.3;
  names.forEach((n, i) => {
    const x = (13.333 - (cw2 * 3 + 0.5)) / 2 + i * (cw2 + 0.25);
    s.addShape(pres.ShapeType.roundRect, {
      x, y: 4.62, w: cw2, h: 0.78, rectRadius: 0.12,
      fill: { color: "FFFFFF", transparency: 82 }, line: { color: "FFFFFF", width: 1, transparency: 55 },
      objectName: `fly_nm${i + 1}__box`,
    });
    s.addText(n, {
      x, y: 4.62, w: cw2, h: 0.78, fontSize: 18, bold: true, color: "FFFFFF",
      align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `fly_nm${i + 1}__t`,
    });
  });

  s.addText("WebtiqAI  ·  Mini Project  ·  HTML, CSS, JavaScript, Node.js, Express, OpenAI API", {
    x: 0, y: 5.92, w: 13.333, h: 0.4, fontSize: 13, color: "BFD9FF", align: "center",
    margin: 0, isTextBox: true, objectName: "fade_foot",
  });

  s.addNotes("Thank you. Happy to take questions, and we can run the live demo again if you would like.");
}

/* ---------- WRITE ---------- */
(async () => {
  await pres.writeFile({ fileName: "WebtiqAI_Presentation.pptx" });
  const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");
  await applyTheme("WebtiqAI_Presentation.pptx", THEME);
  console.log("deck written + theme applied");
})();
