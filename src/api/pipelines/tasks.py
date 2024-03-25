from db.service import celery_app

from .service import (
    PipelineProcessor,
    PipelineTaskSyncService,
    process_orchestrator,
    PipelineAsyncService,
)

import asyncio
import json


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def process_pipeline(self, index_id: str, pipeline: dict, payload: dict):
    task_id = self.request.id

    # service for managing the tasks db create task
    pipeline_tasks = PipelineTaskSyncService(index_id, task_id)
    pipeline_tasks.create({"pipeline_tasks": pipeline})

    # remove _id because its a bson
    # pipeline.pop("_id", None)

    # service for pipeline processing
    pipeline_service = PipelineAsyncService(index_id)

    asyncio.run(process_orchestrator(index_id, pipeline, payload))
    # Fetch the document
    # doc = batch_service.get_one({"task_id": task_id})

    # Insert the new data at the desired position
    # doc["batches"][i]["response"] = resp

    # Save the document back to the database
    # batch_service.update_one({"task_id": task_id}, {"batches": doc["batches"]})

    # self.update_state(state="COMPLETED")
    # batch_service.update_one({"task_id": task_id}, {"status": "COMPLETED"})
