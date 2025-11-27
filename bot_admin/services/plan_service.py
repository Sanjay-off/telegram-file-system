# bot_admin/services/plan_service.py

from core.database import db


class PlanService:

    # ---------------------------------------------------
    # ADD NEW PLAN
    # ---------------------------------------------------
    @staticmethod
    def add_plan(plan_id: str, days: int, price: float):
        """
        Add a new premium plan.
        """
        doc = {
            "plan_id": plan_id,
            "days": days,
            "price": price
        }

        db.plans.insert_one(doc)
        return True

    # ---------------------------------------------------
    # REMOVE PLAN
    # ---------------------------------------------------
    @staticmethod
    def remove_plan(plan_id: str):
        """
        Delete a premium plan.
        """
        result = db.plans.delete_one({"plan_id": plan_id})
        return result.deleted_count > 0

    # ---------------------------------------------------
    # LIST PLANS
    # ---------------------------------------------------
    @staticmethod
    def list_plans(limit: int = 50):
        """
        Get all premium plans sorted by duration.
        """
        return list(db.plans.find().sort("days", 1).limit(limit))

    # ---------------------------------------------------
    # GET SINGLE PLAN
    # ---------------------------------------------------
    @staticmethod
    def get_plan(plan_id: str):
        """
        Fetch a specific plan using plan_id.
        """
        return db.plans.find_one({"plan_id": plan_id})

    # ---------------------------------------------------
    # CHECK IF PLAN EXISTS
    # ---------------------------------------------------
    @staticmethod
    def plan_exists(plan_id: str) -> bool:
        """
        Return True if plan exists, False if not.
        """
        return db.plans.count_documents({"plan_id": plan_id}) > 0

    # ---------------------------------------------------
    # GET PRICE
    # ---------------------------------------------------
    @staticmethod
    def get_price(plan_id: str):
        """
        Return price of a plan.
        """
        plan = PlanService.get_plan(plan_id)
        return plan["price"] if plan else None

    # ---------------------------------------------------
    # GET DAYS
    # ---------------------------------------------------
    @staticmethod
    def get_days(plan_id: str):
        """
        Return plan duration in days.
        """
        plan = PlanService.get_plan(plan_id)
        return plan["days"] if plan else None
