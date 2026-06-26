import streamlit as st
import pandas as pd

from database import *
from utils.helpers import *


def analytics_page():
    st.header("Analytics")
    st.caption("Training patterns, exercise frequency, and muscle-group logging summary.")

    summary = get_program_count_summary()
    if not summary.empty:
        a, b, c = st.columns(3)
        a.metric("Active Programs", int(summary["active_programs"].iloc[0] or 0))
        b.metric("Archived Programs", int(summary["archived_programs"].iloc[0] or 0))
        c.metric("Total Programs", int(summary["total_programs"].iloc[0] or 0))

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Workout Frequency</div>', unsafe_allow_html=True)

    weekly = get_weekly_workout_summary()

    if weekly.empty:
        st.info("No completed workout data yet.")
    else:
        weekly["completion_date"] = weekly["completion_date"].astype(str)
        st.line_chart(weekly.set_index("completion_date")["completed_workouts"])
        st.dataframe(weekly, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Training Time Insights</div>', unsafe_allow_html=True)

    sessions = fetch_df("""
        SELECT session_date, day, workout_name, started_at, ended_at,
               duration_minutes, exercise_count, set_count, total_volume, notes
        FROM workout_sessions
        WHERE ended_at IS NOT NULL
          AND duration_minutes IS NOT NULL
        ORDER BY started_at ASC
    """)

    if sessions.empty:
        render_empty_state("No timed workout sessions yet. Finish a workout with the Gym Session timer to unlock duration analytics.")
    else:
        sessions["session_date"] = sessions["session_date"].astype(str)
        sessions["duration_minutes"] = sessions["duration_minutes"].fillna(0).astype(float)
        sessions["total_volume"] = sessions["total_volume"].fillna(0).astype(float)

        avg_duration = sessions["duration_minutes"].mean()
        longest_duration = sessions["duration_minutes"].max()
        shortest_duration = sessions["duration_minutes"].min()
        total_hours = sessions["duration_minutes"].sum() / 60
        avg_volume = sessions["total_volume"].mean()
        best_volume = sessions["total_volume"].max()

        st.markdown(
            f"""
            <div class="momentum-insight-grid">
                <div class="momentum-insight-card">
                    <div class="momentum-insight-label">Average Workout</div>
                    <div class="momentum-insight-value">{duration_label(avg_duration)}</div>
                    <div class="momentum-insight-sub">Across {len(sessions)} timed sessions</div>
                </div>
                <div class="momentum-insight-card">
                    <div class="momentum-insight-label">Longest Session</div>
                    <div class="momentum-insight-value">{duration_label(longest_duration)}</div>
                    <div class="momentum-insight-sub">Shortest: {duration_label(shortest_duration)}</div>
                </div>
                <div class="momentum-insight-card">
                    <div class="momentum-insight-label">Total Gym Time</div>
                    <div class="momentum-insight-value">{total_hours:.1f}h</div>
                    <div class="momentum-insight-sub">Logged by completed sessions</div>
                </div>
                <div class="momentum-insight-card">
                    <div class="momentum-insight-label">Average Volume</div>
                    <div class="momentum-insight-value">{avg_volume:,.0f}</div>
                    <div class="momentum-insight-sub">Per timed session</div>
                </div>
                <div class="momentum-insight-card">
                    <div class="momentum-insight-label">Best Volume</div>
                    <div class="momentum-insight-value">{best_volume:,.0f}</div>
                    <div class="momentum-insight-sub">Highest completed session</div>
                </div>
                <div class="momentum-insight-card">
                    <div class="momentum-insight-label">Session Count</div>
                    <div class="momentum-insight-value">{len(sessions)}</div>
                    <div class="momentum-insight-sub">Timed workouts completed</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        chart_data = sessions[["session_date", "duration_minutes", "total_volume"]].copy()
        chart_data = chart_data.set_index("session_date")

        st.subheader("Workout Duration Trend")
        st.line_chart(chart_data["duration_minutes"])

        if chart_data["total_volume"].sum() > 0:
            st.subheader("Session Volume Trend")
            st.line_chart(chart_data["total_volume"])

        weekly_sessions = sessions.copy()
        weekly_sessions["week"] = pd.to_datetime(
            weekly_sessions["session_date"],
            errors="coerce"
        ).dt.to_period("W").astype(str)

        weekly_summary = weekly_sessions.groupby("week", as_index=False)["duration_minutes"].sum()
        weekly_summary["gym_hours"] = (weekly_summary["duration_minutes"] / 60).round(2)

        monthly_sessions = sessions.copy()
        monthly_sessions["month"] = pd.to_datetime(
            monthly_sessions["session_date"],
            errors="coerce"
        ).dt.to_period("M").astype(str)

        monthly_summary = monthly_sessions.groupby("month", as_index=False)["duration_minutes"].sum()
        monthly_summary["gym_hours"] = (monthly_summary["duration_minutes"] / 60).round(2)

        wcol, mcol = st.columns(2)

        with wcol:
            st.subheader("Weekly Gym Hours")
            st.dataframe(
                weekly_summary[["week", "gym_hours"]].sort_values("week", ascending=False),
                use_container_width=True,
            )

        with mcol:
            st.subheader("Monthly Gym Hours")
            st.dataframe(
                monthly_summary[["month", "gym_hours"]].sort_values("month", ascending=False),
                use_container_width=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Workout Session History</div>', unsafe_allow_html=True)

    recent_sessions = get_recent_workout_sessions(25)

    if recent_sessions.empty:
        render_empty_state("No timed workout sessions yet.")
    else:
        st.dataframe(recent_sessions, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Exercise Frequency</div>', unsafe_allow_html=True)

        frequency = get_exercise_frequency()

        if frequency.empty:
            st.info("No exercise logs yet.")
        else:
            st.dataframe(frequency, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Muscle Group Log Summary</div>', unsafe_allow_html=True)

        muscle_summary = get_muscle_volume_summary()

        if muscle_summary.empty:
            st.info("No muscle-group data yet.")
        else:
            st.dataframe(muscle_summary, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)