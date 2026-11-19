# -*- coding: utf-8 -*-
# Chapters 6 to 10. Executed from build_report.py with the same globals.

# ============================================================ 6. IMPLEMENTATION
h1(doc, "6.  IMPLEMENTATION")

para(doc, "This chapter describes how the design of Chapter 5 was turned into working code. It "
          "begins with the folder structure, then covers the front end, then the back end, then "
          "the artificial intelligence integration and the two fallback engines, and finally the "
          "measures taken for security. Only the parts of the source code that are necessary to "
          "follow the explanation are reproduced here; the complete source is contained in the "
          "project folder submitted with this report.")

h2(doc, "6.1  Folder structure")

code(doc, [
    "html_project/",
    "  index.html              landing page, eleven sections",
    "  demo.html               live demo: train the bot and chat with it",
    "  css/style.css           all styling, responsive rules and animations",
    "  js/api.js               one place that talks to the backend",
    "  js/script.js            menu, hero demo, counters, pricing, FAQ, form, widget",
    "  js/demo.js              knowledge base panel, chat panel, leads table",
    "  server/server.js        the whole backend (Express + OpenAI)",
    "  server/package.json     dependencies",
    "  server/.env             the API key (never shared, never committed)",
    "  server/.env.example     the same file without the key",
    "  server/data/            the JSON database, created automatically",
    "      knowledge.json",
    "      leads.json",
    "      messages.json",
], caption="Listing 6.1: Folder structure of the project")

para(doc, "The separation is deliberate. Everything above the server folder is pure front end and "
          "can be opened directly in a browser with no server at all; everything inside the "
          "server folder is back end. The file js/api.js is the only file in the front end that "
          "knows the address of the server, so that moving the back end to a different host "
          "would require a change to one line.")

h2(doc, "6.2  Front end implementation")

h3(doc, "6.2.1  HTML structure")

para(doc, "Both pages use semantic HTML5 elements \u2014 header, nav, section, form, footer \u2014 rather "
          "than a page built out of undifferentiated div elements. Every section carries an id, "
          "which serves both the navigation links and the scripts. Interactive controls that have "
          "no visible text, such as the floating chat button and the mobile menu button, carry an "
          "aria-label attribute so that a screen reader can announce them.")

para(doc, "Several elements carry custom data attributes which the JavaScript reads later. The "
          "statistic counters hold their target value in a data-target attribute, so the counting "
          "animation needs no hard coded numbers; the pricing cards hold the monthly and the "
          "yearly price in data-m and data-y attributes, so the toggle simply reads whichever one "
          "it needs. The contact form carries the novalidate attribute, which switches off the "
          "built in validation messages of the browser so that our own error messages, which are "
          "more specific and are styled to match the page, are displayed instead.")

h3(doc, "6.2.2  Styling and responsiveness")

para(doc, "The stylesheet is 688 lines long and is divided into sixteen numbered sections, each "
          "introduced by a comment banner, so that any rule can be located quickly. Every colour "
          "in the project is declared once as a CSS custom property on the root element and is "
          "then referred to by name. Changing the brand colour of the entire site is therefore a "
          "single edit.")

code(doc, [
    ":root {",
    "  --page:  #fff8ef;      /* page background        */",
    "  --ink:   #1f1b2d;      /* main text and borders  */",
    "  --brand: #6c4df6;      /* primary purple         */",
    "  --radius: 18px;",
    "  --shadow: 6px 6px 0 var(--ink);",
    "}",
    "",
    ".feature-grid {                 /* two dimensions  -> Grid    */",
    "  display: grid;",
    "  grid-template-columns: repeat(3, 1fr);",
    "  gap: 26px;",
    "}",
    ".navbar-inner {                 /* one dimension   -> Flexbox */",
    "  display: flex;",
    "  align-items: center;",
    "  justify-content: space-between;",
    "}",
    "",
    "@media (max-width: 980px) {",
    "  .feature-grid { grid-template-columns: repeat(2, 1fr); }",
    "}",
    "@media (max-width: 680px) {",
    "  .feature-grid { grid-template-columns: 1fr; }",
    "  .nav-links    { display: none; }",
    "}",
], caption="Listing 6.2: Colour variables, the Grid and Flexbox choice, and the two breakpoints")

para(doc, "The rule applied throughout is that **Flexbox is used when items are arranged along one "
          "axis** \u2014 the navigation bar, a row of buttons, a chat bubble and its timestamp \u2014 and "
          "**Grid is used when items are arranged along two axes** \u2014 the six feature cards, the four "
          "bot cards, the three pricing plans. Two breakpoints are defined. At 980 pixels the "
          "three column grids become two column grids; at 680 pixels they become a single column, "
          "the navigation links are replaced by the hamburger menu, and the two panels of the "
          "demo page stack vertically.")

para(doc, "Movement on the page is produced with CSS keyframe animations rather than JavaScript "
          "wherever possible, because the browser can run them on the compositor and they "
          "therefore remain smooth. The fadeUp animation is used for the scroll reveal, bounce "
          "for the three dots of the typing indicator, and pulse for the floating chat button.")

h3(doc, "6.2.3  JavaScript behaviour")

para(doc, "The front end logic is divided into three files. The file api.js contains nothing but "
          "the communication with the server: a single request helper that performs the fetch, "
          "sets the Content-Type header, serialises the body and throws a meaningful error if the "
          "response is not successful, and a set of small named functions built on top of it. "
          "Because every network call in the project goes through this one helper, error handling "
          "exists in exactly one place.")

