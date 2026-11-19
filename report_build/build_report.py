# -*- coding: utf-8 -*-
"""Builds WebtiqAI_Project_Report.docx"""
from doclib import *
from doclib import _spacing, _set_font

doc = new_doc(a4=True, left=1.5, right=1.0, top=1.0, bottom=1.0)
footer_pagenum(doc, different_first=True)

# ============================================================ COVER
s = doc.sections[0]
cover(doc)
page_break(doc)

# ============================================================ CERTIFICATE
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
_spacing(p, line=1.0, before=18, after=20)
_set_font(p.add_run("CERTIFICATE"), size=18, bold=True)

para(doc, "This is to certify that Ishika Mittal (Roll No. ____________), Nikhil Sharma "
          "(Roll No. ____________) and Ojasvi Garg (Roll No. ____________), students of "
          "Master of Computer Applications (MCA), First Semester, have successfully completed "
          "the project work entitled “WebtiqAI — An AI Chatbot Website for Small Businesses” "
          "as part of the course Front End Web Development (26CA205PCB) during the academic "
          "session 2026–27, under my supervision and guidance at the Department of Computer "
          "Applications, KIET Deemed to be University, Delhi-NCR, Ghaziabad.", after=12)

para(doc, "The work presented in this project report is based on the students’ sincere efforts "
          "and learning. To the best of my knowledge, this project work is original and has not "
          "been submitted elsewhere for the award of any other degree or diploma.", after=40)

for t in ("Supervisor’s Name: Dr. Shashank Bhardwaj",
          "Designation: Associate Professor",
          "Signature of Supervisor: ______________________",
          "Date: ______________________"):
    para(doc, "**" + t + "**", align="left", after=10, line=1.5)

page_break(doc)

# ============================================================ ACKNOWLEDGEMENT
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
_spacing(p, line=1.0, before=18, after=20)
_set_font(p.add_run("ACKNOWLEDGEMENT"), size=18, bold=True)

para(doc, "The successful completion of this project would not have been possible without the "
          "guidance, support and encouragement of several individuals, and we take this "
          "opportunity to record our gratitude to them.")
para(doc, "We would like to express our sincere gratitude to our project supervisor, "
          "**Dr. Shashank Bhardwaj**, for his valuable guidance, continuous support, constructive "
          "suggestions and encouragement throughout the development of this project. His insights "
          "and feedback greatly helped us in completing this work successfully.")
para(doc, "We are also deeply thankful to **Dr. Sachin Malhotra**, Professor and Dean, Department of "
          "Computer Applications, KIET Deemed to be University, Ghaziabad, for his valuable "
          "support, guidance and encouragement.")
para(doc, "We would also like to express our heartfelt gratitude to our families for their constant "
          "motivation, patience and moral support. Their encouragement has been a continuous "
          "source of inspiration.")
para(doc, "Finally, we extend our thanks to our friends and classmates for their cooperation, "
          "discussions and support during the completion of this project.", after=36)

for t in ("Ishika Mittal", "Nikhil Sharma", "Ojasvi Garg"):
    para(doc, "**" + t + "**  —  Roll Number: ______________  —  Signature: ______________",
         align="left", after=10)
para(doc, "**Department of Computer Applications**", align="left", after=0)
para(doc, "**KIET Deemed to be University, Delhi-NCR, Ghaziabad, Uttar Pradesh**", align="left")

page_break(doc)

# ============================================================ TABLE OF CONTENTS
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
_spacing(p, line=1.0, before=12, after=14)
_set_font(p.add_run("TABLE OF CONTENTS"), size=18, bold=True)

tp = doc.add_paragraph()
_spacing(tp, line=1.5, after=6)
field(tp, 'TOC \\o "1-2" \\h \\z \\u')

page_break(doc)

# ============================================================ 1. INTRODUCTION
h1(doc, "1.  INTRODUCTION")

para(doc, "A website is, for most small businesses today, the first place a customer meets them. "
          "A visitor who lands on the page of a local store, a coaching centre or a small clinic "
          "almost always arrives with a question in mind: what are the opening hours, is there "
          "home delivery, what does it cost, can an order be returned, where exactly is the shop. "
          "These questions are simple and repetitive, and the answers rarely change. The problem "
          "is not that the answers are difficult; the problem is that nobody is available to give "
          "them at eleven o’clock at night, and that a visitor who does not find an answer "
          "within a few seconds usually leaves and does not come back.")

