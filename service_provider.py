"""Service Provider Pattern for session management."""
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Service(ABC):
    """Base class for all services."""
    
    @abstractmethod
    def execute(self, args: list) -> Dict[str, Any]:
        """Execute the service with given arguments."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Service name identifier."""
        pass


class ServiceRegistry:
    """Registry for managing services."""
    
    def __init__(self):
        self._services: Dict[str, Service] = {}
    
    def register(self, service: Service) -> None:
        """Register a service with the registry."""
        self._services[service.name] = service
    
    def get(self, name: str) -> Optional[Service]:
        """Get a service by name."""
        return self._services.get(name)
    
    def execute(self, name: str, args: list) -> Dict[str, Any]:
        """Execute a service by name with arguments."""
        service = self.get(name)
        if service:
            return service.execute(args)
        return {"error": f"Service {name} not found"}


class SessionManager:
    """Main orchestrator that coordinates all services."""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
    
    def run(self, service_name: str, args: list) -> Dict[str, Any]:
        """Run a service with the given arguments."""
        return self.registry.execute(service_name, args)
    
    def list_services(self) -> list:
        """List all registered services."""
        return list(self.registry._services.keys())