code(doc, [
    "var API_BASE = (location.protocol === \"file:\") ? \"http://localhost:5000\" : \"\";",
    "",
    "var Api = {",
    "  request: function (path, options) {",
    "    return fetch(API_BASE + path, options).then(function (res) {",
    "      return res.json().then(function (data) {",
    "        if (!res.ok) throw new Error(data.error || \"Request failed\");",
    "        return data;",
    "      });",
    "    });",
    "  },",
    "  checkHealth: function () { return Api.request(\"/api/health\"); },",
    "  chat: function (message) {",
    "    return Api.request(\"/api/chat\", {",
    "      method: \"POST\",",
    "      headers: { \"Content-Type\": \"application/json\" },",
    "      body: JSON.stringify({ message: message })",
    "    });",
    "  }",
    "  /* getKnowledge, addKnowledge, deleteKnowledge, loadSample,",
    "     siteChat, getLeads, contact follow the same pattern */",
    "};",
], caption="Listing 6.3: The fetch helper in js/api.js")

para(doc, "The file script.js contains the behaviour of the landing page. The statistic counters "
          "illustrate the use of the IntersectionObserver interface: rather than listening to "
          "every scroll event, which fires hundreds of times and wastes processor time, the "
          "observer notifies the script once, when the element actually becomes visible, and the "
          "counting then runs with a timer. The FAQ accordion animates by setting the maximum "
          "height of a panel to its measured scrollHeight, which is the standard technique for "
          "animating an element whose height is not known in advance.")

para(doc, "Validation of the contact form is performed field by field, and the error message is "
          "placed next to the field that caused it. The email address is checked against a "
          "regular expression.")

code(doc, [
    "var emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/;",
    "",
    "function validateForm() {",
    "  var ok = true;",
    "  clearErrors();",
    "",
    "  if (nameInput.value.trim().length < 3) {",
    "    showError(errName, \"Please enter your full name.\");  ok = false;",
    "  }",
    "  if (!emailPattern.test(emailInput.value.trim())) {",
    "    showError(errEmail, \"Please enter a valid email address.\");  ok = false;",
    "  }",
    "  if (websiteInput.value.trim().length < 4) {",
    "    showError(errWebsite, \"Please enter your website address.\");  ok = false;",
    "  }",
    "  if (messageInput.value.trim().length < 10) {",
    "    showError(errMessage, \"Please write a little more.\");  ok = false;",
    "  }",
    "  return ok;",
    "}",
], caption="Listing 6.4: Field by field validation of the contact form")

para(doc, "The file demo.js drives the demonstration page. Chat bubbles are built with "
          "document.createElement and the text is inserted with the textContent property. This is "
          "not a stylistic preference but a security measure: textContent writes the string as "
          "text, so a visitor who types a script tag sees that script tag printed on the screen "
          "rather than executed. Had innerHTML been used, the same input would have been a cross "
          "site scripting vulnerability.")

code(doc, [
    "function addBubble(box, from, text, source) {",
    "  var wrap = document.createElement(\"div\");",
    "  wrap.className = \"bubble \" + from;",
    "",
    "  var p = document.createElement(\"p\");",
    "  p.textContent = text;              // never innerHTML - XSS safe",
    "  wrap.appendChild(p);",
    "",
    "  if (source) {",
    "    var small = document.createElement(\"small\");",
    "    small.textContent = 'Source: \"' + source + '\"';",
    "    wrap.appendChild(small);",
    "  }",
    "  box.appendChild(wrap);",
    "  box.scrollTop = box.scrollHeight;",
    "}",
], caption="Listing 6.5: Building a chat bubble safely")

h2(doc, "6.3  Back end implementation")

para(doc, "The back end is a single file, server/server.js, of 436 lines. It begins by loading the "
          "environment variables, creating the Express application and registering three pieces "
          "of middleware. The order matters: middleware runs in the order in which it is "
          "registered, so the body of a request must be parsed before any route tries to read it.")

code(doc, [
    "require(\"dotenv\").config();",
    "",
    "const express = require(\"express\");",
    "const cors    = require(\"cors\");",
    "const fs      = require(\"fs\");",
    "const path    = require(\"path\");",
    "",
    "const app  = express();",
    "const PORT = process.env.PORT || 5000;",
    "const OPENAI_API_KEY = process.env.OPENAI_API_KEY || \"\";",
    "const OPENAI_MODEL   = process.env.OPENAI_MODEL   || \"gpt-4o-mini\";",
    "",
    "app.use(cors());                                   // allow the page to call us",
    "app.use(express.json({ limit: \"100kb\" }));         // parse JSON bodies",
    "app.use(express.static(path.join(__dirname, \"..\"))); // serve the front end",
], caption="Listing 6.6: Server setup and the middleware pipeline")

para(doc, "The key is read from process.env and never written in the code. The file server/.env "
          "that holds it is listed in .gitignore, so it cannot be committed to version control by "
          "accident, and a second file, .env.example, documents the names of the variables "
          "without their values.")

para(doc, "Eleven endpoints are registered. They follow REST conventions: the method describes the "
          "action and the path describes the resource, so that reading the list of endpoints is "
          "enough to understand what the server can do.")

