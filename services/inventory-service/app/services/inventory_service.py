import redis
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class InventoryService:
    redis_client = None
    
    @classmethod
    def get_redis_client(cls):
        if not cls.redis_client:
            try:
                cls.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    decode_responses=True
                )
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {str(e)}")
        return cls.redis_client
    
    @classmethod
    def reserve_inventory(cls, product_id: str, quantity: int) -> bool:
        try:
            client = cls.get_redis_client()
            if not client:
                return False
            
            key = f"inventory:{product_id}"
            current = client.get(key)
            
            if current is None:
                client.set(key, 1000)
                current = 1000
            else:
                current = int(current)
            
            if current >= quantity:
                client.decrby(key, quantity)
                logger.info(f"Reserved {quantity} units of {product_id}")
                return True
            else:
                logger.warning(f"Insufficient inventory for {product_id}")
                return False
        except Exception as e:
            logger.error(f"Error reserving inventory: {str(e)}")
            return False
