import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
from database import *


def total_reps(reps):
    total = 0
    for part in str(reps).replace(" ", "").split(","):
        try:
            total += float(part)
        except ValueError:
            pass
    return total


def get_personal_records():
    logs = fetch_df("""
        SELECT wl.log_date, e.exercise_name, e.muscle_group, wl.weight, wl.reps
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        WHERE wl.weight IS NOT NULL AND wl.weight > 0
    """)

    if logs.empty:
        return logs

    logs["total_reps"] = logs["reps"].apply(total_reps)
    logs["volume"] = logs["weight"] * logs["total_reps"]

    records = []
    for exercise_name, group in logs.groupby("exercise_name"):
        best_weight = group["weight"].max()
        best_reps = group["total_reps"].max()
        best_volume_row = group.loc[group["volume"].idxmax()]

        records.append({
            "Exercise": exercise_name,
            "Muscle Group": best_volume_row["muscle_group"],
            "Best Weight": round(best_weight, 1),
            "Best Total Reps": round(best_reps, 1),
            "Best Volume": round(best_volume_row["volume"], 1),
            "PR Date": best_volume_row["log_date"],
        })

    import pandas as pd
    return pd.DataFrame(records).sort_values("Best Volume", ascending=False)


def get_today_checkin():
    df = fetch_df("SELECT * FROM daily_checkins WHERE checkin_date = ?", (str(date.today()),))
    return None if df.empty else df.iloc[0]

def calculate_momentum_score():
    score = 0
    details = []

    checkin = get_today_checkin()
    completions_today = fetch_df("SELECT * FROM workout_completions WHERE completion_date = ?", (str(date.today()),))

    if not completions_today.empty:
        score += 30
        details.append("Workout completed: +30")
    else:
        details.append("Workout completed: +0")

    if checkin is not None:
        if int(checkin["protein_hit"] or 0) == 1:
            score += 20
            details.append("Protein hit: +20")
        else:
            details.append("Protein hit: +0")

        if int(checkin["steps_hit"] or 0) == 1:
            score += 20
            details.append("Steps hit: +20")
        else:
            details.append("Steps hit: +0")

        if int(checkin["water_hit"] or 0) == 1:
            score += 10
            details.append("Water hit: +10")
        else:
            details.append("Water hit: +0")

        sleep = float(checkin["sleep_hours"] or 0)
        if sleep >= 7:
            score += 20
            details.append("Sleep 7h+: +20")
        elif sleep >= 6:
            score += 10
            details.append("Sleep 6h+: +10")
        else:
            details.append("Sleep below 6h: +0")
    else:
        details.append("No daily check-in yet.")

    return score, details

def smart_progression_plan(exercise, latest_log):
    if latest_log is None:
        return {
            "Next Weight": "Baseline",
            "Target": f"{exercise['target_sets']} sets × {exercise['min_reps']}–{exercise['max_reps']}",
            "Reason": "No previous log exists yet."
        }

    weight, reps_text, rir, notes, log_date = latest_log
    reps = []
    for part in str(reps_text).replace(" ", "").split(","):
        try:
            reps.append(float(part))
        except ValueError:
            pass

    target_sets = int(exercise["target_sets"])
    min_reps = int(exercise["min_reps"])
    max_reps = int(exercise["max_reps"])
    progression_type = exercise["progression_type"]

    if progression_type in ["time", "cardio_time", "steps"]:
        return {
            "Next Weight": "N/A",
            "Target": f"Reach {max_reps} cleanly",
            "Reason": "Progress this exercise by duration, steps, or difficulty."
        }

    if len(reps) < target_sets:
        return {
            "Next Weight": weight,
            "Target": f"Complete all {target_sets} sets",
            "Reason": "Previous log did not include all target sets."
        }

    if all(r >= max_reps for r in reps):
        if rir is not None and float(rir) <= 2:
            suggested = float(weight or 0) + 5
            return {
                "Next Weight": suggested,
                "Target": f"{target_sets} sets × {min_reps}",
                "Reason": "Top rep range reached with low RIR. Increase load next session."
            }
        return {
            "Next Weight": weight,
            "Target": f"{target_sets} sets × {max_reps}",
            "Reason": "Top reps reached, but RIR is still high. Keep load and improve control."
        }

    if any(r < min_reps for r in reps):
        return {
            "Next Weight": weight,
            "Target": f"Rebuild toward {min_reps}+ reps per set",
            "Reason": "Performance fell below the target range."
        }

    return {
        "Next Weight": weight,
        "Target": f"Beat previous reps: {reps_text}",
        "Reason": "Stay at the same load and progress reps first."
    }



