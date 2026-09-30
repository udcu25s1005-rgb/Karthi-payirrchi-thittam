import json
import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def generate_plan(goal, level, training_days, equipment):
	api_key = os.getenv("GOOGLE_API_KEY")
	if api_key:
		try:
			genai.configure(api_key=api_key)
			model = genai.GenerativeModel("gemini-2.5-flash")
			response = model.generate_content(
				"Return only valid JSON with keys title, summary, and days. "
				"Each day has name, focus, and exercises (an array of strings). "
				f"Create exactly {training_days} days for goal: {goal}; level: {level}; "
				f"available equipment: {equipment}. Keep the plan practical and concise."
			)
			plan = json.loads(response.text)
			if isinstance(plan.get("days"), list) and plan["days"]:
				return plan, True
		except Exception:
			pass
	return _starter_plan(goal, level, training_days, equipment), False


def _starter_plan(goal, level, training_days, equipment):
	workouts = [
		("Full body A", "Squat, push, and pull", [
			"Goblet squat: 3 sets x 8-10 reps",
			"Push-up: 3 sets x 8-12 reps",
			"Dumbbell or backpack row: 3 sets x 10 reps",
			"Glute bridge: 3 sets x 12 reps",
		]),
		("Full body B", "Hinge, press, and core", [
			"Hip hinge: 3 sets x 10 reps",
			"Overhead press or pike push-up: 3 sets x 8 reps",
			"Reverse lunge: 3 sets x 8 reps per side",
			"Dead bug: 3 sets x 10 reps per side",
		]),
		("Conditioning", "Steady cardio and mobility", [
			"Brisk walk, cycle, or jog: 20-30 minutes",
			"Bodyweight squat: 2 sets x 12 reps",
			"Bird dog: 2 sets x 10 reps per side",
			"Easy full-body stretching: 5 minutes",
		]),
		("Strength and stability", "Single-leg strength and upper body", [
			"Split squat: 3 sets x 8 reps per side",
			"Incline push-up: 3 sets x 10 reps",
			"Backpack row: 3 sets x 10 reps per side",
			"Side plank: 3 sets x 20 seconds per side",
		]),
		("Recovery cardio", "Low-impact movement and recovery", [
			"Comfortable walk: 20-30 minutes",
			"Cat-cow: 2 sets x 8 reps",
			"Hip flexor stretch: 2 x 30 seconds per side",
			"Shoulder mobility: 2 minutes",
		]),
		("Full body C", "Repeat key movements with control", [
			"Squat variation: 3 sets x 10 reps",
			"Push-up variation: 3 sets x 8-12 reps",
			"Hip hinge: 3 sets x 10 reps",
			"Front plank: 3 sets x 20-30 seconds",
		]),
	]
	days = [
		{"name": f"Day {index + 1}: {workouts[index][0]}",
		 "focus": workouts[index][1], "exercises": workouts[index][2]}
		for index in range(training_days)
	]
	return {
		"title": f"{goal.title()} starter plan",
		"summary": (
			f"A {training_days}-day plan for a {level} level using {equipment}. "
			"Rest 60-90 seconds between sets and stop if you feel pain."
		),
		"days": days,
	}
