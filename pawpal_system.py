"""
PawPal+ Pet Care Scheduling System

This module contains the core classes for representing owners, pets, and tasks.
Based on the UML design with Owner, Pet, Task, and Scheduler classes.
"""

from dataclasses import dataclass, field
from datetime import time, datetime, timedelta
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    """Priority levels for tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Frequency(Enum):
    """Task frequency/recurrence options."""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    """
    Represents a single pet care activity.

    Attributes:
        title: Name of the task (e.g., "Morning walk")
        duration_minutes: How long the task takes
        priority: Importance level (LOW, MEDIUM, HIGH)
        description: Details about the task
        scheduled_time: Preferred time to do the task (optional)
        frequency: How often the task repeats (ONCE, DAILY, WEEKLY, MONTHLY)
        is_completed: Whether the task has been completed
    """
    title: str
    duration_minutes: int
    priority: Priority
    description: str = ""
    scheduled_time: Optional[time] = None
    frequency: Frequency = Frequency.DAILY
    is_completed: bool = False

    def get_priority_value(self) -> int:
        """Return numeric priority value for comparison (1-3)."""
        return self.priority.value

    def get_duration(self) -> int:
        """Return the duration of the task in minutes."""
        return self.duration_minutes

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False

    def __str__(self) -> str:
        return f"{self.title} ({self.duration_minutes}min, {self.priority.name}, {self.frequency.value})"


@dataclass
class Pet:
    """
    Represents a pet with details and care tasks.

    Attributes:
        name: Pet's name
        species: Type of pet (dog, cat, other)
        age: Age in years
        special_needs: List of special care requirements
        tasks: List of care tasks for this pet
    """
    name: str
    species: str  # "dog", "cat", "other"
    age: int
    special_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Validate pet attributes after initialization."""
        if self.age < 0:
            raise ValueError("Pet age cannot be negative")

    def has_special_needs(self) -> bool:
        """Check if the pet has any special care requirements."""
        return len(self.special_needs) > 0

    def get_care_requirements(self) -> List[Task]:
        """Return a list of care requirements (tasks) for this pet."""
        return self.tasks

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_incomplete_tasks(self) -> List[Task]:
        """Return only the incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed]

    def __str__(self) -> str:
        return f"{self.name} ({self.species}, {self.age} years old)"


class Owner:
    """
    Represents a pet owner who manages multiple pets.

    Provides access to all pets and their tasks, with availability constraints.
    """

    def __init__(self, name: str, available_start_time: time = None, available_end_time: time = None):
        """Initialize owner with name, availability window, and empty pets list."""
        self.name = name
        self.available_start_time = available_start_time or time(8, 0)  # Default: 8 AM
        self.available_end_time = available_end_time or time(22, 0)  # Default: 10 PM
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_available_hours(self) -> float:
        """Calculate total available hours in a day."""
        start = datetime.combine(datetime.today(), self.available_start_time)
        end = datetime.combine(datetime.today(), self.available_end_time)
        duration = end - start
        return duration.total_seconds() / 3600

    def get_availability_window(self) -> tuple:
        """Return the owner's availability as (start_time, end_time)."""
        return (self.available_start_time, self.available_end_time)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_care_requirements())
        return all_tasks

    def get_incomplete_tasks(self) -> List[Task]:
        """Get all incomplete tasks across all pets."""
        incomplete_tasks = []
        for pet in self.pets:
            incomplete_tasks.extend(pet.get_incomplete_tasks())
        return incomplete_tasks

    def get_tasks_for_pet(self, pet: Pet) -> List[Task]:
        """Get all tasks for a specific pet."""
        if pet in self.pets:
            return pet.get_care_requirements()
        return []

    def __str__(self) -> str:
        return f"Owner: {self.name} ({len(self.pets)} pet(s))"