para(doc, "The standard solutions to this problem are unsatisfactory in different ways. A static "
          "Frequently Asked Questions page answers only the questions the owner thought of in "
          "advance, and it forces the visitor to read through a long list. A rule based chatbot, "
          "built on fixed keywords, breaks as soon as the visitor phrases the question in a "
          "slightly different way. A general purpose artificial intelligence chatbot understands "
          "the question very well, but it does not know anything about this particular business, "
          "and when it does not know something it tends to invent a plausible sounding answer. "
          "For a business, a confidently invented answer about a refund policy or a delivery "
          "charge is worse than no answer at all.")

para(doc, "**WebtiqAI** is our attempt at the middle path. It is a website for an embeddable AI "
          "chatbot service. A business owner types in the questions and answers that matter to his "
          "or her business, which together form a small **knowledge base**. A visitor then asks a "
          "question in ordinary language. The question and the stored content are sent together to "
          "an AI language model with one strict instruction: answer only from the content that has "
          "been provided, and if the answer is not present in that content, say so honestly "
          "instead of guessing. Every answer the bot gives on screen also shows the stored "
          "question it came from, so the visitor can see the source. Every question the bot could "
          "not answer is recorded as a **lead**, so that a gap in the knowledge base immediately "
          "becomes a business opportunity rather than a silent failure.")

para(doc, "This project was developed as the mini project for the course **Front End Web Development "
          "(26CA205PCB)**. The front end, which is the main subject of the course, is written "
          "entirely in plain HTML5, CSS3 and vanilla JavaScript. No front end framework, no "
          "component library, no CSS preprocessor and no build tool of any kind has been used, so "
          "that every line of the interface can be read, explained and defended. To make the "
          "application complete rather than merely decorative, a small back end was added using "
          "Node.js and the Express framework. The back end stores data in JSON files, keeps the "
          "secret API key away from the browser, and performs the call to the OpenAI Chat "
          "Completions API.")

para(doc, "A second idea shaped the project almost as strongly as the first. A demonstration that "
          "fails in front of an audience is of no use, and an internet connection in a classroom "
          "cannot be relied upon. The application was therefore designed to **degrade gracefully**. "
          "It runs in three modes: with the server and a valid API key it answers through the "
          "language model; with the server but without a key it answers through a word matching "
          "algorithm written inside the server; and with no server at all the same matching runs "
          "in the browser and the data is kept in the browser’s own storage. The page always "
          "states, in a badge at the top, which of the three modes is currently active. The "
          "demonstration therefore cannot break, and the honesty of the badge is itself part of "
          "the design philosophy of the project.")

para(doc, "The remainder of this report is organised as follows. Chapter 2 describes the project "
          "and its scope in detail. Chapter 3 lists the objectives that were set before the work "
          "began. Chapter 4 presents the requirement analysis, including the feasibility study, "
          "the functional and non-functional requirements and the tools used. Chapter 5 contains "
          "the system design: the entity relationship model, the data flow diagrams, the schema "
          "design and the overall website architecture. Chapter 6 explains the implementation of "
          "both the front end and the back end, with the relevant portions of the source code. "
          "Chapter 7 reports the testing that was carried out, together with a table of test "
          "cases and their outcomes. Chapter 8 presents screenshots of the working application. "
          "Chapter 9 discusses the future scope of the work, and Chapter 10 lists the references "
          "that were consulted.")

page_break(doc)

# ============================================================ 2. PROJECT DESCRIPTION
h1(doc, "2.  PROJECT DESCRIPTION")

para(doc, "WebtiqAI is a complete, working website for a product that lets any business add an AI "
          "chatbot to its own site. The project consists of two web pages, a stylesheet, three "
          "JavaScript files and one Node.js server file, together with three JSON files that act "
          "as the database. The whole application is served from a single address, "
          "**http://localhost:5000**, because the Express server also serves the static front end "
          "files. No separate web server, no XAMPP installation and no live-reload extension is "
          "required to run it.")

h2(doc, "2.1  The two pages")

para(doc, "The first page, **index.html**, is the marketing website of the product. It contains "
          "eleven distinct sections: a sticky navigation bar with a working mobile menu; a hero "
          "area with a chat card that plays a short conversation by itself; a strip of four "
          "statistics that count up from zero when they are scrolled into view; a grid of six "
          "feature cards; a three step explanation of how the product is used, including a "
          "one line embed snippet with a copy button; a row of four bot cards that present the "
          "product as a small team of specialised bots; a pricing section with three plans and a "
          "monthly to yearly toggle that rewrites the prices; a frequently asked questions "
          "accordion; a contact form with full client side validation; a footer; and a floating "
          "chat widget in the lower right corner that answers questions about WebtiqAI itself.")

