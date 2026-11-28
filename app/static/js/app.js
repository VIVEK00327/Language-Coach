// Language Coach Client Application. OWNER: Role 4.
// Modular architecture: UI State Machine, Web Audio Visualizer, Browser WAV Converter, API Client, and History Table.

/* ==========================================================================
   1. DOM Element Cache & Constants
   ========================================================================== */
const DOM = {
  // Selectors & Displays
  langSel: document.getElementById("language"),
  wordSel: document.getElementById("word"),
  targetDisplay: document.getElementById("target-display"),
  listenBtn: document.getElementById("listen"),
  recordBtn: document.getElementById("record"),
  stopBtn: document.getElementById("stop"),
  tryAgainBtn: document.getElementById("try-again"),

  // Flow State Containers
  stateReady: document.getElementById("state-ready"),
  stateListening: document.getElementById("state-listening"),
  stateChecking: document.getElementById("state-checking"),
  stateResult: document.getElementById("state-result"),

  // Visualizer & Timer
  timerText: document.getElementById("timer-text"),
  timerRingFill: document.getElementById("timer-ring-fill"),
  waveformCanvas: document.getElementById("waveform-canvas"),
  volumeFill: document.getElementById("volume-fill"),
  quietWarning: document.getElementById("quiet-warning"),

  // Checking State
  checkingTitle: document.getElementById("checking-title"),
  checkingSub: document.getElementById("checking-sub"),

  // Result Elements
  scoreNumber: document.getElementById("score-number"),
  scoreRingFill: document.getElementById("score-ring-fill"),
  scoreVerdict: document.getElementById("score-verdict"),
  wordsContainer: document.getElementById("words-cards-container"),
  feedbackList: document.getElementById("feedback-list"),
  timingDisplay: document.getElementById("timing-display"),

  // Error Banner
  errorBanner: document.getElementById("error-banner"),
  errorTitle: document.getElementById("error-title"),
  errorDesc: document.getElementById("error-desc"),
  errorClose: document.getElementById("error-close"),

  // History Table
  historyTable: document.getElementById("history-table"),
  historyTbody: document.getElementById("history-tbody"),
  historyEmpty: document.getElementById("history-empty"),

  // Compatibility Fallbacks
  statusDiv: document.getElementById("status"),
  resultPre: document.getElementById("result")
};

const VOICE_LANGS = {
  english: "en-US",
  hindi: "hi-IN",
  sanskrit: "hi-IN",
  french: "fr-FR"
};

const MAX_RECORD_SECONDS = 10.0;
const TIMER_CIRCUMFERENCE = 188.5; // 2 * PI * 30
const SCORE_CIRCUMFERENCE = 314.15; // 2 * PI * 50

/* ==========================================================================
   2. State Machine Manager
   ========================================================================== */
const AppState = {
  READY: "ready",
  LISTENING: "listening",
  CHECKING: "checking",
  RESULT: "result"
};

let currentState = AppState.READY;

function setState(state) {
  currentState = state;
  if (!DOM.stateReady) return; // Not on practice page

  DOM.stateReady.classList.toggle("hidden", state !== AppState.READY);
  DOM.stateListening.classList.toggle("hidden", state !== AppState.LISTENING);
  DOM.stateChecking.classList.toggle("hidden", state !== AppState.CHECKING);
  DOM.stateResult.classList.toggle("hidden", state !== AppState.RESULT);

  const isBusy = (state === AppState.LISTENING || state === AppState.CHECKING);
  if (DOM.langSel) DOM.langSel.disabled = isBusy;
  if (DOM.wordSel) DOM.wordSel.disabled = isBusy;
  if (DOM.listenBtn) DOM.listenBtn.disabled = isBusy;
}

function showError(title, message) {
  if (DOM.errorTitle && DOM.errorDesc && DOM.errorBanner) {
    DOM.errorTitle.textContent = title;
    DOM.errorDesc.textContent = message;
    DOM.errorBanner.classList.remove("hidden");
  }
  if (DOM.statusDiv) DOM.statusDiv.textContent = `Error: ${title} - ${message}`;
}