table(doc, ["Method", "Endpoint", "Purpose", "Status returned"],
      [["GET", "/api/health", "Is the server up, and is a key configured?", "200"],
       ["GET", "/api/knowledge", "Everything the bot knows", "200"],
       ["POST", "/api/knowledge", "Teach the bot one pair", "201, or 400 if invalid"],
       ["DELETE", "/api/knowledge/:id", "Forget one item", "200, or 404 if absent"],
       ["DELETE", "/api/knowledge", "Clear the knowledge base", "200"],
       ["POST", "/api/knowledge/sample", "Load five sample items", "201"],
       ["POST", "/api/chat", "Ask the business bot a question", "200, or 400 if empty"],
       ["POST", "/api/site-chat", "Ask the widget about WebtiqAI itself", "200"],
       ["GET", "/api/leads", "List the captured leads", "200"],
       ["DELETE", "/api/leads", "Clear the lead list", "200"],
       ["POST", "/api/contact", "Save a contact form submission", "201, or 400 if invalid"]],
      caption="Table 6.1: The eleven endpoints of the back end",
      widths=[0.8, 1.7, 2.4, 1.1], size=10)

para(doc, "Validation is repeated on the server even though the browser has already performed it. "
          "This is a deliberate principle rather than duplication: validation in the browser is a "
          "convenience for the honest user, but it can be bypassed entirely by anyone who sends a "
          "request with a command line tool, so the server must never trust what it receives. "
          "Every field is therefore converted to a string, trimmed and length checked before it "
          "is used, and an invalid request is answered with status 400 and a message explaining "
          "what was wrong.")

h2(doc, "6.4  Artificial intelligence integration")

para(doc, "The heart of the project is the function askOpenAI. Its task is to build a prompt in "
          "which the rules, the content and the question are clearly separated, and then to send "
          "that prompt to the Chat Completions endpoint.")

code(doc, [
    "async function askOpenAI(question, knowledge) {",
    "  const content = knowledge",
    "    .map(function (item, i) { return (i+1) + \". Q: \" + item.q + \"\\n   A: \" + item.a; })",
    "    .join(\"\\n\");",
    "",
    "  const systemPrompt =",
    "    \"You are the website support assistant for \" + BUSINESS_NAME + \".\\n\" +",
    "    \"Answer ONLY using the content below. Never invent facts, prices or policies.\\n\" +",
    "    \"If the answer is not in the content, reply with exactly: NO_ANSWER\\n\" +",
    "    \"Keep answers short (1-3 sentences) and friendly.\\n\\n\" +",
    "    \"--- CONTENT ---\\n\" + content;",
    "",
    "  const response = await fetch(\"https://api.openai.com/v1/chat/completions\", {",
    "    method: \"POST\",",
    "    headers: {",
    "      \"Content-Type\":  \"application/json\",",
    "      \"Authorization\": \"Bearer \" + OPENAI_API_KEY",
    "    },",
    "    body: JSON.stringify({",
    "      model:       OPENAI_MODEL,     // gpt-4o-mini",
    "      temperature: 0.2,              // low -> factual, repeatable",
    "      max_tokens:  200,              // keeps answers short and cheap",
    "      messages: [",
    "        { role: \"system\", content: systemPrompt },",
    "        { role: \"user\",   content: question }",
    "      ]",
    "    })",
    "  });",
    "",
    "  if (!response.ok) {",
    "    throw new Error(\"OpenAI returned \" + response.status);",
    "  }",
    "  const data = await response.json();",
    "  return (data.choices[0].message.content || \"\").trim();",
    "}",
], caption="Listing 6.7: Building the grounded prompt and calling the API")

para(doc, "Three details deserve attention. First, the conversation sent to the model has two "
          "messages with different roles: the **system** message carries the rules and the content "
          "and is written by us, while the **user** message carries only the visitor\u2019s question. "
          "Keeping them apart is what makes the instruction authoritative. Second, the temperature "
          "is set to 0.2. Temperature controls randomness; a value near one produces creative and "
          "varied language, which is exactly what a support bot must not produce, so a low value "
          "is used to obtain short, factual and repeatable answers. Third, max_tokens is limited "
          "to two hundred, which caps both the length of the answer and the cost of the call.")

para(doc, "This technique of placing trusted content directly into the prompt is a simple form of "
          "what is called **retrieval augmented generation**. A production system would store the "
          "content as vector embeddings and retrieve only the passages closest in meaning to the "
          "question; in this project the whole knowledge base is small enough to be sent every "
          "time, which achieves the same grounding effect without the additional machinery.")

para(doc, "Figure 6.1 traces one complete request through the system, from the moment the visitor "
          "presses Send to the moment the bubble appears on the screen.")

figure(doc, "fig_seq.png", "Figure 6.1: Sequence of one question, end to end", width=6.1)

h2(doc, "6.5  The fallback engine")

para(doc, "If there is no key, or if the call to OpenAI fails for any reason, the same request is "
          "answered by the function matchLocally. The algorithm is deliberately simple, because "
          "it must be explainable in a viva examination, and it is surprisingly effective on a "
          "small knowledge base.")

code(doc, [
    "function cleanWords(text) {",
    "  return String(text)",
    "    .toLowerCase()                      // case does not matter",
    "    .replace(/[^a-z0-9\\s]/g, \" \")       // drop punctuation",
    "    .split(/\\s+/)",
    "    .filter(function (w) {              // drop very common words",
    "      return w.length > 1 && !STOP_WORDS.includes(w);",
    "    });",
    "}",
    "",
    "function matchLocally(question, knowledge) {",
    "  const askedWords = cleanWords(question);",
    "  let best = null, bestScore = 0;",
    "",
    "  knowledge.forEach(function (item) {",
    "    const itemWords = cleanWords(item.q + \" \" + item.a);",
    "    let score = 0;",
    "",
    "    askedWords.forEach(function (word) {",
    "      itemWords.forEach(function (itemWord) {",
    "        if (itemWord === word) score += 2;                 // exact match",
    "        else if (itemWord.startsWith(word)) score += 1;    // partial match",
    "      });",
    "    });",
    "",
    "    if (score > bestScore) { bestScore = score; best = item; }",
    "  });",
    "",
    "  return bestScore >= 2 ? best : null;   // below the threshold = do not know",
    "}",
], caption="Listing 6.8: The offline matching engine")

