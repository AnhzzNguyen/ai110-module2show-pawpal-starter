"""
PawPal+ Pet Care Scheduling System

This module contains the core classes for representing owners, pets, and tasks.
Based on the UML design with Owner, Pet, and Task classes.
"""

from dataclasses import dataclass, field
from datetime import time
from typing import List


@dataclass
class Task:
    """Represents a pet care task that needs to be scheduled."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    description: str = ""

    def get_priority_value(self) -> int:
        """Return numeric priority value for comparison."""
        pass

    def get_duration(self) -> int:
        """Return the duration of the task in minutes."""
        pass


@dataclass
class Pet:
    """Represents a pet with basic information and care needs."""
    name: str
    species: str  # "dog", "cat", "other"
    age: int
    special_needs: List[str] = field(default_factory=list)

    def has_special_needs(self) -> bool:
        """Check if the pet has any special care requirements."""
        pass

    def get_care_requirements(self) -> List:
        """Return a list of care requirements for this pet."""
        pass


class Owner:
    """Represents a pet owner with availability constraints."""

    def __init__(self, name: str, available_start_time: time = None, available_end_time: time = None):
        """Initialize an Owner with name and availability window."""
        self.name = name
        self.available_start_time = available_start_time or time(8, 0)  # Default: 8 AM
        self.available_end_time = available_end_time or time(22, 0)  # Default: 10 PM

    def get_available_hours(self) -> float:
        """Calculate total available hours in a day."""
        pass

    def get_availability_window(self) -> tuple:
        """Return the owner's availability as (start_time, end_time)."""
        pass
