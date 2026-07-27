import streamlit as st
from datetime import date

from database import (
    fetch_df,
    save_bodyweight_entry,
    clear_bodyweight_entry,
)


def bodyweight_page():
    st.header("Bodyweight Log")
    st.caption("Use this page to add, edit, or clear bodyweight entries by date.")

    c1, c2 = st.columns(2)

    entry_date = c1.date_input(
        "Date",
        value=date.today(),
    )

    entry_weight = c2.number_input(
        "Body Weight",
        min_value=0.0,
        step=0.5,
    )

    if st.button("Save Bodyweight Entry"):
        save_bodyweight_entry(
            str(entry_date),
            entry_weight,
        )
        st.success("Bodyweight entry saved.")

    weight_logs = fetch_df(
        """
        SELECT checkin_date, body_weight
        FROM daily_checkins
        WHERE body_weight IS NOT NULL
          AND body_weight > 0
        ORDER BY checkin_date DESC
        """
    )

    if weight_logs.empty:
        st.info("No bodyweight entries yet.")

    else:
        st.subheader("Bodyweight History")

        st.dataframe(
            weight_logs,
            use_container_width=True,
        )

        clear_date = st.selectbox(
            "Clear entry for date",
            weight_logs["checkin_date"].tolist(),
        )

        if st.button("Clear Selected Bodyweight Entry"):
            clear_bodyweight_entry(clear_date)
            st.success(
                "Selected bodyweight entry cleared. Refresh to update the table."
            )