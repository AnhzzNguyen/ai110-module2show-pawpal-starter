"""
PawPal+ Demo Script

This script demonstrates the PawPal+ system in action:
- Creating an owner with availability constraints
- Adding multiple pets with different care needs
- Scheduling tasks based on priority and time
- Displaying today's schedule
"""

from datetime import datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler, Priority, Frequency


def print_separator(title: str = ""):
    """Print a formatted separator line."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'='*60}\n")


def main():
    """Run the PawPal+ demo."""

    # ==================== SETUP ====================
    print_separator("🐾 PawPal+ System Demo 🐾")

    # Create an owner
    owner = Owner(
        name="Jordan",
        available_start_time=time(8, 0),   # 8 AM
        available_end_time=time(22, 0)     # 10 PM
    )
    print(f"✓ Created owner: {owner.name}")
    print(f"  Available: {owner.available_start_time} to {owner.available_end_time}")
    print(f"  Total hours available: {owner.get_available_hours():.1f} hours\n")

    # ==================== CREATE PETS ====================
    print_separator("Adding Pets")

    # Pet 1: Dog
    mochi = Pet(
        name="Mochi",
        species="dog",
        age=3,
        special_needs=["needs lots of exercise"]
    )
    owner.add_pet(mochi)
    print(f"✓ Added: {mochi}")
    print(f"  Special needs: {', '.join(mochi.special_needs)}")

    # Pet 2: Cat
    whiskers = Pet(
        name="Whiskers",
        species="cat",
        age=5,
        special_needs=["sensitive stomach"]
    )
    owner.add_pet(whiskers)
    print(f"\n✓ Added: {whiskers}")
    print(f"  Special needs: {', '.join(whiskers.special_needs)}")

    # ==================== ADD TASKS ====================
    print_separator("Adding Care Tasks")

    # Mochi's tasks
    morning_walk = Task(
        title="Morning Walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        description="Take Mochi for a walk in the park",
        scheduled_time=time(8, 0),
        frequency=Frequency.DAILY
    )
    mochi.add_task(morning_walk)
    print(f"✓ Task 1: {morning_walk}")

    breakfast = Task(
        title="Breakfast",
        duration_minutes=15,
        priority=Priority.HIGH,
        description="Feed Mochi breakfast",
        scheduled_time=time(8, 30),
        frequency=Frequency.DAILY
    )
    mochi.add_task(breakfast)
    print(f"✓ Task 2: {breakfast}")

    evening_walk = Task(
        title="Evening Walk",
        duration_minutes=45,
        priority=Priority.MEDIUM,
        description="Evening exercise at dog park",
        scheduled_time=time(18, 0),
        frequency=Frequency.DAILY
    )
    mochi.add_task(evening_walk)
    print(f"✓ Task 3: {evening_walk}")

    # Whiskers' tasks
    litter_box = Task(
        title="Clean Litter Box",
        duration_minutes=10,
        priority=Priority.MEDIUM,
        description="Daily litter box cleaning",
        scheduled_time=time(9, 0),
        frequency=Frequency.DAILY
    )
    whiskers.add_task(litter_box)
    print(f"✓ Task 4: {litter_box}")

    cat_meal = Task(
        title="Cat Meal",
        duration_minutes=10,
        priority=Priority.HIGH,
        description="Special diet meal for sensitive stomach",
        scheduled_time=time(12, 0),
        frequency=Frequency.DAILY
    )
    whiskers.add_task(cat_meal)
    print(f"✓ Task 5: {cat_meal}")

    playtime = Task(
        title="Playtime",
        duration_minutes=20,
        priority=Priority.LOW,
        description="Interactive play with laser pointer",
        scheduled_time=time(19, 0),
        frequency=Frequency.DAILY
    )
    whiskers.add_task(playtime)
    print(f"✓ Task 6: {playtime}")

    # Add conflicting tasks to test conflict detection
    medication = Task(
        title="Give Mochi Medication",
        duration_minutes=10,
        priority=Priority.HIGH,
        description="Daily allergy medication",
        scheduled_time=time(8, 20),  # Conflicts with Breakfast (8:30-8:45)
        frequency=Frequency.DAILY
    )
    mochi.add_task(medication)
    print(f"✓ Task 7: {medication} [CONFLICT with Breakfast]")

    grooming = Task(
        title="Brush Whiskers",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        description="Daily grooming routine",
        scheduled_time=time(8, 30),  # SAME TIME as Mochi's Breakfast (8:30-8:45)
        frequency=Frequency.DAILY
    )
    whiskers.add_task(grooming)
    print(f"✓ Task 8: {grooming} [CRITICAL: Owner can't do both at 8:30!]")

    # ==================== SCHEDULER ====================
    print_separator("Scheduling Today's Tasks")

    scheduler = Scheduler()

    # Get today's date
    today = datetime.now()
    print(f"Date: {today.strftime('%A, %B %d, %Y')}\n")

    # ==================== DISPLAY SCHEDULE ====================
    print_separator("📅 TODAY'S SCHEDULE 📅")

    # Get the daily schedule for all pets
    daily_schedule = scheduler.get_daily_schedule(owner, today)

    for pet_name, scheduled_tasks in daily_schedule.items():
        print(f"\n🐾 {pet_name}'s Schedule:")
        print(f"   {'-'*50}")

        if scheduled_tasks:
            for i, task in enumerate(scheduled_tasks, 1):
                priority_str = f"[{task.priority.name}]".ljust(8)
                time_str = f"~{task.scheduled_time}" if task.scheduled_time else "~TBD"
                duration_str = f"({task.duration_minutes}min)"

                print(f"   {i}. {priority_str} {task.title}")
                print(f"      ⏰ {time_str} {duration_str}")
                print(f"      📝 {task.description}\n")
        else:
            print(f"   No tasks scheduled today\n")

    # ==================== TEST SORTING & FILTERING ====================
    print_separator("🧪 TESTING SORT & FILTER METHODS 🧪")

    # Get all tasks
    all_tasks = owner.get_all_tasks()
    print(f"Total tasks in system: {len(all_tasks)}\n")

    # Test 1: Sort by time (chronological)
    print("TEST 1: Sort by time (earliest first)")
    print("-" * 50)
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    for task in sorted_by_time:
        time_str = f"{task.scheduled_time}" if task.scheduled_time else "UNSCHEDULED"
        print(f"  • {task.title:20} @ {time_str}")
    print()

    # Test 2: Sort by duration (shortest first)
    print("TEST 2: Sort by duration (shortest first)")
    print("-" * 50)
    sorted_by_duration = scheduler.sort_by_duration(all_tasks)
    for task in sorted_by_duration:
        print(f"  • {task.title:20} ({task.duration_minutes:2}min)")
    print()

    # Test 3: Sort by priority then time
    print("TEST 3: Sort by priority (HIGH→LOW), then by time")
    print("-" * 50)
    sorted_by_priority = scheduler.sort_by_priority_then_time(all_tasks)
    for task in sorted_by_priority:
        priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
        time_str = f"{task.scheduled_time}" if task.scheduled_time else "UNSCHEDULED"
        emoji = priority_emoji.get(task.priority.name, "")
        print(f"  {emoji} {task.priority.name:6} | {task.title:20} @ {time_str}")
    print()

    # Test 4: Filter by pet name
    print("TEST 4: Filter tasks by pet name")
    print("-" * 50)
    mochi_tasks = scheduler.filter_by_pet_name(owner, "Mochi", status="all")
    print(f"Mochi's tasks ({len(mochi_tasks)}):")
    for task in mochi_tasks:
        print(f"  • {task.title}")
    print()

    whiskers_tasks = scheduler.filter_by_pet_name(owner, "Whiskers", status="all")
    print(f"Whiskers' tasks ({len(whiskers_tasks)}):")
    for task in whiskers_tasks:
        print(f"  • {task.title}")
    print()

    # Test 5: Filter by status
    print("TEST 5: Filter by completion status")
    print("-" * 50)

    # Mark some tasks as completed for demonstration
    if len(morning_walk.title) > 0:
        morning_walk.mark_completed()
        breakfast.mark_completed()
        cat_meal.mark_completed()

    completed_tasks = scheduler.filter_by_status(all_tasks, "completed")
    incomplete_tasks = scheduler.filter_by_status(all_tasks, "incomplete")

    print(f"Completed tasks ({len(completed_tasks)}):")
    for task in completed_tasks:
        print(f"  ✅ {task.title}")
    print()

    print(f"Incomplete tasks ({len(incomplete_tasks)}):")
    for task in incomplete_tasks:
        print(f"  ⏳ {task.title}")
    print()

    # Test 6: Advanced filtering (Mochi's incomplete tasks only)
    print("TEST 6: Advanced - Mochi's incomplete tasks")
    print("-" * 50)
    mochi_incomplete = scheduler.filter_by_pet_name(owner, "Mochi", status="incomplete")
    for task in mochi_incomplete:
        status_icon = "✅" if task.is_completed else "⏳"
        print(f"  {status_icon} {task.title} ({task.duration_minutes}min)")
    print()

    # Test 7: Filter then sort
    print("TEST 7: Filter (incomplete) then sort by priority")
    print("-" * 50)
    incomplete_sorted = scheduler.sort_by_priority_then_time(incomplete_tasks)
    priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
    for task in incomplete_sorted:
        emoji = priority_emoji.get(task.priority.name, "")
        pet_name = "Mochi" if task in mochi.tasks else "Whiskers"
        print(f"  {emoji} {task.priority.name:6} | {pet_name:10} | {task.title}")
    print()

    # ==================== TEST RECURRING TASK COMPLETION ====================
    print_separator("♻️ TESTING RECURRING TASK COMPLETION ♻️")

    print(f"Before completing task:")
    print(f"  Mochi's tasks: {len(mochi.tasks)}")
    for i, t in enumerate(mochi.tasks, 1):
        status = "✅" if t.is_completed else "⏳"
        print(f"    {i}. {status} {t.title}")
    print()

    # Complete the morning walk (DAILY task) - should create next occurrence
    print("Completing 'Morning Walk' (DAILY recurring task)...")
    next_occurrence = scheduler.complete_recurring_task(mochi, morning_walk)

    print(f"\nAfter completing task:")
    print(f"  Mochi's tasks: {len(mochi.tasks)}")
    for i, t in enumerate(mochi.tasks, 1):
        status = "✅" if t.is_completed else "⏳"
        freq = f" [{t.frequency.value}]" if t != morning_walk else " [DAILY]"
        print(f"    {i}. {status} {t.title}{freq}")
    print()

    if next_occurrence:
        print(f"✓ New task created automatically!")
        print(f"  Original task: {morning_walk.title} - {morning_walk.is_completed}")
        print(f"  Next occurrence: {next_occurrence.title} - {'Complete' if next_occurrence.is_completed else 'Incomplete'}")
        print(f"  Frequency: {next_occurrence.frequency.value}")
        print(f"  Scheduled time: {next_occurrence.scheduled_time}")
    else:
        print("✗ No recurring task was created")
    print()

    # Test with a ONCE task (should not regenerate)
    print("Completing 'Playtime' (LOW priority task)...")
    playtime_original_freq = playtime.frequency
    next_playtime = scheduler.complete_recurring_task(whiskers, playtime)

    if next_playtime:
        print(f"  ✓ New task created (frequency: {playtime_original_freq.value})")
    else:
        print(f"  ✗ No new task created (frequency: {playtime_original_freq.value} - not recurring)")
    print()

    # Show final task count
    print("Final task summary:")
    summary = scheduler.get_task_summary(owner)
    print(f"  Total tasks: {summary['total_tasks']}")
    print(f"  Completed: {summary['completed_tasks']}")
    print(f"  Incomplete: {summary['incomplete_tasks']}")
    print()

    # ==================== TEST CONFLICT DETECTION ====================
    print_separator("🚨 CONFLICT DETECTION TEST 🚨")

    print("Detecting scheduling conflicts for all pets...\n")

    conflicts = scheduler.detect_conflicts_with_warnings(owner, today)

    if conflicts:
        print(f"Found {len(conflicts)} conflict(s):\n")
        for idx, conflict in enumerate(conflicts, 1):
            severity = conflict["severity"]
            print(f"\nConflict #{idx} [{severity.upper()}]")
            print(f"━" * 70)
            print(f"{conflict['message']}")
            print(f"\n💡 Suggestion:")
            print(f"   {conflict['suggestion']}")
            print(f"\nOverlap: {conflict['overlap_minutes']:.1f} minutes")
            print(f"Pets involved: {conflict['pet1_name']} ↔ {conflict['pet2_name']}")
    else:
        print("✓ No scheduling conflicts detected!")
    print()

    # ==================== SUMMARY ====================
    print_separator("📊 TASK SUMMARY 📊")

    summary = scheduler.get_task_summary(owner)

    print(f"Total Tasks: {summary['total_tasks']}")
    print(f"  ✅ Completed: {summary['completed_tasks']}")
    print(f"  ⏳ Incomplete: {summary['incomplete_tasks']}")
    print(f"\nBy Priority:")
    print(f"  🔴 High: {summary['high_priority']}")
    print(f"  🟡 Medium: {summary['medium_priority']}")
    print(f"  🟢 Low: {summary['low_priority']}")

    # ==================== OWNER SUMMARY ====================
    print_separator("👤 OWNER SUMMARY 👤")

    print(f"{owner.name} has {len(owner.pets)} pet(s):")
    for pet in owner.pets:
        print(f"  • {pet.name}: {len(pet.tasks)} task(s)")

    print_separator()
    print("✨ Demo complete! All systems operational. ✨\n")


if __name__ == "__main__":
    main()