para(doc, "The second page, **demo.html**, is where the product is actually demonstrated. It is "
          "divided into two panels. In the left panel the visitor plays the role of the business "
          "owner: a question and an answer can be typed in and taught to the bot, individual "
          "items can be deleted, the whole knowledge base can be cleared, and a set of five "
          "sample answers for an imaginary shop can be loaded with one click. In the right panel "
          "the visitor plays the role of the customer and chats with the bot that has just been "
          "trained. Below both panels sits a leads table, which fills up with every question the "
          "bot was unable to answer.")

h2(doc, "2.2  The three roles")

para(doc, "Although the application has no login system, three distinct roles are visible in its "
          "design. The **business owner** trains the bot and later reads the captured leads. The "
          "**website visitor** asks questions and may submit the contact form. The **language model** "
          "is a third participant: it is not a user, but it is an external actor that the system "
          "depends upon, and the system is written so that it continues to function when that "
          "actor is unavailable.")

h2(doc, "2.3  The principle of the honest bot")

para(doc, "The single most important design decision in this project is that the bot is never "
          "allowed to invent an answer. This is enforced in the instruction sent to the language "
          "model, which states explicitly that the model must answer only from the content "
          "supplied, must never invent facts, prices or policies, and must reply with the exact "
          "word NO_ANSWER when the answer is not present. The server inspects the reply: if it is "
          "NO_ANSWER, the visitor is told plainly that the bot has not been taught that yet, and "
          "the question is written into the leads file. If it is a real answer, the stored "
          "question that produced it is attached to the reply and displayed under the answer as a "
          "source line.")

para(doc, "This single rule turns what would otherwise be a weakness into a feature. A bot that "
          "says “I do not know, but I have passed your question to the team” loses nothing; a bot "
          "that invents a delivery charge costs the business a customer. The same behaviour also "
          "produces the lead list, which is arguably the most commercially valuable output of the "
          "whole system, because it tells the owner precisely what customers want to know and the "
          "website does not yet say.")

h2(doc, "2.4  Scope of the project")

para(doc, "The following work is inside the scope of this project and has been completed: a fully "
          "responsive front end built with plain HTML, CSS and JavaScript; a REST style back end "
          "with eleven endpoints; persistent storage in JSON files; integration with the OpenAI "
          "Chat Completions API using a key kept on the server; a server side fallback answering "
          "engine; a browser side fallback that works with no server at all; lead capture; a "
          "validated contact form; and an honest status badge that reports the active mode.")

para(doc, "The following work is deliberately outside the scope, because it is not required by the "
          "course and would have made the project too large to explain: user registration and "
          "login, multiple business accounts, a relational database, automatic crawling of a "
          "customer website, vector embeddings and semantic search, payment integration for the "
          "pricing plans, and deployment to a public server. Several of these are discussed in "
          "Chapter 9 as future scope.")

page_break(doc)

# ============================================================ 3. OBJECTIVES
h1(doc, "3.  OBJECTIVES OF THE PROJECT")

para(doc, "The objectives below were fixed before implementation began, and each of them was used "
          "later as a checklist during testing. They are divided into learning objectives, which "
          "relate to the course, and product objectives, which relate to the application itself.")

h2(doc, "3.1  Learning objectives")
num_reset()

for t in [
    "To design and build a complete, responsive, multi-section website using only **HTML5, CSS3 and "
    "vanilla JavaScript**, without any framework, library or build step, so that every part of the "
    "interface is understood from first principles.",
    "To apply modern CSS layout techniques correctly, choosing **Flexbox** for one dimensional "
    "arrangement and **CSS Grid** for two dimensional arrangement, and to make the result work on "
    "mobile, tablet and desktop widths through media queries.",
    "To practise **DOM manipulation and event handling** in JavaScript: creating elements, reading "
    "form values, listening to clicks, submissions and scrolling, and updating the page without "
    "reloading it.",
    "To implement **client side form validation** using regular expressions and length checks, and to "
    "display clear, specific error messages next to the field that caused the problem.",
    "To understand **asynchronous JavaScript** by calling a back end with the fetch API, handling "
    "promises with async and await, and dealing correctly with failure.",
    "To learn the fundamentals of **server side development** with Node.js and Express: middleware, "
    "routing, request and response objects, status codes and JSON bodies.",
    "To learn how an application talks to a **third party web API** safely, including the use of "
    "environment variables so that a secret key never appears in the source code or in the browser.",
]:
    numbered(doc, t)

h2(doc, "3.2  Product objectives")
num_reset()

