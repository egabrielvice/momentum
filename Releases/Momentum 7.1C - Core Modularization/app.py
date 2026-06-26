
import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
from database import *

st.set_page_config(page_title="Momentum 6.9", page_icon="🏋️", layout="wide", initial_sidebar_state="collapsed")
init_db()


from utils.auth import require_password

from styles.theme import apply_theme

apply_theme()

# st.title("Momentum v2.1")  # Hidden for premium dashboard layout
require_password()
st.caption("Training intelligence for progressive overload.")

st.sidebar.markdown(
    """
    <div class="m55-sidebar-brand">
        <div class="m55-brand-mark">Momentum</div>
        <div class="m55-brand-sub">Built for consistency</div>
    </div>
    """,
    unsafe_allow_html=True,
)

NAV_OPTIONS = [
    "Dashboard",
    "Today's Workout",
    "Workout Journal",
    "Exercise Intelligence",
    "Training Calendar",
    "Progress Center",
    "Progress Hub",
    "Analytics",
    "Workout Log",
    "Exercise History",
    "Bodyweight Log",
    "Program Manager",
    "Program Editor",
    "Export / Backup",
    "Settings",
]

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Dashboard"

page = st.sidebar.radio(
    "Navigation",
    NAV_OPTIONS,
    key="nav_page",
)

from utils.helpers import *

week = current_week()
phase = get_phase(week)
next_workout = get_next_workout()

