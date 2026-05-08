/* ═══════════════════════════════════════════════
   FINDLY CHATBOT  ·  app.js  v2.0
═══════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {

  const msgInput   = document.getElementById("msg");
  const chatBox    = document.getElementById("chat");
  const typingRow  = document.getElementById("typingRow");
  const sendBtn    = document.getElementById("sendBtn");
  const suggestions = document.getElementById("suggestions");

  // ── Helpers ──────────────────────────────────

  /** Format HH:MM */
  function nowTime() {
    return new Date().toLocaleTimeString("mn-MN", { hour: "2-digit", minute: "2-digit" });
  }

  /**
   * Convert plain-text response to safe HTML:
   *  - escape HTML entities
   *  - \n → <br>
   *  - URLs → clickable links (open in new tab)
   */
  function formatText(text) {
    // 1. Escape HTML
    const escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // 2. Linkify URLs
    const linked = escaped.replace(
      /(https?:\/\/[^\s<>"]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );

    // 3. Newlines → <br>
    return linked.replace(/\n/g, "<br>");
  }

  /** Append a message bubble to the chat */
  function appendMessage(role, text) {
    const row = document.createElement("div");
    row.className = `msg-row ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = formatText(text);

    const ts = document.createElement("div");
    ts.className = "ts";
    ts.textContent = nowTime();

    const wrapper = document.createElement("div");
    wrapper.className = "msg-wrapper";

    if (role === "bot") {
      // Bot avatar
      const img = document.createElement("img");
      img.src = "/static/images/bot.png";
      img.className = "msg-avatar";
      img.alt = "Findly";
      row.appendChild(img);
    }

    wrapper.appendChild(bubble);
    wrapper.appendChild(ts);
    row.appendChild(wrapper);
    chatBox.appendChild(row);

    // Smooth scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  /** Show / hide the animated typing indicator */
  function setTyping(visible) {
    typingRow.style.display = visible ? "flex" : "none";
    if (visible) chatBox.scrollTop = chatBox.scrollHeight;
  }

  /** Disable / enable input while waiting for response */
  function setLoading(loading) {
    sendBtn.disabled = loading;
    msgInput.disabled = loading;
  }

  // ── Core send logic ───────────────────────────

  async function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed) return;

    // Hide suggestion chips after first message
    if (suggestions) suggestions.style.display = "none";

    appendMessage("user", trimmed);
    msgInput.value = "";
    setLoading(true);
    setTyping(true);

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      const data = await res.json();

      // Small delay so typing indicator feels natural
      await new Promise(r => setTimeout(r, 600));
      setTyping(false);

      const reply = data.response || data.detail || "Алдаа гарлаа. Дахин оролдоно уу.";
      appendMessage("bot", reply);

    } catch (err) {
      setTyping(false);
      appendMessage("bot", "⚠️ Серверт холбогдоход алдаа гарлаа. Интернет холболтоо шалгана уу.");
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
      msgInput.focus();
    }
  }

  // ── Event listeners ───────────────────────────

  // Enter key sends message
  msgInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(msgInput.value);
    }
  });

  // Send button click
  sendBtn.addEventListener("click", () => sendMessage(msgInput.value));

  // Suggestion chips (called from inline onclick in HTML)
  window.sendSuggestion = (text) => {
    msgInput.value = text;
    sendMessage(text);
  };

  // Also expose window.send for any legacy references
  window.send = () => sendMessage(msgInput.value);

  // ── Welcome message ───────────────────────────
  appendMessage(
    "bot",
    "Сайн байна уу! Би Findly — Zeely-ийн туслах bot. 👋\n\nТанд юугаар туслах вэ? Доорх товчнуудаас сонгох эсвэл асуултаа бичнэ үү."
  );

});