function clearError() {
  if (DOM.errorBanner) DOM.errorBanner.classList.add("hidden");
}

if (DOM.errorClose) {
  DOM.errorClose.addEventListener("click", clearError);
}

/* ==========================================================================
   3. Content & Target Loading
   ========================================================================== */
async function loadLanguages() {
  if (!DOM.langSel) return;
  try {
    const res = await fetch("/api/languages");
    if (!res.ok) throw new Error("Could not load languages list");
    const langs = await res.json();
    DOM.langSel.innerHTML = langs.map(l =>
      `<option value="${l}">${l.charAt(0).toUpperCase() + l.slice(1)}</option>`
    ).join("");

    // Read URL query parameter (e.g. /practice?lang=hindi)
    const urlParams = new URLSearchParams(window.location.search);
    const requestedLang = urlParams.get("lang");
    if (requestedLang && langs.includes(requestedLang.toLowerCase())) {
      DOM.langSel.value = requestedLang.toLowerCase();
    }

    await loadWords();
  } catch (err) {
    showError("Network Error", "Failed to load languages: " + err.message);
  }
}

async function loadWords() {
  if (!DOM.wordSel) return;
  try {
    const lang = DOM.langSel.value;
    const res = await fetch(`/api/content/${lang}`);
    if (!res.ok) throw new Error("Could not load words for " + lang);
    const data = await res.json();
    const items = Object.values(data.levels || {}).flat();
    DOM.wordSel.innerHTML = items.map(i => `<option value="${i.text}">${i.text}</option>`).join("");
    updateTargetDisplay();
  } catch (err) {
    showError("Content Error", "Failed to load word curriculum: " + err.message);
  }
}

function updateTargetDisplay() {
  if (!DOM.targetDisplay || !DOM.wordSel) return;
  const currentText = DOM.wordSel.value || "—";
  DOM.targetDisplay.textContent = currentText;
}

if (DOM.langSel) DOM.langSel.addEventListener("change", loadWords);
if (DOM.wordSel) DOM.wordSel.addEventListener("change", updateTargetDisplay);

/* ==========================================================================
   4. Speech Synthesis Reference Playback
   ========================================================================== */
if (DOM.listenBtn) {
  DOM.listenBtn.addEventListener("click", () => {
    const text = DOM.wordSel ? DOM.wordSel.value : "";
    if (!text) return;

    if (!("speechSynthesis" in window)) {
      showError("Audio Unsupported", "Speech synthesis is not supported on this browser.");
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const targetLocale = VOICE_LANGS[DOM.langSel.value] || "en-US";
    utterance.lang = targetLocale;

    if (DOM.langSel.value === "sanskrit" && DOM.statusDiv) {
      DOM.statusDiv.textContent = "Playing reference audio (Hindi voice approximation for Sanskrit).";
    }

    utterance.onstart = () => DOM.listenBtn.classList.add("playing");
    utterance.onend = () => DOM.listenBtn.classList.remove("playing");
    utterance.onerror = (e) => {
      DOM.listenBtn.classList.remove("playing");
      showError("Playback Error", "Failed to play reference pronunciation: " + e.error);
    };

    window.speechSynthesis.speak(utterance);
  });
}

/* ==========================================================================
   5. Live Audio Visualizer & Recording Engine
   ========================================================================== */
let mediaStream = null;
let mediaRecorder = null;
let recordedChunks = [];
let audioContext = null;
let analyserNode = null;
let animationFrameId = null;
let recordingStartTime = 0;
let timerInterval = null;
let quietTimer = 0;
let checkingTimerId = null;

async function startRecording() {
  clearError();
  recordedChunks = [];

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
      showError(
        "Microphone Access Denied",
        "Permission was blocked. Click the lock or camera icon in your browser address bar to allow microphone access."
      );
    } else {
      showError("Microphone Error", "Unable to access microphone: " + err.message);
    }
    return;
  }

  // Setup Web Audio Analyser
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  audioContext = new AudioCtx();
  const source = audioContext.createMediaStreamSource(mediaStream);
  analyserNode = audioContext.createAnalyser();
  analyserNode.fftSize = 256;
  source.connect(analyserNode);

  mediaRecorder = new MediaRecorder(mediaStream);
  mediaRecorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) recordedChunks.push(e.data);
  };

  mediaRecorder.onstop = handleRecordingComplete;
  mediaRecorder.start();

  setState(AppState.LISTENING);
  recordingStartTime = performance.now();
  quietTimer = 0;
  if (DOM.quietWarning) DOM.quietWarning.classList.add("hidden");

  drawWaveform();
  startTimer();
}

