from vector_db.faiss_db import FAISSVectorDB
from vector_db.milvus_db import MilvusVectorDB

class VectorDBFactory:
    @staticmethod
    def create_vector_db(config):
        db_type = config.get('vector_db_type')
        if db_type == 'faiss':
            return FAISSVectorDB()
        elif db_type == 'milvus':
            return MilvusVectorDB(
                host=config.get('milvus_host'),
                port=config.get('milvus_port')
            )
        else:
            raise ValueError(f"Unsupported vectorDB type: {db_type}")