if page == "Dashboard":
    programs = get_programs()
    active_program_id = get_active_program_id()
    active_program = programs[programs["id"] == active_program_id].iloc[0] if not programs.empty else None

    score, score_details = calculate_momentum_score()
    recovery_status = get_today_recovery().title()
    weeks_left = max(0, 12 - week)
    completed_workouts = len(fetch_df("SELECT * FROM workout_completions"))

    st.markdown('<div class="momentum-logo">Momentum</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="m5-hero">
            <h1>{dynamic_greeting()}</h1>
            <div class="m5-hero-sub">Training intelligence for progressive overload, consistency, and execution.</div>
            <div class="m5-pill-row">
                <span class="m5-pill">{str(date.today())}</span>
                <span class="m5-pill m5-pill-red">Week {week} of 12</span>
                <span class="m5-pill">{weeks_left} weeks left</span>
                <span class="m5-pill m5-pill-red">Momentum {score}/100</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    timeline_html = ""
    for i in range(1, 13):
        if i < week:
            timeline_html += f'<div class="m5-week-chip done">W{i}<br>✓</div>'
        elif i == week:
            timeline_html += f'<div class="m5-week-chip current">W{i}<br>●</div>'
        else:
            timeline_html += f'<div class="m5-week-chip">W{i}<br>&nbsp;</div>'

    st.markdown(
        f"""
        <div class="m5-timeline">
            <div class="m5-eyebrow">12 Week Timeline</div>
            <div class="m5-timeline-grid">{timeline_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Week", f"{week}/12")
    m2.metric("Recovery", recovery_status)
    m3.metric("Momentum", f"{score}/100")
    m4.metric("Weeks Left", weeks_left)

    left, right = st.columns([1.05, 1])

    with left:
        upcoming_exercises = (
            get_exercises(next_workout["day"])
            if next_workout["day"] != "No Day"
            else fetch_df("SELECT * FROM exercises WHERE 1=0")
        )

        exercise_rows = ""
        if not upcoming_exercises.empty:
            for _, row in upcoming_exercises.head(7).iterrows():
                exercise_rows += (
                    f'<div class="m5-exercise-row">'
                    f'<span class="m5-exercise-name">{row["exercise_name"]}</span>'
                    f'<span class="m5-exercise-target">{row["target_sets"]}×{row["min_reps"]}–{row["max_reps"]}</span>'
                    f'</div>'
                )

        if upcoming_exercises.empty:
            exercise_rows = '<div class="m5-muted">No exercises yet. Add exercises in Program Manager.</div>'

        st.markdown(
            f"""
            <div class="m5-workout-card">
                <div class="m5-eyebrow">Today's Priority</div>
                <div class="m5-main">{next_workout["day"]} — {next_workout["workout_name"]}</div>
                <div class="m5-muted">Your next workout is ready. Log each exercise from Today’s Workout.</div>
                <div class="m5-exercise-list">
                    {exercise_rows}
                </div>
                <div class="m5-action">Start Today’s Workout</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="m5-card m5-recovery-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Recovery Overview</div>', unsafe_allow_html=True)

        today_checkin = get_today_checkin()

        if today_checkin is None:
            st.info("No check-in yet today.")
        else:
            sleep_value = float(today_checkin["sleep_hours"] or 0)
            energy_value = float(today_checkin["energy"] or 0)
            stress_value = float(today_checkin["stress"] or 0)

            st.write(f"**Sleep:** {sleep_value:g} / 8 h")
            st.progress(min(sleep_value / 8, 1.0), text=f"{sleep_value:g} hours logged")

            st.write(f"**Energy:** {energy_value:g} / 5")
            st.progress(min(energy_value / 5, 1.0), text=f"{energy_value:g} out of 5")

            st.write(f"**Stress:** {stress_value:g} / 5")
            st.progress(min(stress_value / 5, 1.0), text=f"{stress_value:g} out of 5")

            hydration_label = "Good" if int(today_checkin["water_hit"] or 0) else "Missing"
            nutrition_label = "Good" if int(today_checkin["protein_hit"] or 0) else "Missing"

            st.write(f"**Hydration:** {hydration_label}")
            st.write(f"**Nutrition:** {nutrition_label}")

        st.markdown('<div class="m5-muted">Recovery determines execution quality.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Log Daily Check-In", expanded=False):
        c1, c2 = st.columns(2)

        body_weight = c1.number_input("Body Weight", min_value=0.0, step=0.5)
        sleep_hours = c1.number_input("Sleep Hours", min_value=0.0, max_value=24.0, step=0.5)
        energy = c2.slider("Energy", 1, 5, 3)
        stress = c2.slider("Stress", 1, 5, 3)

        c3, c4, c5 = st.columns(3)
        protein_hit = c3.checkbox("Protein Hit")
        water_hit = c4.checkbox("Water Hit")
        steps_hit = c5.checkbox("Steps Hit")

        if st.button("Save Daily Check-In"):
            save_checkin(
                str(date.today()),
                body_weight,
                sleep_hours,
                energy,
                stress,
                int(protein_hit),
                int(water_hit),
                int(steps_hit),
            )
            st.success("Daily check-in saved.")

    row1_left, row1_right = st.columns(2)

    with row1_left:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Bodyweight Trend</div>', unsafe_allow_html=True)

        weight_logs = fetch_df("""
            SELECT checkin_date, body_weight
            FROM daily_checkins
            WHERE body_weight IS NOT NULL AND body_weight > 0
            ORDER BY checkin_date ASC
        """)

        if weight_logs.empty:
            st.info("No bodyweight data yet.")
        else:
            weight_logs["checkin_date"] = weight_logs["checkin_date"].astype(str)

            current_weight = round(weight_logs["body_weight"].iloc[-1], 1)
            avg_7 = round(weight_logs["body_weight"].tail(7).mean(), 1)
            change = (
                round(weight_logs["body_weight"].iloc[-1] - weight_logs["body_weight"].iloc[0], 1)
                if len(weight_logs) >= 2
                else 0
            )

            w1, w2, w3 = st.columns(3)
            w1.metric("Current", current_weight)
            w2.metric("7-Day Avg", avg_7)
            w3.metric("Trend", f"{change:+.1f}")

            st.line_chart(weight_logs.set_index("checkin_date")["body_weight"])

        st.markdown("</div>", unsafe_allow_html=True)

    with row1_right:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Momentum Score</div>', unsafe_allow_html=True)

        st.metric("Today", f"{score}/100", "Consistency")

        with st.expander("Score Breakdown"):
            for item in score_details:
                st.write(item)

        st.markdown('<div class="m5-muted">Consistency compounds quietly.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    row2_left, row2_right = st.columns([0.9, 1.35])

    with row2_left:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Recent Workouts</div>', unsafe_allow_html=True)

        recent = get_recent_workouts(5)

        if recent.empty:
            st.info("No completed workouts yet.")
        else:
            for _, row in recent.iterrows():
                st.write(f"**{row['day']} — {row['workout_name']}**")
                st.caption(row["completion_date"])

        st.markdown("</div>", unsafe_allow_html=True)

    with row2_right:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Personal Records</div>', unsafe_allow_html=True)

        prs = get_personal_records()

        if prs.empty:
            st.info("No personal records yet.")
        else:
            st.dataframe(prs.head(6), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="quote-card">
            “Discipline today. Freedom tomorrow.”
        </div>
        """,
        unsafe_allow_html=True,
    )

elif page == "Today's Workout":
    st.header("Today's Workout")
    st.caption("A cleaner training screen for logging sessions with less visual clutter.")

    days = get_workout_days()

    if days.empty:
        st.warning("No workout days exist for the active program yet. Go to Program Manager to create days and exercises.")
        st.stop()

    day_options = [f"{row.day} — {row.workout_name}" for _, row in days.iterrows()]
    next_label = f"{next_workout['day']} — {next_workout['workout_name']}"
    default_index = day_options.index(next_label) if next_label in day_options else 0

    selected_label = st.selectbox("Workout", day_options, index=default_index)
    selected_day = selected_label.split(" — ")[0]
    selected_row = days[days["day"] == selected_day].iloc[0]

    st.markdown(
        f"""
        <div class="m55-card">
            <div class="m55-title">Current Session</div>
            <div class="m55-headline">{selected_row['day']} — {selected_row['workout_name']}</div>
            <div class="m55-muted">Week {week}/12 · {phase} · Recommended: {next_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_session = get_active_workout_session()
    active_session_id = int(active_session["id"]) if active_session else None

    if st.session_state.pop("auto_start_workout_from_dashboard", False) and active_session is None:
        start_workout_session(selected_row["day"], int(selected_row["day_order"]), selected_row["workout_name"])
        st.session_state["session_paused"] = False
        st.session_state["session_paused_seconds"] = 0.0
        st.session_state["session_pause_started_at"] = None
        st.session_state["momentum_last_set_saved_at"] = None
        st.rerun()

    if "session_paused" not in st.session_state:
        st.session_state["session_paused"] = False
    if "session_paused_seconds" not in st.session_state:
        st.session_state["session_paused_seconds"] = 0.0
    if "session_pause_started_at" not in st.session_state:
        st.session_state["session_pause_started_at"] = None

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Gym Session</div>', unsafe_allow_html=True)

    if active_session:
        paused_seconds = float(st.session_state.get("session_paused_seconds", 0.0) or 0.0)
        if st.session_state.get("session_paused") and st.session_state.get("session_pause_started_at"):
            try:
                paused_seconds += (datetime.now() - datetime.fromisoformat(st.session_state["session_pause_started_at"])).total_seconds()
            except Exception:
                pass

        elapsed_label = format_elapsed_since(active_session["started_at"], paused_seconds)
        st.markdown('<div class="m55-headline">Workout Active</div>', unsafe_allow_html=True)
        render_live_timer_component(
            active_session["started_at"],
            paused_seconds=float(st.session_state.get("session_paused_seconds", 0.0) or 0.0),
            paused=bool(st.session_state.get("session_paused")),
            pause_started_at=st.session_state.get("session_pause_started_at"),
        )
        st.markdown(f'<div class="m55-muted">Started {short_time(active_session["started_at"])} · {active_session["day"]} — {active_session["workout_name"]}</div>', unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        if not st.session_state.get("session_paused"):
            if b1.button("Pause Session"):
                st.session_state["session_paused"] = True
                st.session_state["session_pause_started_at"] = datetime.now().isoformat(timespec="seconds")
                st.rerun()
        else:
            if b1.button("Resume Session"):
                if st.session_state.get("session_pause_started_at"):
                    try:
                        st.session_state["session_paused_seconds"] += (datetime.now() - datetime.fromisoformat(st.session_state["session_pause_started_at"])).total_seconds()
                    except Exception:
                        pass
                st.session_state["session_paused"] = False
                st.session_state["session_pause_started_at"] = None
                st.rerun()

        if b2.button("Restart Workout"):
            finish_workout_session(active_session_id, "Restarted session", paused_seconds)
            start_workout_session(active_session["day"], int(active_session["day_order"]), active_session["workout_name"])
            st.session_state["session_paused"] = False
            st.session_state["session_paused_seconds"] = 0.0
            st.session_state["session_pause_started_at"] = None
            st.session_state["momentum_last_set_saved_at"] = None
            st.rerun()

        finish_notes = st.text_input("Session Notes", placeholder="Optional notes for this session")
        if b3.button("Finish Workout"):
            final_paused_seconds = float(st.session_state.get("session_paused_seconds", 0.0) or 0.0)
            if st.session_state.get("session_paused") and st.session_state.get("session_pause_started_at"):
                try:
                    final_paused_seconds += (datetime.now() - datetime.fromisoformat(st.session_state["session_pause_started_at"])).total_seconds()
                except Exception:
                    pass

            summary = finish_workout_session(active_session_id, finish_notes, final_paused_seconds)
            mark_workout_complete(active_session["day"], int(active_session["day_order"]), active_session["workout_name"])
            st.session_state["session_paused"] = False
            st.session_state["session_paused_seconds"] = 0.0
            st.session_state["session_pause_started_at"] = None
            if summary:
                st.success(
                    f"Workout finished: {format_duration_from_minutes(summary['duration_minutes'])} · "
                    f"{summary['exercise_count']} exercises · {summary['set_count']} sets · "
                    f"{summary['total_volume']:,.1f} volume"
                )
            st.rerun()
    else:
        st.markdown('<div class="m55-headline">Ready to Train</div>', unsafe_allow_html=True)
        st.markdown('<div class="m55-muted">Start the session when you arrive. Momentum will save duration and session analytics automatically.</div>', unsafe_allow_html=True)
        if st.button("Start Workout"):
            start_workout_session(selected_row["day"], int(selected_row["day_order"]), selected_row["workout_name"])
            st.session_state["session_paused"] = False
            st.session_state["session_paused_seconds"] = 0.0
            st.session_state["session_pause_started_at"] = None
            st.session_state["momentum_last_set_saved_at"] = None
            st.rerun()

    if st.session_state.get("momentum_last_set_saved_at"):
        try:
            rest_elapsed = datetime.now() - datetime.fromisoformat(st.session_state["momentum_last_set_saved_at"])
            rest_seconds = int(rest_elapsed.total_seconds())
            rest_label = f"{rest_seconds // 60:02d}:{rest_seconds % 60:02d}"
            st.info(f"Rest Timer: {rest_label} since last saved set.")
        except Exception:
            pass

    st.markdown('</div>', unsafe_allow_html=True)

    exercises = get_exercises(selected_day)
    recovery_status = get_today_recovery()

    if exercises.empty:
        st.info("This workout day exists, but it has no exercises yet. Add exercises in Program Manager.")
        st.stop()

    compact_mode = st.toggle("Compact gym mode", value=True)
    st.caption("Use compact mode during gym sessions. Turn it off when you want full notes.")

    for _, ex in exercises.iterrows():
        latest = get_latest_log(int(ex["id"]))
        rec = recommendation(ex, latest, recovery_status)
        plan = smart_progression_plan(ex, latest)

        st.markdown(
            f"""
            <div class="m55-exercise-card">
                <div class="m55-exercise-title">{ex['exercise_name']}</div>
                <div class="m55-exercise-meta">
                    {ex['muscle_group']} · {ex['target_sets']} sets × {ex['min_reps']}–{ex['max_reps']} · {ex['progression_type']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if latest:
            weight, reps, rir, notes, log_date = latest
            st.write(f"**Last:** {weight or 0:g} · reps/time: {reps} · RIR: {rir if rir is not None else 'N/A'} · {log_date}")
        else:
            st.write("**Last:** No previous log. Use today as baseline.")

        if count_stall_sessions(int(ex["id"])):
            st.error("Plateau warning: same result logged for 3 sessions.")

        st.markdown(
            f"""
            <div class="m55-action-strip">
                <strong>Next:</strong> {plan['Next Weight']} · <strong>Target:</strong> {plan['Target']}<br>
                {plan['Reason']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not compact_mode:
            st.success(f"Recommendation: {rec}")
            with st.expander("Smart Progression Plan"):
                p1, p2, p3 = st.columns(3)
                p1.metric("Next Weight", plan["Next Weight"])
                p2.metric("Target", plan["Target"])
                p3.write(plan["Reason"])

        default_weight = float(latest[0] or 0) if latest else 0.0
        default_reps = str(latest[1]) if latest else ""

        with st.form(f"log_{ex['id']}"):
            c1, c2 = st.columns(2)
            weight_input = c1.number_input("Actual Weight / Load", min_value=0.0, step=2.5, value=default_weight, key=f"w_{ex['id']}")
            reps_input = c2.text_input("Actual Reps / Time / Steps", value=default_reps, placeholder="Example: 8,8,7,6", key=f"r_{ex['id']}")
            rir_input = st.slider("RIR", 0.0, 5.0, 2.0, 0.5, key=f"rir_{ex['id']}")
            notes_input = "" if compact_mode else st.text_area("Notes", key=f"notes_{ex['id']}")

            if st.form_submit_button("Save Exercise Log"):
                if reps_input.strip():
                    save_workout_log(str(date.today()), int(ex["id"]), weight_input, reps_input, rir_input, notes_input)
                    st.session_state["momentum_last_set_saved_at"] = datetime.now().isoformat(timespec="seconds")
                    st.success(f"{ex['exercise_name']} saved. Rest timer started.")
                else:
                    st.error("Enter reps/time/steps before saving.")

    st.markdown("---")
    st.caption("Use Finish Workout in the Gym Session panel to save duration and mark the workout complete. Manual completion remains available as a fallback.")
    if st.button("Mark Workout Complete Without Timer"):
        mark_workout_complete(selected_row["day"], int(selected_row["day_order"]), selected_row["workout_name"])
        st.success("Workout marked complete. Refresh to see next workout update.")

elif page == "Workout Journal":
    st.header("Workout Journal")
    st.caption("Review completed training sessions without changing the core Momentum layout.")

    sessions = fetch_df("""
        SELECT id, session_date, day, workout_name, started_at, ended_at,
               duration_minutes, exercise_count, set_count, total_volume, notes
        FROM workout_sessions
        WHERE ended_at IS NOT NULL
        ORDER BY id DESC
    """)

    if sessions.empty:
        render_empty_state("No completed workout sessions yet. Finish a workout with the Gym Session timer to build your journal.")
    else:
        labels = []
        for _, row in sessions.iterrows():
            labels.append(f"{row['session_date']} — {row['day']} — {row['workout_name']} — {duration_label(row['duration_minutes'])}")

        selected_label = st.selectbox("Select workout", labels)
        selected_index = labels.index(selected_label)
        selected_session = sessions.iloc[selected_index]

        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Training Snapshot</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="m55-headline">{selected_session['day']} — {selected_session['workout_name']}</div>
            <div class="m55-muted">{selected_session['session_date']} · Started {short_time(selected_session['started_at'])} · Finished {short_time(selected_session['ended_at'])}</div>
            """,
            unsafe_allow_html=True,
        )
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Duration", duration_label(selected_session["duration_minutes"]))
        s2.metric("Exercises", int(selected_session["exercise_count"] or 0))
        s3.metric("Sets", int(selected_session["set_count"] or 0))
        s4.metric("Volume", f"{float(selected_session['total_volume'] or 0):,.0f}")
        if str(selected_session.get("notes", "") or "").strip():
            st.write(f"**Notes:** {selected_session['notes']}")
        st.markdown('</div>', unsafe_allow_html=True)

        logs = session_logs_between(selected_session["started_at"], selected_session["ended_at"])
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Exercise Breakdown</div>', unsafe_allow_html=True)
        if logs.empty:
            render_empty_state("No set logs were captured inside this session window.")
        else:
            for exercise_name, group in logs.groupby("exercise_name", sort=False):
                group = group.copy()
                group["total_reps"] = group["reps"].apply(lambda x: sum(safe_reps_list(x)))
                group["volume"] = group["weight"].fillna(0) * group["total_reps"]
                st.write(f"**{exercise_name}**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Sets", len(group))
                c2.metric("Volume", f"{group['volume'].sum():,.0f}")
                c3.metric("Best Load", f"{group['weight'].max():g}")
                st.dataframe(group[["created_at", "weight", "reps", "rir", "notes"]], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Exercise Intelligence":
    st.header("Exercise Intelligence")
    st.caption("Exercise-level progress, estimated strength, volume, and recent performance.")

    exercises = get_exercises()
    if exercises.empty:
        render_empty_state("No exercises found. Add exercises in Program Manager first.")
    else:
        exercise_name = st.selectbox("Exercise", sorted(exercises["exercise_name"].unique()))
        exercise_ids = exercises.loc[exercises["exercise_name"] == exercise_name, "id"].tolist()
        placeholders = ",".join("?" for _ in exercise_ids)
        logs = fetch_df(f"""
            SELECT wl.log_date, wl.created_at, e.day, e.workout_name, e.exercise_name, e.muscle_group,
                   wl.weight, wl.reps, wl.rir, wl.notes
            FROM workout_logs wl
            JOIN exercises e ON wl.exercise_id = e.id
            WHERE wl.exercise_id IN ({placeholders})
            ORDER BY wl.log_date ASC, wl.id ASC
        """, tuple(exercise_ids))

        if logs.empty:
            render_empty_state("No logs for this exercise yet. Log it from Today's Workout to unlock intelligence.")
        else:
            logs = logs.copy()
            logs["total_reps"] = logs["reps"].apply(lambda x: sum(safe_reps_list(x)))
            logs["best_set_reps"] = logs["reps"].apply(lambda x: max(safe_reps_list(x)) if safe_reps_list(x) else 0)
            logs["volume"] = logs["weight"].fillna(0) * logs["total_reps"]
            logs["estimated_1rm"] = logs.apply(lambda r: estimate_1rm(r["weight"], r["best_set_reps"]), axis=1)

            best_weight = logs["weight"].max()
            best_volume = logs["volume"].max()
            best_1rm = logs["estimated_1rm"].max()
            sessions_count = len(logs)
            total_volume = logs["volume"].sum()
            recent = logs.tail(5)
            first_weight = float(logs["weight"].dropna().iloc[0]) if not logs["weight"].dropna().empty else 0
            last_weight = float(logs["weight"].dropna().iloc[-1]) if not logs["weight"].dropna().empty else 0
            progress_delta = last_weight - first_weight

            st.markdown('<div class="m55-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="m55-title">Exercise Profile</div><div class="m55-headline">{exercise_name}</div>', unsafe_allow_html=True)
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("Best Load", f"{best_weight:g}")
            p2.metric("Est. 1RM", f"{best_1rm:,.1f}")
            p3.metric("Total Volume", f"{total_volume:,.0f}")
            p4.metric("Sessions", sessions_count)
            st.metric("Load Progress", f"{progress_delta:+.1f}", "first to latest")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="m55-card">', unsafe_allow_html=True)
            st.markdown('<div class="m55-title">Progress Charts</div>', unsafe_allow_html=True)
            chart = logs[["log_date", "weight", "volume", "estimated_1rm"]].copy().set_index("log_date")
            st.subheader("Load Trend")
            st.line_chart(chart["weight"])
            st.subheader("Volume Trend")
            st.line_chart(chart["volume"])
            st.subheader("Estimated 1RM Trend")
            st.line_chart(chart["estimated_1rm"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="m55-card">', unsafe_allow_html=True)
            st.markdown('<div class="m55-title">Recent Sessions</div>', unsafe_allow_html=True)
            st.dataframe(recent[["log_date", "day", "workout_name", "weight", "reps", "rir", "volume", "estimated_1rm", "notes"]].sort_index(ascending=False), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "Training Calendar":
    st.header("Training Calendar")
    st.caption("A monthly timeline of completed workouts and timed sessions.")

    import calendar as py_calendar
    import pandas as pd

    today = date.today()
    month_start = today.replace(day=1)
    selected_month = st.date_input("Month", value=month_start)
    year = selected_month.year
    month = selected_month.month

    completions = fetch_df("SELECT completion_date, day, workout_name FROM workout_completions")
    sessions = fetch_df("""
        SELECT session_date, day, workout_name, duration_minutes, total_volume, notes
        FROM workout_sessions
        WHERE ended_at IS NOT NULL
    """)

    cal = py_calendar.Calendar(firstweekday=0)
    weeks = cal.monthdatescalendar(year, month)
    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="m55-title">{py_calendar.month_name[month]} {year}</div>', unsafe_allow_html=True)

    header_cols = st.columns(7)
    for col, name in zip(header_cols, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        col.markdown(f"**{name}**")

    completed_dates = set(completions["completion_date"].astype(str).tolist()) if not completions.empty else set()
    session_dates = set(sessions["session_date"].astype(str).tolist()) if not sessions.empty else set()

    for week_days in weeks:
        cols = st.columns(7)
        for col, day_obj in zip(cols, week_days):
            day_str = str(day_obj)
            if day_obj.month != month:
                col.caption(" ")
            else:
                marker = "🟢" if day_str in completed_dates or day_str in session_dates else "⚪"
                col.markdown(f"{marker} **{day_obj.day}**")

    st.markdown('</div>', unsafe_allow_html=True)

    selected_day = st.date_input("View day", value=today)
    selected_day_str = str(selected_day)
    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="m55-title">Day Detail</div><div class="m55-headline">{selected_day_str}</div>', unsafe_allow_html=True)
    day_sessions = sessions[sessions["session_date"].astype(str) == selected_day_str] if not sessions.empty else sessions
    day_completions = completions[completions["completion_date"].astype(str) == selected_day_str] if not completions.empty else completions

    if day_sessions.empty and day_completions.empty:
        render_empty_state("No workout recorded for this day.")
    else:
        if not day_sessions.empty:
            st.write("**Timed Sessions**")
            st.dataframe(day_sessions, use_container_width=True)
        if not day_completions.empty:
            st.write("**Completed Workouts**")
            st.dataframe(day_completions, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Progress Center":
    st.header("Progress Center")
    st.caption("A high-level training command center for consistency, volume, sessions, and achievements.")

    sessions = fetch_df("""
        SELECT session_date, day, workout_name, duration_minutes, exercise_count, set_count, total_volume
        FROM workout_sessions
        WHERE ended_at IS NOT NULL
        ORDER BY session_date ASC
    """)
    logs = fetch_df("""
        SELECT wl.log_date, e.exercise_name, e.muscle_group, wl.weight, wl.reps
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        ORDER BY wl.log_date ASC
    """)
    completions = fetch_df("SELECT completion_date FROM workout_completions ORDER BY completion_date ASC")

    total_sessions = len(sessions)
    total_hours = float(sessions["duration_minutes"].fillna(0).sum() / 60) if not sessions.empty else 0
    total_volume = float(sessions["total_volume"].fillna(0).sum()) if not sessions.empty else 0
    total_sets = int(sessions["set_count"].fillna(0).sum()) if not sessions.empty else 0
    total_logs = len(logs)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Timed Sessions", total_sessions)
    c2.metric("Gym Hours", f"{total_hours:.1f}")
    c3.metric("Total Volume", f"{total_volume:,.0f}")
    c4.metric("Sets Logged", total_sets)

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Achievements</div>', unsafe_allow_html=True)
    achievements = []
    if total_sessions >= 1: achievements.append("First timed workout")
    if total_sessions >= 10: achievements.append("10 timed workouts")
    if total_sessions >= 25: achievements.append("25 timed workouts")
    if total_sets >= 100: achievements.append("100 sets logged")
    if total_volume >= 100000: achievements.append("100,000 volume logged")
    if total_hours >= 10: achievements.append("10 gym hours tracked")
    if total_logs >= 50: achievements.append("50 exercise logs")

    if achievements:
        for item in achievements:
            st.success(item)
    else:
        render_empty_state("No achievements yet. Complete workouts and log sets to unlock them.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Training Trends</div>', unsafe_allow_html=True)
    if sessions.empty:
        render_empty_state("No session trend data yet.")
    else:
        trend = sessions.copy()
        trend["session_date"] = trend["session_date"].astype(str)
        st.subheader("Duration")
        st.line_chart(trend.set_index("session_date")["duration_minutes"])
        if trend["total_volume"].fillna(0).sum() > 0:
            st.subheader("Volume")
            st.line_chart(trend.set_index("session_date")["total_volume"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Most Trained Exercises</div>', unsafe_allow_html=True)
    if logs.empty:
        render_empty_state("No exercise logs yet.")
    else:
        frequency = logs.groupby(["exercise_name", "muscle_group"], as_index=False).size().rename(columns={"size": "logs"}).sort_values("logs", ascending=False)
        st.dataframe(frequency.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Progress Hub":
    st.header("Progress Hub")
    st.caption("Your current phase, bodyweight trend, personal records, and consistency score.")

    score, score_details = calculate_momentum_score()
    weeks_left = max(0, 12 - week)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Current Week", f"{week}/12")
    p2.metric("Weeks Left", weeks_left)
    p3.metric("Momentum Score", f"{score}/100")
    p4.metric("Recovery", get_today_recovery().title())

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Bodyweight Trend</div>', unsafe_allow_html=True)

    weight_logs = fetch_df("""
        SELECT checkin_date, body_weight
        FROM daily_checkins
        WHERE body_weight IS NOT NULL AND body_weight > 0
        ORDER BY checkin_date ASC
    """)

    if weight_logs.empty:
        st.info("No bodyweight data yet.")
    else:
        weight_logs["checkin_date"] = weight_logs["checkin_date"].astype(str)
        current_weight = round(weight_logs["body_weight"].iloc[-1], 1)
        avg_7 = round(weight_logs["body_weight"].tail(7).mean(), 1)
        avg_30 = round(weight_logs["body_weight"].tail(30).mean(), 1)
        trend = round(weight_logs["body_weight"].iloc[-1] - weight_logs["body_weight"].iloc[0], 1) if len(weight_logs) >= 2 else 0

        w1, w2, w3, w4 = st.columns(4)
        w1.metric("Current", current_weight)
        w2.metric("7-Day Avg", avg_7)
        w3.metric("30-Day Avg", avg_30)
        w4.metric("Trend", f"{trend:+.1f}")
        st.line_chart(weight_logs.set_index("checkin_date")["body_weight"])

    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Personal Records</div>', unsafe_allow_html=True)
        prs = get_personal_records()
        if prs.empty:
            st.info("No personal records yet.")
        else:
            st.dataframe(prs.head(10), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Momentum Score Breakdown</div>', unsafe_allow_html=True)
        for item in score_details:
            st.write(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Analytics":
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
        import pandas as pd
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
        weekly_sessions["week"] = pd.to_datetime(weekly_sessions["session_date"], errors="coerce").dt.to_period("W").astype(str)
        weekly_summary = weekly_sessions.groupby("week", as_index=False)["duration_minutes"].sum()
        weekly_summary["gym_hours"] = (weekly_summary["duration_minutes"] / 60).round(2)

        monthly_sessions = sessions.copy()
        monthly_sessions["month"] = pd.to_datetime(monthly_sessions["session_date"], errors="coerce").dt.to_period("M").astype(str)
        monthly_summary = monthly_sessions.groupby("month", as_index=False)["duration_minutes"].sum()
        monthly_summary["gym_hours"] = (monthly_summary["duration_minutes"] / 60).round(2)

        wcol, mcol = st.columns(2)
        with wcol:
            st.subheader("Weekly Gym Hours")
            st.dataframe(weekly_summary[["week", "gym_hours"]].sort_values("week", ascending=False), use_container_width=True)
        with mcol:
            st.subheader("Monthly Gym Hours")
            st.dataframe(monthly_summary[["month", "gym_hours"]].sort_values("month", ascending=False), use_container_width=True)

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

elif page == "Workout Log":
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
            format_func=lambda x: f"ID {x} — {logs.loc[logs['id'] == x, 'exercise_name'].iloc[0]} — {logs.loc[logs['id'] == x, 'log_date'].iloc[0]}"
        )

        selected = logs[logs["id"] == log_id].iloc[0]

        with st.form("edit_workout_log_form"):
            edit_date = st.date_input("Log Date", value=date.fromisoformat(str(selected["log_date"])))
            edit_weight = st.number_input("Weight / Load", min_value=0.0, step=2.5, value=float(selected["weight"] or 0))
            edit_reps = st.text_input("Reps / Time / Steps", value=str(selected["reps"]))
            edit_rir = st.slider("RIR", 0.0, 5.0, float(selected["rir"] if selected["rir"] is not None else 2.0), 0.5)
            edit_notes = st.text_area("Notes", value="" if selected["notes"] is None else str(selected["notes"]))

            save_edit = st.form_submit_button("Save Changes")
            if save_edit:
                if edit_reps.strip():
                    update_workout_log(log_id, str(edit_date), edit_weight, edit_reps, edit_rir, edit_notes)
                    st.success("Workout log updated. Refresh to see changes.")
                else:
                    st.error("Reps/time/steps cannot be blank.")

        st.warning("Delete is permanent for this selected log only.")
        confirm_delete = st.checkbox("I understand this will delete the selected workout log only.")
        if st.button("Delete Selected Log"):
            if confirm_delete:
                delete_workout_log(log_id)
                st.success("Workout log deleted. Refresh to update the table.")
            else:
                st.error("Check the confirmation box before deleting.")

elif page == "Exercise History":
    st.header("Exercise History")
    exercises = get_exercises()
    exercise_name = st.selectbox("Select Exercise", exercises["exercise_name"].unique())
    exercise_ids = exercises.loc[exercises["exercise_name"] == exercise_name, "id"].tolist()
    placeholders = ",".join("?" for _ in exercise_ids)
    logs = fetch_df(f"""
        SELECT wl.log_date, e.day, e.workout_name, wl.weight, wl.reps, wl.rir, wl.notes
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        WHERE wl.exercise_id IN ({placeholders})
        ORDER BY wl.id ASC
    """, tuple(exercise_ids))
    if logs.empty:
        st.info("No history for this exercise yet.")
    else:
        logs["total_reps"] = logs["reps"].apply(total_reps)
        logs["volume"] = logs["weight"] * logs["total_reps"]

        st.subheader("Personal Record")
        best_weight = round(logs["weight"].max(), 1)
        best_total_reps = round(logs["total_reps"].max(), 1)
        best_volume_row = logs.loc[logs["volume"].idxmax()]
        best_volume = round(best_volume_row["volume"], 1)
        pr_date = best_volume_row["log_date"]

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Best Weight", best_weight)
        p2.metric("Best Total Reps", best_total_reps)
        p3.metric("Best Volume", best_volume)
        p4.metric("PR Date", pr_date)

        st.dataframe(logs, use_container_width=True)
        st.subheader("Weight Trend")
        st.line_chart(logs.set_index("log_date")["weight"])
        st.subheader("Volume Trend")
        st.line_chart(logs.set_index("log_date")["volume"])


elif page == "Bodyweight Log":
    st.header("Bodyweight Log")
    st.caption("Use this page to add, edit, or clear bodyweight entries by date.")

    c1, c2 = st.columns(2)
    entry_date = c1.date_input("Date", value=date.today())
    entry_weight = c2.number_input("Body Weight", min_value=0.0, step=0.5)

    if st.button("Save Bodyweight Entry"):
        save_bodyweight_entry(str(entry_date), entry_weight)
        st.success("Bodyweight entry saved.")

    weight_logs = fetch_df("""
        SELECT checkin_date, body_weight
        FROM daily_checkins
        WHERE body_weight IS NOT NULL AND body_weight > 0
        ORDER BY checkin_date DESC
    """)

    if weight_logs.empty:
        st.info("No bodyweight entries yet.")
    else:
        st.subheader("Bodyweight History")
        st.dataframe(weight_logs, use_container_width=True)

        clear_date = st.selectbox("Clear entry for date", weight_logs["checkin_date"].tolist())
        if st.button("Clear Selected Bodyweight Entry"):
            clear_bodyweight_entry(clear_date)
            st.success("Selected bodyweight entry cleared. Refresh to update the table.")



elif page == "Program Manager":
    st.header("Program Manager")
    st.caption("Build and manage training programs. Each program can represent a different specialization block.")

    programs = get_programs()
    active_program_id = get_active_program_id()

    if programs.empty:
        st.warning("No programs found.")
        st.stop()

    program_names = programs["program_name"].tolist()
    program_ids = programs["id"].tolist()
    selected_index = program_ids.index(active_program_id) if active_program_id in program_ids else 0

    selected_program_name = st.selectbox("Program", program_names, index=selected_index)
    selected_program = programs[programs["program_name"] == selected_program_name].iloc[0]
    selected_program_id = int(selected_program["id"])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Selected Program", selected_program_name)
    with c2:
        st.metric("Duration", f"{int(selected_program['duration_weeks'])} weeks")

    if st.button("Set as Active Program"):
        set_active_program(selected_program_id)
        reset_workout_progress()
        st.success("Active program updated. Workout progress reset so Momentum starts from Day 1 for this program.")

    st.subheader("Available Programs")
    st.dataframe(programs, use_container_width=True)

    st.subheader("Create Program")
    with st.form("create_program_form"):
        new_program_name = st.text_input("Program Name", placeholder="Example: Arm Specialization")
        new_duration = st.number_input("Duration Weeks", min_value=1, max_value=52, value=12)
        new_goal = st.text_area("Goal", placeholder="Example: Prioritize forearms, biceps, and triceps while maintaining lower body.")
        create_button = st.form_submit_button("Create Program")

        if create_button:
            if new_program_name.strip():
                create_program(new_program_name.strip(), new_duration, new_goal)
                st.success("Program created. Refresh to see it in the list.")
            else:
                st.error("Program name is required.")

    st.markdown("---")
    st.subheader("Workout Day Builder")

    with st.form("add_day_form"):
        d1, d2, d3 = st.columns(3)
        day_order = d1.number_input("Day Order", min_value=1, max_value=14, value=1)
        day_label = d2.text_input("Day Label", value=f"Day {day_order}")
        workout_name = d3.text_input("Workout Name", placeholder="Example: Biceps + Forearms")

        add_day = st.form_submit_button("Add Workout Day")
        if add_day:
            if day_label.strip() and workout_name.strip():
                add_workout_day(selected_program_id, day_label.strip(), int(day_order), workout_name.strip())
                st.success("Workout day added.")
            else:
                st.error("Day label and workout name are required.")

    days = get_workout_days()
    if days.empty:
        st.info("No workout days created for the active program yet.")
    else:
        st.subheader("Current Active Program Split")
        st.dataframe(days, use_container_width=True)

    st.markdown("---")
    st.subheader("Exercise Builder")

    program_days = get_program_exercises(selected_program_id)
    visible_days = program_days[["day", "day_order", "workout_name"]].drop_duplicates().sort_values(["day_order", "day"])

    if visible_days.empty:
        st.info("Create at least one workout day before adding exercises.")
    else:
        day_options = [f"{row.day} — {row.workout_name}" for _, row in visible_days.iterrows()]
        selected_day_label = st.selectbox("Add Exercise To", day_options)
        selected_day = selected_day_label.split(" — ")[0]
        selected_day_row = visible_days[visible_days["day"] == selected_day].iloc[0]

        with st.form("add_exercise_form"):
            e1, e2 = st.columns(2)
            exercise_name = e1.text_input("Exercise Name", placeholder="Example: Hammer Curl")
            muscle_group = e2.text_input("Muscle Group", placeholder="Example: Biceps")

            s1, s2, s3 = st.columns(3)
            target_sets = s1.number_input("Target Sets", min_value=1, max_value=10, value=3)
            min_reps = s2.number_input("Min Reps / Time / Steps", min_value=0, max_value=100000, value=8)
            max_reps = s3.number_input("Max Reps / Time / Steps", min_value=0, max_value=100000, value=12)

            progression_type = st.selectbox(
                "Progression Type",
                ["weight", "core_load", "time", "cardio_time", "steps", "reps", "optional_reps", "each_leg"]
            )

            add_exercise = st.form_submit_button("Add Exercise")
            if add_exercise:
                if exercise_name.strip() and muscle_group.strip():
                    add_exercise_to_day(
                        selected_program_id,
                        selected_day,
                        int(selected_day_row["day_order"]),
                        selected_day_row["workout_name"],
                        exercise_name.strip(),
                        muscle_group.strip(),
                        int(target_sets),
                        int(min_reps),
                        int(max_reps),
                        progression_type
                    )
                    st.success("Exercise added.")
                else:
                    st.error("Exercise name and muscle group are required.")

    st.markdown("---")
    st.subheader("Program Exercises")
    all_exercises = get_program_exercises(selected_program_id)

    if all_exercises.empty:
        st.info("No days or exercises for this program yet.")
    else:
        display_exercises = all_exercises.copy()
        display_exercises["exercise_name"] = display_exercises["exercise_name"].replace("__DAY_PLACEHOLDER__", "(day shell)")
        st.dataframe(
            display_exercises[["id", "day", "day_order", "workout_name", "exercise_name", "muscle_group", "target_sets", "min_reps", "max_reps", "progression_type"]],
            use_container_width=True
        )

        st.subheader("Delete")
        delete_options = display_exercises["id"].tolist()
        delete_id = st.selectbox(
            "Select Exercise/Day Shell ID to Delete",
            delete_options,
            format_func=lambda x: f"ID {x} — {display_exercises.loc[display_exercises['id'] == x, 'day'].iloc[0]} — {display_exercises.loc[display_exercises['id'] == x, 'exercise_name'].iloc[0]}"
        )
        confirm_delete_item = st.checkbox("I understand this deletes the selected exercise/day shell only.")
        if st.button("Delete Selected Item"):
            if confirm_delete_item:
                delete_exercise(delete_id)
                st.success("Selected item deleted. Refresh to update.")
            else:
                st.error("Check the confirmation box before deleting.")




elif page == "Program Editor":
    st.header("Program Editor")
    st.caption("Edit programs, workout days, and exercises without touching code.")

    programs = get_programs()

    if programs.empty:
        st.warning("No programs available.")
        st.stop()

    program_name = st.selectbox("Select Program to Edit", programs["program_name"].tolist())
    selected_program = programs[programs["program_name"] == program_name].iloc[0]
    selected_program_id = int(selected_program["id"])

    st.subheader("Program Details")
    with st.form("edit_program_form"):
        edited_program_name = st.text_input("Program Name", value=str(selected_program["program_name"]))
        edited_duration = st.number_input("Duration Weeks", min_value=1, max_value=52, value=int(selected_program["duration_weeks"]))
        edited_goal = st.text_area("Goal", value="" if selected_program["goal"] is None else str(selected_program["goal"]))

        if st.form_submit_button("Save Program Changes"):
            if edited_program_name.strip():
                update_program(selected_program_id, edited_program_name.strip(), edited_duration, edited_goal)
                st.success("Program updated. Refresh to see changes.")
            else:
                st.error("Program name cannot be blank.")


    st.subheader("Archive Program")
    st.caption("Archiving hides nothing yet, but marks programs you are not actively using.")
    archive_col, unarchive_col = st.columns(2)
    if archive_col.button("Archive Selected Program"):
        if selected_program_id == 1:
            st.error("Shoulder Specialization is protected and cannot be archived.")
        else:
            archive_program(selected_program_id)
            st.success("Program archived.")

    if unarchive_col.button("Unarchive Selected Program"):
        unarchive_program(selected_program_id)
        st.success("Program unarchived.")


    st.subheader("Duplicate Program")
    st.info("Option A: duplication copies the full program, including all workout days and exercises.")
    with st.form("duplicate_program_form"):
        duplicate_name = st.text_input("New Program Name", placeholder=f"{program_name} Copy")
        if st.form_submit_button("Duplicate Full Program"):
            if duplicate_name.strip():
                duplicate_program(selected_program_id, duplicate_name.strip())
                st.success("Program duplicated with all days and exercises. Refresh to see the copy.")
            else:
                st.error("New program name is required.")

    st.subheader("Delete Program")
    st.warning("Deleting a program also deletes its workout days and exercise templates. Shoulder Specialization is protected.")
    confirm_delete_program = st.checkbox("I understand this deletes the selected program and its exercises.")
    if st.button("Delete Selected Program"):
        if selected_program_id == 1:
            st.error("Shoulder Specialization is protected and cannot be deleted.")
        elif confirm_delete_program:
            delete_program(selected_program_id)
            reset_workout_progress()
            st.success("Program deleted. Active program reset to Shoulder Specialization if needed.")
        else:
            st.error("Check the confirmation box first.")

    st.markdown("---")
    st.subheader("Workout Day Editor")

    program_exercises = get_program_exercises(selected_program_id)

    if program_exercises.empty:
        st.info("No workout days exist for this program yet. Use Program Manager to create days.")
        st.stop()

    day_table = program_exercises[["day", "day_order", "workout_name"]].drop_duplicates().sort_values(["day_order", "day"])

    if day_table.empty:
        st.info("No workout days found.")
    else:
        day_options = [f"{row.day} — {row.workout_name}" for _, row in day_table.iterrows()]
        selected_day_label = st.selectbox("Select Workout Day", day_options)
        selected_day = selected_day_label.split(" — ")[0]
        selected_day_row = day_table[day_table["day"] == selected_day].iloc[0]

        with st.form("edit_day_form"):
            new_day_order = st.number_input("Day Order", min_value=1, max_value=14, value=int(selected_day_row["day_order"]))
            new_day_label = st.text_input("Day Label", value=str(selected_day_row["day"]))
            new_workout_name = st.text_input("Workout Name", value=str(selected_day_row["workout_name"]))

            if st.form_submit_button("Save Workout Day Changes"):
                if new_day_label.strip() and new_workout_name.strip():
                    update_workout_day(
                        selected_program_id,
                        selected_day,
                        new_day_label.strip(),
                        int(new_day_order),
                        new_workout_name.strip()
                    )
                    st.success("Workout day updated. Refresh to see changes.")
                else:
                    st.error("Day label and workout name are required.")

    st.markdown("---")
    st.subheader("Exercise Editor")

    editable_exercises = program_exercises[program_exercises["exercise_name"] != "__DAY_PLACEHOLDER__"]

    if editable_exercises.empty:
        st.info("No editable exercises exist for this program yet.")
    else:
        exercise_id = st.selectbox(
            "Select Exercise",
            editable_exercises["id"].tolist(),
            format_func=lambda x: f"ID {x} — {editable_exercises.loc[editable_exercises['id'] == x, 'day'].iloc[0]} — {editable_exercises.loc[editable_exercises['id'] == x, 'exercise_name'].iloc[0]}"
        )

        selected_exercise = editable_exercises[editable_exercises["id"] == exercise_id].iloc[0]

        with st.form("edit_exercise_form"):
            e1, e2 = st.columns(2)
            edited_exercise_name = e1.text_input("Exercise Name", value=str(selected_exercise["exercise_name"]))
            edited_muscle_group = e2.text_input("Muscle Group", value=str(selected_exercise["muscle_group"]))

            s1, s2, s3 = st.columns(3)
            edited_sets = s1.number_input("Target Sets", min_value=0, max_value=10, value=int(selected_exercise["target_sets"]))
            edited_min_reps = s2.number_input("Min Reps / Time / Steps", min_value=0, max_value=100000, value=int(selected_exercise["min_reps"]))
            edited_max_reps = s3.number_input("Max Reps / Time / Steps", min_value=0, max_value=100000, value=int(selected_exercise["max_reps"]))

            progression_options = ["weight", "core_load", "time", "cardio_time", "steps", "reps", "optional_reps", "each_leg", "placeholder"]
            current_progression = str(selected_exercise["progression_type"])
            progression_index = progression_options.index(current_progression) if current_progression in progression_options else 0
            edited_progression_type = st.selectbox("Progression Type", progression_options, index=progression_index)

            if st.form_submit_button("Save Exercise Changes"):
                if edited_exercise_name.strip() and edited_muscle_group.strip():
                    update_exercise_template(
                        exercise_id,
                        edited_exercise_name.strip(),
                        edited_muscle_group.strip(),
                        int(edited_sets),
                        int(edited_min_reps),
                        int(edited_max_reps),
                        edited_progression_type
                    )
                    st.success("Exercise updated. Refresh to see changes.")
                else:
                    st.error("Exercise name and muscle group are required.")

        st.markdown("---")
        st.subheader("Move / Duplicate Exercise")

        move_day_options = [f"{row.day} — {row.workout_name}" for _, row in day_table.iterrows()]

        if not move_day_options:
            st.info("No target days available.")
        else:
            target_day_label = st.selectbox("Target Day", move_day_options)
            target_day = target_day_label.split(" — ")[0]
            target_day_row = day_table[day_table["day"] == target_day].iloc[0]

            m1, m2 = st.columns(2)

            if m1.button("Move Exercise to Target Day"):
                move_exercise_to_day(
                    exercise_id,
                    target_day,
                    int(target_day_row["day_order"]),
                    str(target_day_row["workout_name"])
                )
                st.success("Exercise moved. Refresh to see changes.")

            if m2.button("Duplicate Exercise to Target Day"):
                duplicate_exercise_to_day(
                    exercise_id,
                    target_day,
                    int(target_day_row["day_order"]),
                    str(target_day_row["workout_name"])
                )
                st.success("Exercise duplicated. Refresh to see changes.")

    st.markdown("---")
    st.subheader("Current Program Template")
    display_table = get_program_exercises(selected_program_id)

    if display_table.empty:
        st.info("No template data.")
    else:
        display_table = display_table.copy()
        display_table["exercise_name"] = display_table["exercise_name"].replace("__DAY_PLACEHOLDER__", "(day shell)")
        st.dataframe(
            display_table[["id", "day", "day_order", "workout_name", "exercise_name", "muscle_group", "target_sets", "min_reps", "max_reps", "progression_type"]],
            use_container_width=True
        )


elif page == "Export / Backup":
    st.header("Export / Backup")
    st.caption("Download your Momentum data as CSV files. This helps protect your logs before future upgrades.")

    tables = get_export_tables()

    for table_name, table_df in tables.items():
        st.subheader(table_name)
        if table_df.empty:
            st.info("No data yet.")
        else:
            st.dataframe(table_df, use_container_width=True)
            csv = table_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {table_name}.csv",
                data=csv,
                file_name=f"{table_name}.csv",
                mime="text/csv"
            )


elif page == "Settings":
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
    start_date = st.date_input("Phase Start Date", value=date.fromisoformat(current_start))
    if st.button("Save Phase Start Date"):
        set_setting("phase_start_date", str(start_date))
        st.success("Phase start date saved.")

    st.subheader("Reset Test Data")
    st.warning("Deletes workout logs, check-ins, and completion history only. Keeps exercise templates.")
    confirm_reset = st.checkbox("I understand this deletes logged test data only.")
    if st.button("Reset Test Data"):
        if confirm_reset:
            reset_test_data()
            st.success("Test data reset complete.")
        else:
            st.error("Check the confirmation box first.")

    st.subheader("Version")
    st.code("Momentum 6.9 - Training Intelligence Bundle")