function startTimer() {
  updateTimerUI(0);
  timerInterval = setInterval(() => {
    const elapsedSec = (performance.now() - recordingStartTime) / 1000;
    updateTimerUI(elapsedSec);

    if (elapsedSec >= MAX_RECORD_SECONDS) {
      stopRecording();
    }
  }, 100);
}

function updateTimerUI(seconds) {
  if (!DOM.timerText || !DOM.timerRingFill) return;
  const clamped = Math.min(seconds, MAX_RECORD_SECONDS);
  const mins = Math.floor(clamped / 60);
  const secs = Math.floor(clamped % 60);
  DOM.timerText.textContent = `${mins}:${secs.toString().padStart(2, "0")}`;

  const progressRatio = clamped / MAX_RECORD_SECONDS;
  const offset = TIMER_CIRCUMFERENCE * (1 - progressRatio);
  DOM.timerRingFill.style.strokeDashoffset = offset;
}

function drawWaveform() {
  if (currentState !== AppState.LISTENING || !analyserNode || !DOM.waveformCanvas) return;

  const canvas = DOM.waveformCanvas;
  const ctx = canvas.getContext("2d");
  const bufferLength = analyserNode.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);
  analyserNode.getByteTimeDomainData(dataArray);

  // Calculate RMS volume level
  let sumSquares = 0;
  for (let i = 0; i < bufferLength; i++) {
    const norm = (dataArray[i] - 128) / 128;
    sumSquares += norm * norm;
  }
  const rms = Math.sqrt(sumSquares / bufferLength);

  if (DOM.volumeFill) {
    const volPct = Math.min(100, Math.round(rms * 280));
    DOM.volumeFill.style.width = `${volPct}%`;
  }

  // Detect low volume
  if (rms < 0.015) {
    quietTimer += 0.016;
    if (quietTimer > 2.0 && DOM.quietWarning) {
      DOM.quietWarning.classList.remove("hidden");
    }
  } else {
    quietTimer = 0;
    if (DOM.quietWarning) DOM.quietWarning.classList.add("hidden");
  }

  // Draw smooth waveform
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue("--accent-primary").trim() || "#4f46e5";
  ctx.beginPath();

  const sliceWidth = canvas.width / bufferLength;
  let x = 0;

  for (let i = 0; i < bufferLength; i++) {
    const v = dataArray[i] / 128.0;
    const y = (v * canvas.height) / 2;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
    x += sliceWidth;
  }

  ctx.lineTo(canvas.width, canvas.height / 2);
  ctx.stroke();

  animationFrameId = requestAnimationFrame(drawWaveform);
}

function stopRecording() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

if (DOM.recordBtn) DOM.recordBtn.addEventListener("click", startRecording);
if (DOM.stopBtn) DOM.stopBtn.addEventListener("click", stopRecording);

/* ==========================================================================
   6. In-Browser 16 kHz Mono WAV Conversion & Assessment Upload
   ========================================================================== */
