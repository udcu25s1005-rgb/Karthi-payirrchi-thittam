from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request

from app.ai.init import generate_plan
from app.database import get_plan, list_plans, save_plan


router = APIRouter()
api = APIRouter(prefix="/api")
templates = Jinja2Templates(directory="templates")


class PlanRequest(BaseModel):
	goal: str = Field(min_length=3, max_length=80)
	level: str = Field(pattern="^(beginner|intermediate|advanced)$")
	training_days: int = Field(ge=3, le=6)
	equipment: str = Field(min_length=2, max_length=100)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html",
		context={"plans": list_plans()},
	)


@api.post("/plans")
def create_plan(payload: PlanRequest):
	plan, ai_generated = generate_plan(
		payload.goal, payload.level, payload.training_days, payload.equipment
	)
	plan_id = str(uuid4())
	save_plan(
		plan_id, payload.goal, payload.level, payload.training_days,
		payload.equipment, plan,
	)
	return {
		"id": plan_id,
		"goal": payload.goal,
		"level": payload.level,
		"training_days": payload.training_days,
		"equipment": payload.equipment,
		"plan": plan,
		"ai_generated": ai_generated,
	}


@api.get("/plans")
def recent_plans():
	return list_plans()


@api.get("/plans/{plan_id}")
def plan_detail(plan_id: str):
	plan = get_plan(plan_id)
	if plan is None:
		raise HTTPException(status_code=404, detail="Plan not found")
	return plan
