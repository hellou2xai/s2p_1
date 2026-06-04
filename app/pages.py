"""The account page, served at the service root. Self-contained HTML,
no external assets. Three tabs: get a key, recover a lost key, check a key.
There are no passwords in this system; the key is the only credential, so
recovery means re-emailing the key, never re-displaying it on screen."""

SIGNUP_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>S2P Course Pack: your license key</title>
<style>
  body { font-family: Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         max-width: 600px; margin: 40px auto; padding: 0 20px; color: #1a1a2e; }
  h1 { font-size: 1.45rem; }
  p  { line-height: 1.5; }
  .tabs { display: flex; gap: 6px; margin: 22px 0 0; border-bottom: 2px solid #1f4e79; }
  .tab { padding: 9px 14px; border: 0; background: #eef1f6; cursor: pointer;
         font-size: 0.95rem; border-radius: 8px 8px 0 0; }
  .tab.active { background: #1f4e79; color: #fff; }
  .panel { display: none; padding: 20px 0; }
  .panel.active { display: block; }
  form { display: flex; gap: 8px; margin: 14px 0; }
  input { flex: 1; padding: 10px 12px; font-size: 1rem;
         border: 1px solid #aaa; border-radius: 6px; }
  button.go { padding: 10px 18px; font-size: 1rem; border: 0; border-radius: 6px;
         background: #1f4e79; color: #fff; cursor: pointer; }
  button.go:disabled { background: #999; }
  .card { display: none; border: 1px solid #1f4e79; border-radius: 8px;
         padding: 16px 20px; margin-top: 16px; }
  .key { font-family: Consolas, monospace; font-size: 1.3rem; font-weight: 700;
         letter-spacing: 1px; }
  .error { color: #a40000; margin-top: 10px; }
  .ok { color: #14591d; margin-top: 10px; }
  ol { line-height: 1.7; }
  code { background: #f0f0f5; padding: 2px 6px; border-radius: 4px;
         font-family: Consolas, monospace; }
  .quiet { color: #555; font-size: 0.9rem; }
  table { border-collapse: collapse; margin: 10px 0; }
  td { padding: 5px 14px 5px 0; }
  td:first-child { color: #555; }
  .linkbtn { border: 0; background: none; color: #1f4e79; cursor: pointer;
         text-decoration: underline; padding: 0; font-size: 0.95rem; }
</style>
</head>
<body>
<h1>S2P Course Pack: your license key</h1>
<p>Twenty hands-on courses teaching procurement work with Claude Code:
spend analysis, sourcing, contract review, and supplier management, all on
realistic practice data. The key is free for 30 days and covers everything.</p>

<div class="tabs">
  <button class="tab active" data-panel="signup">Get a free key</button>
  <button class="tab" data-panel="recover">I lost my key</button>
  <button class="tab" data-panel="status">Check my key</button>
</div>

<div class="panel active" id="signup">
  <p>One key per work email, valid on up to 2 machines.</p>
  <form id="signup-form">
    <input type="email" id="signup-email" placeholder="you@company.com" required>
    <button type="submit" class="go">Get my free key</button>
  </form>
  <div class="error" id="signup-error"></div>
  <div class="card" id="signup-result">
    <p>Your key. Copy it now and treat it like a building pass:</p>
    <p class="key" id="signup-key"></p>
    <p class="quiet" id="signup-expiry"></p>
    <p class="ok" id="signup-emailed"></p>
    <p>Next steps:</p>
    <ol>
      <li>Download the course pack zip and extract it to a folder of its own.</li>
      <li>Open a terminal in that folder and run: <code>python fetch.py course-02</code></li>
      <li>Paste this key when asked. It is saved after the first time.</li>
    </ol>
    <p>Full setup instructions are in <code>START_HERE.md</code> inside the pack.</p>
  </div>
</div>

<div class="panel" id="recover">
  <p>Enter the email you signed up with. If a key exists for it, the key
  arrives in that inbox within a minute. For security it is never shown
  on this page.</p>
  <form id="recover-form">
    <input type="email" id="recover-email" placeholder="you@company.com" required>
    <button type="submit" class="go">Email me my key</button>
  </form>
  <div class="error" id="recover-error"></div>
  <div class="ok" id="recover-ok"></div>
</div>

<div class="panel" id="status">
  <p>Paste your key to see its status, machines, and course progress.</p>
  <form id="status-form">
    <input type="text" id="status-key" placeholder="U2X-XXXX-XXXX-XXXX" required>
    <button type="submit" class="go">Check</button>
  </form>
  <div class="error" id="status-error"></div>
  <div class="card" id="status-result">
    <table>
      <tr><td>Status</td><td id="st-status"></td></tr>
      <tr><td>Valid until</td><td id="st-expires"></td></tr>
      <tr><td>Machines</td><td id="st-machines"></td></tr>
      <tr><td>Courses fetched</td><td id="st-courses"></td></tr>
    </table>
    <p><button class="linkbtn" id="reset-machines">Sign out all machines</button>
    <span class="quiet">(use this when switching laptops; your data and drafts
    are not affected)</span></p>
    <div class="ok" id="reset-ok"></div>
  </div>
</div>

<script>
function fmtDate(iso) {
  const d = new Date(iso);
  return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
}
async function post(path, body, headers) {
  const response = await fetch(path, {
    method: "POST",
    headers: Object.assign({ "Content-Type": "application/json" }, headers || {}),
    body: JSON.stringify(body || {})
  });
  return { ok: response.ok, data: await response.json() };
}
function errMsg(data) {
  return (data.detail && data.detail.message) || "Something went wrong. Try again.";
}

document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.panel).classList.add("active");
  });
});

document.getElementById("signup-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const error = document.getElementById("signup-error");
  error.textContent = "";
  const { ok, data } = await post("/signup",
    { email: document.getElementById("signup-email").value });
  if (!ok) { error.textContent = errMsg(data); return; }
  document.getElementById("signup-key").textContent = data.key;
  document.getElementById("signup-expiry").textContent =
    "Valid until " + fmtDate(data.expires_at) + " (" + data.trial_days + " days).";
  document.getElementById("signup-emailed").textContent =
    data.emailed ? "A copy is on its way to your inbox." : "";
  document.getElementById("signup-result").style.display = "block";
  document.getElementById("signup-form").style.display = "none";
});

document.getElementById("recover-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const error = document.getElementById("recover-error");
  const okBox = document.getElementById("recover-ok");
  error.textContent = ""; okBox.textContent = "";
  const { ok, data } = await post("/resend-key",
    { email: document.getElementById("recover-email").value });
  if (!ok) { error.textContent = errMsg(data); return; }
  okBox.textContent = data.message;
});

let currentKey = "";
document.getElementById("status-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const error = document.getElementById("status-error");
  error.textContent = "";
  currentKey = document.getElementById("status-key").value.trim();
  const response = await fetch("/status",
    { headers: { "Authorization": "Bearer " + currentKey } });
  const data = await response.json();
  if (!response.ok) { error.textContent = errMsg(data); return; }
  document.getElementById("st-status").textContent = data.status;
  document.getElementById("st-expires").textContent = fmtDate(data.expires_at);
  document.getElementById("st-machines").textContent =
    data.machines_used + " of " + data.machines_max;
  document.getElementById("st-courses").textContent =
    data.courses_fetched + " of 20";
  document.getElementById("reset-ok").textContent = "";
  document.getElementById("status-result").style.display = "block";
});

document.getElementById("reset-machines").addEventListener("click", async () => {
  const { ok, data } = await post("/reset-machines", {},
    { "Authorization": "Bearer " + currentKey });
  document.getElementById("reset-ok").textContent =
    ok ? data.message : errMsg(data);
});
</script>
</body>
</html>"""
