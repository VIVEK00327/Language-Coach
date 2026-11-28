# Language Coach — Troubleshooting Guide

This matrix catalogs common setup, runtime, and environment issues with their root causes and verified fixes.

---

## Troubleshooting Matrix

| Symptom | Root Cause | Verified Fix |
|---|---|---|
| **Assessment result looks fake (spoken sounds always `w, o, t, e, r`, latency 0s).** | `USE_MOCK_ML=1` is active in `.env`. The mock recognizer is returning simulated static test phonemes. | Open `.env`, set `USE_MOCK_ML=0`, and restart the Flask server (`python run.py`). Ensure `PHONEME_MODEL_NAME=facebook/wav2vec2-lv-60-espeak-cv-ft` is set. |
| **`RuntimeError: PHONEME_MODEL_NAME environment variable is empty or not configured`** | `USE_MOCK_ML=0` is set, but `PHONEME_MODEL_NAME` is missing or commented out in `.env`. | Add `PHONEME_MODEL_NAME=facebook/wav2vec2-lv-60-espeak-cv-ft` to `.env` and restart the server. |
| **Changes made in `.env` have no effect.** | Environment variables are loaded once when Python initializes `app/config.py`. Live processes do not detect file edits. | Stop the running server with `Ctrl+C` in your terminal and restart with `python run.py`. |
| **`RuntimeError: Error opening ...: Format not recognised` (WAV/WebM issue)** | The browser sent raw WebM audio directly to Python `soundfile`, which requires RIFF WAVE format. | Ensure `app/static/js/wav.js` is loaded on `practice.html`. The browser `OfflineAudioContext` decodes WebM and encodes a 16 kHz mono 16-bit PCM WAV before upload. |
| **`phonemizer.backend.EspeakBackendError: espeak not installed` or not found** | eSpeak NG binary is missing from system `PATH` or dynamic library cannot be resolved by Python. | **Windows:** Install eSpeak NG from GitHub Releases MSI. If needed, set: `$env:PHONEMIZER_ESPEAK_LIBRARY="C:\Program Files\eSpeak NG\libespeak-ng.dll"`.<br>**Linux:** `sudo apt-get install -y espeak-ng`.<br>**macOS:** `brew install espeak-ng`. |
| **PowerShell error: `The token '&&' is not a valid statement separator in this version.`** | Windows PowerShell 5.1 does not support the bash `&&` chaining operator. | Run commands individually on separate lines, or use a semicolon `;` instead of `&&`. For example:<br>`git add -A`<br>`git commit -m "msg"`<br>`git push` |
| **Microphone blocked: "Microphone Access Denied" alert in UI.** | Browser security denied microphone access, or site is not on `localhost`/`127.0.0.1`. | Click the camera/microphone icon or lock icon in the browser address bar, set Microphone to **Allow**, and refresh. Access the app via `http://127.0.0.1:5000` (browsers treat `127.0.0.1` as a secure origin). |
| **First assessment request takes 60–90 seconds to respond.** | On the very first request in `USE_MOCK_ML=0` mode, PyTorch downloads the 1.18 GB wav2vec 2.0 weights and warms up the CPU cache. | This is normal one-time behavior. The UI displays: *"First run loads the model... This can take a minute while neural weights load into CPU memory."* Subsequent attempts will process in 0.5–1.5 seconds. |
| **`OSError: [Errno 98] Address already in use` or `[WinError 10048] Only one usage of each socket address`** | Port 5000 is occupied by an orphaned Flask process or another service (e.g. macOS AirPlay Receiver). | **Windows:** Kill the process holding port 5000:<br>`Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process`<br>**Linux/Mac:** `lsof -ti:5000 | xargs kill -9`<br>Alternatively, run Flask on an alternate port: `python run.py --port 5001`. |
| **PyTorch install slow or failing (`pip install torch`)** | Default PyTorch wheel includes multi-gigabyte CUDA GPU drivers which are unnecessary for our CPU-only architecture. | Install the official lightweight CPU-only wheel directly:<br>`pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| **`OSError: [Errno 28] No space left on device` during model download** | The default Hugging Face cache directory (`~/.cache/huggingface/`) ran out of disk space. | Set the cache directory to a drive with at least 5 GB free space in `.env` or terminal:<br>`$env:HF_HOME="D:\hf_cache"` |
| **`git status` shows `.env` as untracked or modified** | `.gitignore` is missing or `.env` was previously added to the Git index cache. | Remove `.env` from git tracking without deleting your local file:<br>`git rm --cached .env`<br>`git commit -m "R1: untrack .env"`<br>Verify `.gitignore` contains `.env`. |
| **`Audio clip is ...s long (max limit is 15.0s)` error banner** | The uploaded audio clip exceeded the maximum allowed duration limit of 15 seconds. | Keep practice recordings concise (single words or short phrases). The UI automatically stops recording at 10 seconds. |
| **Sanskrit words produce no sound in "Listen" mode** | Browser `speechSynthesis` voices lack a native classical Sanskrit (`sa-IN`) voice package. | Language Coach automatically maps Sanskrit to the Hindi voice (`hi-IN`) as an acoustic approximation, and displays an informative notification. |

---

## Still Having Issues?

Run the diagnostic script:
```powershell
python scripts\check_setup.py
```
If all checks report `[PASS]`, run unit tests to isolate the component:
```powershell
python -m pytest tests -v
```
To test specific subsystems:
- Speech preprocessing: `python -m pytest tests/test_audio_utils.py`
- Reference phonemizer: `python -m pytest tests/test_reference.py`
- Phoneme scoring: `python -m pytest tests/test_scorer.py`
- Flask API endpoints: `python -m pytest tests/test_api.py`
