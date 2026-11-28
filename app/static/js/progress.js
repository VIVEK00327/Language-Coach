// Progress dashboard page logic. OWNER: R4.
(function () {
  var totalEl = document.getElementById("stat-total");
  var avgEl = document.getElementById("stat-average");
  var topLangEl = document.getElementById("stat-top-lang");
  var emptyEl = document.getElementById("progress-empty");
  var tableEl = document.getElementById("progress-table");
  var tbodyEl = document.getElementById("progress-tbody");
  var refreshBtn = document.getElementById("refresh-history");
  var chartCanvas = document.getElementById("score-chart");
  var chartEmpty = document.getElementById("chart-empty");

  if (!totalEl) return; // Not on progress page

  async function load() {
    try {
      var res = await fetch("/api/progress");
      if (!res.ok) return;
      var attempts = await res.json();

      totalEl.textContent = attempts.length;

      if (!attempts || attempts.length === 0) {
        avgEl.textContent = "0%";
        topLangEl.textContent = "—";
        if (emptyEl) emptyEl.classList.remove("hidden");
        if (tableEl) tableEl.classList.add("hidden");
        if (chartCanvas) chartCanvas.classList.add("hidden");
        if (chartEmpty) chartEmpty.classList.remove("hidden");
        return;
      }

      if (emptyEl) emptyEl.classList.add("hidden");
      if (tableEl) tableEl.classList.remove("hidden");

      var sum = 0, langC = {};
      attempts.forEach(function (a) {
        sum += (a.overall_score || 0);
        var l = a.language || "unknown";
        langC[l] = (langC[l] || 0) + 1;
      });
      avgEl.textContent = Math.round(sum / attempts.length) + "%";

      var topL = "—", maxC = 0;
      Object.keys(langC).forEach(function (lang) {
        if (langC[lang] > maxC) { maxC = langC[lang]; topL = lang.charAt(0).toUpperCase() + lang.slice(1); }
      });
      topLangEl.textContent = topL;

      // Render table
      tbodyEl.innerHTML = attempts.map(function (r) {
        var s = Math.round(r.overall_score || 0);
        var bc = s >= 70 ? "badge-high" : (s >= 40 ? "badge-medium" : "badge-low");
        var verdict = s >= 70 ? "Native match" : (s >= 40 ? "Near miss" : "Needs practice");
        var d = r.created_at || "";
        if (d.length > 16) d = d.replace("T", " ");
        return '<tr><td><small class="muted-text">' + d + '</small></td><td><span class="lang-pill">' + r.language + '</span></td><td><strong>' + r.target_text + '</strong></td><td><span class="score-badge ' + bc + '">' + s + '%</span></td><td><small class="muted-text">' + verdict + "</small></td></tr>";
      }).join("");

      // Draw score chart (plain canvas line chart)
      drawScoreChart(attempts);

    } catch (err) { console.warn("Failed to load progress dashboard:", err); }
  }

  function drawScoreChart(attempts) {
    if (!chartCanvas) return;
    if (attempts.length < 2) {
      chartCanvas.classList.add("hidden");
      if (chartEmpty) chartEmpty.classList.remove("hidden");
      return;
    }
    chartCanvas.classList.remove("hidden");
    if (chartEmpty) chartEmpty.classList.add("hidden");

    var ctx = chartCanvas.getContext("2d");
    var dpr = window.devicePixelRatio || 1;
    var rect = chartCanvas.parentElement.getBoundingClientRect();
    chartCanvas.width = rect.width * dpr;
    chartCanvas.height = 200 * dpr;
    chartCanvas.style.width = rect.width + "px";
    chartCanvas.style.height = "200px";
    ctx.scale(dpr, dpr);

    var w = rect.width, h = 200;
    var pad = { top: 20, right: 20, bottom: 30, left: 40 };
    var plotW = w - pad.left - pad.right;
    var plotH = h - pad.top - pad.bottom;

    // Data (oldest first for chart)
    var pts = attempts.slice().reverse().map(function (a) { return Math.round(a.overall_score || 0); });

    var cs = getComputedStyle(document.documentElement);
    var accent = cs.getPropertyValue("--accent-1").trim() || "#7c3aed";
    var muted = cs.getPropertyValue("--text-muted").trim() || "#999";
    var border = cs.getPropertyValue("--surface-border").trim() || "#ddd";

    ctx.clearRect(0, 0, w, h);

    // Grid lines
    ctx.strokeStyle = border;
    ctx.lineWidth = 1;
    for (var g = 0; g <= 100; g += 25) {
      var gy = pad.top + plotH * (1 - g / 100);
      ctx.beginPath(); ctx.moveTo(pad.left, gy); ctx.lineTo(pad.left + plotW, gy); ctx.stroke();
      ctx.fillStyle = muted; ctx.font = "11px sans-serif"; ctx.textAlign = "right";
      ctx.fillText(g + "%", pad.left - 6, gy + 4);
    }

    // Data line
    ctx.strokeStyle = accent;
    ctx.lineWidth = 2.5;
    ctx.lineJoin = "round";
    ctx.beginPath();
    pts.forEach(function (v, i) {
      var x = pad.left + (i / (pts.length - 1)) * plotW;
      var y = pad.top + plotH * (1 - v / 100);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Dots
    pts.forEach(function (v, i) {
      var x = pad.left + (i / (pts.length - 1)) * plotW;
      var y = pad.top + plotH * (1 - v / 100);
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = accent;
      ctx.fill();
    });

    // X axis label
    ctx.fillStyle = muted; ctx.font = "11px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("Attempts →", pad.left + plotW / 2, h - 4);
  }

  document.addEventListener("DOMContentLoaded", load);
  if (refreshBtn) refreshBtn.addEventListener("click", load);
})();