para(doc, "The question and each stored item are reduced to a list of meaningful words: everything "
          "is lowercased, punctuation is replaced by spaces, and a list of stop words such as "
          "\u201cthe\u201d, \u201cis\u201d, \u201cyou\u201d and \u201cwhat\u201d is removed, because those words appear in almost every "
          "sentence and would make everything match everything. Each remaining word of the "
          "question is then compared with each word of the item: an exact match scores two "
          "points and a partial match scores one. The item with the highest score wins, but only "
          "if that score reaches the threshold of two. The threshold is the important part of the "
          "algorithm, because it is what allows the engine to answer \u201cI do not know\u201d instead of "
          "returning the least bad of a set of irrelevant items.")

figure(doc, "fig_flow.png", "Figure 6.2: Flowchart of the offline matching algorithm", width=4.4)

h2(doc, "6.6  Lead capture")

para(doc, "Lead capture is implemented in a single short function. Whenever an answer could not be "
          "produced \u2014 whether the model returned NO_ANSWER or the offline engine failed to reach "
          "the threshold \u2014 saveLead is called with the question. It appends a record containing a "
          "generated identifier, the question, the status \u201cNew lead\u201d and the current time, and "
          "writes the file back immediately, so that the lead survives even if the server is "
          "stopped a moment later.")

code(doc, [
    "function saveLead(question) {",
    "  const leads = readData(FILES.leads);",
    "  leads.push({",
    "    id:       Date.now(),",
    "    question: question,",
    "    status:   \"New lead\",",
    "    time:     new Date().toISOString()",
    "  });",
    "  writeData(FILES.leads, leads);",
    "}",
], caption="Listing 6.9: Capturing a lead")

h2(doc, "6.7  The three operating modes")

para(doc, "When either page loads, it calls GET /api/health before doing anything else. The reply "
          "states whether the server is running and whether a key is configured, and from that "
          "reply the page chooses one of three modes and prints it in a badge. Figure 6.3 shows "
          "the three modes.")

figure(doc, "fig_modes.png", "Figure 6.3: The three operating modes and the badge shown for each",
       width=6.1)

para(doc, "In mode one the badge is green and reads \u201cAI connected\u201d, and answers come from the "
          "language model. In mode two the badge is amber and states that offline matching is in "
          "use because no key is configured; answers come from matchLocally inside the server and "
          "all data is still written to the JSON files. In mode three the server cannot be "
          "reached at all, the badge turns grey, and both the matching and the storage move into "
          "the browser, using localStorage. The important property is that the user is never "
          "misled about which mode is active: the badge always tells the truth.")

h2(doc, "6.8  Security measures")

para(doc, "Although this is a small academic project, four concrete security measures were "
          "implemented, and each can be demonstrated.")

num_reset()
numbered(doc, "**The secret key never leaves the server.** It is read from server/.env through "
              "process.env, it is never written into any file that the browser downloads, and the "
              ".env file is excluded by .gitignore. Opening the browser developer tools during the "
              "demonstration shows that no request from the page carries the key.")
numbered(doc, "**All user text is inserted as text, never as markup.** Chat bubbles, knowledge base "
              "entries and the leads table are built with createElement and textContent, which "
              "removes the possibility of cross site scripting.")
numbered(doc, "**The server validates every input independently of the browser.** Length limits are "
              "enforced on the question, the answer and the chat message, and the JSON body parser "
              "is limited to one hundred kilobytes, which prevents an oversized request from "
              "exhausting memory.")
numbered(doc, "**Failures are contained.** Every call to the external service is wrapped in a try and "
              "catch block; a failure is logged on the server and the request is answered by the "
              "fallback engine, so an error in a third party service can never present an error "
              "page to the visitor.")

page_break(doc)

# ============================================================ 7. TESTING
h1(doc, "7.  TESTING")

para(doc, "Testing was carried out continuously during development rather than as a single stage "
          "at the end. Four techniques were used. **Manual functional testing** exercised every "
          "feature through the user interface. **Black box testing** supplied inputs and compared "
          "the observed output with the expected output, without reference to the internal code. "
          "**Boundary value testing** concentrated on the edges of the permitted ranges, for example "
          "a question of exactly four and exactly five characters, since five is the stated "
          "minimum. **API testing** exercised each endpoint directly with the command line tool "
          "curl, which bypasses the browser entirely and therefore proves that the server "
          "validates its own input rather than relying on the page.")

para(doc, "In addition, **responsive testing** was performed with the device toolbar of Chrome "
          "DevTools at widths of 1366, 980, 768 and 414 pixels, and **failure testing** was performed "
          "by stopping the server while the page was open, in order to confirm that the "
          "application falls back to browser mode and that the badge changes accordingly.")

para(doc, "The tests were run in all three operating modes. Most of the interface behaviour is "
          "identical in every mode, so each case was executed once in the mode that makes it "
          "meaningful; the cases that concern the language model itself were executed with a live "
          "API key present, and are described in detail in Section 7.3.")

h2(doc, "7.1  Test Cases")

para(doc, "Table 7.1 records the test cases, the input supplied, the expected result, the observed "
          "result and the verdict. All of the cases listed were executed on the finished system.")

