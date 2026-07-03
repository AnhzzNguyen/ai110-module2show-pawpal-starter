"""
Unit tests for PawPal+ system classes.

Tests cover:
- Task completion status tracking
- Pet task management
- Owner availability calculations
- Scheduler logic
"""

import pytest
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler, Priority, Frequency


class TestTaskCompletion:
    """Tests for Task completion status tracking."""

    def test_task_completion_status_changes(self):
        """
        Verify that calling mark_completed() actually changes the task's status.

        Given: A task with is_completed = False
        When: mark_completed() is called
        Then: is_completed should be True
        """
        # Arrange
        task = Task(
            title="Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            description="Take the dog for a walk"
        )
        assert task.is_completed == False, "Task should start as incomplete"

        # Act
        task.mark_completed()

        # Assert
        assert task.is_completed == True, "Task should be marked as completed"

    def test_task_incomplete_status_reverts(self):
        """
        Verify that calling mark_incomplete() reverts the task back to incomplete.

        Given: A completed task
        When: mark_incomplete() is called
        Then: is_completed should be False
        """
        # Arrange
        task = Task(
            title="Feeding",
            duration_minutes=15,
            priority=Priority.HIGH
        )
        task.mark_completed()
        assert task.is_completed == True

        # Act
        task.mark_incomplete()

        # Assert
        assert task.is_completed == False, "Task should be marked as incomplete"


class TestTaskAddition:
    """Tests for Pet task management."""

    def test_adding_task_increases_pet_task_count(self):
        """
        Verify that adding a task to a Pet increases that pet's task count.

        Given: A pet with 0 tasks
        When: A task is added via add_task()
        Then: The pet's task list length should increase by 1
        """
        # Arrange
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3
        )
        initial_task_count = len(pet.tasks)
        assert initial_task_count == 0, "Pet should start with 0 tasks"

        # Act
        task = Task(
            title="Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH
        )
        pet.add_task(task)

        # Assert
        final_task_count = len(pet.tasks)
        assert final_task_count == 1, "Pet should have 1 task after adding"
        assert final_task_count == initial_task_count + 1, "Task count should increase by 1"

    def test_adding_multiple_tasks_to_pet(self):
        """
        Verify that multiple tasks can be added to a pet and the count increases correctly.

        Given: A pet with 0 tasks
        When: Multiple tasks are added
        Then: The pet's task count should match the number of added tasks
        """
        # Arrange
        pet = Pet(
            name="Whiskers",
            species="cat",
            age=5
        )

        # Act - Add 3 tasks
        tasks = [
            Task("Feeding", 10, Priority.HIGH),
            Task("Playtime", 20, Priority.MEDIUM),
            Task("Grooming", 30, Priority.LOW)
        ]

        for task in tasks:
            pet.add_task(task)

        # Assert
        assert len(pet.tasks) == 3, "Pet should have 3 tasks"
        assert pet.get_care_requirements() == tasks, "Tasks should be retrievable"


class TestPetValidation:
    """Tests for Pet data validation."""

    def test_negative_age_raises_error(self):
        """
        Verify that creating a pet with negative age raises ValueError.

        Given: A negative age value
        When: Creating a Pet with that age
        Then: ValueError should be raised
        """
        # Act & Assert
        with pytest.raises(ValueError, match="Pet age cannot be negative"):
            Pet(
                name="Mochi",
                species="dog",
                age=-5  # Invalid: negative age
            )

    def test_pet_with_special_needs(self):
        """
        Verify that a pet can have special needs and the method reports correctly.

        Given: A pet with special needs
        When: has_special_needs() is called
        Then: Should return True
        """
        # Arrange
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=["needs lots of exercise"]
        )

        # Assert
        assert pet.has_special_needs() == True, "Pet with special needs should return True"

    def test_pet_without_special_needs(self):
        """Verify that a pet without special needs returns False."""
        # Arrange
        pet = Pet(
            name="Whiskers",
            species="cat",
            age=5
        )

        # Assert
        assert pet.has_special_needs() == False, "Pet without special needs should return False"