async function handleRecordingComplete() {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
  }
  if (audioContext && audioContext.state !== "closed") {
    await audioContext.close();
    audioContext = null;
  }

  if (recordedChunks.length === 0) {
    showError("Recording Empty", "No audio was captured. Please speak into your microphone and try again.");
    setState(AppState.READY);
    return;
  }

  setState(AppState.CHECKING);
  if (DOM.checkingTitle) DOM.checkingTitle.textContent = "Checking your pronunciation...";
  if (DOM.checkingSub) DOM.checkingSub.textContent = "Analyzing acoustic waveform against phonetic reference";

  checkingTimerId = setTimeout(() => {
    if (currentState === AppState.CHECKING) {
      if (DOM.checkingTitle) DOM.checkingTitle.textContent = "First run loads the model...";
      if (DOM.checkingSub) DOM.checkingSub.textContent = "This can take a minute while neural weights load into CPU memory. Please wait.";
    }
  }, 8000);

  try {
    const rawBlob = new Blob(recordedChunks, { type: mediaRecorder.mimeType || "audio/webm" });
    const wavBlob = await convertTo16kHzMonoWav(rawBlob);

    const formData = new FormData();
    formData.append("audio", wavBlob, "recording.wav");
    formData.append("language", DOM.langSel.value);
    formData.append("text", DOM.wordSel.value);

    const res = await fetch("/api/assess", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    clearTimeout(checkingTimerId);

    if (!res.ok) {
      showError("Assessment Error", data.error || "The server could not assess the audio.");
      setState(AppState.READY);
      return;
    }

    renderResults(data);
    await loadHistory();
    setState(AppState.RESULT);

    if (DOM.resultPre) DOM.resultPre.textContent = JSON.stringify(data, null, 2);
    if (DOM.statusDiv) DOM.statusDiv.textContent = `Assessed: ${data.overall_score}%`;

  } catch (err) {
    clearTimeout(checkingTimerId);
    showError("Processing Failed", err.message || "An unexpected error occurred while processing audio.");
    setState(AppState.READY);
  }
}

/**
 * Convert arbitrary browser audio blob to 16 kHz Mono 16-bit PCM WAV.
 */