table(doc, ["ID", "Test case", "Input", "Expected result", "Actual result", "Verdict"],
      [["TC-01", "Server starts", "npm start in the server folder",
        "Console prints the address and the mode", "As expected", "Pass"],
       ["TC-02", "Health endpoint", "GET /api/health",
        "JSON with status, aiEnabled, model, knowledgeItems", "As expected", "Pass"],
       ["TC-03", "Teach the bot", "Valid question and answer",
        "201 Created; item appears in the list and in knowledge.json", "As expected", "Pass"],
       ["TC-04", "Question too short", "Question of 4 characters",
        "400 Bad Request with a clear message; nothing stored", "As expected", "Pass"],
       ["TC-05", "Boundary: minimum length", "Question and answer of exactly 5 characters",
        "Accepted and stored", "As expected", "Pass"],
       ["TC-06", "Empty fields", "Both fields blank",
        "Inline error message; no request sent", "As expected", "Pass"],
       ["TC-07", "Load sample data", "Click \u201cLoad sample data\u201d",
        "Five items appear; counter shows 5", "As expected", "Pass"],
       ["TC-08", "Delete one item", "Click the delete button on one item",
        "That item disappears; the others remain", "As expected", "Pass"],
       ["TC-09", "Delete unknown id", "DELETE /api/knowledge/99999",
        "404 Not Found", "As expected", "Pass"],
       ["TC-10", "Clear all", "Click \u201cClear all\u201d",
        "List empties; knowledge.json becomes []", "As expected", "Pass"],
       ["TC-11", "Known question", "\u201cdo you deliver?\u201d after sample data",
        "The delivery answer with its source line", "As expected", "Pass"],
       ["TC-12", "Rephrased question", "\u201cis home delivery available\u201d",
        "The same delivery answer", "As expected", "Pass"],
       ["TC-13", "Unknown question", "\u201cdo you sell laptops?\u201d",
        "An honest refusal; a new row in the leads table", "As expected", "Pass"],
       ["TC-14", "Lead is persistent", "Reload the page after TC-13",
        "The lead is still listed and present in leads.json", "As expected", "Pass"],
       ["TC-15", "Empty knowledge base", "Ask a question with no items stored",
        "A message asking the owner to teach the bot first", "As expected", "Pass"],
       ["TC-16", "Empty chat message", "POST /api/chat with an empty string",
        "400 Bad Request", "As expected", "Pass"],
       ["TC-17", "Script injection", "Teach an item whose answer is a <script> tag",
        "The tag is displayed as text and is not executed", "As expected", "Pass"],
       ["TC-18", "Widget question", "\u201cwhat is the price?\u201d in the floating widget",
        "The pricing answer about WebtiqAI itself", "Failed on the first attempt", "Fixed"],
       ["TC-19", "Contact form, invalid", "Name \u201cA\u201d, email \u201cwrong-email\u201d, short message",
        "Four field level errors; nothing saved", "As expected", "Pass"],
       ["TC-20", "Contact form, valid", "All four fields filled correctly",
        "Success message; record written to messages.json", "As expected", "Pass"],
       ["TC-21", "Server side validation", "curl POST /api/contact with a bad email",
        "400 Bad Request even though the browser was bypassed", "As expected", "Pass"],
       ["TC-22", "Pricing toggle", "Switch from monthly to yearly",
        "All three prices change to the yearly values", "As expected", "Pass"],
       ["TC-23", "FAQ accordion", "Click a question",
        "Its answer expands smoothly; the others close", "As expected", "Pass"],
       ["TC-24", "Copy the snippet", "Click the copy button",
        "The snippet is on the clipboard; the button confirms", "As expected", "Pass"],
       ["TC-25", "Responsive layout", "Widths of 1366, 980, 768 and 414 pixels",
        "Grids reflow; the hamburger menu appears below 680 pixels", "As expected", "Pass"],
       ["TC-26", "Server stopped", "Stop the server, then reload and chat",
        "Badge turns grey; the bot still answers from browser storage", "As expected", "Pass"],
       ["TC-27", "Live AI, known question", "“how are you doing today?”, with the matching item stored",
        "Stored answer returned unchanged, mode “ai”", "As expected", "Pass"],
       ["TC-28", "Live AI, unknown question", "“do you sell laptops?”",
        "NO_ANSWER, honest refusal, lead saved, mode “ai”", "As expected", "Pass"],
       ["TC-29", "Key removed mid-run", "Delete the key from .env and restart",
        "Badge turns amber; answers continue from the word matcher", "As expected", "Pass"]],
      caption="Table 7.1: Test cases and their results",
      widths=[0.62, 1.05, 1.15, 1.45, 0.95, 0.55], size=9)

h2(doc, "7.2  Defects found and corrected")

para(doc, "Testing is only useful if it finds defects, and three were found and corrected during "
          "this project. They are recorded here honestly.")

para(doc, "The first appears in Table 7.1 as test case TC-18. When the floating widget was asked "
          "\u201cwhat is the price?\u201d while the system was running in offline mode, it replied that it "
          "could not find the answer, although the pricing information was present in the site "
          "knowledge used by the widget. The cause was the matching algorithm rather than the "
          "content: the stored question used the word \u201cplans\u201d while the visitor had used the word "
          "\u201cprice\u201d, and the single remaining word was not enough to reach the threshold of two "
          "points. The correction was to enrich the stored questions with the words a visitor "
          "actually uses \u2014 price, pricing, plans, charges, rupees \u2014 so that the score reaches the "
          "threshold. This is a good illustration of the difference between a language model, "
          "which understands that the two words mean the same thing, and a word matcher, which "
          "does not.")

