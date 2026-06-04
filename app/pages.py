"""The signup page, served at the service root. Self-contained HTML,
no external assets, so it deploys with the API and nothing else."""

SIGNUP_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>S2P Course Pack: get your free key</title>
<style>
  body { font-family: Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         max-width: 560px; margin: 48px auto; padding: 0 20px; color: #1a1a2e; }
  h1 { font-size: 1.5rem; }
  p  { line-height: 1.5; }
  form { display: flex; gap: 8px; margin: 24px 0; }
  input[type=email] { flex: 1; padding: 10px 12px; font-size: 1rem;
         border: 1px solid #aaa; border-radius: 6px; }
  button { padding: 10px 18px; font-size: 1rem; border: 0; border-radius: 6px;
         background: #1f4e79; color: #fff; cursor: pointer; }
  button:disabled { background: #999; }
  #result { display: none; border: 1px solid #1f4e79; border-radius: 8px;
         padding: 16px 20px; margin-top: 20px; }
  #key { font-family: Consolas, monospace; font-size: 1.3rem; font-weight: 700;
         letter-spacing: 1px; }
  #error { color: #a40000; margin-top: 12px; }
  ol { line-height: 1.7; }
  code { background: #f0f0f5; padding: 2px 6px; border-radius: 4px;
         font-family: Consolas, monospace; }
  .quiet { color: #555; font-size: 0.9rem; }
</style>
</head>
<body>
<h1>S2P Course Pack: get your free key</h1>
<p>Twenty hands-on courses teaching procurement work with Claude Code:
spend analysis, sourcing, contract review, and supplier management, all on
realistic practice data. The key is free for 30 days and covers everything.</p>

<form id="form">
  <input type="email" id="email" placeholder="you@company.com" required>
  <button type="submit" id="btn">Get my free key</button>
</form>
<div id="error"></div>

<div id="result">
  <p>Your key. Copy it now and treat it like a building pass; it is shown once:</p>
  <p id="key"></p>
  <p class="quiet" id="expiry"></p>
  <p>Next steps:</p>
  <ol>
    <li>Download the course pack zip and extract it to a folder of its own.</li>
    <li>Open a terminal in that folder and run: <code>python fetch.py course-02</code></li>
    <li>Paste this key when asked. It is saved after the first time.</li>
  </ol>
  <p>Full setup instructions are in <code>START_HERE.md</code> inside the pack.</p>
</div>

<script>
document.getElementById("form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const btn = document.getElementById("btn");
  const error = document.getElementById("error");
  btn.disabled = true; error.textContent = "";
  try {
    const response = await fetch("/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: document.getElementById("email").value })
    });
    const data = await response.json();
    if (!response.ok) {
      const detail = data.detail || {};
      error.textContent = detail.message || "Something went wrong. Try again.";
      btn.disabled = false;
      return;
    }
    document.getElementById("key").textContent = data.key;
    const ends = new Date(data.expires_at);
    document.getElementById("expiry").textContent =
      "Valid until " + (ends.getMonth() + 1) + "/" + ends.getDate() + "/" + ends.getFullYear()
      + " (" + data.trial_days + " days).";
    document.getElementById("result").style.display = "block";
    document.getElementById("form").style.display = "none";
  } catch {
    error.textContent = "Cannot reach the server. Check your connection and try again.";
    btn.disabled = false;
  }
});
</script>
</body>
</html>"""
