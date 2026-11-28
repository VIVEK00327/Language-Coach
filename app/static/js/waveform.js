// Live audio waveform visualizer (Web Audio AnalyserNode). OWNER: R4.

var waveformState = {
  analyser: null,
  canvas: null,
  animId: null,
  active: false
};

/**
 * Start drawing the waveform using an AnalyserNode.
 * @param {AnalyserNode} analyser
 * @param {HTMLCanvasElement} canvas
 * @param {HTMLElement} volumeFill - Volume bar fill element.
 * @param {HTMLElement} quietWarning - Low-volume warning element.
 */
function startWaveform(analyser, canvas, volumeFill, quietWarning) {
  waveformState.analyser = analyser;
  waveformState.canvas = canvas;
  waveformState.active = true;
  waveformState._quietTimer = 0;
  waveformState._volumeFill = volumeFill;
  waveformState._quietWarning = quietWarning;
  drawFrame();
}

function stopWaveform() {
  waveformState.active = false;
  if (waveformState.animId) {
    cancelAnimationFrame(waveformState.animId);
    waveformState.animId = null;
  }
}

function drawFrame() {
  if (!waveformState.active || !waveformState.analyser || !waveformState.canvas) return;

  var analyser = waveformState.analyser;
  var canvas = waveformState.canvas;
  var ctx = canvas.getContext("2d");
  var bufLen = analyser.frequencyBinCount;
  var data = new Uint8Array(bufLen);
  analyser.getByteTimeDomainData(data);

  // RMS volume
  var sum = 0;
  for (var i = 0; i < bufLen; i++) {
    var norm = (data[i] - 128) / 128;
    sum += norm * norm;
  }
  var rms = Math.sqrt(sum / bufLen);

  if (waveformState._volumeFill) {
    waveformState._volumeFill.style.width = Math.min(100, Math.round(rms * 280)) + "%";
  }

  // Quiet detection
  if (rms < 0.015) {
    waveformState._quietTimer += 0.016;
    if (waveformState._quietTimer > 2.0 && waveformState._quietWarning) {
      waveformState._quietWarning.classList.remove("hidden");
    }
  } else {
    waveformState._quietTimer = 0;
    if (waveformState._quietWarning) waveformState._quietWarning.classList.add("hidden");
  }

  // Draw
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.lineWidth = 2.5;
  var accent = getComputedStyle(document.documentElement).getPropertyValue("--accent-1").trim() || "#7c3aed";
  ctx.strokeStyle = accent;
  ctx.beginPath();

  var sliceW = canvas.width / bufLen;
  var x = 0;
  for (var j = 0; j < bufLen; j++) {
    var v = data[j] / 128.0;
    var y = (v * canvas.height) / 2;
    if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    x += sliceW;
  }
  ctx.lineTo(canvas.width, canvas.height / 2);
  ctx.stroke();

  waveformState.animId = requestAnimationFrame(drawFrame);
}
