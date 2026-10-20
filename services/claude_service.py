"""Claude session service wrapper."""
import subprocess
import sys
from typing import Dict, List

from service_provider import Service, ServiceRegistry


class ClaudeService(Service):
    """Service for managing Claude sessions via the existing claude-sessions CLI."""
    
    @property
    def name(self) -> str:
        return "claude"
    
    def execute(self, args: List[str]) -> Dict[str, any]:
        """Execute claude-sessions with the given arguments."""
        try:
            cmd = ["python3", "-I", "claude-sessions"] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