async function convertTo16kHzMonoWav(blob) {
  const arrayBuffer = await blob.arrayBuffer();
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  const ctx = new AudioCtx();

  const decodedBuffer = await ctx.decodeAudioData(arrayBuffer);
  const targetSampleRate = 16000;
  const offlineCtx = new OfflineAudioContext(
    1,
    Math.ceil(decodedBuffer.duration * targetSampleRate),
    targetSampleRate
  );

  const source = offlineCtx.createBufferSource();
  source.buffer = decodedBuffer;
  source.connect(offlineCtx.destination);
  source.start(0);

  const renderedBuffer = await offlineCtx.startRendering();
  await ctx.close();

  const channelData = renderedBuffer.getChannelData(0);
  const numSamples = channelData.length;
  const wavBuffer = new ArrayBuffer(44 + numSamples * 2);
  const view = new DataView(wavBuffer);

  function writeString(offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }

  writeString(0, "RIFF");
  view.setUint32(4, 36 + numSamples * 2, true);
  writeString(8, "WAVE");

  writeString(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM
  view.setUint16(22, 1, true); // Mono
  view.setUint32(24, targetSampleRate, true);
  view.setUint32(28, targetSampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);

  writeString(36, "data");
  view.setUint32(40, numSamples * 2, true);

  let byteOffset = 44;
  for (let i = 0; i < numSamples; i++) {
    const s = Math.max(-1, Math.min(1, channelData[i]));
    view.setInt16(byteOffset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    byteOffset += 2;
  }

  return new Blob([view], { type: "audio/wav" });
}

/* ==========================================================================
   7. Result Rendering (Animated Score Ring, Chips, Feedback)
   ========================================================================== */
function renderResults(data) {
  if (!DOM.scoreNumber || !DOM.scoreRingFill) return;
  const score = Math.round(data.overall_score || 0);
  DOM.scoreNumber.textContent = score;

  const offset = SCORE_CIRCUMFERENCE * (1 - score / 100);
  DOM.scoreRingFill.style.strokeDashoffset = offset;

  const scoreCard = document.querySelector(".score-card");
  if (scoreCard) {
    scoreCard.classList.remove("score-high", "score-medium", "score-low");
    if (score >= 70) {
      scoreCard.classList.add("score-high");
      DOM.scoreVerdict.textContent = "Great Pronunciation!";
    } else if (score >= 40) {
      scoreCard.classList.add("score-medium");
      DOM.scoreVerdict.textContent = "Good Effort — Getting Closer";
    } else {
      scoreCard.classList.add("score-low");
      DOM.scoreVerdict.textContent = "Needs Practice";
    }
  }

  if (DOM.wordsContainer) {
    DOM.wordsContainer.innerHTML = "";
    const words = data.words || [];

    words.forEach(w => {
      const card = document.createElement("div");
      card.className = "word-card";

      const header = document.createElement("div");
      header.className = "word-card-header";

      const wScore = Math.round(w.score || 0);
      const pillClass = wScore >= 70 ? "pill-high" : (wScore >= 40 ? "pill-medium" : "pill-low");
      header.innerHTML = `
        <span class="word-name">${w.word}</span>
        <span class="word-score-pill ${pillClass}">${wScore}%</span>
      `;
      card.appendChild(header);

      const chipsRow = document.createElement("div");
      chipsRow.className = "phoneme-chips-row";

      (w.phonemes || []).forEach(p => {
        const chip = document.createElement("span");
        chip.className = `phone-chip ${p.correct ? "chip-correct" : "chip-wrong"}`;

        if (p.correct) {
          chip.textContent = `/${p.expected}/`;
        } else if (p.expected && p.spoken) {
          chip.innerHTML = `/${p.expected}/ <span class="chip-arrow" aria-hidden="true">&rarr;</span> /${p.spoken}/`;
        } else if (p.expected) {
          chip.textContent = `[missing /${p.expected}/]`;
        } else {
          chip.textContent = `[extra /${p.spoken}/]`;
        }
        chipsRow.appendChild(chip);
      });

      card.appendChild(chipsRow);
      DOM.wordsContainer.appendChild(card);
    });
  }

  if (DOM.feedbackList) {
    DOM.feedbackList.innerHTML = "";
    const tips = data.feedback || ["Great pronunciation!"];
    tips.forEach(tip => {
      const li = document.createElement("li");
      li.textContent = tip;
      DOM.feedbackList.appendChild(li);
    });
  }

  if (DOM.timingDisplay) {
    if (data.timing) {
      const t = data.timing;
      DOM.timingDisplay.textContent =
        `Latency: ${t.total_sec}s (Reference: ${t.reference_sec}s, Recognizer: ${t.recognizer_sec}s, Scorer: ${t.scoring_sec}s)`;
    } else {
      DOM.timingDisplay.textContent = "";
    }
  }
}

if (DOM.tryAgainBtn) {
  DOM.tryAgainBtn.addEventListener("click", () => {
    setState(AppState.READY);
  });
}

/* ==========================================================================
   8. History List Management
   ========================================================================== */
async function loadHistory() {
  if (!DOM.historyTable || !DOM.historyTbody) return;
  try {
    const res = await fetch("/api/progress");
    if (!res.ok) return;
    const attempts = await res.json();

    if (!attempts || attempts.length === 0) {
      if (DOM.historyEmpty) DOM.historyEmpty.classList.remove("hidden");
      DOM.historyTable.classList.add("hidden");
      return;
    }

    if (DOM.historyEmpty) DOM.historyEmpty.classList.add("hidden");
    DOM.historyTable.classList.remove("hidden");

    DOM.historyTbody.innerHTML = attempts.slice(0, 10).map(row => {
      const score = Math.round(row.overall_score || 0);
      const badgeClass = score >= 70 ? "badge-high" : (score >= 40 ? "badge-medium" : "badge-low");

      let dateStr = row.created_at || "";
      if (dateStr.length > 16) dateStr = dateStr.slice(5, 16).replace("T", " ");

      return `
        <tr>
          <td><small class="muted-text">${dateStr}</small></td>
          <td><span class="lang-pill">${row.language}</span></td>
          <td><strong>${row.target_text}</strong></td>
          <td><span class="score-badge ${badgeClass}">${score}%</span></td>
        </tr>
      `;
    }).join("");

  } catch (err) {
    console.warn("Failed to load history:", err);
  }
}

/* ==========================================================================
   9. Initialization
   ========================================================================== */
document.addEventListener("DOMContentLoaded", () => {
  loadLanguages();
  loadHistory();
  setState(AppState.READY);
});
