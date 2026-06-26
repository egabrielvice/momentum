import streamlit as st
from datetime import date

from database import *
from utils.helpers import *


def workout_page():
    st.header("Workout Log")

    logs = fetch_df("""
        SELECT wl.id, wl.log_date, e.day, e.workout_name, e.exercise_name, e.muscle_group, wl.weight, wl.reps, wl.rir, wl.notes
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        ORDER BY wl.id DESC
    """)

    if logs.empty:
        st.info("No workouts logged yet.")
    else:
        st.dataframe(logs, use_container_width=True)

        st.subheader("Edit or Delete Log")

        log_id = st.selectbox(
            "Select Log ID",
            logs["id"].tolist(),
            format_func=lambda x: f"ID {x} — {logs.loc[logs['id'] == x, 'exercise_name'].iloc[0]} — {logs.loc[logs['id'] == x, 'log_date'].iloc[0]}",
            key="workout_log_select_id",
        )

        selected = logs[logs["id"] == log_id].iloc[0]

        with st.form("edit_workout_log_form"):
            edit_date = st.date_input(
                "Log Date",
                value=date.fromisoformat(str(selected["log_date"])),
            )

            edit_weight = st.number_input(
                "Weight / Load",
                min_value=0.0,
                step=2.5,
                value=float(selected["weight"] or 0),
            )

            edit_reps = st.text_input(
                "Reps / Time / Steps",
                value=str(selected["reps"]),
            )

            edit_rir = st.slider(
                "RIR",
                0.0,
                5.0,
                float(selected["rir"] if selected["rir"] is not None else 2.0),
                0.5,
            )

            edit_notes = st.text_area(
                "Notes",
                value="" if selected["notes"] is None else str(selected["notes"]),
            )

            save_edit = st.form_submit_button("Save Changes")

            if save_edit:
                if edit_reps.strip():
                    update_workout_log(
                        log_id,
                        str(edit_date),
                        edit_weight,
                        edit_reps,
                        edit_rir,
                        edit_notes,
                    )
                    st.success("Workout log updated. Refresh to see changes.")
                else:
                    st.error("Reps/time/steps cannot be blank.")

        st.warning("Delete is permanent for this selected log only.")

        confirm_delete = st.checkbox(
            "I understand this will delete the selected workout log only.",
            key="confirm_delete_workout_log",
        )

        if st.button("Delete Selected Log", key="delete_selected_workout_log"):
            if confirm_delete:
                delete_workout_log(log_id)
                st.success("Workout log deleted. Refresh to update the table.")
            else:
                st.error("Check the confirmation box before deleting.")