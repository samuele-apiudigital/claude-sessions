"""Main session manager orchestrator using service provider pattern."""
import sys
import os
import subprocess

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service_provider import ServiceRegistry, SessionManager
from services.claude_service import ClaudeService
from services.opencode_service import OpenCodeService


def create_registry() -> SessionManager:
    """Create and configure the service registry."""
    registry = ServiceRegistry()
    
    # Register available services
    claude_service = ClaudeService()
    opencode_service = OpenCodeService()
    
    registry.register(claude_service)
    registry.register(opencode_service)
    
    return SessionManager(registry)


def run_claude_service(args):
    """Run the claude-sessions shell script."""
    try:
        result = subprocess.run(
            ["./claude-sessions"] + args,
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


def run_opencode_service(args):
    """Run the opencode service."""
    try:
        result = subprocess.run(
            ["python3", "-c", 
             "import sys; sys.path.insert(0, '.'); "
             "from services.opencode_service import OpenCodeService; "
             "service = OpenCodeService(); "
             "print(service.execute(args))"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {"success": True, "output": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """Main entry point for the session manager."""
    manager = create_registry()
    
    if len(sys.argv) < 2:
        print("Usage: python3 session_manager.py <service> [args...]")
        print("Available services:", ", ".join(manager.list_services()))
        return
    
    service_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    if service_name == "claude":
        result = run_claude_service(args)
    elif service_name == "opencode":
        result = run_opencode_service(args)
    else:
        result = manager.run(service_name, args)
    
    print(result)


if __name__ == "__main__":
    main()
