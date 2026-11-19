/* ==========================================================
   WebtiqAI — Main JavaScript
   1. Mobile menu            5. Pricing toggle
   2. Navbar on scroll       6. FAQ accordion
   3. Hero chat demo         7. Contact form validation
   4. Counter animation      8. Floating chat widget
   9. Scroll reveal
   ========================================================== */

/* ---------- 1. MOBILE MENU ---------- */
var menuBtn = document.getElementById("menuBtn");
var navLinks = document.getElementById("navLinks");

if (menuBtn) {
  menuBtn.addEventListener("click", function () {
    navLinks.classList.toggle("open");
  });
  // close the menu when a link is clicked
  navLinks.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      navLinks.classList.remove("open");
    });
  });
}

/* ---------- 2. NAVBAR ON SCROLL ---------- */
var navbar = document.getElementById("navbar");
window.addEventListener("scroll", function () {
  if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 20);
});

/* ---------- 3. HERO CHAT DEMO (auto typing) ---------- */
var heroChat = document.getElementById("heroChat");

var heroScript = [
  { from: "bot",  text: "Hi! I am your website assistant. Ask me anything." },
  { from: "user", text: "Do you deliver to Mumbai?" },
  { from: "bot",  text: "Yes! We deliver across Mumbai in 2-3 working days. Delivery is free above Rs 999.", source: "Source: Shipping Policy" },
  { from: "user", text: "What are your office hours?" },
  { from: "bot",  text: "We are open Monday to Saturday, 10 AM to 7 PM.", source: "Source: Contact page" }
];

function addBubble(box, from, text, source) {
  var div = document.createElement("div");
  div.className = "msg " + (from === "user" ? "msg-user" : "msg-bot");
  div.textContent = text;
  if (source) {
    var small = document.createElement("small");
    small.className = "msg-source";
    small.textContent = source;
    div.appendChild(small);
  }
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  return div;
}

function showTyping(box) {
  var div = document.createElement("div");
  div.className = "msg msg-bot typing";
  div.innerHTML = "<span></span><span></span><span></span>";
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  return div;
}

function playHeroDemo(i) {
  if (!heroChat) return;

  if (i >= heroScript.length) {
    // restart the demo after a pause
    setTimeout(function () {
      heroChat.innerHTML = "";
      playHeroDemo(0);
    }, 4000);
    return;
  }

  var step = heroScript[i];

  if (step.from === "bot" && i > 0) {
    var dots = showTyping(heroChat);
    setTimeout(function () {
      dots.remove();
      addBubble(heroChat, "bot", step.text, step.source);
      setTimeout(function () { playHeroDemo(i + 1); }, 1400);
    }, 1100);
  } else {
    addBubble(heroChat, step.from, step.text, step.source);
    setTimeout(function () { playHeroDemo(i + 1); }, step.from === "bot" ? 1400 : 900);
  }
}
playHeroDemo(0);

/* ---------- 4. COUNTER ANIMATION ---------- */
function runCounter(el) {
  var target = parseInt(el.getAttribute("data-target"), 10);
  var current = 0;
  var step = Math.max(1, Math.ceil(target / 30));

  var timer = setInterval(function () {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = current;
  }, 40);
}

var statsGrid = document.getElementById("statsGrid");
if (statsGrid && "IntersectionObserver" in window) {
  var statsObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll(".count").forEach(runCounter);
        statsObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });
  statsObserver.observe(statsGrid);
}

/* ---------- 5. PRICING TOGGLE ---------- */
var planToggle = document.getElementById("planToggle");
if (planToggle) {
  planToggle.addEventListener("click", function () {
    var yearly = planToggle.classList.toggle("on");

    document.querySelectorAll(".amount").forEach(function (el) {
      el.textContent = yearly ? el.getAttribute("data-y") : el.getAttribute("data-m");
    });
    document.querySelectorAll(".per").forEach(function (el) {
      el.textContent = yearly ? "/month, billed yearly" : "/month";
    });

    document.getElementById("labelMonthly").classList.toggle("active", !yearly);
    document.getElementById("labelYearly").classList.toggle("active", yearly);
  });
}

/* ---------- 6. FAQ ACCORDION ---------- */
document.querySelectorAll(".faq-q").forEach(function (question) {
  question.addEventListener("click", function () {
    var item = question.parentElement;
    var answer = item.querySelector(".faq-a");
    var isOpen = item.classList.contains("open");

    // close all first (only one open at a time)
    document.querySelectorAll(".faq-item").forEach(function (other) {
      other.classList.remove("open");
      other.querySelector(".faq-a").style.maxHeight = null;
    });

    if (!isOpen) {
      item.classList.add("open");
      answer.style.maxHeight = answer.scrollHeight + "px";
    }
  });
});

/* ---------- COPY CODE BUTTON ---------- */
var copyBtn = document.getElementById("copyBtn");
if (copyBtn) {
  copyBtn.addEventListener("click", function () {
    var code = document.getElementById("snippet").textContent;
    if (navigator.clipboard) navigator.clipboard.writeText(code);
    copyBtn.textContent = "Copied!";
    setTimeout(function () { copyBtn.textContent = "Copy code"; }, 1800);
  });
}

/* ---------- 7. CONTACT FORM VALIDATION ---------- */
var contactForm = document.getElementById("contactForm");

