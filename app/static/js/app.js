// Starter UI. OWNER: Role 4. Records audio and posts it to /api/assess.
const langSel = document.getElementById("language");
const wordSel = document.getElementById("word");
const result = document.getElementById("result");
const recBtn = document.getElementById("record");
const stopBtn = document.getElementById("stop");
let recorder, chunks = [];

async function loadLanguages() {
  const langs = await (await fetch("/api/languages")).json();
  langSel.innerHTML = langs.map(l => `<option>${l}</option>`).join("");
  await loadWords();
}

async function loadWords() {
  const data = await (await fetch(`/api/content/${langSel.value}`)).json();
  const items = Object.values(data.levels).flat();
  wordSel.innerHTML = items.map(i => `<option>${i.text}</option>`).join("");
}

langSel.addEventListener("change", loadWords);

recBtn.addEventListener("click", async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    chunks = [];
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.start();
    recBtn.disabled = true; stopBtn.disabled = false;
  } catch (err) {
    result.textContent = "Microphone not available: " + err.message;
  }
});

stopBtn.addEventListener("click", () => {
  recorder.onstop = async () => {
    const blob = new Blob(chunks, { type: recorder.mimeType });
    const form = new FormData();
    form.append("audio", blob, "recording.webm");
    form.append("language", langSel.value);
    form.append("text", wordSel.value);
    result.textContent = "Checking...";
    const res = await fetch("/api/assess", { method: "POST", body: form });
    result.textContent = JSON.stringify(await res.json(), null, 2);
    recBtn.disabled = false; stopBtn.disabled = true;
  };
  recorder.stop();
});

loadLanguages();
