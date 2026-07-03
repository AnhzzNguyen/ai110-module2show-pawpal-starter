import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler, Priority, Frequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# Initialize session state (persistent storage)
def init_session_state():
    """Initialize all session state objects on first load."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Jordan")
    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler()

init_session_state()

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+—a pet care planning assistant that helps you manage your pets' daily tasks.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# ============================================================================
# OWNER SETUP
# ============================================================================
st.divider()
st.header("👤 Owner Info")

owner = st.session_state.owner

col1, col2 = st.columns(2)
with col1:
    new_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
    if new_name != owner.name:
        owner.name = new_name

with col2:
    owner.available_start_time = st.time_input("Available from", value=owner.available_start_time, key="start_time")
    owner.available_end_time = st.time_input("Available until", value=owner.available_end_time, key="end_time")

st.info(f"✓ {owner.name} has {owner.get_available_hours():.1f} hours available per day")

# ============================================================================
# PET MANAGEMENT
# ============================================================================
st.divider()
st.header("🐾 Pets")

st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species_select")
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=50, value=3, key="age_input")

if st.button("Add pet", key="add_pet_btn"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(new_pet)
    st.success(f"✓ Added {pet_name} the {species}")
    st.rerun()

# Display current pets
if owner.pets:
    st.subheader("Your Pets")
    for idx, pet in enumerate(owner.pets):
        with st.expander(f"🐾 {pet.name} ({pet.species}, {pet.age} years)"):
            st.write(f"**Species:** {pet.species}")
            st.write(f"**Age:** {pet.age} years")
            st.write(f"**Tasks:** {len(pet.tasks)}")
else:
    st.info("No pets yet. Add one above!")

# ============================================================================
# TASK MANAGEMENT
# ============================================================================
st.divider()
st.header("📋 Care Tasks")

if not owner.pets:
    st.warning("Add a pet first to start creating tasks.")
else:
    st.subheader("Add a Task")

    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox(
            "Task for which pet?",
            options=[p.name for p in owner.pets],
            key="task_pet_select"
        )

    with col2:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title_input")

    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30, key="duration_input")
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority_select")
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"], index=1, key="frequency_select")

    task_description = st.text_area("Description (optional)", key="task_desc_input")

    if st.button("Add task", key="add_task_btn"):
        # Find the selected pet
        pet = next((p for p in owner.pets if p.name == selected_pet), None)
        if pet:
            priority_enum = Priority[priority.upper()]
            frequency_enum = Frequency[frequency.upper()]
            new_task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority_enum,
                description=task_description,
                frequency=frequency_enum
            )
            pet.add_task(new_task)
            st.success(f"✓ Added '{task_title}' for {pet.name}")
            st.rerun()

    # Display all tasks with filtering
    st.subheader("View & Filter Tasks")

    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox(
            "Filter by pet",
            options=["All Pets"] + [p.name for p in owner.pets],
            key="filter_pet_select"
        )

    with col2:
        filter_status = st.selectbox(
            "Filter by status",
            options=["All", "Incomplete", "Completed"],
            key="filter_status_select"
        )

    # Apply filters
    scheduler = st.session_state.scheduler
    all_tasks = owner.get_all_tasks()

    if filter_pet != "All Pets":
        # Filter by pet name
        status_map = {"All": "all", "Incomplete": "incomplete", "Completed": "completed"}
        filtered_tasks = scheduler.filter_by_pet_name(owner, filter_pet, status_map[filter_status])
    else:
        # Filter by status only (all pets)
        status_map = {"All": "all", "Incomplete": "incomplete", "Completed": "completed"}
        filtered_tasks = scheduler.filter_by_status(all_tasks, status_map[filter_status])

    # Display filtered tasks
    if filtered_tasks:
        st.write(f"**Found {len(filtered_tasks)} task(s)**")
        for task in filtered_tasks:
            col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])
            with col1:
                status_icon = "✅" if task.is_completed else "⏳"
                st.write(status_icon)
            with col2:
                st.write(f"**{task.title}**")
                if task.description:
                    st.caption(task.description)
            with col3:
                st.caption(f"⏱️ {task.duration_minutes}min")
            with col4:
                priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
                st.caption(f"{priority_emoji.get(task.priority.name, '')} {task.priority.name}")
    else:
        st.info("No tasks match the selected filters.")

# ============================================================================
# SCHEDULING
# ============================================================================
st.divider()
st.header("📅 Daily Schedule")

all_tasks = owner.get_all_tasks()

if not all_tasks:
    st.warning("Add some tasks to generate a schedule.")
else:
    if st.button("Generate schedule", key="generate_schedule_btn"):
        scheduler = st.session_state.scheduler
        today = datetime.today()
        daily_schedule = scheduler.get_daily_schedule(owner, today)

        st.subheader(f"Schedule for {today.strftime('%A, %B %d, %Y')}")

        for pet_name, tasks in daily_schedule.items():
            with st.expander(f"🐾 {pet_name}'s Schedule"):
                if tasks:
                    for i, task in enumerate(tasks, 1):
                        priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
                        st.write(
                            f"{i}. [{priority_emoji.get(task.priority.name, '')} {task.priority.name}] "
                            f"**{task.title}** ({task.duration_minutes} min)"
                        )
                        if task.description:
                            st.caption(task.description)
                else:
                    st.info("No tasks fit in the available time.")

        # Show summary
        st.divider()
        summary = scheduler.get_task_summary(owner)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", summary["total_tasks"])
        with col2:
            st.metric("Scheduled", summary["total_tasks"] - summary["incomplete_tasks"])
        with col3:
            st.metric("Hours Available", f"{owner.get_available_hours():.1f}h")
