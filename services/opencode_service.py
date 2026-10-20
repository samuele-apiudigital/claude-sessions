"""OpenCode session service with headless support and caching."""
import json
import os
from typing import Dict, List

from service_provider import Service, ServiceRegistry


class OpenCodeService(Service):
    """Service for managing OpenCode sessions with headless execution and cache."""
    
    def __init__(self, cache_path: str = "~/.claude/sessions-cache.json"):
        self.cache_path = os.path.expanduser(cache_path)
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self) -> None:
        """Ensure the cache directory exists."""
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
    
    @property
    def name(self) -> str:
        return "opencode"
    
    def _load_cache(self) -> Dict:
        """Load session cache from disk."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self, cache: Dict) -> None:
        """Save session cache to disk."""
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(cache, f, indent=2)
    
    def execute(self, args: List[str]) -> Dict[str, any]:
        """Execute OpenCode session management."""
        if "--list" in args:
            return self._list_sessions()
        elif "--cache" in args:
            return self._get_cache()
        else:
            # Default: run opencode headless
            return self._run_headless()
    
    def _list_sessions(self) -> Dict[str, any]:
        """List cached sessions."""
        cache = self._load_cache()
        return {
            "success": True,
            "sessions": list(cache.keys()),
            "cache_path": self.cache_path
        }
    
    def _get_cache(self) -> Dict[str, any]:
        """Get session cache."""
        cache = self._load_cache()
        return {
            "success": True,
            "cache": cache
        }
    
    def _run_headless(self) -> Dict[str, any]:
        """Run OpenCode in headless mode."""
        try:
            # Check if opencode is available
            result = subprocess.run(
                ["opencode", "--headless"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except FileNotFoundError:
            return {"success": False, "error": "opencode command not found"}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
