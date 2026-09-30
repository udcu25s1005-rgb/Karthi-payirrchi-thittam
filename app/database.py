import json
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parents[1] / "fitbuddy.db"


def _connect():
	connection = sqlite3.connect(DATABASE_PATH)
	connection.row_factory = sqlite3.Row
	return connection


def init_db():
	with _connect() as connection:
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS plans (
				id TEXT PRIMARY KEY,
				goal TEXT NOT NULL,
				level TEXT NOT NULL,
				training_days INTEGER NOT NULL,
				equipment TEXT NOT NULL,
				plan_json TEXT NOT NULL,
				created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
			)
			"""
		)


def save_plan(plan_id, goal, level, training_days, equipment, plan):
	with _connect() as connection:
		connection.execute(
			"""
			INSERT INTO plans (id, goal, level, training_days, equipment, plan_json)
			VALUES (?, ?, ?, ?, ?, ?)
			""",
			(plan_id, goal, level, training_days, equipment, json.dumps(plan)),
		)


def list_plans(limit=6):
	with _connect() as connection:
		rows = connection.execute(
			"""
			SELECT id, goal, level, training_days, equipment, plan_json, created_at
			FROM plans ORDER BY created_at DESC LIMIT ?
			""",
			(limit,),
		).fetchall()
	return [_row_to_plan(row) for row in rows]


def get_plan(plan_id):
	with _connect() as connection:
		row = connection.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
	return _row_to_plan(row) if row else None


def _row_to_plan(row):
	item = dict(row)
	item["plan"] = json.loads(item.pop("plan_json"))
	return item
