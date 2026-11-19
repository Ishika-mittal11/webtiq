/* ==========================================================
   WebtiqAI — API helper
   One small file that talks to the backend.

   If the backend is running  -> real API calls (OpenAI)
   If it is not running       -> the pages fall back to the
                                 offline engine in the browser
   ========================================================== */

// When the page is opened directly from the file system
// (file:///E:/html_project/index.html) we still point at the
// local server. When the server itself serves the page, a
// relative path is enough.
var API_BASE = (location.protocol === "file:") ? "http://localhost:5000" : "";

var Api = {

  online: false,       // is the backend reachable?
  aiEnabled: false,    // does the backend have an OpenAI key?
  model: "offline",

  /* Low level: one fetch with JSON in and JSON out */
  request: function (path, method, body) {
    var options = { method: method || "GET", headers: { "Content-Type": "application/json" } };
    if (body) options.body = JSON.stringify(body);

    return fetch(API_BASE + path, options).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) throw new Error(data.error || ("Request failed: " + response.status));
        return data;
      });
    });
  },

  /* Ask the backend if it is alive and whether AI is on */
  checkHealth: function () {
    return this.request("/api/health")
      .then(function (data) {
        Api.online = true;
        Api.aiEnabled = data.aiEnabled;
        Api.model = data.model;
        return data;
      })
      .catch(function () {
        Api.online = false;
        return null;
      });
  },

  /* Knowledge Base */
  getKnowledge:    function ()   { return this.request("/api/knowledge"); },
  addKnowledge:    function (q, a) { return this.request("/api/knowledge", "POST", { q: q, a: a }); },
  deleteKnowledge: function (id) { return this.request("/api/knowledge/" + id, "DELETE"); },
  clearKnowledge:  function ()   { return this.request("/api/knowledge", "DELETE"); },
  loadSample:      function ()   { return this.request("/api/knowledge/sample", "POST"); },

  /* Chat */
  chat:     function (message) { return this.request("/api/chat", "POST", { message: message }); },
  siteChat: function (message) { return this.request("/api/site-chat", "POST", { message: message }); },

  /* Leads and contact form */
  getLeads: function ()     { return this.request("/api/leads"); },
  contact:  function (form) { return this.request("/api/contact", "POST", form); }
};

/* A small badge that shows the current mode.
   Any page can show it by adding <span id="apiStatus"></span>. */
function paintApiStatus() {
  var el = document.getElementById("apiStatus");
  if (!el) return;

  if (Api.online && Api.aiEnabled) {
    el.textContent = "AI connected (" + Api.model + ")";
    el.className = "api-status ok";
  } else if (Api.online) {
    el.textContent = "Backend on - offline matching (no API key)";
    el.className = "api-status warn";
  } else {
    el.textContent = "Browser mode - backend not running";
    el.className = "api-status off";
  }
}

// Check once as soon as the page loads.
Api.checkHealth().then(paintApiStatus);
