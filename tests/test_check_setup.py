"""Test for scripts/check_setup.py diagnostic tool."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_setup.py"


def test_check_setup_script_runs():
    """Verify that python scripts/check_setup.py executes and exits cleanly."""
    assert SCRIPT.exists(), f"Diagnostic script not found at {SCRIPT}"

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )

    assert result.returncode == 0, f"check_setup.py failed with returncode {result.returncode}:\n{result.stdout}\n{result.stderr}"
    assert "Language Coach" in result.stdout
    assert "Python version" in result.stdout
    assert "Core Python packages" in result.stdout