if (contactForm) {
  contactForm.addEventListener("submit", function (e) {
    e.preventDefault();

    var name = document.getElementById("name").value.trim();
    var email = document.getElementById("email").value.trim();
    var website = document.getElementById("website").value.trim();
    var message = document.getElementById("message").value.trim();
    var valid = true;

    // clear old errors
    ["errName", "errEmail", "errWebsite", "errMessage"].forEach(function (id) {
      document.getElementById(id).textContent = "";
    });

    if (name.length < 3) {
      document.getElementById("errName").textContent = "Please enter at least 3 characters.";
      valid = false;
    }

    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    if (!emailPattern.test(email)) {
      document.getElementById("errEmail").textContent = "Please enter a valid email address.";
      valid = false;
    }

    if (website.length < 4) {
      document.getElementById("errWebsite").textContent = "Please enter your website address.";
      valid = false;
    }

    if (message.length < 10) {
      document.getElementById("errMessage").textContent = "Please write at least 10 characters.";
      valid = false;
    }

    if (!valid) return;

    function showSuccess(text) {
      var box = document.getElementById("formSuccess");
      box.textContent = text;
      box.classList.add("show");
      contactForm.reset();
      setTimeout(function () { box.classList.remove("show"); }, 5000);
    }

    // Send it to the backend, which saves it in data/messages.json.
    if (typeof Api !== "undefined" && Api.online) {
      Api.contact({ name: name, email: email, website: website, message: message })
        .then(function (data) {
          showSuccess(data.message + " (saved on the server)");
        })
        .catch(function (err) {
          document.getElementById("errMessage").textContent = err.message;
        });
    } else {
      showSuccess("Thank you! Your message has been received. We will reply within 24 hours.");
    }
  });
}

/* ---------- 8. FLOATING CHAT WIDGET ---------- */
var widgetBtn = document.getElementById("widgetBtn");
var widget = document.getElementById("widget");
var widgetClose = document.getElementById("widgetClose");
var widgetForm = document.getElementById("widgetForm");
var widgetInput = document.getElementById("widgetInput");
var widgetBody = document.getElementById("widgetBody");

// The bot's knowledge about WebtiqAI itself.
// Each item has keywords; the reply with the most matching keywords wins.
var siteKnowledge = [
  { keys: ["price", "pricing", "cost", "plan", "rupees", "charge"],
    answer: "We have 3 plans: Starter is free, Growth is Rs 999/month and Business is Rs 2499/month. Yearly billing saves 20%." },
  { keys: ["free", "trial", "demo", "try"],
    answer: "Yes! The Starter plan is free and includes 100 chats a month. You can also try the live demo page right now." },
  { keys: ["install", "setup", "code", "snippet", "integrate", "add"],
    answer: "Setup takes about 3 minutes: add your website, train the bot, then paste one script tag before the closing body tag." },
  { keys: ["train", "learn", "knowledge", "content", "teach"],
    answer: "You paste your FAQs, services, prices and policies into the Knowledge Base. The bot answers only from that content." },
  { keys: ["language", "hindi", "english", "languages"],
    answer: "The bot replies in the visitor's own language and supports over 40 languages." },
  { keys: ["lead", "contact", "human", "team", "agent"],
    answer: "When the bot cannot answer, it offers your human team and collects the visitor's name and email as a lead." },
  { keys: ["work", "how", "what", "about", "webtiqai"],
    answer: "WebtiqAI is an AI chatbot for business websites. It learns from your content and answers your visitors 24/7." },
  { keys: ["hi", "hello", "hey", "namaste"],
    answer: "Hello! I am the WebtiqAI assistant. Ask me about pricing, setup or features." },
  { keys: ["time", "hours", "support", "24"],
    answer: "The bot answers 24 hours a day, 7 days a week. Our human support replies within 24 hours." }
];

function findAnswer(question) {
  var text = question.toLowerCase();
  var best = null;
  var bestScore = 0;

  siteKnowledge.forEach(function (item) {
    var score = 0;
    item.keys.forEach(function (key) {
      if (text.indexOf(key) !== -1) score++;
    });
    if (score > bestScore) {
      bestScore = score;
      best = item;
    }
  });

  return bestScore > 0 ? best.answer : null;
}

if (widgetBtn) {
  widgetBtn.addEventListener("click", function () {
    widget.classList.toggle("open");
    // first greeting
    if (widget.classList.contains("open") && widgetBody.children.length === 0) {
      addBubble(widgetBody, "bot", "Hi there! Ask me anything about WebtiqAI - pricing, setup, features.");
    }
  });

  widgetClose.addEventListener("click", function () {
    widget.classList.remove("open");
  });

  widgetForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var question = widgetInput.value.trim();
    if (question === "") return;

    addBubble(widgetBody, "user", question);
    widgetInput.value = "";

    var dots = showTyping(widgetBody);

    // Backend first (real OpenAI answer). If it is not running,
    // fall back to the keyword list above so the page still works.
    if (typeof Api !== "undefined" && Api.online) {
      Api.siteChat(question)
        .then(function (data) {
          dots.remove();
          addBubble(widgetBody, "bot", data.reply);
        })
        .catch(function () {
          dots.remove();
          answerLocally(question);
        });
    } else {
      setTimeout(function () {
        dots.remove();
        answerLocally(question);
      }, 900);
    }
  });

  function answerLocally(question) {
    var answer = findAnswer(question);
    if (answer) {
      addBubble(widgetBody, "bot", answer);
    } else {
      addBubble(widgetBody, "bot", "I could not find that in my content. Would you like our team to contact you? Use the contact form below the FAQ section.");
    }
  }
}

/* ---------- 9. SCROLL REVEAL ---------- */
var revealItems = document.querySelectorAll(".card, .step, .stat, .faq-item, .panel");
revealItems.forEach(function (el) { el.classList.add("reveal"); });

if ("IntersectionObserver" in window) {
  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  revealItems.forEach(function (el) { revealObserver.observe(el); });
} else {
  revealItems.forEach(function (el) { el.classList.add("visible"); });
}
