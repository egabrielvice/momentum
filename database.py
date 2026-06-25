
import sqlite3
from pathlib import Path
from datetime import date, datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "momentum.db"

WORKOUT_EXERCISES = [
    ("Day 1", 1, "Shoulders + Core", "Seated DB Press", "Shoulders", 4, 6, 8, "weight"),
    ("Day 1", 1, "Shoulders + Core", "Seated DB Lateral Raise", "Side Delts", 4, 12, 15, "weight"),
    ("Day 1", 1, "Shoulders + Core", "Rear Delt Machine", "Rear Delts", 3, 12, 15, "weight"),
    ("Day 1", 1, "Shoulders + Core", "Face Pull", "Rear Delts", 3, 12, 15, "weight"),
    ("Day 1", 1, "Shoulders + Core", "Cable Crunch", "Core", 3, 10, 15, "core_load"),
    ("Day 1", 1, "Shoulders + Core", "Plank", "Core", 3, 45, 60, "time"),

    ("Day 2", 2, "Glutes A", "Hip Thrust", "Glutes", 4, 6, 8, "weight"),
    ("Day 2", 2, "Glutes A", "Romanian Deadlift", "Hamstrings", 3, 8, 10, "weight"),
    ("Day 2", 2, "Glutes A", "Bulgarian Split Squat", "Glutes", 3, 8, 10, "weight"),
    ("Day 2", 2, "Glutes A", "Hamstring Curl", "Hamstrings", 3, 10, 12, "weight"),
    ("Day 2", 2, "Glutes A", "Walking Lunges", "Glutes", 2, 20, 20, "steps"),

    ("Day 3", 3, "Conditioning + Core", "Lat Pulldown", "Back", 3, 10, 12, "weight"),
    ("Day 3", 3, "Conditioning + Core", "Seated Cable Row", "Back", 3, 10, 12, "weight"),
    ("Day 3", 3, "Conditioning + Core", "Incline Treadmill", "Cardio", 1, 30, 30, "cardio_time"),
    ("Day 3", 3, "Conditioning + Core", "Cable Crunch", "Core", 3, 12, 15, "core_load"),
    ("Day 3", 3, "Conditioning + Core", "Hanging Leg Raise", "Core", 3, 10, 15, "reps"),
    ("Day 3", 3, "Conditioning + Core", "Plank", "Core", 3, 60, 60, "time"),
    ("Day 3", 3, "Conditioning + Core", "Push-Ups", "Chest", 2, 8, 15, "optional_reps"),

    ("Day 4", 4, "Shoulders + Core", "Arnold Press", "Shoulders", 3, 8, 10, "weight"),
    ("Day 4", 4, "Shoulders + Core", "Cable Lateral Raise", "Side Delts", 4, 12, 15, "weight"),
    ("Day 4", 4, "Shoulders + Core", "Rear Delt Machine", "Rear Delts", 3, 15, 15, "weight"),
    ("Day 4", 4, "Shoulders + Core", "Face Pull", "Rear Delts", 3, 15, 15, "weight"),
    ("Day 4", 4, "Shoulders + Core", "Hanging Leg Raise", "Core", 3, 10, 15, "reps"),
    ("Day 4", 4, "Shoulders + Core", "Plank", "Core", 3, 45, 60, "time"),

    ("Day 5", 5, "Glutes B", "Squat", "Glutes", 3, 8, 10, "weight"),
    ("Day 5", 5, "Glutes B", "Hip Thrust", "Glutes", 3, 10, 12, "weight"),
    ("Day 5", 5, "Glutes B", "Step-Ups", "Glutes", 3, 10, 10, "each_leg"),
    ("Day 5", 5, "Glutes B", "Cable Kickbacks", "Glutes", 3, 12, 15, "weight"),
    ("Day 5", 5, "Glutes B", "Hamstring Curl", "Hamstrings", 3, 10, 12, "weight"),

    ("Day 6", 6, "Conditioning + Core", "Assisted Pull-Up or Lat Pulldown", "Back", 3, 10, 12, "weight"),
    ("Day 6", 6, "Conditioning + Core", "Chest-Supported Row or Seated Row", "Back", 3, 10, 12, "weight"),
    ("Day 6", 6, "Conditioning + Core", "Incline Treadmill", "Cardio", 1, 30, 30, "cardio_time"),
    ("Day 6", 6, "Conditioning + Core", "Cable Crunch", "Core", 3, 12, 15, "core_load"),
    ("Day 6", 6, "Conditioning + Core", "Leg Raises", "Core", 3, 12, 15, "reps"),
    ("Day 6", 6, "Conditioning + Core", "Weighted Plank", "Core", 3, 45, 60, "time"),
    ("Day 6", 6, "Conditioning + Core", "Mobility Work", "Mobility", 1, 10, 10, "time"),

    ("Day 7", 7, "Recovery Walk + Mobility", "Long Walk", "Cardio", 1, 10000, 15000, "steps"),
    ("Day 7", 7, "Recovery Walk + Mobility", "Mobility", "Mobility", 1, 10, 30, "time"),
    ("Day 7", 7, "Recovery Walk + Mobility", "Stretching", "Mobility", 1, 10, 30, "time"),
]

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name TEXT NOT NULL UNIQUE,
            duration_weeks INTEGER NOT NULL DEFAULT 12,
            goal TEXT
        )
    """)

    cur.execute("""
        INSERT OR IGNORE INTO programs (id, program_name, duration_weeks, goal)
        VALUES (1, 'Shoulder Specialization', 12, 'Build capped shoulders, maintain glutes, improve core strength.')
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER NOT NULL DEFAULT 1,
            day TEXT NOT NULL,
            day_order INTEGER NOT NULL,
            workout_name TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            target_sets INTEGER NOT NULL,
            min_reps INTEGER NOT NULL,
            max_reps INTEGER NOT NULL,
            progression_type TEXT NOT NULL,
            UNIQUE(program_id, day, exercise_name)
        )
    """)

    existing_columns = [row[1] for row in cur.execute("PRAGMA table_info(exercises)").fetchall()]
    if "program_id" not in existing_columns:
        cur.execute("ALTER TABLE exercises ADD COLUMN program_id INTEGER NOT NULL DEFAULT 1")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            exercise_id INTEGER NOT NULL,
            weight REAL,
            reps TEXT NOT NULL,
            rir REAL,
            notes TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workout_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            completion_date TEXT NOT NULL,
            day TEXT NOT NULL,
            day_order INTEGER NOT NULL,
            workout_name TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkin_date TEXT NOT NULL UNIQUE,
            body_weight REAL,
            sleep_hours REAL,
            energy INTEGER,
            stress INTEGER,
            protein_hit INTEGER,
            water_hit INTEGER,
            steps_hit INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cur.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('phase_start_date', ?)", (str(date.today()),))
    cur.execute(
    "INSERT OR IGNORE INTO app_settings (key, value) VALUES ('active_program_id', '1')"
)
    for item in WORKOUT_EXERCISES:
        cur.execute("""
            INSERT OR IGNORE INTO exercises
            (program_id, day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item)
    conn.commit()
    conn.close()
    ensure_program_archive_column()

