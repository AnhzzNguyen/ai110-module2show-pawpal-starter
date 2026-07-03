import streamlit as st
import pandas as pd
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

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Owner", owner.name)
with col2:
    st.metric("Available Hours", f"{owner.get_available_hours():.1f}h")
with col3:
    st.metric("Time Window", f"{owner.available_start_time.strftime('%H:%M')}–{owner.available_end_time.strftime('%H:%M')}")

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

    # Create pets dataframe
    pets_data = []
    for pet in owner.pets:
        species_emoji = {"dog": "🐕", "cat": "🐱", "other": "🐾"}
        pets_data.append({
            "Pet Name": f"{species_emoji.get(pet.species, '🐾')} {pet.name}",
            "Species": pet.species.capitalize(),
            "Age": f"{pet.age} years",
            "Tasks": len(pet.tasks),
            "Special Needs": "✅ Yes" if pet.has_special_needs() else "—"
        })

    df_pets = pd.DataFrame(pets_data)
    st.dataframe(
        df_pets,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Pet Name": st.column_config.Column(width="medium"),
            "Species": st.column_config.Column(width="small"),
            "Age": st.column_config.Column(width="small"),
            "Tasks": st.column_config.Column(width="small"),
            "Special Needs": st.column_config.Column(width="small"),
        }
    )

    # Pet details in expanders
    for pet in owner.pets:
        species_emoji = {"dog": "🐕", "cat": "🐱", "other": "🐾"}
        with st.expander(f"{species_emoji.get(pet.species, '🐾')} **{pet.name}** — {len(pet.tasks)} task(s)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Species", pet.species.capitalize())
            with col2:
                st.metric("Age", f"{pet.age} years")
            with col3:
                st.metric("Tasks", len(pet.tasks))

            if pet.has_special_needs():
                st.warning("⚠️ **Special Needs:**")
                for need in pet.special_needs:
                    st.write(f"• {need}")
