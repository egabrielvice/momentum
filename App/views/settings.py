import streamlit as st
from datetime import date

from database import *


def settings_page():
    st.header("Settings")

    st.subheader("Access")
    if st.button("Log Out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.subheader("Deployment / Data")
    st.code(f"Database: {get_database_path()}")
    st.code(f"Latest Backup: {get_latest_backup()}")

    if st.button("Create Database Backup"):
        backup_path = create_database_backup()
        if backup_path:
            st.success(f"Backup created: {backup_path}")
        else:
            st.error("No database file found yet.")

    st.subheader("Phase Settings")
    current_start = get_setting("phase_start_date", str(date.today()))
    start_date = st.date_input(
        "Phase Start Date",
        value=date.fromisoformat(current_start),
    )

    if st.button("Save Phase Start Date"):
        set_setting("phase_start_date", str(start_date))
        st.success("Phase start date saved.")

    st.subheader("Reset Test Data")

    st.warning(
        "Deletes workout logs, check-ins, and completion history only. Keeps exercise templates."
    )

    confirm_reset = st.checkbox(
        "I understand this deletes logged test data only."
    )

    if st.button("Reset Test Data"):
        if confirm_reset:
            reset_test_data()
            st.success("Test data reset complete.")
        else:
            st.error("Check the confirmation box first.")

    st.subheader("Version")
    st.code("Momentum 6.9 - Training Intelligence Bundle")