para(doc, "The second defect concerned the contact form. The form was submitted programmatically "
          "during an early test, and the validation did not prevent the submission. The cause was "
          "that the event used to trigger it had not been created as a cancellable event, so the "
          "call to preventDefault had no effect. The correction was to create the event with the "
          "cancelable option set to true.")

para(doc, "The third was not a defect in the code but a conflict in the environment: the server "
          "was originally written to listen on port 3000, which was already occupied by another "
          "application on the development machine, and starting it produced the error "
          "EADDRINUSE. The default port was changed to 5000 in the server, in the environment "
          "files and in js/api.js.")

h2(doc, "7.3  Verification of the live AI mode")

para(doc, "The test cases in Table 7.1 exercise the behaviour of the application as a whole. "
          "Because the most important claim of this project concerns the language model — that it "
          "answers only from the supplied content and refuses honestly otherwise — that claim was "
          "verified separately, in mode one, with a live API key present in server/.env. The "
          "health endpoint confirmed the mode before the tests were run:")

code(doc, [
    "$ curl http://localhost:5000/api/health",
    '{"status":"ok","aiEnabled":true,"model":"gpt-4o-mini","knowledgeItems":1}',
], caption="Listing 7.1: The server reporting that the live AI mode is active")

para(doc, "The knowledge base at that moment held a single item, taught through the interface: the "
          "question “how are you?” with the answer “yes i am fine”. Two requests were then sent "
          "directly to the endpoint with curl, which bypasses the browser completely.")

code(doc, [
    "$ curl -X POST http://localhost:5000/api/chat \\",
    '       -H \"Content-Type: application/json\" \\',
    '       -d \'{\"message\":\"how are you doing today?\"}\'',
    "",
    '{\"reply\":\"yes i am fine\",\"answered\":true,\"source\":null,\"mode\":\"ai\"}',
    "",
    "$ curl -X POST http://localhost:5000/api/chat \\",
    '       -H \"Content-Type: application/json\" \\',
    '       -d \'{\"message\":\"do you sell laptops?\"}\'',
    "",
    '{\"reply\":\"Sorry, I could not find that in my content, and I will not guess.',
    '           Our team will get back to you - I have saved your question.\",',
    ' \"answered\":false,\"source\":null,\"mode\":\"ai\"}',
], caption="Listing 7.2: Two live requests answered by the language model")

para(doc, "Both responses carry **mode: “ai”**, which proves that they came from the external call "
          "and not from the fallback engine. The first request is the more interesting of the two. "
          "The question asked was “how are you doing today?”, which does not match the stored "
          "question word for word, yet the model returned the stored answer unchanged and added "
          "nothing of its own — this is precisely the grounding behaviour the system prompt is "
          "designed to produce. The second request concerned laptops, a subject entirely absent "
          "from the knowledge base. The model returned NO_ANSWER, the server converted that into "
          "an honest refusal, and the question was written into leads.json with the status “New "
          "lead” and a timestamp. The model did not invent a product range, a price or a policy.")

para(doc, "One small observation is worth recording. In the first response the source field is "
          "null, even though the answer did come from the stored item. This is expected rather "
          "than a defect: the source line is produced by matchLocally, the word based engine, and "
          "the words of “how are you doing today” that survive stop word removal do not reach the "
          "threshold of two points against that particular item. It illustrates the difference "
          "between the two engines clearly — the language model understood the question, the word "
          "matcher did not — and it is the reason the language model is used for the answer while "
          "the matcher is used only to label the source.")

para(doc, "Modes two and three were verified separately by removing the key and by stopping the "
          "server, as recorded in test cases TC-26 and in Section 7.2. All three operating modes "
          "of the application have therefore been exercised.")

page_break(doc)

# ============================================================ 8. SCREENSHOTS
h1(doc, "8.  SCREENSHOTS AND OUTPUT")

para(doc, "All of the screenshots in this chapter were captured from the application while it was "
          "running on the development machine at the address http://localhost:5000. None of them "
          "is a mock-up or a design drawing. The green badge visible in several of them is the "
          "honest status indicator described in Chapter 6, reporting that the system was running "
          "in mode one, connected to the language model, at the time of capture.")

h2(doc, "8.1  The landing page")

figure(doc, "s01_hero.png", "Figure 8.1: Navigation bar and hero section with the self-playing chat card",
       width=6.1)

para(doc, "The hero section states the proposition of the product in one sentence and demonstrates "
          "it immediately: the chat card on the right plays a short conversation by itself, with "
          "a typing indicator between the messages, so that a visitor understands what the "
          "product does without clicking anything.")

figure(doc, "s06_stats.png", "Figure 8.2: The four statistic counters, which count up when scrolled into view",
       width=6.1)

figure(doc, "s02_features.png", "Figure 8.3: The six feature cards, arranged with CSS Grid", width=6.1)

figure(doc, "s03_how.png", "Figure 8.4: The three steps and the embed snippet with its copy button",
       width=6.1)

para(doc, "The third step shows the single line of code that a business would paste into its own "
          "website. The copy button writes it to the clipboard using the Clipboard API and then "
          "confirms by changing its own label for two seconds.")

figure(doc, "s04_bots.png", "Figure 8.5: The bot team section", width=6.1)

figure(doc, "s05_pricing.png", "Figure 8.6: The three pricing plans and the monthly to yearly toggle",
       width=6.1)

para(doc, "Each plan card holds both of its prices in data attributes, so the toggle merely reads "
          "the correct attribute and rewrites the text; no second set of cards is hidden behind "
          "the first.")

