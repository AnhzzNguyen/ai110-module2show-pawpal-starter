# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the demo script to see the PawPal+ system in action:

```bash
python3 main.py
```

Sample terminal output:

```
============================================================
  🐾 PawPal+ System Demo 🐾
============================================================

✓ Created owner: Jordan
  Available: 08:00:00 to 22:00:00
  Total hours available: 14.0 hours


============================================================
  Adding Pets
============================================================

✓ Added: Mochi (dog, 3 years old)
  Special needs: needs lots of exercise

✓ Added: Whiskers (cat, 5 years old)
  Special needs: sensitive stomach

============================================================
  Adding Care Tasks
============================================================

✓ Task 1: Morning Walk (30min, HIGH, daily)
✓ Task 2: Breakfast (15min, HIGH, daily)
✓ Task 3: Evening Walk (45min, MEDIUM, daily)
✓ Task 4: Clean Litter Box (10min, MEDIUM, daily)
✓ Task 5: Cat Meal (10min, HIGH, daily)
✓ Task 6: Playtime (20min, LOW, daily)

============================================================
  Scheduling Today's Tasks
============================================================

Date: Thursday, July 02, 2026


============================================================
  📅 TODAY'S SCHEDULE 📅
============================================================


🐾 Mochi's Schedule:
   --------------------------------------------------
   1. [HIGH]   Morning Walk
      ⏰ ~08:00:00 (30min)
      📝 Take Mochi for a walk in the park

   2. [HIGH]   Breakfast
      ⏰ ~08:30:00 (15min)
      📝 Feed Mochi breakfast

   3. [MEDIUM] Evening Walk
      ⏰ ~18:00:00 (45min)
      📝 Evening exercise at dog park


🐾 Whiskers's Schedule:
   --------------------------------------------------
   1. [HIGH]   Cat Meal
      ⏰ ~12:00:00 (10min)
      📝 Special diet meal for sensitive stomach

   2. [MEDIUM] Clean Litter Box
      ⏰ ~09:00:00 (10min)
      📝 Daily litter box cleaning

   3. [LOW]    Playtime
      ⏰ ~19:00:00 (20min)
      📝 Interactive play with laser pointer


============================================================
  📊 TASK SUMMARY 📊
============================================================

Total Tasks: 6
  ✅ Completed: 0
  ⏳ Incomplete: 6

By Priority:
  🔴 High: 3
  🟡 Medium: 2
  🟢 Low: 1

============================================================
  👤 OWNER SUMMARY 👤
============================================================

Jordan has 2 pet(s):
  • Mochi: 3 task(s)
  • Whiskers: 3 task(s)
============================================================

✨ Demo complete! All systems operational. ✨
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

The PawPal+ scheduler includes advanced features for intelligent task management and scheduling:

### **1. Task Sorting** 🔀

Tasks can be sorted by multiple criteria to help organize and prioritize work:

| Method | Behavior | Use Case |
|--------|----------|----------|
| `Scheduler.sort_by_time()` | Sorts tasks chronologically (earliest first) | Organize schedule chronologically |
| `Scheduler.sort_by_duration()` | Sorts tasks by duration (shortest first) | Find quick tasks to fit in gaps |
| `Scheduler.sort_by_priority_then_time()` | Multi-level sort: priority first, then time | Prioritize high-importance work first |

**Example:**
```python
# Sort all tasks by priority, then by scheduled time
prioritized = scheduler.sort_by_priority_then_time(all_tasks)
# Result: All HIGH priority tasks first, sorted by time; then MEDIUM; then LOW
```

---

### **2. Task Filtering** 🔍

Filter tasks by pet and completion status for targeted task management:

| Method | Behavior | Parameters |
|--------|----------|-----------|
| `Scheduler.filter_tasks()` | Advanced filtering by multiple criteria | `pet`, `status` ("all"/"completed"/"incomplete"), `priority` |
| `Scheduler.filter_by_pet_name()` | Get tasks for a specific pet by name | `owner`, `pet_name` (string), `status` |
| `Scheduler.filter_by_status()` | Quick filter by completion status only | `tasks`, `status` ("all"/"completed"/"incomplete") |

**Example:**
```python
# Get all incomplete tasks for Mochi
mochi_todo = scheduler.filter_by_pet_name(owner, "Mochi", status="incomplete")