class TestOwnerAvailability:
    """Tests for Owner availability calculations."""

    def test_owner_available_hours_calculation(self):
        """
        Verify that get_available_hours() calculates the correct duration.

        Given: An owner available from 8 AM to 10 PM
        When: get_available_hours() is called
        Then: Should return 14.0 hours
        """
        # Arrange
        owner = Owner(
            name="Jordan",
            available_start_time=time(8, 0),
            available_end_time=time(22, 0)
        )

        # Act
        hours = owner.get_available_hours()

        # Assert
        assert hours == 14.0, "8 AM to 10 PM should be 14 hours"

    def test_owner_pets_count(self):
        """
        Verify that adding pets to an owner increases the pet count.

        Given: An owner with no pets
        When: Pets are added
        Then: Pet count should increase
        """
        # Arrange
        owner = Owner(name="Jordan")
        assert len(owner.pets) == 0, "Owner should start with 0 pets"

        # Act
        pet1 = Pet("Mochi", "dog", 3)
        pet2 = Pet("Whiskers", "cat", 5)
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        # Assert
        assert len(owner.pets) == 2, "Owner should have 2 pets"


class TestSchedulerBasics:
    """Tests for basic Scheduler functionality."""

    def test_prioritize_tasks_sorts_by_priority(self):
        """
        Verify that prioritize_tasks() sorts by priority (high to low).

        Given: Tasks with mixed priorities
        When: prioritize_tasks() is called
        Then: Tasks should be ordered HIGH → MEDIUM → LOW
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Low Priority Task", 10, Priority.LOW),
            Task("High Priority Task", 10, Priority.HIGH),
            Task("Medium Priority Task", 10, Priority.MEDIUM),
        ]

        # Act
        sorted_tasks = scheduler.prioritize_tasks(tasks)

        # Assert
        assert sorted_tasks[0].priority == Priority.HIGH, "First task should be HIGH priority"
        assert sorted_tasks[1].priority == Priority.MEDIUM, "Second task should be MEDIUM priority"
        assert sorted_tasks[2].priority == Priority.LOW, "Third task should be LOW priority"


class TestSortingCorrectness:
    """Tests for task sorting—verify chronological and priority-based ordering."""

    def test_sort_by_time_chronological_order(self):
        """
        Verify that sort_by_time() returns tasks in chronological order.

        Given: Tasks with different scheduled times
        When: sort_by_time() is called
        Then: Tasks should be ordered earliest to latest
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Evening Walk", 45, Priority.MEDIUM, scheduled_time=time(18, 0)),
            Task("Breakfast", 15, Priority.HIGH, scheduled_time=time(8, 30)),
            Task("Lunch", 30, Priority.HIGH, scheduled_time=time(12, 0)),
        ]

        # Act
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Assert
        assert sorted_tasks[0].title == "Breakfast", "First task should be at 8:30"
        assert sorted_tasks[1].title == "Lunch", "Second task should be at 12:00"
        assert sorted_tasks[2].title == "Evening Walk", "Third task should be at 18:00"

    def test_sort_by_time_unscheduled_tasks_at_end(self):
        """
        Verify that tasks without scheduled_time sort to the end.

        Given: Mix of scheduled and unscheduled tasks
        When: sort_by_time() is called
        Then: Unscheduled tasks should appear last
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Unscheduled 1", 20, Priority.LOW),  # No time
            Task("Morning Task", 15, Priority.HIGH, scheduled_time=time(8, 0)),
            Task("Unscheduled 2", 10, Priority.HIGH),  # No time
            Task("Afternoon Task", 30, Priority.MEDIUM, scheduled_time=time(14, 0)),
        ]

        # Act
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Assert
        # First two should be scheduled (in time order)
        assert sorted_tasks[0].title == "Morning Task"
        assert sorted_tasks[1].title == "Afternoon Task"
        # Last two should be unscheduled (in original order due to stable sort)
        assert sorted_tasks[2].title == "Unscheduled 1"
        assert sorted_tasks[3].title == "Unscheduled 2"

    def test_sort_by_time_all_unscheduled(self):
        """
        Verify sort_by_time() handles all unscheduled tasks gracefully.

        Given: Tasks with no scheduled_time
        When: sort_by_time() is called
        Then: Should return all tasks without error
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Task A", 20, Priority.HIGH),
            Task("Task B", 10, Priority.MEDIUM),
            Task("Task C", 30, Priority.LOW),
        ]

        # Act
        sorted_tasks = scheduler.sort_by_time(tasks)

        # Assert
        assert len(sorted_tasks) == 3, "All tasks should be returned"
        assert sorted_tasks == tasks, "Order should remain unchanged (stable sort)"

    def test_sort_by_duration_shortest_first(self):
        """
        Verify that sort_by_duration() orders tasks shortest to longest.

        Given: Tasks with varying durations
        When: sort_by_duration() is called
        Then: Tasks should be ordered by duration ascending
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Long Task", 60, Priority.HIGH),
            Task("Quick Task", 5, Priority.HIGH),
            Task("Medium Task", 20, Priority.LOW),
        ]

        # Act
        sorted_tasks = scheduler.sort_by_duration(tasks)

        # Assert
        assert sorted_tasks[0].duration_minutes == 5, "First task should be 5 minutes"
        assert sorted_tasks[1].duration_minutes == 20, "Second task should be 20 minutes"
        assert sorted_tasks[2].duration_minutes == 60, "Third task should be 60 minutes"

    def test_sort_by_priority_then_time(self):
        """
        Verify that sort_by_priority_then_time() orders by priority first, then time.

        Given: Tasks with mixed priorities and times
        When: sort_by_priority_then_time() is called
        Then: HIGH priority tasks come first (sorted by time), then MEDIUM, then LOW
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Evening Walk", 45, Priority.MEDIUM, scheduled_time=time(18, 0)),
            Task("Morning Feed", 15, Priority.HIGH, scheduled_time=time(8, 30)),
            Task("Playtime", 20, Priority.HIGH, scheduled_time=time(19, 0)),
            Task("Afternoon Nap", 10, Priority.LOW, scheduled_time=time(14, 0)),
        ]

        # Act
        sorted_tasks = scheduler.sort_by_priority_then_time(tasks)

        # Assert
        # HIGH priority tasks first (sorted by time: 8:30, 19:00)
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[0].title == "Morning Feed"
        assert sorted_tasks[1].priority == Priority.HIGH
        assert sorted_tasks[1].title == "Playtime"
        # MEDIUM priority next
        assert sorted_tasks[2].priority == Priority.MEDIUM
        assert sorted_tasks[2].title == "Evening Walk"
        # LOW priority last
        assert sorted_tasks[3].priority == Priority.LOW
        assert sorted_tasks[3].title == "Afternoon Nap"

    def test_sort_by_priority_then_time_with_unscheduled(self):
        """
        Verify that unscheduled tasks within same priority come last.

        Given: Tasks with same priority, some scheduled and some not
        When: sort_by_priority_then_time() is called
        Then: Scheduled tasks come before unscheduled within priority level
        """
        # Arrange
        scheduler = Scheduler()
        tasks = [
            Task("Unscheduled High", 10, Priority.HIGH),
            Task("Scheduled High AM", 15, Priority.HIGH, scheduled_time=time(9, 0)),
            Task("Scheduled High PM", 20, Priority.HIGH, scheduled_time=time(17, 0)),
        ]

        # Act
        sorted_tasks = scheduler.sort_by_priority_then_time(tasks)

        # Assert
        assert sorted_tasks[0].title == "Scheduled High AM"
        assert sorted_tasks[1].title == "Scheduled High PM"
        assert sorted_tasks[2].title == "Unscheduled High"


