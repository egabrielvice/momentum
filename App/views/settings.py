import streamlit as st
from datetime import date

from database import *


def settings_page():
    st.header("Settings")

    st.subheader("Training Program Timeline")
    st.caption(
        "Choose the date your current training program began. Momentum calculates Week 1, Week 2, and the following weeks automatically."
    )

    current_start = get_setting("phase_start_date", str(date.today()))
    saved_start_date = date.fromisoformat(current_start)

    c1, c2 = st.columns(2)
    c1.metric("Current Week", f"Week {current_week()}")
    c2.metric("Saved Start Date", saved_start_date.strftime("%B %d, %Y"))

    start_date = st.date_input(
        "Program Start Date",
        value=saved_start_date,
        help="Select the real first day of your current training program.",
    )

    save_col, restart_col = st.columns(2)

    if save_col.button("Save Start Date", use_container_width=True):
        set_setting("phase_start_date", str(start_date))
        st.success(
            f"Program start date saved as {start_date.strftime('%B %d, %Y')}."
        )
        st.rerun()

    if restart_col.button("Restart at Week 1 Today", use_container_width=True):
        set_setting("phase_start_date", str(date.today()))
        st.success(
            "Your program now starts today at Week 1. Workout history and personal records were kept."
        )
        st.rerun()

    st.info(
        "Changing the start date does not delete workout history, exercise logs, or personal records."
    )

    st.divider()
    st.subheader("Access")
    if st.button("Log Out", key="settings_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.divider()
    st.subheader("Deployment / Data")
    st.code(f"Database: {get_database_path()}")
    st.code(f"Latest Backup: {get_latest_backup()}")

    if st.button("Create Database Backup", key="settings_create_backup"):
        backup_path = create_database_backup()
        if backup_path:
            st.success(f"Backup created: {backup_path}")
        else:
            st.error("No database file found yet.")

    st.divider()
    st.subheader("Workout History")

    session_count = int(fetch_df("SELECT COUNT(*) AS total FROM workout_sessions").iloc[0]["total"])
    log_count = int(fetch_df("SELECT COUNT(*) AS total FROM workout_logs").iloc[0]["total"])
    completion_count = int(fetch_df("SELECT COUNT(*) AS total FROM workout_completions").iloc[0]["total"])
    checkin_count = int(fetch_df("SELECT COUNT(*) AS total FROM daily_checkins").iloc[0]["total"])

    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Sessions", session_count)
    h2.metric("Exercise Logs", log_count)
    h3.metric("Completions", completion_count)
    h4.metric("Old Check-ins", checkin_count)

    st.warning(
        "Use this once to remove test history before beginning your real training record. "
        "Program templates, exercises, settings, and the saved program start date are preserved."
    )

    confirm_clear = st.checkbox(
        "I understand this permanently deletes workout sessions, exercise logs, completion history, and old daily check-ins.",
        key="confirm_clear_workout_history",
    )

    if st.button(
        "Clear Test & Workout History",
        key="clear_test_workout_history",
        type="primary",
        use_container_width=True,
    ):
        if confirm_clear:
            reset_test_data()
            st.success("Workout and test history cleared. Program templates and settings were kept.")
            st.rerun()
        else:
            st.error("Check the confirmation box before clearing history.")

    st.divider()
    st.subheader("Version")
    st.code("Momentum v1.0 - Training Intelligence System")
