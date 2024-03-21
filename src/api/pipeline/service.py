from db.service import BaseSyncDBService


class PipelineSyncService(BaseSyncDBService):
    def __init__(self, index_id):
        super().__init__("pipelines", index_id)

    def check_connection(self):
        # Implement the logic to check the connection
        pass

    def create_pipeline(self, pipeline):
        # Implement the logic to create a pipeline
        pass
