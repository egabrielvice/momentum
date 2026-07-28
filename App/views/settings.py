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
    if st.button("Log Out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.divider()
    st.subheader("Deployment / Data")
    st.code(f"Database: {get_database_path()}")
    st.code(f"Latest Backup: {get_latest_backup()}")

    if st.button("Create Database Backup"):
        backup_path = create_database_backup()
        if backup_path:
            st.success(f"Backup created: {backup_path}")
        else:
            st.error("No database file found yet.")

    st.divider()
    st.subheader("Version")
    st.code("Momentum 6.9 - Training Intelligence Bundle")