for t in [
    "To allow a business owner to **train a chatbot** on his or her own content through a simple "
    "interface, with no technical knowledge required.",
    "To make the bot answer **only from that content**, and to make it state honestly when it does "
    "not know something, rather than inventing an answer.",
    "To show the **source** of every answer on screen, so that the visitor can judge how trustworthy "
    "it is.",
    "To turn every unanswered question into a **captured lead**, so that gaps in the knowledge base "
    "become visible and useful to the business.",
    "To ensure that the application **never breaks in front of an audience**, by providing two levels "
    "of fallback and by reporting the active mode honestly on the page.",
    "To store all data **persistently**, so that items taught to the bot survive a page refresh and a "
    "restart of the server.",
    "To keep the entire project **small enough to explain line by line** in a viva examination, while "
    "still demonstrating a genuine end to end system.",
]:
    numbered(doc, t)

page_break(doc)

# ============================================================ 4. REQUIREMENT ANALYSIS
h1(doc, "4.  REQUIREMENT ANALYSIS")

para(doc, "Requirement analysis is the stage at which a vague idea is converted into a precise list "
          "of things the software must do, together with an honest judgement of whether building it "
          "is possible with the time, skill and money available. This chapter records that analysis "
          "for WebtiqAI. It begins with the feasibility study, then states the functional "
          "requirements, then the non-functional requirements, and finally lists the tools and "
          "technologies that were selected.")

h2(doc, "4.1  Feasibility Analysis")

para(doc, "A feasibility study asks whether a proposed system should be built at all. Four kinds of "
          "feasibility were considered: technical, economic, operational and schedule feasibility.")

h3(doc, "4.1.1  Technical feasibility")

para(doc, "Technical feasibility asks whether the system can be built with the technology and the "
          "skills that are actually available. Every technology used in this project is free, "
          "mature and widely documented. HTML, CSS and JavaScript run in every browser without "
          "installation. Node.js is a single installer, and Express is installed with one command. "
          "The only external dependency is the OpenAI Chat Completions API, which is an ordinary "
          "HTTPS endpoint that accepts and returns JSON; Node.js version 18 and above includes a "
          "built in fetch function, so not even an HTTP library is needed. Storing data in JSON "
          "files removes the need to install and administer a database server. The conclusion is "
          "that the project is technically feasible, and the finished application confirms this: "
          "the entire system is about two and a half thousand lines of code spread over seven "
          "files.")

h3(doc, "4.1.2  Economic feasibility")

para(doc, "Economic feasibility asks whether the benefit justifies the cost. The development cost "
          "of this project is effectively zero. Visual Studio Code, Node.js, Express, Git and the "
          "browser developer tools are all free. The only possible running cost is the usage "
          "charge of the language model. The model chosen, **gpt-4o-mini**, is the least expensive "
          "model in its family, and the design keeps the usage very small: the reply is limited to "
          "two hundred tokens, the temperature is set low so that answers are short and factual, "
          "and only the knowledge base, which is a few hundred words, is sent with each question. "
          "A small business asking a few hundred questions a month would spend a negligible "
          "amount. Furthermore, the system continues to work with no key at all, so the cost can "
          "be reduced to zero without the application failing.")

h3(doc, "4.1.3  Operational feasibility")

para(doc, "Operational feasibility asks whether the intended users will actually be able and "
          "willing to use the system. The owner facing part of the application is a form with two "
          "fields, a question and an answer, and a button that says “Teach the bot”. A “Load "
          "sample data” button fills the knowledge base with five realistic items in one click, so "
          "that a new user can see the system working before typing anything. The visitor facing "
          "part is a chat box, a pattern that every user of a messaging application already "
          "understands. Suggestion chips below the chat box offer ready made questions, so the "
          "visitor is never faced with an empty box and no idea what to type. No training "
          "material is required to operate the system, which makes it operationally feasible.")

h3(doc, "4.1.4  Schedule feasibility")

para(doc, "The project had to be completed alongside regular coursework. The work was therefore "
          "divided into small, independently testable stages: first the static page structure, "
          "then the stylesheet and the responsive behaviour, then the JavaScript interactions, "
          "then the back end and its endpoints, then the AI integration, then the fallback "
          "engines, and finally testing and documentation. Because the front end was built to "
          "work on its own before the back end existed, no stage was blocked by another, and the "
          "project was completed within the time allotted.")

table(doc,
      ["Type of feasibility", "Key question", "Outcome"],
      [["Technical", "Can it be built with the available skills and tools?",
        "Yes. All technologies are free, standard and well documented."],
       ["Economic", "Is the cost justified?",
        "Yes. Development cost is zero; the only running cost is a very small API usage charge, "
        "and the system works without it."],
       ["Operational", "Will users be able to use it?",
        "Yes. Two input fields for the owner, a familiar chat box for the visitor."],
       ["Schedule", "Can it be finished in time?",
        "Yes. The work was split into independent stages, each testable on its own."]],
      caption="Table 4.1: Summary of the feasibility analysis",
      widths=[1.3, 2.0, 2.5])

