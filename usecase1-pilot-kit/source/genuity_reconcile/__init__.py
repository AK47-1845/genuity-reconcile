"""Evidence-first industrial document reconciliation for Genuity IO."""

from .pipeline import ReconciliationPipeline, run_demo
from .release import build_operational_release, build_release_from_output

__all__ = ["ReconciliationPipeline", "run_demo", "build_operational_release", "build_release_from_output"]

__version__ = "1.1.0"
