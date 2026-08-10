import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime

from database import *

from views.dashboard import dashboard_page
from views.workout import workout_page
from views.analytics import analytics_page
from views.settings import settings_page
from views.exports import exports_page

st.set_page_config(
    page_title="Momentum",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)
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
    "Running",
    "Exercise Intelligence",
    "Training Calendar",
    "Progress Center",
    "Progress Hub",
    "Analytics",
    "Workout Log",
    "Exercise History",
    "Program Manager",
    "Program Editor",
    "Export / Backup",
    "Settings",
]

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Today's Workout"

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

    score, score_details = calculate_training_momentum_score()
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

    m1, m2, m3 = st.columns(3)
    m1.metric("Week", f"{week}/12")
    m2.metric("Momentum", f"{score}/100")
    m3.metric("Weeks Left", weeks_left)

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
        if st.button("Start Today's Workout", type="primary", use_container_width=True):
            st.session_state["nav_page"] = "Today's Workout"
            st.session_state["auto_start_workout_from_dashboard"] = True
            st.rerun()

    with right:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Active Program</div>', unsafe_allow_html=True)

        if active_program is None:
            st.info("No active program selected.")
        else:
            st.markdown(f"### {active_program['program_name']}")
            st.write(f"**Goal:** {active_program['goal'] or 'No goal added yet.'}")
            st.write(f"**Program length:** {int(active_program['duration_weeks'])} weeks")
            st.write(f"**Start date:** {get_setting('phase_start_date', str(date.today()))}")
            st.write(f"**Current phase:** {phase}")

        st.caption("Change the program start date or restart at Week 1 from Settings.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="m5-card">', unsafe_allow_html=True)
    st.markdown('<div class="m5-eyebrow">Momentum Score</div>', unsafe_allow_html=True)
    st.metric("Current", f"{score}/100", "Training consistency")
    with st.expander("Score Breakdown"):
        for item in score_details:
            st.write(item)
    st.markdown('<div class="m5-muted">Nutrition, bodyweight, and daily health tracking are managed in your Excel planner.</div>', unsafe_allow_html=True)
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

    readiness = get_today_readiness()
    r1, r2 = st.columns([0.65, 1.35])
    with r1:
        score_label = "—" if readiness["score"] is None else f"{readiness['score']}/100"
        st.metric("Readiness", score_label, readiness["status"])
        st.caption(readiness["recommendation"])
    with r2:
        with st.expander("10-second readiness check", expanded=readiness["score"] is None):
            with st.form("readiness_check"):
                q1, q2, q3, q4, q5 = st.columns(5)
                energy = q1.slider("Energy", 1, 5, 3)
                sleep_quality = q2.slider("Sleep", 1, 5, 3)
                soreness = q3.slider("Soreness", 1, 5, 2)
                pain = q4.slider("Pain", 1, 5, 1)
                motivation = q5.slider("Motivation", 1, 5, 3)
                if st.form_submit_button("Save Readiness"):
                    save_readiness_checkin(energy, sleep_quality, soreness, pain, motivation)
                    st.rerun()

    with st.expander("Plan or reschedule training"):
        schedule_date = st.date_input("Training date", value=date.today(), key="schedule_date")
        schedule_notes = st.text_input("Plan note", placeholder="Optional: moved from Tuesday")
        s1, s2 = st.columns(2)
        if s1.button("Schedule Selected Workout", use_container_width=True):
            schedule_workout(
                schedule_date,
                selected_row["day"],
                int(selected_row["day_order"]),
                selected_row["workout_name"],
                schedule_notes,
            )
            st.success(f"Scheduled for {schedule_date}.")
            st.rerun()
        today_schedule = get_scheduled_workout(str(date.today()))
        if s2.button("Skip Today's Plan", use_container_width=True, disabled=today_schedule is None):
            skip_scheduled_workout(str(date.today()), schedule_notes or "Skipped from Today")
            st.success("Today's plan was skipped. Your workout history was not changed.")
            st.rerun()

        upcoming = get_upcoming_schedule()
        if not upcoming.empty:
            st.dataframe(
                upcoming[["scheduled_date", "day", "workout_name", "notes"]],
                use_container_width=True,
                hide_index=True,
            )

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

    def persist_session_notes(session_id, widget_key):
        if session_id:
            update_workout_session_notes(session_id, st.session_state.get(widget_key, ""))

    def persist_exercise_draft(session_id, exercise_id, weight_key, reps_key, rir_key, notes_key):
        if not session_id:
            return
        upsert_workout_draft(
            session_id=session_id,
            exercise_id=exercise_id,
            weight=st.session_state.get(weight_key, 0.0),
            reps=st.session_state.get(reps_key, ""),
            rir=st.session_state.get(rir_key, 2.0),
            notes=st.session_state.get(notes_key, ""),
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
            clear_workout_drafts(active_session_id)
            finish_workout_session(active_session_id, "Restarted session", paused_seconds)
            start_workout_session(active_session["day"], int(active_session["day_order"]), active_session["workout_name"])
            st.session_state["session_paused"] = False
            st.session_state["session_paused_seconds"] = 0.0
            st.session_state["session_pause_started_at"] = None
            st.session_state["momentum_last_set_saved_at"] = None
            st.rerun()

        session_notes_key = f"session_notes_{active_session_id}"
        if session_notes_key not in st.session_state:
            st.session_state[session_notes_key] = active_session.get("notes") or ""
        finish_notes = st.text_input(
            "Session Notes",
            placeholder="Optional notes for this session",
            key=session_notes_key,
            on_change=persist_session_notes,
            args=(active_session_id, session_notes_key),
        )
        if b3.button("Finish Workout"):
            final_paused_seconds = float(st.session_state.get("session_paused_seconds", 0.0) or 0.0)
            if st.session_state.get("session_paused") and st.session_state.get("session_pause_started_at"):
                try:
                    final_paused_seconds += (datetime.now() - datetime.fromisoformat(st.session_state["session_pause_started_at"])).total_seconds()
                except Exception:
                    pass

            clear_workout_drafts(active_session_id)
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
    recovery_status = "poor" if readiness["status"] in {"Reduce", "Modify"} else "normal"

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
        exercise_id = int(ex["id"])
        draft = get_workout_draft(active_session_id, exercise_id) if active_session_id else None

        weight_key = f"w_{active_session_id}_{exercise_id}"
        reps_key = f"r_{active_session_id}_{exercise_id}"
        rir_key = f"rir_{active_session_id}_{exercise_id}"
        notes_key = f"notes_{active_session_id}_{exercise_id}"
        reset_key = f"reset_draft_{active_session_id}_{exercise_id}"

        if st.session_state.pop(reset_key, False):
            for widget_key in (weight_key, reps_key, rir_key, notes_key):
                st.session_state.pop(widget_key, None)
            draft = None

        if weight_key not in st.session_state:
            st.session_state[weight_key] = float(draft["weight"] if draft and draft["weight"] is not None else default_weight)
        if reps_key not in st.session_state:
            st.session_state[reps_key] = str(draft["reps"] if draft and draft["reps"] is not None else default_reps)
        if rir_key not in st.session_state:
            st.session_state[rir_key] = float(draft["rir"] if draft and draft["rir"] is not None else 2.0)
        if notes_key not in st.session_state:
            st.session_state[notes_key] = str(draft["notes"] if draft and draft["notes"] is not None else "")

        callback_args = (active_session_id, exercise_id, weight_key, reps_key, rir_key, notes_key)
        c1, c2 = st.columns(2)
        weight_input = c1.number_input(
            "Actual Weight / Load", min_value=0.0, step=2.5, key=weight_key,
            on_change=persist_exercise_draft, args=callback_args,
        )
        reps_input = c2.text_input(
            "Actual Reps / Time / Steps", placeholder="Example: 8,8,7,6", key=reps_key,
            on_change=persist_exercise_draft, args=callback_args,
        )
        rir_input = st.slider(
            "RIR", 0.0, 5.0, 0.5, key=rir_key,
            on_change=persist_exercise_draft, args=callback_args,
        )
        if compact_mode:
            notes_input = st.session_state.get(notes_key, "")
        else:
            notes_input = st.text_area(
                "Notes", key=notes_key,
                on_change=persist_exercise_draft, args=callback_args,
            )

        if draft:
            st.caption(f"Draft restored · Last updated {short_time(draft['updated_at'])}")
        elif active_session_id:
            st.caption("Draft autosaves as you enter each field.")

        if st.button("Save Exercise Log", key=f"save_log_{active_session_id}_{exercise_id}"):
            if reps_input.strip():
                save_workout_log(str(date.today()), exercise_id, weight_input, reps_input, rir_input, notes_input)
                if active_session_id:
                    delete_workout_draft(active_session_id, exercise_id)
                st.session_state[reset_key] = True
                st.session_state["momentum_last_set_saved_at"] = datetime.now().isoformat(timespec="seconds")
                st.success(f"{ex['exercise_name']} saved. Rest timer started.")
                st.rerun()
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

        st.markdown("---")
        st.subheader("Delete Journal Entry")
        st.caption("Changing the program start date does not delete training history. Use this section to remove the selected session.")

        delete_logs_too = st.checkbox(
            "Also delete workout-set logs recorded during this session",
            value=False,
            key=f"delete_session_logs_{int(selected_session['id'])}",
        )
        confirm_session_delete = st.checkbox(
            "I understand this permanently deletes the selected journal entry.",
            key=f"confirm_session_delete_{int(selected_session['id'])}",
        )

        if st.button(
            "Delete Selected Workout Session",
            type="secondary",
            key=f"delete_session_{int(selected_session['id'])}",
        ):
            if not confirm_session_delete:
                st.error("Confirm the deletion first.")
            else:
                deleted = delete_workout_session(
                    int(selected_session["id"]),
                    delete_session_logs=delete_logs_too,
                )
                if deleted:
                    st.success("Workout session deleted.")
                    st.rerun()
                else:
                    st.error("The workout session could not be found.")

elif page == "Running":
    st.header("Running")
    st.caption("Build running capacity gradually while managing effort and lower-body stress.")

    weekly = get_running_summary(7).iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Runs · 7 days", int(weekly["sessions"]))
    c2.metric("Minutes", f"{float(weekly['minutes']):.0f}")
    c3.metric("Distance", f"{float(weekly['miles']):.2f} mi")
    c4.metric("Average RPE", f"{float(weekly['average_rpe']):.1f}")

    with st.form("running_session_form", clear_on_submit=True):
        st.subheader("Log Run")
        f1, f2, f3 = st.columns(3)
        run_date = f1.date_input("Date", value=date.today())
        run_type = f2.selectbox("Session", ["Easy Run", "Intervals", "Long Run", "Recovery Run", "Walk/Run"])
        planned_minutes = f3.number_input("Planned minutes", min_value=0, step=5, value=30)

        f4, f5, f6 = st.columns(3)
        completed_minutes = f4.number_input("Completed minutes", min_value=1, step=1, value=30)
        distance_miles = f5.number_input("Distance · miles", min_value=0.0, step=0.1, value=0.0)
        run_walk_pattern = f6.text_input("Run/walk pattern", placeholder="Example: 2 min run / 1 min walk")

        f7, f8 = st.columns(2)
        run_rpe = f7.slider("Effort · RPE", 1, 10, 5)
        run_pain = f8.slider("Pain/discomfort", 1, 5, 1)
        run_notes = st.text_area("Notes", placeholder="Breathing, route, discomfort, or what to adjust next time")

        if st.form_submit_button("Save Run", type="primary"):
            save_running_session(
                run_date, run_type, planned_minutes, completed_minutes,
                distance_miles, run_walk_pattern, run_rpe, run_pain, run_notes,
            )
            st.success("Run saved.")
            st.rerun()

    runs = get_running_sessions()
    if runs.empty:
        render_empty_state("No running sessions yet. Your first entry will establish a baseline.")
    else:
        st.subheader("Running History")
        st.dataframe(
            runs[["session_date", "run_type", "planned_minutes", "completed_minutes",
                  "distance_miles", "run_walk_pattern", "rpe", "pain", "notes"]],
            use_container_width=True,
            hide_index=True,
        )
        with st.expander("Delete a running entry"):
            run_ids = runs["id"].tolist()
            selected_run_id = st.selectbox("Entry", run_ids, format_func=lambda value: (
                f"{runs.loc[runs['id'] == value, 'session_date'].iloc[0]} — "
                f"{runs.loc[runs['id'] == value, 'run_type'].iloc[0]}"
            ))
            confirm_run_delete = st.checkbox("I understand this permanently deletes this running entry.")
            if st.button("Delete Selected Run"):
                if confirm_run_delete:
                    delete_running_session(selected_run_id)
                    st.success("Running entry deleted.")
                    st.rerun()
                else:
                    st.error("Confirm the deletion first.")

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
    st.caption("Your training phase, personal records, and consistency score.")

    score, score_details = calculate_training_momentum_score()
    weeks_left = max(0, 12 - week)

    p1, p2, p3 = st.columns(3)
    p1.metric("Current Week", f"{week}/12")
    p2.metric("Weeks Left", weeks_left)
    p3.metric("Momentum Score", f"{score}/100")

    st.info("Bodyweight, nutrition, measurements, and daily health logs are tracked in your Excel planner.")

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
    analytics_page()

elif page == "Workout Log":
   workout_page()

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
   exports_page()

elif page == "Settings":
    settings_page()