# Get all completed tasks across all pets
done_tasks = scheduler.filter_by_status(owner.get_all_tasks(), "completed")
```

---

### **3. Conflict Detection** ⚠️

Intelligent conflict detection identifies scheduling problems and provides actionable suggestions:

| Method | Detects | Severity Levels |
|--------|---------|-----------------|
| `Scheduler.detect_conflicts()` | Time overlaps between tasks | Returns raw conflict tuples |
| `Scheduler.detect_conflicts_with_warnings()` | **CRITICAL**: Owner can't do both tasks at same time<br>**WARNING**: Same pet has overlapping tasks<br>**INFO**: No time buffer between tasks | 3-tier severity with suggestions |

**Conflict Types:**

- **🚨 CRITICAL**: Different pets scheduled at same time → owner physically can't do both
  - Example: Mochi's breakfast (8:30-8:45) + Whiskers' grooming (8:30-8:45)
  - Suggestion: Reschedule one task to a different time

- **⚠️ WARNING**: Same pet has overlapping tasks → pet can't do both
  - Example: Mochi's morning walk (8:00-8:30) + medication (8:20-8:30)
  - Suggestion: Reduce duration or reschedule one task

- **ℹ️ INFO**: Back-to-back tasks with no buffer → efficiency warning
  - Example: Task ends at 8:30, next task starts at 8:30 (no transition time)
  - Suggestion: Add 5-10 minute buffer between tasks

**Example:**
```python
# Detect all conflicts for today's schedule
conflicts = scheduler.detect_conflicts_with_warnings(owner, today)

for conflict in conflicts:
    print(f"[{conflict['severity']}] {conflict['message']}")
    print(f"  → {conflict['suggestion']}")
    # Output:
    # [CRITICAL] Owner can't do both tasks at 08:30!
    #   → Option 1: Reschedule 'Brush Whiskers' to 08:45 or later
```

---

### **4. Recurring Task Logic** ♻️

Automatically manage recurring tasks (daily, weekly, etc.) with smart regeneration:

| Method | Feature | Behavior |
|--------|---------|----------|
| `Scheduler.complete_recurring_task()` | Auto-regeneration | Mark task complete + create next occurrence |
| `Scheduler.expand_recurring_tasks()` | Schedule expansion | Expand DAILY/WEEKLY tasks across multiple days |

**Recurring Task Frequencies:**
- **ONCE**: Task appears once, no regeneration
- **DAILY**: Task recreates every day when marked complete
- **WEEKLY**: Task recreates every 7 days when marked complete
- **MONTHLY**: Task appears once per month (if requested window ≥ 30 days)

**Example 1: Daily Task Completion**
```python
# Mark morning walk complete - automatically creates tomorrow's walk
next_walk = scheduler.complete_recurring_task(mochi, morning_walk)

# Before: Mochi has 3 tasks
# After: Mochi has 4 tasks (original walk now ✅, new walk appears as ⏳)
```

**Example 2: Expanding Recurring Tasks**
```python
# Expand a week of tasks for schedule analysis
tasks = [
    Task("Morning Walk", 30, Priority.HIGH, frequency=Frequency.DAILY),
    Task("Vet Visit", 60, Priority.HIGH, frequency=Frequency.ONCE),
]

expanded = scheduler.expand_recurring_tasks(tasks, num_days=7)
# Result: 7 morning walks + 1 vet visit = 8 total tasks
```

---

### **How These Features Work Together**

```
┌─────────────────────────────────────────────────────────┐
│  User adds tasks with frequency (daily/weekly/once)    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Scheduler.expand_recurring_tasks()                     │
│  → Explodes daily tasks into full week schedule        │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Scheduler.detect_conflicts_with_warnings()             │
│  → Identifies overlaps, same-time conflicts, buffers   │
│  → Returns CRITICAL/WARNING/INFO with suggestions       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Scheduler.sort_by_priority_then_time()                 │
│  → Organizes tasks: HIGH priority first, then by time  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Scheduler.filter_by_pet_name() or filter_by_status()  │
│  → Display only relevant tasks (pet/completion status)  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  UI displays organized, conflict-free schedule         │
│  User marks task complete → auto-regenerates (if daily)│
└─────────────────────────────────────────────────────────┘
```

---

### **Testing the Scheduler**

Run the demo to see all features in action:

```bash
python3 main.py
```

The demo includes:
- ✅ Creating owners, pets, and tasks
- ✅ Sorting tasks (by time, duration, priority)
- ✅ Filtering tasks (by pet, status)
- ✅ Detecting scheduling conflicts with warnings
- ✅ Testing recurring task completion
- ✅ Expanding tasks across multiple days

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