class TestRecurrenceLogic:
    """Tests for recurring task handling and completion flow."""

    def test_complete_daily_task_creates_new_task(self):
        """
        Verify that marking a DAILY task complete creates a new incomplete task.

        Given: A pet with a DAILY recurring task
        When: complete_recurring_task() is called on that task
        Then: The original task should be marked completed
             AND a new incomplete task should be added to the pet
        """
        # Arrange
        scheduler = Scheduler()
        pet = Pet("Mochi", "dog", 3)
        daily_walk = Task(
            "Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            frequency=Frequency.DAILY,
            scheduled_time=time(8, 0)
        )
        pet.add_task(daily_walk)
        initial_task_count = len(pet.tasks)

        # Act
        new_task = scheduler.complete_recurring_task(pet, daily_walk)

        # Assert
        assert daily_walk.is_completed == True, "Original task should be marked completed"
        assert new_task is not None, "New task should be created for DAILY recurring"
        assert new_task.is_completed == False, "New task should start as incomplete"
        assert len(pet.tasks) == initial_task_count + 1, "Pet should have one additional task"
        assert new_task in pet.tasks, "New task should be added to pet's task list"

    def test_complete_daily_task_preserves_properties(self):
        """
        Verify that the new task generated from completing a daily task preserves all properties.

        Given: A DAILY task with title, duration, priority, description
        When: complete_recurring_task() creates a new instance
        Then: All properties should match the original (except is_completed)
        """
        # Arrange
        scheduler = Scheduler()
        pet = Pet("Mochi", "dog", 3)
        original_task = Task(
            title="Feeding Time",
            duration_minutes=15,
            priority=Priority.HIGH,
            description="Give Mochi her afternoon meal",
            frequency=Frequency.DAILY,
            scheduled_time=time(12, 0)
        )
        pet.add_task(original_task)

        # Act
        new_task = scheduler.complete_recurring_task(pet, original_task)

        # Assert
        assert new_task.title == original_task.title, "Title should match"
        assert new_task.duration_minutes == original_task.duration_minutes, "Duration should match"
        assert new_task.priority == original_task.priority, "Priority should match"
        assert new_task.description == original_task.description, "Description should match"
        assert new_task.scheduled_time == original_task.scheduled_time, "Scheduled time should match"
        assert new_task.frequency == original_task.frequency, "Frequency should match"

    def test_complete_weekly_task_creates_new_task(self):
        """
        Verify that marking a WEEKLY task complete creates a new incomplete task.

        Given: A pet with a WEEKLY recurring task
        When: complete_recurring_task() is called
        Then: A new incomplete task should be created
        """
        # Arrange
        scheduler = Scheduler()
        pet = Pet("Mochi", "dog", 3)
        weekly_groom = Task(
            "Grooming",
            duration_minutes=60,
            priority=Priority.MEDIUM,
            frequency=Frequency.WEEKLY,
            scheduled_time=time(10, 0)
        )
        pet.add_task(weekly_groom)

        # Act
        new_task = scheduler.complete_recurring_task(pet, weekly_groom)

        # Assert
        assert new_task is not None, "WEEKLY tasks should generate new instance"
        assert new_task.is_completed == False

    def test_complete_once_task_does_not_create_new(self):
        """
        Verify that marking a ONCE task complete does NOT create a new task.

        Given: A pet with a ONCE task
        When: complete_recurring_task() is called
        Then: Original task marked completed, but no new task created (returns None)
        """
        # Arrange
        scheduler = Scheduler()
        pet = Pet("Mochi", "dog", 3)
        vet_visit = Task(
            "Vet Checkup",
            duration_minutes=45,
            priority=Priority.HIGH,
            frequency=Frequency.ONCE
        )
        pet.add_task(vet_visit)
        initial_task_count = len(pet.tasks)

        # Act
        new_task = scheduler.complete_recurring_task(pet, vet_visit)

        # Assert
        assert vet_visit.is_completed == True, "Task should be marked completed"
        assert new_task is None, "ONCE task should not generate a new instance"
        assert len(pet.tasks) == initial_task_count, "Task count should not increase"

    def test_complete_monthly_task_does_not_create_new(self):
        """
        Verify that marking a MONTHLY task complete does NOT create a new task.

        Given: A pet with a MONTHLY recurring task
        When: complete_recurring_task() is called
        Then: Original task marked completed, but no new task created (returns None)
        """
        # Arrange
        scheduler = Scheduler()
        pet = Pet("Whiskers", "cat", 5)
        nail_trim = Task(
            "Nail Trimming",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            frequency=Frequency.MONTHLY
        )
        pet.add_task(nail_trim)

        # Act
        new_task = scheduler.complete_recurring_task(pet, nail_trim)

        # Assert
        assert nail_trim.is_completed == True
        assert new_task is None, "MONTHLY tasks should not generate new instance yet"

    def test_complete_recurring_task_chain(self):
        """
        Verify that completing a task multiple times chains correctly.

        Given: A DAILY task
        When: complete_recurring_task() is called, then again on the new task
        Then: Should create a sequence of tasks, all properly marked
        """
        # Arrange
        scheduler = Scheduler()
        pet = Pet("Mochi", "dog", 3)
        daily_task = Task(
            "Walk",
            30,
            Priority.HIGH,
            frequency=Frequency.DAILY,
            scheduled_time=time(9, 0)
        )
        pet.add_task(daily_task)

        # Act - First completion
        task_1 = daily_task
        task_2 = scheduler.complete_recurring_task(pet, task_1)
        assert task_2 is not None

        # Second completion
        task_3 = scheduler.complete_recurring_task(pet, task_2)
        assert task_3 is not None

        # Assert
        assert task_1.is_completed == True, "First task should be completed"
        assert task_2.is_completed == True, "Second task should be completed"
        assert task_3.is_completed == False, "Third task should be incomplete"
        assert len(pet.tasks) == 3, "Pet should have 3 task instances"


