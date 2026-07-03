# PawPal+ Project Reflection

## 1. System Design
- core actions: add a pet, schedule a walk, see today's tasks

**a. Initial design**

  1. Owner
Attributes: name, available_start_time, available_end_time (daily availability window)
Methods: get_available_hours(), get_availability_window()
Purpose: Represents the pet owner with time constraints for scheduling

1. Pet
Attributes: name, species (dog/cat/other), age, special_needs (list)
Methods: has_special_needs(), get_care_requirements()
Purpose: Represents the pet and its characteristics that affect care planning

1. Task
Attributes: title, duration_minutes, priority (low/medium/high), description
Methods: get_priority_value(), get_duration()
Purpose: Represents individual care tasks (e.g., "morning walk", "feeding", "playtime")


**b. Design changes**

Yes, the design evolved during the skeleton implementation to fix missing relationships and improve type safety:

1. **Added Priority Enum**
   - Changed: Task.priority from `str` ("low", "medium", "high") to `Priority` enum
   - Why: Type safety prevents misspellings (e.g., "hih" instead of "high"). Enum values can be compared directly without parsing strings. Single source of truth for priority definitions.

2. **Added Owner.pets list**
   - Changed: Owner now has `pets: List[Pet]` attribute and an `add_pet()` method
   - Why: Owners need to track their pets. Without this, you can't navigate from an owner to their pets. This models the real 1-to-many relationship where one owner can have multiple pets.

3. **Added Pet.tasks list**
   - Changed: Pet now has `tasks: List[Task]` attribute
   - Why: Pets need to know what care tasks they need. This enables quick lookup of all tasks for a pet during scheduling, and models the reality that each pet has specific care requirements.

4. **Added Pet.__post_init__() validation**
   - Changed: Pet dataclass now validates age >= 0 after initialization
   - Why: Prevents invalid data states (negative ages are nonsensical). Fails fast at object creation time with a clear error message, rather than causing mysterious bugs later.

5. **Added Scheduler class**
   - Changed: Created new Scheduler class with schedule_tasks() and prioritize_tasks() methods
   - Why: Separates scheduling logic from data models. Makes testing easier (test scheduling independently), improves reusability (same scheduler works with any owner/pet), and clarifies responsibilities (Scheduler owns the scheduling algorithm).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**c. Encapsulation: How Scheduler Retrieves Tasks**

A key design decision: **How should Scheduler access all tasks from an Owner's pets?**

Two main approaches:

1. **Option 1: Use Owner's Delegation Method (RECOMMENDED)**
   ```python
   all_tasks = owner.get_all_tasks()  # Owner handles the details
   ```
   - **Encapsulation**: Owner is responsible for its pets—Scheduler doesn't need to know HOW
   - **Single Responsibility**: Owner manages pet collection, Scheduler focuses on scheduling
   - **Maintainability**: If Owner's internal structure changes (e.g., pets stored in dict instead of list), only Owner needs updating
   - **Reusability**: `get_all_tasks()` available to any component that needs it
   - **Coupling**: Low coupling between Scheduler and Owner

2. **Option 2: Direct Iteration (NOT Recommended)**
   ```python
   all_tasks = []
   for pet in owner.pets:
       all_tasks.extend(pet.get_care_requirements())
   ```
   - **Problem**: Scheduler couples to Owner's internal structure (`owner.pets`)
   - **Problem**: Violates encapsulation—Scheduler knows too much about Owner
   - **Problem**: Duplicates logic already in `Owner.get_all_tasks()`
   - **Consequence**: If Owner changes how it stores pets, Scheduler must also change

**Why Option 1 is better**: It follows the **Delegation Pattern**—Owner says "I know my pets," Scheduler says "Owner, give me all tasks." This loose coupling makes the code more flexible and easier to maintain as the system grows.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