h2(doc, "4.2  Functional Requirements")

para(doc, "A functional requirement states something the system must do. The functional "
          "requirements of WebtiqAI were gathered by walking through the journey of each of the "
          "three actors identified in Chapter 2, and they are listed in Table 4.2. Each "
          "requirement has been implemented and each was verified during testing, as recorded in "
          "Chapter 7.")

table(doc,
      ["ID", "Functional requirement", "Where it is implemented"],
      [["FR-01", "The owner shall be able to add a question and answer pair to the knowledge base.",
        "POST /api/knowledge, demo.html"],
       ["FR-02", "The system shall reject a pair in which either field is shorter than five characters.",
        "server.js, demo.js"],
       ["FR-03", "The owner shall be able to view every item currently stored.",
        "GET /api/knowledge"],
       ["FR-04", "The owner shall be able to delete a single item by its identifier.",
        "DELETE /api/knowledge/:id"],
       ["FR-05", "The owner shall be able to clear the entire knowledge base.",
        "DELETE /api/knowledge"],
       ["FR-06", "The owner shall be able to load five sample items with one click.",
        "POST /api/knowledge/sample"],
       ["FR-07", "A visitor shall be able to ask the bot a question in ordinary language.",
        "POST /api/chat"],
       ["FR-08", "The bot shall answer only from the stored knowledge base.",
        "askOpenAI() system prompt"],
       ["FR-09", "The bot shall display the stored question from which the answer was taken.",
        "source field, addBubble()"],
       ["FR-10", "When the bot cannot answer, it shall say so plainly and shall not guess.",
        "NO_ANSWER handling"],
       ["FR-11", "Every unanswered question shall be stored as a lead with a timestamp.",
        "saveLead()"],
       ["FR-12", "The owner shall be able to view the list of captured leads.",
        "GET /api/leads"],
       ["FR-13", "A visitor shall be able to ask the floating widget about WebtiqAI itself.",
        "POST /api/site-chat"],
       ["FR-14", "A visitor shall be able to submit a contact form with name, email, website and message.",
        "POST /api/contact"],
       ["FR-15", "The contact form shall validate every field before submission and show field level errors.",
        "script.js validation"],
       ["FR-16", "The system shall report its own status and active mode to the browser.",
        "GET /api/health"],
       ["FR-17", "The page shall display the active mode honestly in a status badge.",
        "paintApiStatus()"],
       ["FR-18", "The application shall continue to answer questions when the server is unavailable.",
        "localStorage fallback in demo.js"],
       ["FR-19", "Prices shall switch between monthly and yearly values when the toggle is used.",
        "script.js pricing toggle"],
       ["FR-20", "The embed snippet shall be copied to the clipboard when the copy button is pressed.",
        "Clipboard API, script.js"]],
      caption="Table 4.2: Functional requirements",
      widths=[0.6, 3.3, 1.9], size=10)

para(doc, "The same information can be expressed visually. Figure 4.1 is the use case diagram of "
          "the system. The two human actors stand outside the system boundary on the left and the "
          "right, the language model appears below as a secondary actor that the system calls "
          "rather than one that calls the system, and the two chat use cases are shown as "
          "including the common use case of generating a grounded answer.")

figure(doc, "fig_usecase.png", "Figure 4.1: Use case diagram of the WebtiqAI system", width=6.0)

h2(doc, "4.3  Non-Functional Requirements")

para(doc, "A non-functional requirement describes a quality the system must possess rather than a "
          "task it must perform. These requirements influenced the design at least as much as the "
          "functional ones; the decision to provide two levels of fallback, for example, follows "
          "directly from the reliability requirement.")