def fetch_df(query, params=()):
    import pandas as pd
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key, value):
    execute("""
        INSERT INTO app_settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
    """, (key, value))

def current_week():
    start = get_setting("phase_start_date", str(date.today()))
    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    return max(1, min(12, ((date.today() - start_date).days // 7) + 1))

def get_phase(week):
    if week <= 4:
        return "Base Phase"
    if week <= 8:
        return "Progression Phase"
    if week == 9:
        return "Deload"
    return "Peak Phase"

def get_programs():
    ensure_program_archive_column()
    return fetch_df("SELECT * FROM programs ORDER BY is_archived, id")

def get_active_program_id():
    return int(get_setting("active_program_id", "1"))

def set_active_program(program_id):
    set_setting("active_program_id", str(int(program_id)))

def create_program(program_name, duration_weeks=12, goal=""):
    execute("""
        INSERT OR IGNORE INTO programs (program_name, duration_weeks, goal)
        VALUES (?, ?, ?)
    """, (program_name, int(duration_weeks), goal))


def add_workout_day(program_id, day, day_order, workout_name):
    """
    Adds a workout day shell by inserting a placeholder exercise.
    The placeholder keeps the day visible until real exercises are added.
    """
    execute("""
        INSERT OR IGNORE INTO exercises
        (program_id, day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(program_id),
        day,
        int(day_order),
        workout_name,
        "__DAY_PLACEHOLDER__",
        "System",
        0,
        0,
        0,
        "placeholder"
    ))

def delete_workout_day(program_id, day):
    execute("DELETE FROM exercises WHERE program_id = ? AND day = ?", (int(program_id), day))

def add_exercise_to_day(program_id, day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type):
    execute("""
        INSERT OR IGNORE INTO exercises
        (program_id, day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(program_id),
        day,
        int(day_order),
        workout_name,
        exercise_name,
        muscle_group,
        int(target_sets),
        int(min_reps),
        int(max_reps),
        progression_type
    ))

    execute("""
        DELETE FROM exercises
        WHERE program_id = ? AND day = ? AND exercise_name = '__DAY_PLACEHOLDER__'
    """, (int(program_id), day))

def delete_exercise(exercise_id):
    execute("DELETE FROM exercises WHERE id = ?", (int(exercise_id),))

def get_exercises(day=None):
    program_id = get_active_program_id()
    if day:
        return fetch_df("""
            SELECT * FROM exercises
            WHERE program_id = ? AND day = ? AND exercise_name != '__DAY_PLACEHOLDER__'
            ORDER BY id
        """, (program_id, day))
    return fetch_df("""
        SELECT * FROM exercises
        WHERE program_id = ? AND exercise_name != '__DAY_PLACEHOLDER__'
        ORDER BY day_order, id
    """, (program_id,))


def get_program_exercises(program_id):
    return fetch_df("""
        SELECT *
        FROM exercises
        WHERE program_id = ?
        ORDER BY day_order, day, id
    """, (int(program_id),))

def get_workout_days():
    program_id = get_active_program_id()
    return fetch_df("SELECT DISTINCT day, day_order, workout_name FROM exercises WHERE program_id = ? ORDER BY day_order", (program_id,))

def reset_workout_progress():
    execute("DELETE FROM workout_completions")

def get_latest_completion():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT completion_date, day, day_order, workout_name FROM workout_completions ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row

def get_next_workout():
    days = get_workout_days()
    latest = get_latest_completion()
    if days.empty:
        return {"day": "No Day", "day_order": 0, "workout_name": "No workout days created"}
    if latest is None:
        return days.iloc[0].to_dict()
    max_order = int(days["day_order"].max())
    next_order = 1 if int(latest[2]) >= max_order else int(latest[2]) + 1
    next_day = days[days["day_order"] == next_order]
    if next_day.empty:
        return days.iloc[0].to_dict()
    return next_day.iloc[0].to_dict()

def mark_workout_complete(day, day_order, workout_name):
    execute("INSERT INTO workout_completions (completion_date, day, day_order, workout_name) VALUES (?, ?, ?, ?)",
            (str(date.today()), day, int(day_order), workout_name))

def get_latest_log(exercise_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT weight, reps, rir, notes, log_date
        FROM workout_logs
        WHERE exercise_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (int(exercise_id),))
    row = cur.fetchone()
    conn.close()
    return row

def parse_reps(reps_text):
    values = []
    for part in str(reps_text).replace(" ", "").split(","):
        try:
            values.append(float(part))
        except ValueError:
            pass
    return values

def count_stall_sessions(exercise_id):
    df = fetch_df("SELECT weight, reps FROM workout_logs WHERE exercise_id = ? ORDER BY id DESC LIMIT 3", (int(exercise_id),))
    return len(df) == 3 and len(set(zip(df["weight"], df["reps"]))) == 1

def recommendation(exercise, latest_log, recovery_status="normal"):
    target_sets = int(exercise["target_sets"])
    min_reps = int(exercise["min_reps"])
    max_reps = int(exercise["max_reps"])
    progression_type = exercise["progression_type"]

    if latest_log is None:
        return "Baseline session: choose a controlled level and log clean performance."

    weight, reps_text, rir, notes, log_date = latest_log
    reps = parse_reps(reps_text)

    if recovery_status == "poor":
        return f"Recovery is low. Match last session instead of chasing progression: {weight or 0:g}, reps {reps_text}."

    if progression_type in ["time", "cardio_time"]:
        return f"Goal: reach {max_reps} on all sets/minutes. Increase difficulty after that."

    if progression_type == "steps":
        return f"Target range: {min_reps:,}–{max_reps:,} steps."

    if len(reps) < target_sets:
        return f"Log all {target_sets} sets. Keep current level until data is complete."

    if all(r >= max_reps for r in reps):
        if rir is not None and rir >= 3:
            return f"Top reps reached, but RIR is high. Keep {weight or 0:g} and use stricter form/control."
        return f"Increase weight next session. Last: {weight or 0:g} for {reps_text}."

    if any(r < min_reps for r in reps):
        return f"Below target range. Keep or reduce from {weight or 0:g} and rebuild clean reps."

    return f"Stay at {weight or 0:g} and beat last reps: {reps_text}."

def update_workout_log(log_id, log_date, weight, reps, rir, notes):
    execute("""
        UPDATE workout_logs
        SET log_date = ?, weight = ?, reps = ?, rir = ?, notes = ?
        WHERE id = ?
    """, (log_date, weight, reps, rir, notes, int(log_id)))

def delete_workout_log(log_id):
    execute("DELETE FROM workout_logs WHERE id = ?", (int(log_id),))


def save_workout_log(log_date, exercise_id, weight, reps, rir, notes):
    execute("INSERT INTO workout_logs (log_date, exercise_id, weight, reps, rir, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (log_date, int(exercise_id), weight, reps, rir, notes))

def save_checkin(checkin_date, body_weight, sleep_hours, energy, stress, protein_hit, water_hit, steps_hit):
    execute("""
        INSERT INTO daily_checkins
        (checkin_date, body_weight, sleep_hours, energy, stress, protein_hit, water_hit, steps_hit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(checkin_date) DO UPDATE SET
            body_weight=excluded.body_weight,
            sleep_hours=excluded.sleep_hours,
            energy=excluded.energy,
            stress=excluded.stress,
            protein_hit=excluded.protein_hit,
            water_hit=excluded.water_hit,
            steps_hit=excluded.steps_hit
    """, (checkin_date, body_weight, sleep_hours, energy, stress, protein_hit, water_hit, steps_hit))

def save_bodyweight_entry(entry_date, body_weight):
    execute("""
        INSERT INTO daily_checkins (checkin_date, body_weight)
        VALUES (?, ?)
        ON CONFLICT(checkin_date) DO UPDATE SET
            body_weight=excluded.body_weight
    """, (entry_date, body_weight))

def clear_bodyweight_entry(entry_date):
    execute("""
        UPDATE daily_checkins
        SET body_weight = NULL
        WHERE checkin_date = ?
    """, (entry_date,))


def get_today_recovery():
    df = fetch_df("SELECT * FROM daily_checkins WHERE checkin_date = ?", (str(date.today()),))
    if df.empty:
        return "normal"
    row = df.iloc[0]
    if row["sleep_hours"] < 6 or row["energy"] <= 2 or row["stress"] >= 4:
        return "poor"
    return "normal"



def update_program(program_id, program_name, duration_weeks, goal):
    execute("""
        UPDATE programs
        SET program_name = ?, duration_weeks = ?, goal = ?
        WHERE id = ?
    """, (program_name, int(duration_weeks), goal, int(program_id)))

def duplicate_program(source_program_id, new_program_name):
    """
    Option A duplication:
    Creates a full copy of the selected program, including all days and exercises.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT duration_weeks, goal
        FROM programs
        WHERE id = ?
    """, (int(source_program_id),))
    source = cur.fetchone()

    if source is None:
        conn.close()
        return

    duration_weeks, goal = source

    cur.execute("""
        INSERT INTO programs (program_name, duration_weeks, goal)
        VALUES (?, ?, ?)
    """, (new_program_name, int(duration_weeks), goal))

    new_program_id = cur.lastrowid

    cur.execute("""
        SELECT day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type
        FROM exercises
        WHERE program_id = ?
        ORDER BY day_order, id
    """, (int(source_program_id),))

    rows = cur.fetchall()

    for row in rows:
        cur.execute("""
            INSERT OR IGNORE INTO exercises
            (program_id, day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_program_id, *row))

    conn.commit()
    conn.close()

def delete_program(program_id):
    """
    Deletes a program and its exercise templates.
    Protected: Shoulder Specialization, id 1.
    """
    if int(program_id) == 1:
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM exercises WHERE program_id = ?", (int(program_id),))
    cur.execute("DELETE FROM programs WHERE id = ?", (int(program_id),))
    cur.execute("""
        UPDATE app_settings
        SET value = '1'
        WHERE key = 'active_program_id' AND value = ?
    """, (str(int(program_id)),))
    conn.commit()
    conn.close()

def update_workout_day(program_id, old_day, new_day, new_day_order, new_workout_name):
    """
    Updates a workout day across all exercises in that day.
    """
    execute("""
        UPDATE exercises
        SET day = ?, day_order = ?, workout_name = ?
        WHERE program_id = ? AND day = ?
    """, (new_day, int(new_day_order), new_workout_name, int(program_id), old_day))

def update_exercise_template(exercise_id, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type):
    execute("""
        UPDATE exercises
        SET exercise_name = ?, muscle_group = ?, target_sets = ?, min_reps = ?, max_reps = ?, progression_type = ?
        WHERE id = ?
    """, (
        exercise_name,
        muscle_group,
        int(target_sets),
        int(min_reps),
        int(max_reps),
        progression_type,
        int(exercise_id)
    ))

def move_exercise_to_day(exercise_id, new_day, new_day_order, new_workout_name):
    execute("""
        UPDATE exercises
        SET day = ?, day_order = ?, workout_name = ?
        WHERE id = ?
    """, (new_day, int(new_day_order), new_workout_name, int(exercise_id)))

def duplicate_exercise_to_day(exercise_id, new_day, new_day_order, new_workout_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT program_id, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type
        FROM exercises
        WHERE id = ?
    """, (int(exercise_id),))
    row = cur.fetchone()

    if row is not None:
        program_id, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type = row

        cur.execute("""
            INSERT OR IGNORE INTO exercises
            (program_id, day, day_order, workout_name, exercise_name, muscle_group, target_sets, min_reps, max_reps, progression_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(program_id),
            new_day,
            int(new_day_order),
            new_workout_name,
            exercise_name,
            muscle_group,
            int(target_sets),
            int(min_reps),
            int(max_reps),
            progression_type
        ))

    conn.commit()
    conn.close()


def ensure_program_archive_column():
    conn = get_connection()
    cur = conn.cursor()
    columns = [row[1] for row in cur.execute("PRAGMA table_info(programs)").fetchall()]
    if "is_archived" not in columns:
        cur.execute("ALTER TABLE programs ADD COLUMN is_archived INTEGER NOT NULL DEFAULT 0")
    conn.commit()
    conn.close()

def archive_program(program_id):
    if int(program_id) == 1:
        return
    ensure_program_archive_column()
    execute("UPDATE programs SET is_archived = 1 WHERE id = ?", (int(program_id),))

def unarchive_program(program_id):
    ensure_program_archive_column()
    execute("UPDATE programs SET is_archived = 0 WHERE id = ?", (int(program_id),))

def get_muscle_volume_summary():
    return fetch_df("""
        SELECT
            e.muscle_group,
            COUNT(wl.id) AS logs,
            ROUND(SUM(COALESCE(wl.weight, 0) * (
                CASE
                    WHEN wl.reps IS NULL THEN 0
                    ELSE 1
                END
            )), 1) AS raw_load
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        GROUP BY e.muscle_group
        ORDER BY logs DESC
    """)

def get_weekly_workout_summary():
    return fetch_df("""
        SELECT
            completion_date,
            COUNT(*) AS completed_workouts
        FROM workout_completions
        GROUP BY completion_date
        ORDER BY completion_date ASC
    """)

def get_exercise_frequency():
    return fetch_df("""
        SELECT
            e.exercise_name,
            e.muscle_group,
            COUNT(wl.id) AS logs
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        GROUP BY e.exercise_name, e.muscle_group
        ORDER BY logs DESC
    """)

def get_program_count_summary():
    ensure_program_archive_column()
    return fetch_df("""
        SELECT
            SUM(CASE WHEN is_archived = 0 THEN 1 ELSE 0 END) AS active_programs,
            SUM(CASE WHEN is_archived = 1 THEN 1 ELSE 0 END) AS archived_programs,
            COUNT(*) AS total_programs
        FROM programs
    """)



def create_database_backup():
    from datetime import datetime
    import shutil

    if not DB_PATH.exists():
        return None

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    backup_path = BACKUP_DIR / f"momentum_backup_{timestamp}.db"
    shutil.copy2(DB_PATH, backup_path)
    return str(backup_path)

def get_latest_backup():
    backups = sorted(BACKUP_DIR.glob("momentum_backup_*.db"), reverse=True)
    return str(backups[0]) if backups else "No backups yet"

def get_database_path():
    return str(DB_PATH)


def get_export_tables():
    return {
        "programs": fetch_df("SELECT * FROM programs ORDER BY id"),
        "exercises": fetch_df("SELECT * FROM exercises ORDER BY program_id, day_order, id"),
        "workout_logs": fetch_df("SELECT * FROM workout_logs ORDER BY id"),
        "workout_completions": fetch_df("SELECT * FROM workout_completions ORDER BY id"),
        "daily_checkins": fetch_df("SELECT * FROM daily_checkins ORDER BY checkin_date"),
        "app_settings": fetch_df("SELECT * FROM app_settings ORDER BY key"),
    }

def reset_test_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM workout_logs")
    cur.execute("DELETE FROM daily_checkins")
    cur.execute("DELETE FROM workout_completions")
    conn.commit()
    conn.close()

def get_database_path():
    return str(DB_PATH)

def get_latest_backup():
    return "No backups yet"

def create_database_backup():
    return None