class Scheduler:
    """
    The "Brain" of the PawPal+ system.

    Retrieves, organizes, and manages tasks across pets based on:
    - Task priorities
    - Owner availability
    - Task duration and scheduling constraints
    """

    def __init__(self):
        """Initialize the scheduler."""
        pass

    def schedule_tasks(self, owner: Owner, pet: Pet, tasks: List[Task], date: datetime) -> List[Task]:
        """Schedule tasks for a pet by prioritizing and fitting them into available time slots."""
        # Filter tasks for this specific pet
        pet_tasks = [t for t in tasks if t in pet.tasks]

        # Sort by priority (highest first)
        sorted_tasks = self.prioritize_tasks(pet_tasks)

        # Get available time window for the day
        available_start, available_end = owner.get_availability_window()
        current_time = datetime.combine(date, available_start)
        end_time = datetime.combine(date, available_end)

        scheduled_tasks = []

        # Greedily schedule tasks starting with highest priority
        for task in sorted_tasks:
            task_duration = timedelta(minutes=task.duration_minutes)
            task_end = current_time + task_duration

            # Check if task fits in remaining time
            if task_end <= end_time:
                scheduled_tasks.append(task)
                current_time = task_end

        return scheduled_tasks

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (highest first), then by scheduled time."""
        return sorted(
            tasks,
            key=lambda t: (-t.get_priority_value(), t.scheduled_time or time.max)
        )

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks chronologically by scheduled_time.

        **Algorithm:**
        Uses Python's built-in sorted() with a tuple key for stable multi-level sorting:
        1. First sorts by whether task has a scheduled_time (unscheduled = True sorts after)
        2. Then sorts by actual time value (uses time.max as fallback for None values)

        **Tuple Key Breakdown:**
            key=lambda t: (t.scheduled_time is None, t.scheduled_time or time.max)

            Level 1: (t.scheduled_time is None)
            - Returns False for tasks WITH a time (False < True, sorts first)
            - Returns True for tasks WITHOUT a time (sorts at end)

            Level 2: (t.scheduled_time or time.max)
            - Actual time(8, 30) for comparison when task is scheduled
            - time.max (23:59:59) as fallback when task.scheduled_time is None

        **Time Complexity:** O(n log n) where n = number of tasks
        **Space Complexity:** O(n) for the sorted list

        Args:
            tasks: List of Task objects to sort

        Returns:
            New sorted list of tasks (earliest first, then unscheduled)
            Original list is not modified

        Raises:
            None - gracefully handles tasks with or without scheduled_time

        Example:
            >>> tasks = [
            ...     Task("Evening Walk", 45, Priority.MEDIUM, scheduled_time=time(18, 0)),
            ...     Task("Breakfast", 15, Priority.HIGH, scheduled_time=time(8, 30)),
            ...     Task("Playtime", 20, Priority.LOW),  # No scheduled_time
            ... ]
            >>> sorted_tasks = scheduler.sort_by_time(tasks)
            >>> [t.title for t in sorted_tasks]
            ['Breakfast', 'Evening Walk', 'Playtime']

        Notes:
            - Stable sort: preserves order of equal elements
            - Does not modify the original list
            - Use this to organize a day's schedule chronologically
        """
        return sorted(
            tasks,
            key=lambda t: (t.scheduled_time is None, t.scheduled_time or time.max)
        )

    def sort_by_duration(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by duration (shortest first).

        **Algorithm:**
        Simple single-key sort on task duration in ascending order (1 min → 240 min).

        **Use Case:**
        Useful for finding "quick wins" - which tasks can fit in remaining time?
        Or scheduling shorter tasks before longer ones to maximize flexibility.

        **Time Complexity:** O(n log n) where n = number of tasks
        **Space Complexity:** O(n) for the sorted list

        Args:
            tasks: List of Task objects to sort

        Returns:
            New sorted list ordered by duration (shortest first)
            Original list is not modified

        Example:
            >>> tasks = [
            ...     Task("Walk", 30, Priority.HIGH),
            ...     Task("Feed", 5, Priority.HIGH),
            ...     Task("Playtime", 20, Priority.LOW),
            ... ]
            >>> by_duration = scheduler.sort_by_duration(tasks)
            >>> [(t.title, t.duration_minutes) for t in by_duration]
            [('Feed', 5), ('Playtime', 20), ('Walk', 30)]

        Notes:
            - Ascending order (shortest → longest)
            - Good strategy for "What can I do in 15 minutes?"
            - Consider combining with sort_by_priority_then_time() for better results
        """
        return sorted(tasks, key=lambda t: t.duration_minutes)

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by priority (highest first), then by scheduled time.

        **Algorithm:**
        Multi-level tuple-based sort with two criteria:
        1. Primary: Priority in descending order (HIGH → MEDIUM → LOW)
        2. Secondary: Scheduled time in ascending order (early → late)

        This implements a "priority + timing" strategy where high-priority tasks
        are grouped first and sorted chronologically within each priority level.

        **Lambda Key Breakdown:**
            key=lambda t: (-t.get_priority_value(), t.scheduled_time or time.max)

            Level 1: -t.get_priority_value()
            - Negates the priority value to reverse sort order
            - HIGH=3 becomes -3, MEDIUM=2 becomes -2, LOW=1 becomes -1
            - Result: -3 < -2 < -1, so HIGH sorts before MEDIUM before LOW
            - Why negate? Ascending sorts, but we want descending priority

            Level 2: t.scheduled_time or time.max
            - Breaks ties: if two tasks have same priority, sort by time
            - Tasks with a scheduled_time sort before unscheduled tasks
            - Unscheduled tasks get time.max (23:59:59) as fallback

        **Time Complexity:** O(n log n) where n = number of tasks
        **Space Complexity:** O(n) for the sorted list

        Args:
            tasks: List of Task objects to sort

        Returns:
            New sorted list: high-priority tasks first, tied tasks sorted by time
            Original list is not modified

        Example:
            >>> tasks = [
            ...     Task("Evening Walk", 45, Priority.MEDIUM, scheduled_time=time(18, 0)),
            ...     Task("Feed", 15, Priority.HIGH, scheduled_time=time(12, 0)),
            ...     Task("Playtime", 20, Priority.HIGH, scheduled_time=time(19, 0)),
            ...     Task("Unscheduled task", 10, Priority.HIGH),
            ... ]
            >>> sorted_tasks = scheduler.sort_by_priority_then_time(tasks)
            >>> [(t.title, t.priority.name, t.scheduled_time) for t in sorted_tasks]
            [('Feed', 'HIGH', 12:00), ('Playtime', 'HIGH', 19:00),
             ('Unscheduled task', 'HIGH', None), ('Evening Walk', 'MEDIUM', 18:00)]

        Notes:
            - Stable sort: equal elements maintain relative order
            - The negative sign is crucial for descending priority sort
            - This is the default strategy used by prioritize_tasks()
            - Good for "What's most important and when should I do it?"
        """
        return sorted(
            tasks,
            key=lambda t: (-t.get_priority_value(), t.scheduled_time or time.max)
        )

    def filter_tasks(self, tasks: List[Task], pet: Optional[Pet] = None,
                     status: str = "all", priority: Optional[Priority] = None) -> List[Task]:
        """
        Filter tasks by pet, completion status, and/or priority.

        Args:
            tasks: List of Task objects to filter
            pet: Optional Pet to filter tasks for a specific pet
            status: "all", "completed", or "incomplete"
            priority: Optional Priority level (Priority.HIGH, etc.)

        Returns:
            Filtered list of tasks

        Example:
            # Get all incomplete high-priority tasks
            important = scheduler.filter_tasks(tasks, status="incomplete", priority=Priority.HIGH)

            # Get all tasks for a specific pet
            mochi_tasks = scheduler.filter_tasks(tasks, pet=mochi)
        """
        filtered = tasks

        # Filter by pet if specified
        if pet is not None:
            filtered = [t for t in filtered if t in pet.tasks]

        # Filter by status
        if status == "completed":
            filtered = [t for t in filtered if t.is_completed]
        elif status == "incomplete":
            filtered = [t for t in filtered if not t.is_completed]

        # Filter by priority if specified
        if priority is not None:
            filtered = [t for t in filtered if t.priority == priority]

        return filtered

    def filter_by_pet_name(self, owner: Owner, pet_name: str,
                           status: str = "all") -> List[Task]:
        """
        Filter tasks by pet name and completion status.

        **Algorithm:**
        1. Linear search O(p) to find pet by name in owner's pets list
        2. Get all tasks from that pet
        3. Linear filter O(t) to apply status filter

        **UI-Friendly:**
        Designed for Streamlit dropdowns where users select pet name (string)
        rather than passing Pet objects directly.

        **Time Complexity:** O(p + t) where p = number of pets, t = tasks for that pet
        **Space Complexity:** O(t) for the filtered result list

        Args:
            owner: The Owner object containing all pets
            pet_name: Name of the pet to filter by (case-sensitive, e.g., "Mochi")
            status: Completion status filter:
                - "all": All tasks for this pet
                - "completed": Only ✅ marked complete
                - "incomplete": Only ⏳ not yet done

        Returns:
            List of Task objects for the specified pet filtered by status
            Empty list if pet not found or no tasks match criteria

        Raises:
            None - gracefully handles missing pets by returning empty list

        Example:
            >>> # Get all incomplete tasks for Mochi
            >>> mochi_todo = scheduler.filter_by_pet_name(owner, "Mochi", status="incomplete")
            >>> [t.title for t in mochi_todo]
            ['Evening Walk', 'Give Mochi Medication']

            >>> # Get all completed tasks for any pet
            >>> done = scheduler.filter_by_pet_name(owner, "Whiskers", status="completed")

            >>> # Pet not found - returns empty list
            >>> missing = scheduler.filter_by_pet_name(owner, "NonExistent", status="all")
            >>> len(missing) == 0
            True

        Notes:
            - Pet name matching is case-sensitive ("Mochi" ≠ "mochi")
            - Returns empty list if pet name not found (no error thrown)
            - Perfect for dropdown filters in Streamlit UI
            - Can be chained with sort_by_priority_then_time() for better results
        """
        # Find the pet by name (linear search)
        pet = next((p for p in owner.pets if p.name == pet_name), None)

        if pet is None:
            return []  # Pet not found - graceful fallback

        # Get all tasks for this pet
        pet_tasks = pet.get_care_requirements()

        # Apply status filter (list comprehension, O(t))
        if status == "completed":
            return [t for t in pet_tasks if t.is_completed]
        elif status == "incomplete":
            return [t for t in pet_tasks if not t.is_completed]
        else:  # "all"
            return pet_tasks

    def filter_by_status(self, tasks: List[Task], status: str) -> List[Task]:
        """
        Filter tasks by completion status only (quick single-criterion filter).

        **Algorithm:**
        Simple linear single-pass filter with list comprehension.
        - For "completed": includes only tasks where is_completed == True
        - For "incomplete": includes only tasks where is_completed == False
        - For "all": returns original list unchanged

        **Time Complexity:** O(n) where n = number of tasks
        **Space Complexity:** O(n) for the filtered result (worst case "all" status)

        Args:
            tasks: List of Task objects to filter
            status: Completion status filter (case-sensitive):
                - "all": All tasks, no filtering applied
                - "completed": Only ✅ tasks (is_completed=True)
                - "incomplete": Only ⏳ tasks (is_completed=False)

        Returns:
            New filtered list of Task objects
            Original list is not modified
            Returns empty list if no tasks match the status

        Raises:
            None - invalid status values are treated as "all"

        Example:
            >>> tasks = [
            ...     Task("Walk", 30, Priority.HIGH),  # incomplete
            ...     Task("Feed", 5, Priority.HIGH),   # incomplete
            ...     Task("Play", 20, Priority.LOW),   # incomplete
            ... ]
            >>> tasks[0].mark_completed()  # Mark Walk as done

            >>> todo = scheduler.filter_by_status(tasks, "incomplete")
            >>> len(todo)
            2

            >>> done = scheduler.filter_by_status(tasks, "completed")
            >>> len(done)
            1

            >>> all_tasks = scheduler.filter_by_status(tasks, "all")
            >>> len(all_tasks)
            3

        Notes:
            - Lightweight operation, suitable for real-time UI updates
            - Good companion to filter_by_pet_name() for dual filtering
            - Consider combining with sort methods for better organization
            - Can be used to generate dashboard statistics
        """
        if status == "completed":
            return [t for t in tasks if t.is_completed]
        elif status == "incomplete":
            return [t for t in tasks if not t.is_completed]
        else:  # "all" or any other value
            return tasks

    def detect_conflicts(self, scheduled_tasks: List[Task],
                        start_times: dict = None) -> List[tuple]:
        """
        Detect time conflicts between scheduled tasks.

        A conflict occurs when two tasks overlap in time.

        Args:
            scheduled_tasks: List of Task objects that are scheduled
            start_times: Optional dict mapping Task to datetime of when it starts
                        If not provided, uses task.scheduled_time (if available)

        Returns:
            List of tuples: [(task1, task2, overlap_duration), ...]
            Empty list if no conflicts

        Example:
            conflicts = scheduler.detect_conflicts(my_scheduled_tasks)
            if conflicts:
                for task1, task2, overlap in conflicts:
                    print(f"Conflict: {task1.title} overlaps with {task2.title}")
        """
        conflicts = []

        # If no start_times provided, use scheduled_time
        if start_times is None:
            start_times = {}
            for task in scheduled_tasks:
                if task.scheduled_time:
                    start_times[task] = datetime.combine(datetime.today(), task.scheduled_time)

        # Compare each pair of tasks
        for i, task1 in enumerate(scheduled_tasks):
            for task2 in scheduled_tasks[i + 1:]:
                # Skip if either task doesn't have a start time
                if task1 not in start_times or task2 not in start_times:
                    continue

                start1 = start_times[task1]
                end1 = start1 + timedelta(minutes=task1.duration_minutes)

                start2 = start_times[task2]
                end2 = start2 + timedelta(minutes=task2.duration_minutes)

                # Check for overlap: task1 starts before task2 ends AND task2 starts before task1 ends
                if start1 < end2 and start2 < end1:
                    overlap_start = max(start1, start2)
                    overlap_end = min(end1, end2)
                    overlap_duration = (overlap_end - overlap_start).total_seconds() / 60
                    conflicts.append((task1, task2, overlap_duration))

        return conflicts

    def detect_conflicts_with_warnings(self, owner: Owner,
                                       date: datetime = None) -> List[dict]:
        """
        Detect time conflicts across all pets and return detailed warning messages.

        **Algorithm:**
        Multi-pass conflict detection with severity classification:

        **Pass 1: Collect all scheduled tasks**
        - Gather all tasks from all pets that have a scheduled_time
        - Create (task, pet) tuples for context tracking
        - Skip unscheduled tasks (no time = no conflict possible)

        **Pass 2: Compare all task pairs (nested loop)**
        - For each unique pair of tasks, check for three types of conflicts:
            a) Time overlap: task1_start < task2_end AND task2_start < task1_end
            b) Back-to-back: task1_end == task2_start (no buffer)
        - Classify severity based on whether tasks are same pet or different pets

        **Severity Classification:**
        - CRITICAL: Different pets at same time → owner can't do both
        - WARNING: Same pet overlapping → pet can't do both
        - INFO: No time buffer → efficiency warning, not blocking

        **Time Complexity:** O(n² * c) where:
        - n = total tasks across all pets
        - c = constant time operations (time comparisons)
        - Worst case: all tasks have scheduled_time (quadratic)

        **Space Complexity:** O(c) where c = number of conflicts
        - Typically much smaller than O(n²) since most schedules don't conflict

        Args:
            owner: The Owner object (contains all pets)
            date: The date to check conflicts for
                - If None, defaults to datetime.today()
                - Used to combine with task.scheduled_time for comparison

        Returns:
            List of conflict dictionaries (may be empty if no conflicts):
                {
                    'severity': str,           # "critical", "warning", or "info"
                    'message': str,            # Human-readable description
                    'task1': Task,             # First conflicting task
                    'task2': Task,             # Second conflicting task
                    'pet1_name': str,          # Name of task1's pet
                    'pet2_name': str,          # Name of task2's pet
                    'overlap_minutes': float,  # Duration of overlap (0 for buffer conflicts)
                    'suggestion': str          # Actionable recommendation
                }

        Raises:
            None - gracefully handles edge cases (no tasks, unscheduled tasks, etc.)

        Example:
            >>> conflicts = scheduler.detect_conflicts_with_warnings(owner, today)
            >>> for conflict in conflicts:
            ...     if conflict['severity'] == 'critical':
            ...         print(f"ALERT: {conflict['message']}")
            ...         print(f"Fix: {conflict['suggestion']}")

            >>> # Check if critical conflicts exist
            >>> critical = [c for c in conflicts if c['severity'] == 'critical']
            >>> if critical:
            ...     print(f"Owner has {len(critical)} blocking conflict(s)")

        Notes:
            - Non-blocking: returns warnings, doesn't prevent scheduling
            - Returns empty list if no conflicts detected
            - Unscheduled tasks (no scheduled_time) are automatically skipped
            - Same task appearing twice due to recurring creates a conflict
            - Consider filtering by severity level in UI for different alert levels
            - Suggestions are specific to each conflict type (reschedule, reduce, etc.)
        """
        if date is None:
            date = datetime.today()

        conflicts = []
        all_tasks_with_pet = []  # List of (task, pet) tuples

        # Gather all tasks with their pet info
        for pet in owner.pets:
            for task in pet.tasks:
                if task.scheduled_time:
                    all_tasks_with_pet.append((task, pet))

        # Compare each pair of tasks
        for i, (task1, pet1) in enumerate(all_tasks_with_pet):
            for task2, pet2 in all_tasks_with_pet[i + 1:]:
                # Get start and end times
                start1 = datetime.combine(date, task1.scheduled_time)
                end1 = start1 + timedelta(minutes=task1.duration_minutes)

                start2 = datetime.combine(date, task2.scheduled_time)
                end2 = start2 + timedelta(minutes=task2.duration_minutes)

                # Check for overlap
                if start1 < end2 and start2 < end1:
                    overlap_start = max(start1, start2)
                    overlap_end = min(end1, end2)
                    overlap_minutes = (overlap_end - overlap_start).total_seconds() / 60

                    # Determine severity
                    if pet1 == pet2:
                        # Same pet can't do two tasks at once
                        severity = "warning"
                        message = (
                            f"⚠️  {pet1.name}'s '{task1.title}' "
                            f"({task1.scheduled_time}-{(start1 + timedelta(minutes=task1.duration_minutes)).time()}) "
                            f"overlaps with '{task2.title}' "
                            f"({task2.scheduled_time}-{(start2 + timedelta(minutes=task2.duration_minutes)).time()})"
                        )
                        suggestion = (
                            f"Reschedule '{task2.title}' to {(end1).time()} or later, "
                            f"or reduce duration of '{task1.title}'"
                        )
                    else:
                        # Different pets but owner can't do both at same time
                        severity = "critical"
                        message = (
                            f"🚨 CRITICAL: Owner can't do both tasks at {task1.scheduled_time}!\n"
                            f"   • {pet1.name}: '{task1.title}' "
                            f"({task1.scheduled_time}-{(start1 + timedelta(minutes=task1.duration_minutes)).time()})\n"
                            f"   • {pet2.name}: '{task2.title}' "
                            f"({task2.scheduled_time}-{(start2 + timedelta(minutes=task2.duration_minutes)).time()})"
                        )
                        suggestion = (
                            f"Option 1: Reschedule '{task2.title}' to {(end1).time()} or later\n"
                            f"   Option 2: Reschedule '{task1.title}' to {(end2).time()} or later\n"
                            f"   Option 3: Reduce duration of one task to avoid overlap"
                        )

                    conflicts.append({
                        "severity": severity,
                        "message": message,
                        "task1": task1,
                        "task2": task2,
                        "pet1_name": pet1.name,
                        "pet2_name": pet2.name,
                        "overlap_minutes": overlap_minutes,
                        "suggestion": suggestion
                    })

                # Check for back-to-back tasks with no buffer (info level)
                elif start2 == end1 or start1 == end2:
                    buffer_task, buffer_next = (task1, task2) if start2 == end1 else (task2, task1)
                    message = (
                        f"ℹ️  No time buffer: '{buffer_task.title}' ends at "
                        f"{(datetime.combine(date, buffer_task.scheduled_time) + timedelta(minutes=buffer_task.duration_minutes)).time()}, "
                        f"'{buffer_next.title}' starts at {buffer_next.scheduled_time}"
                    )
                    suggestion = (
                        f"Consider adding 5-10 minute buffer between tasks for transitions"
                    )

                    conflicts.append({
                        "severity": "info",
                        "message": message,
                        "task1": buffer_task,
                        "task2": buffer_next,
                        "pet1_name": pet1.name if buffer_task == task1 else pet2.name,
                        "pet2_name": pet2.name if buffer_task == task1 else pet1.name,
                        "overlap_minutes": 0,
                        "suggestion": suggestion
                    })

        return conflicts

    def expand_recurring_tasks(self, tasks: List[Task],
                              num_days: int = 7) -> List[Task]:
        """
        Expand recurring tasks into individual task instances across multiple days.

        **Algorithm:**
        For each input task, check frequency and generate copies accordingly:
        - ONCE: Include once (no copy)
        - DAILY: Generate num_days copies
        - WEEKLY: Generate ceil(num_days / 7) copies
        - MONTHLY: Generate 1 copy if num_days >= 30

        **Use Case:**
        Explode a compact task definition into a full schedule for analysis, display,
        or conflict detection. Useful for multi-day schedule generation.

        **Example Expansion:**
        Input: [Morning Walk (DAILY), Vet (ONCE), Water Plant (WEEKLY)]
        Expand for 7 days:
        Output: [Walk, Walk, Walk, Walk, Walk, Walk, Walk, Vet, Water Plant]
        (7 walks, 1 vet visit, 1 water plant)

        **Time Complexity:** O(n * m) where:
        - n = number of input tasks
        - m = average expansion factor (max is num_days for DAILY tasks)
        - Worst case: all DAILY tasks → O(n * num_days)

        **Space Complexity:** O(output size)
        - Each expanded task is a deep copy (independent object)

        Args:
            tasks: List of Task objects (may include mixed frequencies)
            num_days: Number of days to expand for (default 7, range 1-365)

        Returns:
            Expanded list of Task objects where:
            - ONCE tasks appear exactly 1 time
            - DAILY tasks appear num_days times
            - WEEKLY tasks appear ceil(num_days / 7) times
            - MONTHLY tasks appear 1 time if num_days >= 30, else 0 times
            - Each instance is an independent deep copy
            - Original list unchanged

        Raises:
            None - gracefully handles empty lists and all frequency types

        Example:
            >>> tasks = [
            ...     Task("Morning Walk", 30, Priority.HIGH, frequency=Frequency.DAILY),
            ...     Task("Vet Visit", 60, Priority.HIGH, frequency=Frequency.ONCE),
            ...     Task("Water Plants", 15, Priority.LOW, frequency=Frequency.WEEKLY),
            ... ]
            >>> expanded = scheduler.expand_recurring_tasks(tasks, num_days=7)

            >>> # Count by frequency
            >>> daily_count = len([t for t in expanded if t.title == "Morning Walk"])
            >>> once_count = len([t for t in expanded if t.title == "Vet Visit"])
            >>> weekly_count = len([t for t in expanded if t.title == "Water Plants"])
            >>> print(f"Daily: {daily_count}, Once: {once_count}, Weekly: {weekly_count}")
            Daily: 7, Once: 1, Weekly: 1

            >>> # Check a 30-day expansion
            >>> month = scheduler.expand_recurring_tasks(tasks, num_days=30)
            >>> walks = len([t for t in month if t.title == "Morning Walk"])
            >>> print(walks)
            30

        **Frequency Details:**
        - ONCE: Include task once, never repeat
        - DAILY: Include every day (num_days copies)
        - WEEKLY: Include every 7 days
            - For 7 days: 1 copy
            - For 8-13 days: 2 copies
            - For 14 days: 2 copies
            - Calculation: ceil(num_days / 7)
        - MONTHLY: Include once if num_days >= 30 (30 days ≈ 1 month)

        Notes:
            - Each copy is independent (deepcopy) - modifications don't affect others
            - All properties preserved: title, duration, priority, description, etc.
            - Original tasks list is not modified
            - Perfect for generating multi-day schedules
            - Consider combining with sort_by_priority_then_time() after expansion
            - Weekly/Monthly logic could be enhanced with actual date calculations
        """
        from copy import deepcopy

        expanded = []

        for task in tasks:
            if task.frequency == Frequency.ONCE:
                # One-time task: include once
                expanded.append(task)

            elif task.frequency == Frequency.DAILY:
                # Daily task: include num_days times
                for _ in range(num_days):
                    task_copy = deepcopy(task)
                    expanded.append(task_copy)

            elif task.frequency == Frequency.WEEKLY:
                # Weekly task: include every 7 days
                # For num_days, this is ceil(num_days / 7)
                num_weeks = (num_days + 6) // 7  # Ceiling division
                for _ in range(num_weeks):
                    if _ * 7 < num_days:  # Only include if within num_days range
                        task_copy = deepcopy(task)
                        expanded.append(task_copy)

            elif task.frequency == Frequency.MONTHLY:
                # Monthly task: include once per month (roughly every 30 days)
                # Include if 30+ days requested
                if num_days >= 30:
                    task_copy = deepcopy(task)
                    expanded.append(task_copy)

        return expanded

    def get_daily_schedule(self, owner: Owner, date: datetime) -> dict:
        """Generate a daily schedule for all pets owned by the owner."""
        daily_schedule = {}

        for pet in owner.pets:
            pet_tasks = self.schedule_tasks(owner, pet, owner.get_incomplete_tasks(), date)
            daily_schedule[pet.name] = pet_tasks

        return daily_schedule

    def get_task_summary(self, owner: Owner) -> dict:
        """Return a summary of all tasks by priority and completion status."""
        all_tasks = owner.get_all_tasks()

        summary = {
            "total_tasks": len(all_tasks),
            "completed_tasks": len([t for t in all_tasks if t.is_completed]),
            "incomplete_tasks": len([t for t in all_tasks if not t.is_completed]),
            "high_priority": len([t for t in all_tasks if t.priority == Priority.HIGH]),
            "medium_priority": len([t for t in all_tasks if t.priority == Priority.MEDIUM]),
            "low_priority": len([t for t in all_tasks if t.priority == Priority.LOW]),
        }

        return summary

    def complete_recurring_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """
        Mark a task complete and automatically create the next occurrence for recurring tasks.

        **Algorithm:**
        1. Mark current task as completed (is_completed = True)
        2. Check if task is recurring (DAILY or WEEKLY)
        3. If not recurring: return None (end of flow)
        4. If recurring:
           a. Deep copy the task to create a new instance (preserves all properties)
           b. Mark new instance as incomplete (is_completed = False)
           c. Keep scheduled_time the same (occurs again next day/week)
           d. Add new task to pet's task list
           e. Return the new task

        **Task Flow:**
        ```
        Original Task (Complete)
            ↓
        Mark as Completed ✅
            ↓
        Is Recurring? (DAILY/WEEKLY)
            ├─ YES → Deep Copy → Mark as Incomplete → Add to Pet → Return New Task
            └─ NO → Return None
        ```

        **Time Complexity:** O(1) constant time
        - Deep copy is O(1) for Task (small object with fixed fields)
        - List append is O(1) amortized

        **Space Complexity:** O(1) for the new task object

        Args:
            pet: The Pet object that owns the task
            task: The Task object to mark complete and potentially regenerate

        Returns:
            Task object: Newly created next-occurrence task (DAILY/WEEKLY recurring)
            None: If task is not recurring (ONCE, MONTHLY, or invalid frequency)

        Raises:
            None - gracefully handles all frequency types

        Example:
            >>> # Daily task - should regenerate
            >>> morning_walk = mochi.tasks[0]  # DAILY frequency
            >>> next_walk = scheduler.complete_recurring_task(mochi, morning_walk)
            >>> print(next_walk is not None)  # True
            >>> print(next_walk.is_completed)  # False (new instance)

            >>> # One-time task - should not regenerate
            >>> vet_visit = mochi.tasks[1]  # ONCE frequency
            >>> next_visit = scheduler.complete_recurring_task(mochi, vet_visit)
            >>> print(next_visit is None)  # True
            >>> print(vet_visit.is_completed)  # True (only marked complete)

        Notes:
            - Deep copy ensures new task is independent (changes don't affect original)
            - All properties preserved: title, duration, priority, description, etc.
            - Scheduled time stays the same (e.g., 8:00am daily means next day at 8:00am)
            - New task starts as incomplete (status = ⏳)
            - Perfect for habit tracking and daily routines
            - Use in app: `st.button("✓ Mark complete")` → calls this method
            - Frequency logic:
                - DAILY: Recreates tomorrow
                - WEEKLY: Recreates in 7 days (future enhancement)
                - ONCE: No recreation
                - MONTHLY: No recreation (future enhancement)
        """
        from copy import deepcopy

        # Mark the current task as complete
        task.mark_completed()

        # Only regenerate DAILY and WEEKLY tasks (not ONCE or MONTHLY)
        if task.frequency not in [Frequency.DAILY, Frequency.WEEKLY]:
            return None

        # Create a new task instance with deep copy
        # This preserves all properties: title, duration, priority, description, etc.
        next_task = deepcopy(task)
        next_task.mark_incomplete()  # New instance starts as incomplete ⏳

        # For daily tasks, scheduled_time stays the same (e.g., 8:00am tomorrow)
        # For weekly tasks, would need date adjustment (future enhancement)
        # Currently, time remains constant - just the date progresses naturally
        if next_task.scheduled_time:
            if task.frequency == Frequency.DAILY:
                # Daily task: same time each day
                # Scheduled_time stays as-is (e.g., 08:00)
                # Conceptually occurs "next day" at this time
                pass
            elif task.frequency == Frequency.WEEKLY:
                # Weekly task: same time each week
                # Currently: scheduled_time unchanged
                # Future: could track which day of week to enforce 7-day spacing
                pass

        # Add the new task to the pet's task list
        pet.add_task(next_task)

        return next_task