def dynamic_greeting():
    return "Welcome back."

def get_recent_workouts(limit=5):
    return fetch_df("""
        SELECT completion_date, day, workout_name
        FROM workout_completions
        ORDER BY id DESC
        LIMIT ?
    """, (int(limit),))


def format_duration_from_minutes(minutes):
    total_seconds = int(float(minutes or 0) * 60)
    hours = total_seconds // 3600
    mins = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{mins:02d}:{secs:02d}"


def format_elapsed_since(started_at, paused_seconds=0):
    try:
        started = datetime.fromisoformat(str(started_at))
        elapsed = max(0, (datetime.now() - started).total_seconds() - float(paused_seconds or 0))
        return format_duration_from_minutes(elapsed / 60)
    except Exception:
        return "00:00:00"


def short_time(timestamp_text):
    try:
        return datetime.fromisoformat(str(timestamp_text)).strftime("%I:%M %p").lstrip("0")
    except Exception:
        return "—"


def duration_label(minutes):
    try:
        minutes = float(minutes or 0)
    except Exception:
        minutes = 0
    hours = int(minutes // 60)
    mins = int(round(minutes % 60))
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def render_empty_state(message):
    st.markdown(f'<div class="momentum-empty-state">{message}</div>', unsafe_allow_html=True)


def estimate_1rm(weight, reps):
    try:
        weight = float(weight or 0)
        reps = float(reps or 0)
        if weight <= 0 or reps <= 0:
            return 0
        return round(weight * (1 + reps / 30), 1)
    except Exception:
        return 0


def safe_reps_list(reps_text):
    values = []
    for part in str(reps_text).replace(" ", "").split(","):
        try:
            values.append(float(part))
        except ValueError:
            pass
    return values


def session_logs_between(started_at, ended_at):
    return fetch_df("""
        SELECT wl.log_date, wl.created_at, e.day, e.workout_name, e.exercise_name, e.muscle_group,
               wl.weight, wl.reps, wl.rir, wl.notes
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        WHERE wl.created_at IS NOT NULL
          AND wl.created_at >= ?
          AND wl.created_at <= ?
        ORDER BY wl.created_at ASC, wl.id ASC
    """, (str(started_at), str(ended_at)))


def render_live_timer_component(started_at, paused_seconds=0, paused=False, pause_started_at=None):
    """Renders a live client-side timer without changing the Streamlit layout."""
    try:
        started = str(started_at)
        paused_at = "" if not pause_started_at else str(pause_started_at)
        paused_total = float(paused_seconds or 0)
    except Exception:
        started = ""
        paused_at = ""
        paused_total = 0

    components.html(
        f"""
        <div id="momentum-live-timer" style="
            font-family: Inter, Arial, sans-serif;
            color: #9B1C1C;
            font-size: 26px;
            font-weight: 880;
            letter-spacing: -0.04em;
            margin: 0 0 4px 0;
        ">00:00:00</div>
        <script>
            const startedAt = new Date("{started}");
            const paused = {str(bool(paused)).lower()};
            const pausedAtText = "{paused_at}";
            const pausedSeconds = {paused_total};
            const timerEl = document.getElementById("momentum-live-timer");

            function pad(n) {{ return String(n).padStart(2, "0"); }}
            function fmt(total) {{
                total = Math.max(0, Math.floor(total));
                const h = Math.floor(total / 3600);
                const m = Math.floor((total % 3600) / 60);
                const s = total % 60;
                return `${{pad(h)}}:${{pad(m)}}:${{pad(s)}}`;
            }}
            function tick() {{
                if (!timerEl || isNaN(startedAt.getTime())) return;
                const end = paused && pausedAtText ? new Date(pausedAtText) : new Date();
                const elapsed = ((end - startedAt) / 1000) - pausedSeconds;
                timerEl.textContent = fmt(elapsed);
            }}
            tick();
            if (!paused) setInterval(tick, 1000);
        </script>
        """,
        height=42,
    )
