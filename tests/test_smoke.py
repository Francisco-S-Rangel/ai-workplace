# tests/test_smoke.py — WHY: proves the test harness runs from Phase 1 on (topic 11:
# tests as a hallucination guard — "done" means a green run, not a claim).
import study_buddy


def test_package_imports():
    assert study_buddy.__version__
