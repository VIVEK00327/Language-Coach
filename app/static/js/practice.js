// Practice page logic: state machine, recording, assessment. OWNER: R4.
// Depends on: wav.js (convertTo16kHzMonoWav), waveform.js (startWaveform, stopWaveform)

(function () {
  /* ---- DOM cache ---- */
  var DOM = {
    langSel: document.getElementById("language"),
    wordSel: document.getElementById("word"),
    targetDisplay: document.getElementById("target-display"),
    listenBtn: document.getElementById("listen"),
    recordBtn: document.getElementById("record"),
    stopBtn: document.getElementById("stop"),
    tryAgainBtn: document.getElementById("try-again"),
    stateReady: document.getElementById("state-ready"),
    stateListening: document.getElementById("state-listening"),
    stateChecking: document.getElementById("state-checking"),
    stateResult: document.getElementById("state-result"),
    timerText: document.getElementById("timer-text"),
    timerRingFill: document.getElementById("timer-ring-fill"),
    waveformCanvas: document.getElementById("waveform-canvas"),
    volumeFill: document.getElementById("volume-fill"),
    quietWarning: document.getElementById("quiet-warning"),
    checkingTitle: document.getElementById("checking-title"),
    checkingSub: document.getElementById("checking-sub"),
    scoreNumber: document.getElementById("score-number"),
    scoreRingFill: document.getElementById("score-ring-fill"),
    scoreVerdict: document.getElementById("score-verdict"),
    wordsContainer: document.getElementById("words-cards-container"),
    feedbackList: document.getElementById("feedback-list"),
    timingDisplay: document.getElementById("timing-display"),
    errorBanner: document.getElementById("error-banner"),
    errorTitle: document.getElementById("error-title"),
    errorDesc: document.getElementById("error-desc"),
    errorClose: document.getElementById("error-close"),
    historyTable: document.getElementById("history-table"),
    historyTbody: document.getElementById("history-tbody"),
    historyEmpty: document.getElementById("history-empty"),
    statusDiv: document.getElementById("status"),
    resultPre: document.getElementById("result")
  };

  if (!DOM.langSel) return; // Not on practice page

  var VOICE_LANGS = { english: "en-US", hindi: "hi-IN", sanskrit: "hi-IN", french: "fr-FR" };
  var MAX_REC_SEC = 10.0;
  var TIMER_C = 188.5;  // 2*PI*30
  var SCORE_C = 314.15;  // 2*PI*50

  /* ---- State machine ---- */
  var AppState = { READY: "ready", LISTENING: "listening", CHECKING: "checking", RESULT: "result" };
  var current = AppState.READY;

  function setState(s) {
    current = s;
    DOM.stateReady.classList.toggle("hidden", s !== AppState.READY);
    DOM.stateListening.classList.toggle("hidden", s !== AppState.LISTENING);
    DOM.stateChecking.classList.toggle("hidden", s !== AppState.CHECKING);
    DOM.stateResult.classList.toggle("hidden", s !== AppState.RESULT);
    var busy = (s === AppState.LISTENING || s === AppState.CHECKING);
    DOM.langSel.disabled = busy;
    DOM.wordSel.disabled = busy;
    if (DOM.listenBtn) DOM.listenBtn.disabled = busy;
  }

  function showError(title, msg) {
    if (DOM.errorTitle && DOM.errorDesc && DOM.errorBanner) {
      DOM.errorTitle.textContent = title;
      DOM.errorDesc.textContent = msg;
      DOM.errorBanner.classList.remove("hidden");
    }
    if (DOM.statusDiv) DOM.statusDiv.textContent = "Error: " + title + " - " + msg;
  }
  function clearError() { if (DOM.errorBanner) DOM.errorBanner.classList.add("hidden"); }
  if (DOM.errorClose) DOM.errorClose.addEventListener("click", clearError);

  /* ---- Content loading ---- */
  async function loadLanguages() {
    try {
      var res = await fetch("/api/languages");
      if (!res.ok) throw new Error("Could not load languages list");
      var langs = await res.json();
      DOM.langSel.innerHTML = langs.map(function (l) {
        return '<option value="' + l + '">' + l.charAt(0).toUpperCase() + l.slice(1) + "</option>";
      }).join("");
      var urlP = new URLSearchParams(window.location.search);
      var reqL = urlP.get("lang");
      if (reqL && langs.indexOf(reqL.toLowerCase()) >= 0) DOM.langSel.value = reqL.toLowerCase();
      await loadWords();
    } catch (err) { showError("Network Error", "Failed to load languages: " + err.message); }
  }

  async function loadWords() {
    try {
      var lang = DOM.langSel.value;
      var res = await fetch("/api/content/" + lang);
      if (!res.ok) throw new Error("Could not load words for " + lang);
      var data = await res.json();
      var items = Object.values(data.levels || {}).flat();
      DOM.wordSel.innerHTML = items.map(function (i) {
        return '<option value="' + i.text + '">' + i.text + "</option>";
      }).join("");
      updateTarget();
    } catch (err) { showError("Content Error", "Failed to load word curriculum: " + err.message); }
  }

  function updateTarget() {
    if (DOM.targetDisplay) DOM.targetDisplay.textContent = DOM.wordSel.value || "—";
  }

  DOM.langSel.addEventListener("change", loadWords);
  DOM.wordSel.addEventListener("change", updateTarget);

  /* ---- Speech synthesis ---- */
  if (DOM.listenBtn) {
    DOM.listenBtn.addEventListener("click", function () {
      var text = DOM.wordSel.value;
      if (!text || !("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      u.lang = VOICE_LANGS[DOM.langSel.value] || "en-US";
      if (DOM.langSel.value === "sanskrit" && DOM.statusDiv)
        DOM.statusDiv.textContent = "Playing reference audio (Hindi voice approximation for Sanskrit).";
      u.onstart = function () { DOM.listenBtn.classList.add("playing"); };
      u.onend = function () { DOM.listenBtn.classList.remove("playing"); };
      u.onerror = function (e) { DOM.listenBtn.classList.remove("playing"); showError("Playback Error", e.error); };
      window.speechSynthesis.speak(u);
    });
  }

  /* ---- Recording ---- */
  var mediaStream = null, mediaRecorder = null, recordedChunks = [];
  var audioCtx = null, analyser = null;
  var recStart = 0, timerIv = null, checkTimerId = null;

  async function startRecording() {
    clearError();
    recordedChunks = [];
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (err) {
      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError")
        showError("Microphone Access Denied", "Permission was blocked. Click the lock icon in your browser address bar to allow microphone access.");
      else showError("Microphone Error", "Unable to access microphone: " + err.message);
      return;
    }
    var AC = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AC();
    var src = audioCtx.createMediaStreamSource(mediaStream);
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 256;
    src.connect(analyser);

    mediaRecorder = new MediaRecorder(mediaStream);
    mediaRecorder.ondataavailable = function (e) { if (e.data && e.data.size > 0) recordedChunks.push(e.data); };
    mediaRecorder.onstop = handleDone;
    mediaRecorder.start();

    setState(AppState.LISTENING);
    recStart = performance.now();
    if (DOM.quietWarning) DOM.quietWarning.classList.add("hidden");
    startWaveform(analyser, DOM.waveformCanvas, DOM.volumeFill, DOM.quietWarning);
    startTimer();
  }

  function startTimer() {
    updateTimerUI(0);
    timerIv = setInterval(function () {
      var el = (performance.now() - recStart) / 1000;
      updateTimerUI(el);
      if (el >= MAX_REC_SEC) stopRecording();
    }, 100);
  }

  function updateTimerUI(sec) {
    if (!DOM.timerText || !DOM.timerRingFill) return;
    var c = Math.min(sec, MAX_REC_SEC);
    DOM.timerText.textContent = Math.floor(c / 60) + ":" + (Math.floor(c % 60) + "").padStart(2, "0");
    DOM.timerRingFill.style.strokeDashoffset = TIMER_C * (1 - c / MAX_REC_SEC);
  }

  function stopRecording() {
    if (timerIv) { clearInterval(timerIv); timerIv = null; }
    stopWaveform();
    if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop();
  }

  DOM.recordBtn.addEventListener("click", startRecording);
  if (DOM.stopBtn) DOM.stopBtn.addEventListener("click", stopRecording);

  /* ---- Post-recording: convert + upload ---- */
  async function handleDone() {
    if (mediaStream) { mediaStream.getTracks().forEach(function (t) { t.stop(); }); mediaStream = null; }
    if (audioCtx && audioCtx.state !== "closed") { await audioCtx.close(); audioCtx = null; }

    if (recordedChunks.length === 0) {
      showError("Recording Empty", "No audio was captured. Please speak into your microphone and try again.");
      setState(AppState.READY);
      return;
    }

    setState(AppState.CHECKING);
    if (DOM.checkingTitle) DOM.checkingTitle.textContent = "Checking your pronunciation...";
    if (DOM.checkingSub) DOM.checkingSub.textContent = "Analyzing acoustic waveform against phonetic reference";
    checkTimerId = setTimeout(function () {
      if (current === AppState.CHECKING) {
        if (DOM.checkingTitle) DOM.checkingTitle.textContent = "First run loads the model...";
        if (DOM.checkingSub) DOM.checkingSub.textContent = "This can take a minute while neural weights load into CPU memory. Please wait.";
      }
    }, 8000);

    try {
      var raw = new Blob(recordedChunks, { type: (mediaRecorder && mediaRecorder.mimeType) || "audio/webm" });
      var wav = await convertTo16kHzMonoWav(raw);

      var fd = new FormData();
      fd.append("audio", wav, "recording.wav");
      fd.append("language", DOM.langSel.value);
      fd.append("text", DOM.wordSel.value);

      var res = await fetch("/api/assess", { method: "POST", body: fd });
      var data = await res.json();
      clearTimeout(checkTimerId);

      if (!res.ok) {
        showError("Assessment Error", data.error || "The server could not assess the audio.");
        setState(AppState.READY);
        return;
      }

      renderResults(data);
      await loadHistory();
      setState(AppState.RESULT);
      if (DOM.resultPre) DOM.resultPre.textContent = JSON.stringify(data, null, 2);
      if (DOM.statusDiv) DOM.statusDiv.textContent = "Assessed: " + data.overall_score + "%";
    } catch (err) {
      clearTimeout(checkTimerId);
      showError("Processing Failed", err.message || "An unexpected error occurred while processing audio.");
      setState(AppState.READY);
    }
  }

  /* ---- Result rendering ---- */
  function renderResults(data) {
    if (!DOM.scoreNumber || !DOM.scoreRingFill) return;
    var score = Math.round(data.overall_score || 0);
    DOM.scoreNumber.textContent = score;
    DOM.scoreRingFill.style.strokeDashoffset = SCORE_C * (1 - score / 100);

    var sc = document.querySelector(".score-card");
    if (sc) {
      sc.classList.remove("score-high", "score-medium", "score-low");
      if (score >= 70) { sc.classList.add("score-high"); DOM.scoreVerdict.textContent = "Great Pronunciation!"; }
      else if (score >= 40) { sc.classList.add("score-medium"); DOM.scoreVerdict.textContent = "Good Effort — Getting Closer"; }
      else { sc.classList.add("score-low"); DOM.scoreVerdict.textContent = "Needs Practice"; }
    }

    if (DOM.wordsContainer) {
      DOM.wordsContainer.innerHTML = "";
      (data.words || []).forEach(function (w) {
        var card = document.createElement("div"); card.className = "word-card";
        var hdr = document.createElement("div"); hdr.className = "word-card-header";
        var ws = Math.round(w.score || 0);
        var pc = ws >= 70 ? "pill-high" : (ws >= 40 ? "pill-medium" : "pill-low");
        hdr.innerHTML = '<span class="word-name">' + w.word + '</span><span class="word-score-pill ' + pc + '">' + ws + "%</span>";
        card.appendChild(hdr);

        var row = document.createElement("div"); row.className = "phoneme-chips-row";
        (w.phonemes || []).forEach(function (p) {
          var chip = document.createElement("span");
          chip.className = "phone-chip " + (p.correct ? "chip-correct" : "chip-wrong");
          if (p.correct) chip.textContent = "/" + p.expected + "/";
          else if (p.expected && p.spoken)
            chip.innerHTML = "/" + p.expected + '/ <span class="chip-arrow" aria-hidden="true">&rarr;</span> /' + p.spoken + "/";
          else if (p.expected) chip.textContent = "[missing /" + p.expected + "/]";
          else chip.textContent = "[extra /" + p.spoken + "/]";
          row.appendChild(chip);
        });
        card.appendChild(row);
        DOM.wordsContainer.appendChild(card);
      });
    }

    if (DOM.feedbackList) {
      DOM.feedbackList.innerHTML = "";
      (data.feedback || ["Great pronunciation!"]).forEach(function (tip) {
        var li = document.createElement("li"); li.textContent = tip; DOM.feedbackList.appendChild(li);
      });
    }

    if (DOM.timingDisplay && data.timing) {
      var t = data.timing;
      DOM.timingDisplay.textContent = "Latency: " + t.total_sec + "s (Reference: " + t.reference_sec + "s, Recognizer: " + t.recognizer_sec + "s, Scorer: " + t.scoring_sec + "s)";
    }
  }

  if (DOM.tryAgainBtn) DOM.tryAgainBtn.addEventListener("click", function () { setState(AppState.READY); });

  /* ---- History ---- */
  async function loadHistory() {
    if (!DOM.historyTable || !DOM.historyTbody) return;
    try {
      var res = await fetch("/api/progress");
      if (!res.ok) return;
      var attempts = await res.json();
      if (!attempts || attempts.length === 0) {
        if (DOM.historyEmpty) DOM.historyEmpty.classList.remove("hidden");
        DOM.historyTable.classList.add("hidden");
        return;
      }
      if (DOM.historyEmpty) DOM.historyEmpty.classList.add("hidden");
      DOM.historyTable.classList.remove("hidden");
      DOM.historyTbody.innerHTML = attempts.slice(0, 10).map(function (r) {
        var s = Math.round(r.overall_score || 0);
        var bc = s >= 70 ? "badge-high" : (s >= 40 ? "badge-medium" : "badge-low");
        var d = r.created_at || "";
        if (d.length > 16) d = d.slice(5, 16).replace("T", " ");
        return '<tr><td><small class="muted-text">' + d + '</small></td><td><span class="lang-pill">' + r.language + '</span></td><td><strong>' + r.target_text + '</strong></td><td><span class="score-badge ' + bc + '">' + s + "%</span></td></tr>";
      }).join("");
    } catch (err) { console.warn("Failed to load history:", err); }
  }

  /* ---- Init ---- */
  document.addEventListener("DOMContentLoaded", function () {
    loadLanguages();
    loadHistory();
    setState(AppState.READY);
  });
})();