table(doc,
      ["ID", "Quality", "Requirement as implemented"],
      [["NFR-01", "Usability",
        "A new user must be able to see the bot working without typing anything, through the "
        "sample data button and the suggestion chips."],
       ["NFR-02", "Responsiveness",
        "The layout must adapt to desktop, tablet and mobile widths. Breakpoints are defined at "
        "980 and 680 pixels."],
       ["NFR-03", "Reliability",
        "The demonstration must not fail. Two independent fallback paths exist, and the active "
        "mode is always displayed."],
       ["NFR-04", "Security",
        "The API key must never reach the browser. It is read from server/.env through "
        "process.env and the file is excluded from version control."],
       ["NFR-05", "Safety of content",
        "All text supplied by a user is inserted with textContent and never with innerHTML, so "
        "that script injection is not possible."],
       ["NFR-06", "Performance",
        "The page must load quickly. There is no framework and no build output; the whole front "
        "end is about seventy kilobytes of text."],
       ["NFR-07", "Maintainability",
        "The stylesheet is divided into sixteen numbered sections and all colours are defined "
        "once as CSS custom properties."],
       ["NFR-08", "Portability",
        "The project must run on any machine with Node.js installed, with no database server and "
        "no web server configuration."],
       ["NFR-09", "Accessibility",
        "Interactive controls carry aria-label attributes, the colour contrast is high, and the "
        "page remains usable with the keyboard."],
       ["NFR-10", "Data persistence",
        "Data must survive a page refresh and a server restart; it is written to disk as JSON "
        "immediately on every change."]],
      caption="Table 4.3: Non-functional requirements",
      widths=[0.7, 1.1, 4.0], size=10)

h2(doc, "4.4  Tools and Technologies Used")

para(doc, "The technologies were chosen according to a single rule: nothing would be used that "
          "could not be explained. This excluded front end frameworks, CSS preprocessors, bundlers "
          "and object relational mappers, all of which would have hidden the very mechanisms the "
          "course is about.")

table(doc,
      ["Layer", "Technology", "Purpose in this project"],
      [["Structure", "HTML5",
        "Semantic markup of both pages, forms, accessible attributes, data-* attributes used by "
        "the scripts."],
       ["Presentation", "CSS3",
        "Custom properties for the colour system, Flexbox and Grid for layout, keyframe animations, "
        "transitions and media queries."],
       ["Behaviour", "JavaScript (ES6)",
        "DOM manipulation, event handling, form validation, fetch calls, IntersectionObserver, "
        "timers, localStorage."],
       ["Runtime", "Node.js 18+",
        "Executes the server. Its built in fetch function is used to call the OpenAI API, so no "
        "HTTP library is required."],
       ["Server framework", "Express 5",
        "Routing, middleware pipeline, JSON body parsing and serving of the static front end."],
       ["Middleware", "cors, express.json, express.static",
        "Cross origin requests during development, parsing of JSON request bodies, delivery of the "
        "HTML, CSS and JavaScript files."],
       ["Configuration", "dotenv",
        "Loads server/.env so that the API key and the port are read from the environment instead "
        "of being written in the code."],
       ["Storage", "Node fs module, JSON files",
        "knowledge.json, leads.json and messages.json act as the database."],
       ["Artificial intelligence", "OpenAI Chat Completions API, model gpt-4o-mini",
        "Produces the grounded answer from the system prompt and the question."],
       ["Editor and tools", "Visual Studio Code, Google Chrome DevTools, curl",
        "Writing the code, inspecting the DOM and the network, and testing the endpoints from the "
        "command line."]],
      caption="Table 4.4: Tools and technologies used",
      widths=[1.2, 1.6, 3.0], size=10)

para(doc, "The hardware and software required to run the project are modest, and are listed in "
          "Table 4.5 for completeness.")

table(doc,
      ["Requirement", "Minimum specification"],
      [["Processor", "Any dual core processor, 1.6 GHz or above"],
       ["Memory", "4 GB RAM (8 GB recommended while the editor and browser are both open)"],
       ["Disk space", "Approximately 60 MB, of which most is the node_modules folder"],
       ["Operating system", "Windows 10 or 11, macOS, or any Linux distribution"],
       ["Software", "Node.js version 18 or later, npm, and any modern browser"],
       ["Network", "An internet connection is required only for the AI mode; the other two modes "
                   "work entirely offline"]],
      caption="Table 4.5: Hardware and software requirements",
      widths=[1.6, 4.2], size=10)

page_break(doc)

# ============================================================ 5. SYSTEM DESIGN
h1(doc, "5.  SYSTEM DESIGN")

para(doc, "System design converts the requirements of Chapter 4 into a structure that can be "
          "implemented. This chapter presents four views of that structure. The entity "
          "relationship diagram shows what data the system keeps and how the pieces relate. The "
          "data flow diagrams show how data moves between the users, the processes and the stores. "
          "The schema design gives the exact shape of each stored record. The architecture "
          "diagram shows the three layers of the running application and the one external service "
          "it depends on.")

h2(doc, "5.1  ER Diagram")

para(doc, "Although WebtiqAI stores its data in JSON files rather than in a relational database, "
          "the data still has a definite logical structure, and that structure is best expressed "
          "as an entity relationship model. Figure 5.1 shows the model. Five entities appear in "
          "it, of which three are persistent and two are conceptual.")

