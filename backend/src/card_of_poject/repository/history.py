from datetime import datetime
from models import ProjectHistory, User, Stage
from typing import List, Optional, Dict
from uuid import UUID as PyUUID
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.card_of_poject.repository.base_repository import BaseRepository


class ProjectHistoryRepository(BaseRepository[ProjectHistory]):
    async def get_last_changes(
        self, project_id: PyUUID, limit: int = 10
    ) -> List[ProjectHistory]:
        query = (
            select(ProjectHistory)
            .where(ProjectHistory.project_id == project_id)
            .options(selectinload(ProjectHistory.changed_by))
            .order_by(ProjectHistory.changed_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_for_period(
        self, start_date: datetime, end_date: datetime
    ) -> List[ProjectHistory]:
        query = (
            select(ProjectHistory)
            .where(ProjectHistory.changed_at.between(start_date, end_date))
            .options(selectinload(ProjectHistory.changed_by))
            .order_by(ProjectHistory.changed_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    # INFO: этапы для Ганта
    async def get_stage_changes(self, project_id: PyUUID) -> List[Dict]:
        query = (
            select(ProjectHistory, Stage.stage_name)
            .join(Stage, ProjectHistory.new_value == Stage.oid)
            .where(ProjectHistory.project_id == project_id)
            .where(ProjectHistory.field_changed == "stage_id")
            .order_by(ProjectHistory.changed_at.asc())
        )
        result = await self.session.execute(query)
        return [
            {"stage_name": row.stage_name, "changed_at": row.ProjectHistory.changed_at}
            for row in result
        ]
