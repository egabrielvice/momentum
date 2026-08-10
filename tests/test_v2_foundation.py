import sys
import tempfile
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "App"
sys.path.insert(0, str(APP_DIR))

import database


class MomentumV2FoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        data_dir = Path(self.temp_dir.name)
        database.DATA_DIR = data_dir
        database.DB_PATH = data_dir / "momentum.db"
        database.BACKUP_DIR = data_dir / "backups"
        database.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        database.init_db()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_readiness_score_and_recommendation(self):
        database.save_readiness_checkin(5, 5, 1, 1, 5)
        readiness = database.get_today_readiness()
        self.assertEqual(readiness["status"], "Ready")
        self.assertGreaterEqual(readiness["score"], 70)

    def test_pain_changes_training_recommendation(self):
        database.save_readiness_checkin(4, 4, 2, 5, 4)
        readiness = database.get_today_readiness()
        self.assertEqual(readiness["status"], "Modify")

    def test_schedule_overrides_sequence_for_today(self):
        days = database.get_workout_days()
        selected = days.iloc[2]
        database.schedule_workout(
            database.local_today(),
            selected["day"],
            int(selected["day_order"]),
            selected["workout_name"],
        )
        next_workout = database.get_next_workout()
        self.assertEqual(next_workout["day"], selected["day"])

    def test_completing_workout_closes_today_schedule(self):
        database.schedule_workout(database.local_today(), "Day 1", 1, "Shoulders + Core")
        database.mark_workout_complete("Day 1", 1, "Shoulders + Core")
        self.assertIsNone(database.get_scheduled_workout(database.local_today()))

    def test_second_launch_creates_daily_backup(self):
        database.init_db()
        backups = list(database.BACKUP_DIR.glob("momentum_daily_*.db"))
        self.assertEqual(len(backups), 1)

    def test_running_session_summary(self):
        database.save_quick_run(database.local_today(), 28, 3.4, "Easy Run")
        summary = database.get_running_summary(7).iloc[0]
        self.assertEqual(int(summary["sessions"]), 1)
        self.assertEqual(float(summary["minutes"]), 28.0)
        self.assertEqual(float(summary["kilometers"]), 3.4)

    def test_phase_prescription_is_non_destructive_guidance(self):
        self.assertEqual(database.get_phase_prescription(1)["target_rir"], "2 RIR")
        self.assertEqual(database.get_phase_prescription(6)["target_rir"], "1 RIR")
        self.assertEqual(database.get_phase_prescription(9)["volume"], "Reduce sets by 30–40%")
        self.assertEqual(database.get_phase_prescription(12)["target_rir"], "1 RIR")

    def test_current_program_report_includes_running_without_steps(self):
        database.save_quick_run(database.local_today(), 32, 4.2, "Easy Run")
        report = database.get_current_program_report()
        self.assertEqual(len(report["runs"]), 1)
        self.assertEqual(float(report["runs"].iloc[0]["completed_minutes"]), 32.0)
        self.assertEqual(float(report["runs"].iloc[0]["distance_km"]), 4.2)
        self.assertNotIn("steps", report)


if __name__ == "__main__":
    unittest.main()
