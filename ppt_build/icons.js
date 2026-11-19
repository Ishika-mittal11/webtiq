const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fs = require("fs");
const Fi = require("react-icons/fi");

if (!fs.existsSync("icons")) fs.mkdirSync("icons");

const LIST = {
  clock: Fi.FiClock, ghost: Fi.FiAlertOctagon, code: Fi.FiCode,
  chat: Fi.FiMessageSquare, book: Fi.FiBookOpen, check: Fi.FiCheckCircle,
  user: Fi.FiUserPlus, shield: Fi.FiShield, zap: Fi.FiZap,
  server: Fi.FiServer, cpu: Fi.FiCpu, database: Fi.FiDatabase,
  layers: Fi.FiLayers, key: Fi.FiKey, refresh: Fi.FiRefreshCw,
  edit: Fi.FiEdit3, wifioff: Fi.FiWifiOff, alert: Fi.FiAlertTriangle,
  globe: Fi.FiGlobe, chart: Fi.FiBarChart2, login: Fi.FiLogIn,
  send: Fi.FiSend, search: Fi.FiSearch, monitor: Fi.FiMonitor,
  terminal: Fi.FiTerminal, lock: Fi.FiLock, target: Fi.FiTarget,
  trending: Fi.FiTrendingUp, mail: Fi.FiMail, file: Fi.FiFileText,
};

(async () => {
  for (const [name, Icon] of Object.entries(LIST)) {
    if (!Icon) { console.log("MISSING", name); continue; }
    const svg = ReactDOMServer.renderToStaticMarkup(
      React.createElement(Icon, { color: "#FFFFFF", size: 256, strokeWidth: 2 })
    );
    await sharp(Buffer.from(svg)).resize(256, 256).png().toFile(`icons/${name}.png`);
  }
  console.log("icons done:", Object.keys(LIST).length);
})();