figure(doc, "s07_faq.png", "Figure 8.7: The FAQ accordion with one answer expanded", width=6.1)

h2(doc, "8.2  The contact form")

figure(doc, "s08_form_errors.png", "Figure 8.8: Validation errors shown next to the fields that caused them",
       width=6.1)

para(doc, "The form was submitted with a one letter name, an address without an at sign, a website "
          "of two characters and a message of two characters. Each field reports its own problem, "
          "and no request is sent to the server.")

figure(doc, "s09_form_success.png", "Figure 8.9: A valid submission, which is saved in messages.json",
       width=6.1)

h2(doc, "8.3  The floating chat widget")

figure(doc, "s10_widget.png", "Figure 8.10: The floating widget answering a question about WebtiqAI itself",
       width=3.4)

para(doc, "The widget is served by a separate endpoint, POST /api/site-chat, which is grounded in "
          "a fixed set of facts about the product rather than in the knowledge base of a business. "
          "It is the same mechanism applied to different content.")

h2(doc, "8.4  The demonstration page")

figure(doc, "s11_kb.png", "Figure 8.11: The demonstration page after the five sample items have been loaded",
       width=6.1)

figure(doc, "s12_kb_added.png", "Figure 8.12: The knowledge base after a sixth item has been taught by hand",
       width=6.1)

para(doc, "The item added here, a question about the warranty, is used in the next figure to show "
          "that the bot answers from content that was typed in during the demonstration itself.")

figure(doc, "s13_chat_answer.png", "Figure 8.13: Two questions answered, each with its source line",
       width=6.1)

para(doc, "This is the central screenshot of the project. The visitor typed \u201cdo you deliver?\u201d, "
          "which does not match the stored question word for word, and received the stored answer "
          "together with the line Source: \u201cDo you offer home delivery?\u201d. The source line is what "
          "makes the answer verifiable.")

figure(doc, "s14_unknown.png", "Figure 8.14: An honest refusal when the question is outside the knowledge base",
       width=6.1)

para(doc, "The bot was asked whether the shop sells laptops. Nothing in the knowledge base relates "
          "to laptops, so instead of producing a plausible sounding guess the bot states that it "
          "has not been taught this and that the question has been passed on.")

figure(doc, "s15_leads.png", "Figure 8.15: The same question captured in the leads table",
       width=6.1)

para(doc, "The unanswered question has become a row in the leads table, with its status and the "
          "time at which it was asked. For a business, this table is a list of things customers "
          "want to know that the website does not yet say.")

h2(doc, "8.5  The API and the stored data")

figure(doc, "s16_health.png", "Figure 8.16: The response of GET /api/health", width=6.0)

para(doc, "The health endpoint reports that the server is running, that aiEnabled is true because a "
          "key is configured, that the active model is gpt-4o-mini, and how many items the "
          "knowledge base currently holds. This single response is what the page uses to choose "
          "its mode, and it is what turns the badge green. With the key removed the same endpoint "
          "would report aiEnabled false and the model offline-matching, and the badge would turn "
          "amber without anything else in the application changing.")

figure(doc, "s17_leads_json.png", "Figure 8.17: The response of GET /api/leads, showing the stored record",
       width=6.0)

h2(doc, "8.6  Responsive behaviour")

two_figures(doc, "s18_mobile_hero.png", "s19_mobile_features.png",
            "Figure 8.18: The same page at a width of 414 pixels \u2014 the hero and the feature cards",
            width=2.45)

para(doc, "At mobile width the navigation links are replaced by the hamburger menu, the hero "
          "becomes a single column with the chat card below the text, and the three column "
          "feature grid becomes one column. No separate mobile page exists; this is the same HTML "
          "rendered under the media queries described in Chapter 6.")

page_break(doc)

# ============================================================ 9. FUTURE SCOPE
h1(doc, "9.  FUTURE SCOPE")

para(doc, "The present version of WebtiqAI is complete as an academic project, but it is "
          "deliberately a foundation rather than a finished product. The following extensions are "
          "the natural next steps, and they are listed roughly in the order in which they would "
          "be undertaken.")

num_reset()
numbered(doc, "**Accounts and authentication.** At present anyone who opens the demonstration page can "
              "train the bot. A real product needs registration, login and sessions, so that each "
              "business owns and sees only its own knowledge base and its own leads. This would be "
              "implemented with hashed passwords and signed tokens.")
numbered(doc, "**A real database.** The three JSON files should be replaced by a relational database "
              "such as PostgreSQL or MySQL. The three schemas given in Chapter 5 translate directly "
              "into three tables, with a foreign key to the owning business. Because every read and "
              "write already passes through the two helper functions readData and writeData, this "
              "change is confined to a single part of the server.")
numbered(doc, "**Automatic training from the existing website.** Typing questions and answers by hand "
              "is the slowest part of the present system. A crawler could read the pages of the "
              "business website, split the text into passages and store those passages as the "
              "knowledge base, so that the bot is useful within minutes of signing up.")
numbered(doc, "**Semantic search with embeddings.** Sending the whole knowledge base with every "
              "question works while that base is small. Once it grows to hundreds of items, each "
              "passage should be converted into a vector embedding and stored in a vector index, so "
              "that only the few passages closest in meaning to the question are sent. This reduces "
              "cost and improves accuracy at the same time.")
numbered(doc, "**A genuine embeddable widget.** The snippet shown in the third step of the landing "
              "page is presently illustrative. It should become a real script that injects the chat "
              "widget into any website inside an iframe, so that the styling of the host page "
              "cannot interfere with the widget and the widget cannot interfere with the host.")
