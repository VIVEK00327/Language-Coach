#!/usr/bin/env python3
"""Cross-platform environment doctor script for Language Coach.
Checks Python version, package imports, eSpeak NG, .env variables (names only),
microphone library, and model cache status.
"""
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASS_ICON = "[PASS]"
FAIL_ICON = "[FAIL]"
WARN_ICON = "[WARN]"


def check_python_version() -> bool:
    v = sys.version_info
    req = (3, 10)
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    if v >= req:
        print(f"  {PASS_ICON} Python version: {version_str} (>= 3.10 required)")
        return True
    else:
        print(f"  {FAIL_ICON} Python version: {version_str} is below required 3.10+")
        print("         Fix: Install Python 3.10 or higher from python.org")
        return False


def check_required_packages() -> bool:
    packages = [
        ("flask", "Flask"),
        ("soundfile", "soundfile"),
        ("numpy", "numpy"),
        ("phonemizer", "phonemizer"),
        ("librosa", "librosa"),
        ("pytest", "pytest"),
    ]
    all_ok = True
    missing = []
    for mod_name, disp_name in packages:
        try:
            __import__(mod_name)
        except ImportError:
            all_ok = False
            missing.append(disp_name)

    if all_ok:
        print(f"  {PASS_ICON} Core Python packages imported successfully ({len(packages)} packages)")
    else:
        print(f"  {FAIL_ICON} Missing packages: {', '.join(missing)}")
        print("         Fix: Run 'pip install -r requirements.txt'")
    return all_ok


def check_espeak() -> bool:
    # 1. Check binary in PATH
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    # 2. Check PHONEMIZER_ESPEAK_LIBRARY environment variable
    lib_env = os.getenv("PHONEMIZER_ESPEAK_LIBRARY")
    
    # 3. Check phonemizer initialization
    phonemizer_works = False
    try:
        from phonemizer.backend import EspeakBackend
        phonemizer_works = EspeakBackend.is_available()
    except Exception:
        pass

    if exe or lib_env or phonemizer_works:
        details = []
        if exe:
            details.append(f"binary at '{exe}'")
        if lib_env:
            details.append(f"PHONEMIZER_ESPEAK_LIBRARY='{lib_env}'")
        if phonemizer_works:
            details.append("phonemizer backend available")
        print(f"  {PASS_ICON} eSpeak NG G2P engine found ({', '.join(details)})")
        return True
    else:
        print(f"  {WARN_ICON} eSpeak NG was not detected on system PATH or via PHONEMIZER_ESPEAK_LIBRARY")
        print("         Fix: On Windows, install eSpeak NG MSI and add to PATH or set PHONEMIZER_ESPEAK_LIBRARY.")
        print("              On Ubuntu/Debian: 'sudo apt install espeak-ng'. On macOS: 'brew install espeak-ng'.")
        print("              (Note: mock mode USE_MOCK_ML=1 will still function without eSpeak).")
        return False


def check_env_file() -> bool:
    env_path = ROOT / ".env"
    example_path = ROOT / ".env.example"

    if not env_path.exists():
        print(f"  {WARN_ICON} .env file not found at '{env_path}'")
        print("         Fix: Copy .env.example to .env: 'Copy-Item .env.example .env' (PowerShell)")
        return False

    print(f"  {PASS_ICON} .env file exists")

    # Read variable NAMES only — never print values!
    expected_vars = [
        "SECRET_KEY",
        "FLASK_DEBUG",
        "DATABASE_PATH",
        "UPLOAD_MAX_MB",
        "USE_MOCK_ML",
        "WHISPER_MODEL_SIZE",
        "PHONEME_MODEL_NAME",
        "HF_TOKEN",
        "LLM_API_KEY",
    ]

    set_vars = []
    empty_vars = []

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.split("#")[0].strip()
                if v:
                    set_vars.append(k)
                else:
                    empty_vars.append(k)

        print(f"       Variables configured: {', '.join(set_vars) if set_vars else '(none)'}")
        if empty_vars:
            print(f"       Variables empty / default: {', '.join(empty_vars)}")
        return True
    except Exception as e:
        print(f"  {WARN_ICON} Could not parse .env: {e}")
        return False


def check_microphone_lib() -> bool:
    try:
        import sounddevice
        print(f"  {PASS_ICON} Microphone audio capture library (sounddevice) is available")
        return True
    except Exception as e:
        print(f"  {WARN_ICON} sounddevice microphone support warning: {e}")
        print("         Fix: Run 'pip install sounddevice'")
        return False


def check_model_cache() -> None:
    # Check default HF cache or local cache
    home = Path.home()
    hf_cache = home / ".cache" / "huggingface" / "hub"
    local_models = ROOT / "models"

    found = []
    if hf_cache.exists() and any(hf_cache.iterdir()):
        found.append(f"Hugging Face cache at '{hf_cache}'")
    if local_models.exists() and any(local_models.iterdir()):
        found.append(f"local models/ directory")

    if found:
        print(f"  {PASS_ICON} Acoustic model storage: found {', '.join(found)}")
    else:
        print(f"  {PASS_ICON} Acoustic model storage: will download on first real inference request (~1.2 GB)")


def main():
    print("=" * 65)
    print(" Language Coach — Environment Diagnostic Doctor")
    print("=" * 65)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Core Python Packages", check_required_packages),
        ("eSpeak NG Phonemizer", check_espeak),
        ("Environment Configuration", check_env_file),
        ("Microphone Recording Lib", check_microphone_lib),
    ]

    results = []
    for name, fn in checks:
        print(f"Checking {name}...")
        ok = fn()
        results.append(ok)
        print()

    print("Checking Acoustic Model Storage...")
    check_model_cache()
    print()

    print("=" * 65)
    if all(results[:2]):  # Python + core packages are mandatory
        print(" Diagnostic Result: HEALTHY. Ready to run Language Coach.")
        print(" Command to start: python run.py")
        print("=" * 65)
        return 0
    else:
        print(" Diagnostic Result: ISSUES FOUND. Please review the fix hints above.")
        print("=" * 65)
        return 1


if __name__ == "__main__":
    sys.exit(main())
