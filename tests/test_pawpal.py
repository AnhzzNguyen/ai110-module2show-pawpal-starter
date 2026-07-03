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


if __name__ == "__main__":
    # Run tests with: pytest tests/test_pawpal.py -v
    pytest.main([__file__, "-v"])