numbered(doc, "**An analytics dashboard for the owner.** The data needed already exists. The number "
              "of questions asked, the proportion that were answered, the most frequent questions "
              "and the growth of the lead list could be presented as charts, turning the lead table "
              "into a decision making tool.")
numbered(doc, "**Notifications.** A lead is only valuable if someone acts on it. An email or a "
              "WhatsApp message to the owner when a lead is captured, and an automatic "
              "acknowledgement to the visitor if an address was supplied, would close that loop.")
numbered(doc, "**Multilingual support.** The instruction given to the model already asks it to reply "
              "in the language the visitor used. Extending this properly \u2014 particularly to Hindi "
              "and to Hinglish typed in Roman script, which is how a large number of Indian "
              "customers actually write \u2014 would widen the usefulness of the product considerably.")
numbered(doc, "**Human handover.** When the bot cannot answer and the owner happens to be online, "
              "the conversation could be transferred to the owner in real time using WebSockets, "
              "rather than merely being recorded as a lead.")
numbered(doc, "**Deployment and continuous delivery.** The application should be deployed to a "
              "public host, with the environment variables configured there, HTTPS enabled and a "
              "rate limit applied to the chat endpoint so that the API budget cannot be exhausted "
              "by automated requests.")

para(doc, "Taken together these extensions would convert the project from a working demonstration "
          "of a principle into a product that a small business could actually subscribe to. The "
          "principle itself, however \u2014 that a support bot must answer only from verified content, "
          "must show its source, and must admit honestly when it does not know \u2014 would remain "
          "unchanged, because it is the part of this project that matters most.")

page_break(doc)

# ============================================================ 10. REFERENCES
h1(doc, "10.  REFERENCES AND BIBLIOGRAPHY")

para(doc, "The following resources were consulted during the design, implementation and testing of "
          "this project.")

refs = [
 "MDN Web Docs, \u201cHTML: HyperText Markup Language\u201d, Mozilla Foundation. "
 "Available at: https://developer.mozilla.org/en-US/docs/Web/HTML",
 "MDN Web Docs, \u201cCSS: Cascading Style Sheets\u201d, Mozilla Foundation. "
 "Available at: https://developer.mozilla.org/en-US/docs/Web/CSS",
 "MDN Web Docs, \u201cCSS Grid Layout\u201d and \u201cFlexbox\u201d guides, Mozilla Foundation. "
 "Available at: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout",
 "MDN Web Docs, \u201cJavaScript Guide\u201d and \u201cDocument Object Model (DOM)\u201d, Mozilla Foundation. "
 "Available at: https://developer.mozilla.org/en-US/docs/Web/JavaScript",
 "MDN Web Docs, \u201cUsing the Fetch API\u201d and \u201cIntersection Observer API\u201d, Mozilla Foundation. "
 "Available at: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API",
 "MDN Web Docs, \u201cWindow.localStorage\u201d, Mozilla Foundation. "
 "Available at: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage",
 "Node.js Foundation, \u201cNode.js v18 Documentation \u2014 File System and Globals\u201d. "
 "Available at: https://nodejs.org/docs/latest-v18.x/api/",
 "Express.js, \u201cExpress 5 Guide: Routing, Middleware and Error Handling\u201d. "
 "Available at: https://expressjs.com/en/5x/api.html",
 "OpenAI, \u201cAPI Reference \u2014 Chat Completions\u201d. "
 "Available at: https://platform.openai.com/docs/api-reference/chat",
 "OpenAI, \u201cPrompt Engineering Guide\u201d. "
 "Available at: https://platform.openai.com/docs/guides/prompt-engineering",
 "npm, \u201cdotenv \u2014 Loads environment variables from a .env file\u201d. "
 "Available at: https://www.npmjs.com/package/dotenv",
 "npm, \u201ccors \u2014 Connect/Express middleware for Cross-Origin Resource Sharing\u201d. "
 "Available at: https://www.npmjs.com/package/cors",
 "OWASP Foundation, \u201cCross Site Scripting Prevention Cheat Sheet\u201d. "
 "Available at: https://cheatsheetseries.owasp.org/",
 "World Wide Web Consortium (W3C), \u201cWeb Content Accessibility Guidelines (WCAG) 2.1\u201d. "
 "Available at: https://www.w3.org/TR/WCAG21/",
 "Fielding, R. T., \u201cArchitectural Styles and the Design of Network-based Software "
 "Architectures\u201d, Doctoral dissertation, University of California, Irvine, 2000. "
 "(The origin of the REST style used for the endpoints in Chapter 6.)",
 "Lewis, P. et al., \u201cRetrieval-Augmented Generation for Knowledge-Intensive NLP Tasks\u201d, "
 "Advances in Neural Information Processing Systems, 2020. "
 "(The grounding technique applied in simplified form in Section 6.4.)",
 "Pressman, R. S. and Maxim, B. R., \u201cSoftware Engineering: A Practitioner\u2019s Approach\u201d, "
 "McGraw-Hill. (Referred to for feasibility analysis, DFD notation and test case design.)",
 "Elmasri, R. and Navathe, S. B., \u201cFundamentals of Database Systems\u201d, Pearson. "
 "(Referred to for entity relationship modelling and schema design.)",
]
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    _spacing(p, line=1.5, after=6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    _set_font(p.add_run("[%d]  " % i), size=12, bold=True)
    _set_font(p.add_run(r), size=12)

para(doc, "All online resources listed above were last accessed in November 2026.", after=0)