figure(doc, "fig_er.png", "Figure 5.1: Entity relationship diagram of WebtiqAI", width=6.1)

para(doc, "**KNOWLEDGE_ITEM** is the central persistent entity. Each instance is one thing the bot "
          "has been taught, and it holds four attributes: a numeric identifier that acts as the "
          "primary key, the question text q, the answer text a, and the creation timestamp "
          "createdAt. The identifier is produced by the JavaScript expression Date.now(), which "
          "returns the number of milliseconds since the first of January 1970; since two items "
          "cannot realistically be created in the same millisecond by a single user, this value "
          "serves as a unique key without the need for a sequence generator.")

para(doc, "**LEAD** is the second persistent entity. It records a question that the bot could not "
          "answer, together with a status, which is set to the text “New lead”, and the time at "
          "which it was asked. **MESSAGE** is the third, and holds one submission of the contact "
          "form: the name, the email address, the website and the message of the person who "
          "submitted it, with a timestamp.")

para(doc, "**BUSINESS OWNER** and **VISITOR** are conceptual entities. They are shown because they make "
          "the relationships intelligible, but the present version of the system has no login and "
          "therefore stores no record of either. **QUESTION** is drawn with a dashed outline because "
          "it is transient: a question exists only for the duration of one request, and it is "
          "written to disk only in the case where it becomes a lead.")

para(doc, "The relationships are read as follows. One business owner trains many knowledge items, "
          "a one to many relationship. One visitor asks many questions, again one to many. Each "
          "question is matched against many knowledge items, and each knowledge item may be "
          "matched by many questions, which makes this a many to many relationship. Each question "
          "generates at most one lead: exactly one when the answer is not known and none when it "
          "is, which is written as a cardinality of zero or one. Finally, one visitor may submit "
          "many contact messages.")

h2(doc, "5.2  Data Flow Diagrams")

para(doc, "A data flow diagram describes a system in terms of the data that moves through it, "
          "rather than in terms of the order in which things happen. It has exactly four kinds of "
          "symbol: external entities, drawn as rectangles, which are the sources and destinations "
          "of data; processes, drawn as circles, which transform data; data stores, drawn as open "
          "rectangles, which hold data; and arrows, which are the data flows themselves and are "
          "always labelled with the data they carry.")

h3(doc, "5.2.1  Level 0 — the context diagram")

para(doc, "The context diagram treats the whole of WebtiqAI as a single process numbered zero, and "
          "shows only what crosses the boundary of the system. It is useful precisely because it "
          "is so small: it fixes the scope of the project in one picture. Figure 5.2 shows that "
          "the system has three external entities. The website visitor supplies questions and "
          "contact details and receives answers. The business owner supplies question and answer "
          "pairs and receives the knowledge list and the lead list. The OpenAI API receives a "
          "prompt and returns a grounded reply. By convention no data store appears at this "
          "level.")

figure(doc, "fig_dfd0.png", "Figure 5.2: Data flow diagram, level 0 (context diagram)", width=5.9)

h3(doc, "5.2.2  Level 1 — the main processes")

para(doc, "The level 1 diagram opens the single process of the context diagram into the four "
          "processes that actually carry the work, and reveals the data stores. Figure 5.3 shows "
          "the result.")

figure(doc, "fig_dfd1.png", "Figure 5.3: Data flow diagram, level 1", width=6.2)

para(doc, "**Process 1.0, Manage knowledge base**, receives new question and answer pairs or a "
          "deletion request from the owner, writes to store D1 and returns the current table. "
          "**Process 2.0, Answer the question**, receives the visitor’s question, reads every pair "
          "from D1, builds the prompt, sends it to the OpenAI API and returns the answer together "
          "with its source line. **Process 3.0, Capture and list leads**, receives from process 2.0 "
          "every question that came back as NO_ANSWER, appends a record to store D2 and supplies "
          "the lead list to the owner. **Process 4.0, Handle contact message**, validates the four "
          "fields of the contact form and appends a record to store D3.")

para(doc, "Two drawing conventions have been used to keep the diagram free of crossing lines. The "
          "store D1 appears twice, drawn with a doubled left edge, which is the standard notation "
          "for a repeated store; both boxes are the same file. The website visitor likewise "
          "appears twice, with the same notation, because it takes part both in the chat flow at "
          "the top and in the contact form flow at the bottom.")

h2(doc, "5.3  Schema Design")

para(doc, "The schema design states the exact shape of every record the system writes to disk. "
          "WebtiqAI uses three files inside the folder server/data, and each file contains one "
          "JSON array. One element of an array is one record, which corresponds to one row of a "
          "table in a relational database. The position of a record in the array carries no "
          "meaning, because every record holds its own identifier.")