class TestConflictDetection:
    """Tests for detecting scheduling conflicts between tasks."""

    def test_detect_conflicts_overlapping_same_pet(self):
        """
        Verify that overlapping tasks for the same pet are detected as warnings.

        Given: One pet with two overlapping tasks
        When: detect_conflicts_with_warnings() is called
        Then: Should detect the overlap and classify as "warning" (same pet)
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog", 3)
        owner.add_pet(pet)

        # Two overlapping tasks: 8:00-8:30 and 8:15-8:45
        task1 = Task(
            "Walk 1",
            duration_minutes=30,
            priority=Priority.HIGH,
            scheduled_time=time(8, 0)
        )
        task2 = Task(
            "Walk 2",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            scheduled_time=time(8, 15)
        )
        pet.add_task(task1)
        pet.add_task(task2)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        assert len(conflicts) > 0, "Should detect conflict"
        assert conflicts[0]["severity"] == "warning", "Same pet overlap should be 'warning'"
        assert conflicts[0]["task1"] == task1
        assert conflicts[0]["task2"] == task2

    def test_detect_conflicts_overlapping_different_pets(self):
        """
        Verify that overlapping tasks for different pets are detected as critical.

        Given: Two pets with tasks scheduled at the same time
        When: detect_conflicts_with_warnings() is called
        Then: Should detect overlap and classify as "critical" (owner can't do both)
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet1 = Pet("Mochi", "dog", 3)
        pet2 = Pet("Whiskers", "cat", 5)
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        # Same time tasks for different pets: both at 8:00
        task1 = Task("Walk", 30, Priority.HIGH, scheduled_time=time(8, 0))
        task2 = Task("Feed", 20, Priority.HIGH, scheduled_time=time(8, 0))
        pet1.add_task(task1)
        pet2.add_task(task2)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        assert len(conflicts) > 0, "Should detect conflict"
        assert conflicts[0]["severity"] == "critical", "Different pets at same time should be 'critical'"
        assert conflicts[0]["pet1_name"] == "Mochi"
        assert conflicts[0]["pet2_name"] == "Whiskers"

    def test_detect_no_conflicts_sequential_tasks(self):
        """
        Verify that sequential (non-overlapping) tasks are not flagged as conflicts.

        Given: Tasks scheduled back-to-back with no overlap
        When: detect_conflicts_with_warnings() is called
        Then: Should return empty conflict list (or only "info" level for buffer)
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog", 3)
        owner.add_pet(pet)

        # Sequential: 8:00-8:30, then 8:30-9:00
        task1 = Task("Walk", 30, Priority.HIGH, scheduled_time=time(8, 0))
        task2 = Task("Feeding", 30, Priority.HIGH, scheduled_time=time(8, 30))
        pet.add_task(task1)
        pet.add_task(task2)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        critical_conflicts = [c for c in conflicts if c["severity"] == "critical"]
        warning_conflicts = [c for c in conflicts if c["severity"] == "warning"]
        assert len(critical_conflicts) == 0, "No critical conflicts should exist"
        assert len(warning_conflicts) == 0, "No warning conflicts should exist"

    def test_detect_conflicts_back_to_back_info_level(self):
        """
        Verify that back-to-back tasks with no buffer trigger info-level alerts.

        Given: Tasks that end and start at exact same time
        When: detect_conflicts_with_warnings() is called
        Then: Should flag as "info" level (efficiency warning, not blocking)
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog", 3)
        owner.add_pet(pet)

        task1 = Task("Walk", 30, Priority.HIGH, scheduled_time=time(8, 0))
        task2 = Task("Feeding", 15, Priority.HIGH, scheduled_time=time(8, 30))
        pet.add_task(task1)
        pet.add_task(task2)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        info_conflicts = [c for c in conflicts if c["severity"] == "info"]
        assert len(info_conflicts) > 0, "Should detect back-to-back tasks as info"

    def test_detect_conflicts_unscheduled_tasks_ignored(self):
        """
        Verify that tasks without scheduled_time are not flagged in conflicts.

        Given: Tasks where some have no scheduled_time
        When: detect_conflicts_with_warnings() is called
        Then: Unscheduled tasks should be silently ignored (not in conflicts)
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog", 3)
        owner.add_pet(pet)

        task1 = Task("Walk", 30, Priority.HIGH, scheduled_time=time(8, 0))
        task2 = Task("Playtime", 20, Priority.MEDIUM)  # No scheduled_time
        task3 = Task("Feeding", 15, Priority.HIGH, scheduled_time=time(8, 30))
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        # With unscheduled task ignored, task1 and task3 don't overlap
        critical = [c for c in conflicts if c["severity"] == "critical"]
        warning = [c for c in conflicts if c["severity"] == "warning"]
        assert len(critical) == 0
        assert len(warning) == 0

    def test_detect_conflicts_partial_overlap(self):
        """
        Verify that partial overlaps are correctly detected.

        Given: Task 1 from 8:00-8:30, Task 2 from 8:15-8:45 (15 min overlap)
        When: detect_conflicts_with_warnings() is called
        Then: Should return conflict with correct overlap duration of 15 minutes
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet = Pet("Mochi", "dog", 3)
        owner.add_pet(pet)

        # Task 1: 8:00-8:30 (30 min), Task 2: 8:15-8:45 (30 min) = 15 min overlap
        task1 = Task("Walk", 30, Priority.HIGH, scheduled_time=time(8, 0))
        task2 = Task("Playtime", 30, Priority.MEDIUM, scheduled_time=time(8, 15))
        pet.add_task(task1)
        pet.add_task(task2)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        assert len(conflicts) > 0, "Should detect one conflict"
        warning_conflicts = [c for c in conflicts if c["severity"] == "warning"]
        assert len(warning_conflicts) > 0, "Same pet overlap should be 'warning'"
        assert warning_conflicts[0]["overlap_minutes"] == 15, "Overlap should be 15 minutes"

    def test_detect_conflicts_with_multiple_pets(self):
        """
        Verify conflict detection works correctly with multiple pets and multiple conflicts.

        Given: Multiple pets with multiple overlapping tasks
        When: detect_conflicts_with_warnings() is called
        Then: Should detect all conflicts correctly
        """
        # Arrange
        from datetime import datetime
        scheduler = Scheduler()
        owner = Owner("Jordan")
        pet1 = Pet("Mochi", "dog", 3)
        pet2 = Pet("Whiskers", "cat", 5)
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        # Create multiple conflicts
        # Mochi: 8:00-8:30 (HIGH)
        # Whiskers: 8:15-8:45 (HIGH) - conflicts with Mochi
        # Mochi: 10:00-10:45 (MEDIUM)
        # Whiskers: 10:30-11:00 (MEDIUM) - conflicts with Mochi
        task1 = Task("Mochi Walk", 30, Priority.HIGH, scheduled_time=time(8, 0))
        task2 = Task("Whiskers Feed", 30, Priority.HIGH, scheduled_time=time(8, 15))
        task3 = Task("Mochi Play", 45, Priority.MEDIUM, scheduled_time=time(10, 0))
        task4 = Task("Whiskers Play", 30, Priority.MEDIUM, scheduled_time=time(10, 30))

        pet1.add_task(task1)
        pet2.add_task(task2)
        pet1.add_task(task3)
        pet2.add_task(task4)

        # Act
        conflicts = scheduler.detect_conflicts_with_warnings(owner, datetime(2026, 7, 3))

        # Assert
        assert len(conflicts) >= 2, "Should detect at least 2 conflicts"
        critical_conflicts = [c for c in conflicts if c["severity"] == "critical"]
        assert len(critical_conflicts) >= 2, "Both overlaps should be critical (different pets)"


if __name__ == "__main__":
    # Run tests with: pytest tests/test_pawpal.py -v
    pytest.main([__file__, "-v"])