else:
    st.info("🐾 No pets yet. Add one above to get started!", icon="🐾")

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

    # Sorting options
    if filtered_tasks:
        col1, col2 = st.columns(2)
        with col1:
            sort_method = st.selectbox(
                "Sort by",
                ["Priority (High→Low)", "Time (Early→Late)", "Duration (Short→Long)"],
                key="sort_method_select"
            )

        # Apply selected sorting
        scheduler = st.session_state.scheduler
        if sort_method == "Priority (High→Low)":
            filtered_tasks = scheduler.sort_by_priority_then_time(filtered_tasks)
        elif sort_method == "Time (Early→Late)":
            filtered_tasks = scheduler.sort_by_time(filtered_tasks)
        elif sort_method == "Duration (Short→Long)":
            filtered_tasks = scheduler.sort_by_duration(filtered_tasks)

    # Display filtered tasks as professional dataframe
    if filtered_tasks:
        # Build task data for dataframe
        task_data = []
        for task in filtered_tasks:
            status_icon = "✅ Done" if task.is_completed else "⏳ Todo"
            priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            freq_emoji = {"ONCE": "1️⃣", "DAILY": "📅", "WEEKLY": "📆", "MONTHLY": "🗓️"}

            task_data.append({
                "Status": status_icon,
                "Title": task.title,
                "Duration": f"{task.duration_minutes} min",
                "Priority": f"{priority_emoji.get(task.priority.name, '')} {task.priority.name}",
                "Frequency": freq_emoji.get(task.frequency.name, ""),
                "Description": task.description or "—"
            })

        # Display as dataframe
        df_tasks = pd.DataFrame(task_data)
        st.dataframe(
            df_tasks,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.Column(width="medium"),
                "Title": st.column_config.Column(width="large"),
                "Duration": st.column_config.Column(width="small"),
                "Priority": st.column_config.Column(width="medium"),
                "Frequency": st.column_config.Column(width="small"),
                "Description": st.column_config.Column(width="large"),
            }
        )

        # Task statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            completed = sum(1 for t in filtered_tasks if t.is_completed)
            st.metric("Completed", completed, delta=f"{completed}/{len(filtered_tasks)}")
        with col2:
            total_duration = sum(t.duration_minutes for t in filtered_tasks)
            st.metric("Total Duration", f"{total_duration} min", delta=f"{total_duration//60}h {total_duration%60}m")
        with col3:
            high_priority = sum(1 for t in filtered_tasks if t.priority == Priority.HIGH)
            st.metric("High Priority", high_priority)
        with col4:
            recurring = sum(1 for t in filtered_tasks if t.frequency != Frequency.ONCE)
            st.metric("Recurring", recurring)
    else:
        st.info("📭 No tasks match the selected filters.")

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

        # ========== CONFLICT DETECTION ==========
        conflicts = scheduler.detect_conflicts_with_warnings(owner, today)

        if conflicts:
            st.divider()

            # Separate by severity
            critical = [c for c in conflicts if c["severity"] == "critical"]
            warnings = [c for c in conflicts if c["severity"] == "warning"]
            info_alerts = [c for c in conflicts if c["severity"] == "info"]

            # Summary pills
            col1, col2, col3 = st.columns(3)
            with col1:
                if critical:
                    st.error(f"🚨 **{len(critical)} Critical**", icon="🚨")
                else:
                    st.write("")
            with col2:
                if warnings:
                    st.warning(f"⚠️ **{len(warnings)} Warning(s)**", icon="⚠️")
                else:
                    st.write("")
            with col3:
                if info_alerts:
                    st.info(f"ℹ️ **{len(info_alerts)} Tip(s)**", icon="ℹ️")
                else:
                    st.write("")

            st.subheader("⚠️ Schedule Alerts")

            # Display critical conflicts
            if critical:
                st.error("🚨 **CRITICAL CONFLICTS** — Owner cannot do both tasks at the same time", icon="🚨")
                for i, conflict in enumerate(critical, 1):
                    with st.container(border=True):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"**Conflict #{i}**")
                            st.write(f"🐾 {conflict['pet1_name']} ↔️ {conflict['pet2_name']}")
                        with col2:
                            st.write(conflict["message"])
                        st.info(f"💡 **Suggestion:** {conflict['suggestion']}")

            # Display warnings
            if warnings:
                st.warning("⚠️ **WARNINGS** — Same pet has overlapping tasks", icon="⚠️")
                for i, conflict in enumerate(warnings, 1):
                    with st.container(border=True):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"**Warning #{i}**")
                            st.write(f"🐾 {conflict['pet1_name']}'s schedule")
                        with col2:
                            st.write(conflict["message"])
                        st.info(f"💡 **Suggestion:** {conflict['suggestion']}")

            # Display info alerts
            if info_alerts:
                st.info("ℹ️ **EFFICIENCY TIPS** — No time buffer between tasks", icon="ℹ️")
                for i, conflict in enumerate(info_alerts, 1):
                    with st.container(border=True):
                        st.caption(f"**Tip #{i}:** {conflict['message']}")
                        st.caption(f"💡 {conflict['suggestion']}")
        else:
            st.success("✅ **Perfect!** No scheduling conflicts detected!", icon="✅")

        st.divider()

        # ========== DAILY SCHEDULE BY PET ==========
        st.subheader("📅 Daily Schedule")

        for pet_name, tasks in daily_schedule.items():
            with st.expander(f"🐾 **{pet_name}** — {len(tasks)} task(s) scheduled"):
                if tasks:
                    # Create schedule dataframe
                    schedule_data = []
                    for i, task in enumerate(tasks, 1):
                        priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
                        time_str = f"🕐 {task.scheduled_time.strftime('%H:%M')}" if task.scheduled_time else "⏰ Unscheduled"

                        schedule_data.append({
                            "#": i,
                            "Time": time_str,
                            "Task": task.title,
                            "Priority": f"{priority_emoji.get(task.priority.name, '')} {task.priority.name}",
                            "Duration": f"{task.duration_minutes} min",
                            "Notes": task.description or "—"
                        })

                    df_schedule = pd.DataFrame(schedule_data)
                    st.dataframe(
                        df_schedule,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "#": st.column_config.Column(width="small"),
                            "Time": st.column_config.Column(width="small"),
                            "Task": st.column_config.Column(width="large"),
                            "Priority": st.column_config.Column(width="medium"),
                            "Duration": st.column_config.Column(width="small"),
                            "Notes": st.column_config.Column(width="large"),
                        }
                    )

                    # Pet-specific stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_time = sum(t.duration_minutes for t in tasks)
                        st.metric(f"Total Time", f"{total_time} min")
                    with col2:
                        high_pri = sum(1 for t in tasks if t.priority == Priority.HIGH)
                        st.metric(f"High Priority", high_pri)
                    with col3:
                        avg_duration = total_time // len(tasks) if tasks else 0
                        st.metric(f"Avg Task Length", f"{avg_duration} min")
                else:
                    st.warning(f"⏳ No tasks fit in the available time for {pet_name}.", icon="⏳")

        # ========== TASK SUMMARY ==========
        st.divider()
        st.subheader("📊 Task Summary & Statistics")

        summary = scheduler.get_task_summary(owner)

        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Tasks",
                summary["total_tasks"],
                delta=f"{summary['completed_tasks']} completed",
                delta_color="normal"
            )
        with col2:
            st.metric(
                "📝 To-Do",
                summary["incomplete_tasks"],
                delta=f"{(summary['incomplete_tasks']/summary['total_tasks']*100):.0f}%" if summary["total_tasks"] > 0 else "—",
                delta_color="inverse"
            )
        with col3:
            st.metric(
                "🔴 High Priority",
                summary["high_priority"],
                delta=f"{(summary['high_priority']/summary['total_tasks']*100):.0f}%" if summary["total_tasks"] > 0 else "—"
            )
        with col4:
            st.metric(
                "⏰ Hours Available",
                f"{owner.get_available_hours():.1f}h",
                delta=f"{owner.available_start_time}–{owner.available_end_time}",
                delta_color="off"
            )

        # Priority breakdown table
        st.subheader("Priority Breakdown")
        priority_data = {
            "Priority Level": ["🔴 High", "🟡 Medium", "🟢 Low"],
            "Count": [summary["high_priority"], summary["medium_priority"], summary["low_priority"]],
            "Percentage": [
                f"{(summary['high_priority']/summary['total_tasks']*100):.1f}%" if summary["total_tasks"] > 0 else "0%",
                f"{(summary['medium_priority']/summary['total_tasks']*100):.1f}%" if summary["total_tasks"] > 0 else "0%",
                f"{(summary['low_priority']/summary['total_tasks']*100):.1f}%" if summary["total_tasks"] > 0 else "0%"
            ]
        }
        df_priority = pd.DataFrame(priority_data)
        st.dataframe(
            df_priority,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority Level": st.column_config.Column(width="medium"),
                "Count": st.column_config.Column(width="small"),
                "Percentage": st.column_config.Column(width="small"),
            }
        )

        # Completion progress
        st.subheader("Completion Progress")
        if summary["total_tasks"] > 0:
            progress = summary["completed_tasks"] / summary["total_tasks"]
            st.progress(progress, text=f"{summary['completed_tasks']}/{summary['total_tasks']} ({progress*100:.0f}%)")
        else:
            st.info("No tasks yet. Add some tasks to get started!", icon="🐾")