figure(doc, "fig_schema.png", "Figure 5.4: Schema design — the three collections and one sample record",
       width=6.1)

para(doc, "The three schemas are given in full in the tables below.")

table(doc, ["Field", "Type", "Constraint", "Description"],
      [["id", "Number", "Primary key, generated by Date.now()", "Unique identifier of the item"],
       ["q", "String", "Minimum 5, maximum 300 characters", "The question the bot has been taught"],
       ["a", "String", "Minimum 5, maximum 2000 characters", "The answer the bot should give"],
       ["createdAt", "String", "ISO 8601 date and time", "When the item was taught"]],
      caption="Table 5.1: Schema of knowledge.json",
      widths=[0.9, 0.8, 2.1, 2.0], size=10)

table(doc, ["Field", "Type", "Constraint", "Description"],
      [["id", "Number", "Primary key, generated by Date.now()", "Unique identifier of the lead"],
       ["question", "String", "Copied from the request", "The question the bot could not answer"],
       ["status", "String", "Fixed value “New lead”", "Allows a workflow to be added later"],
       ["time", "String", "ISO 8601 date and time", "When the question was asked"]],
      caption="Table 5.2: Schema of leads.json",
      widths=[0.9, 0.8, 2.1, 2.0], size=10)

table(doc, ["Field", "Type", "Constraint", "Description"],
      [["id", "Number", "Primary key, generated by Date.now()", "Unique identifier of the message"],
       ["name", "String", "Minimum 3 characters", "Name of the person enquiring"],
       ["email", "String", "Must match the email pattern", "Address for the reply"],
       ["website", "String", "Minimum 4 characters", "The site the bot would be added to"],
       ["message", "String", "Minimum 10 characters", "The enquiry itself"],
       ["time", "String", "ISO 8601 date and time", "When the form was submitted"]],
      caption="Table 5.3: Schema of messages.json",
      widths=[0.9, 0.8, 2.1, 2.0], size=10)

para(doc, "Two helper functions isolate the rest of the server from the storage format. readData "
          "reads a file, parses it and returns an array, returning an empty array if the file is "
          "missing or damaged so that a corrupt file can never crash the server. writeData writes "
          "the whole array back, formatted with an indent of two spaces so that the file remains "
          "readable during a demonstration. Because every read and write passes through these two "
          "functions, replacing the JSON files with a real database in a later version would "
          "require changes in only one place.")

h2(doc, "5.4  Website Architecture")

para(doc, "The application is built in three layers, with one external service. Figure 5.5 shows "
          "the complete picture.")

figure(doc, "fig_arch.png", "Figure 5.5: Three-layer architecture of WebtiqAI", width=6.1)

para(doc, "The **presentation layer** runs entirely inside the visitor’s browser and consists of the "
          "two HTML pages, the single stylesheet and the three JavaScript files. It never speaks "
          "to the OpenAI API and never sees the API key; it speaks only to its own server, and it "
          "does so with the fetch function, exchanging JSON.")

para(doc, "The **application layer** is the Express server. A request entering it passes first "
          "through the middleware pipeline: the cors middleware adds the headers that allow the "
          "page to call the server while it is being opened directly from the file system during "
          "development, express.json parses a JSON body into a JavaScript object, and "
          "express.static serves the front end files. The request then reaches one of the eleven "
          "routes. The functions askOpenAI, matchLocally and saveLead carry the logic of the "
          "application: the first builds the grounded prompt and calls the external service, the "
          "second answers from the knowledge base without any network access, and the third "
          "records a lead.")

para(doc, "The **data layer** is the folder of three JSON files, accessed with the synchronous "
          "functions of the Node file system module. Synchronous access is normally avoided in a "
          "server, because it blocks the event loop, but for a single user demonstration with "
          "files of a few kilobytes it is both safe and much easier to read, and that trade off "
          "was made deliberately.")

para(doc, "The **external service** is the OpenAI Chat Completions endpoint. It is reached over HTTPS "
          "from the application layer only, with the key in the Authorization header. If that call "
          "fails for any reason at all — no key, no internet, an expired key, a rate limit, a "
          "malformed response — the same request is answered by matchLocally instead, and the "
          "visitor still receives a reply.")

para(doc, "Figure 5.6 shows the same application from the point of view of its pages and sections, "
          "which is useful when navigating the source code.")

figure(doc, "fig_sitemap.png", "Figure 5.6: Site map and page structure", width=6.0)

page_break(doc)

# ============================================================ rest
exec(open("part2.py", encoding="utf-8").read())

doc.save("WebtiqAI_Project_Report.docx")
print("saved report")
