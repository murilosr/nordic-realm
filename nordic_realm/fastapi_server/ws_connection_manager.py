import asyncio
import logging
from typing import Literal

import redis.asyncio as redis
from fastapi import WebSocket
from pydantic import BaseModel

from nordic_realm.di import ConfigStore
from nordic_realm.utils import generate_id

redis_logger = logging.getLogger("RedisPubSub")


class RedisMessage(BaseModel):
    type: Literal["broadcast", "send_to_user"]
    process: str
    user_id: str | None = None
    message: str


class WebsocketConnectionManager:
    def __init__(self, config_store: ConfigStore):
        self.section_connections: dict[str, list[WebSocket]] = {}
        self._process_id = generate_id(12)
        self._redis_conn = redis.from_url(config_store.get("redis.host"))
        asyncio.get_event_loop().create_task(self._redis_subscribe())

    async def _redis_subscribe(self):
        redis_logger.info(f"Process '{self._process_id}' connected to redis")
        async with self._redis_conn.pubsub() as pubsub:
            await pubsub.psubscribe("ws")

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=20)
                redis_logger.log(0, message)
                if message is not None:
                    redis_logger.debug(f"Received ({self._process_id}): {message}")
                    recv_data = RedisMessage.model_validate_json(message["data"].decode())
                    if recv_data.process != self._process_id:
                        if recv_data.type == "send_to_user" and recv_data.user_id is not None:
                            await self.send_to_user(recv_data.message, recv_data.user_id, _redis_publish=False)

    async def _redis_publish(self, type: str, message: str, user_id: str | None = None):
        payload = RedisMessage(type=type, message=message, user_id=user_id, process=self._process_id).model_dump_json()

        redis_logger.debug(f"Publish: {payload}")
        await self._redis_conn.publish("ws", payload.encode())

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        _user_id: str = websocket.user.id

        if _user_id not in self.section_connections:
            self.section_connections[_user_id] = []
        self.section_connections[_user_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        _user_id: str = websocket.user.id

        ws_list = self.section_connections.get(_user_id, [])
        ws_list.remove(websocket)

        if len(ws_list) == 0:
            self.section_connections.pop(_user_id)

    async def send_to_user(self, message: str, user_id: str, _redis_publish: bool = True):
        if _redis_publish:
            await self._redis_publish("send_to_user", message, user_id)
        for _conn in self.section_connections.get(user_id, []):
            await _conn.send_text(message)

    async def send_to_connection(self, message: str, websocket: WebSocket, _redis_publish: bool = True):
        if _redis_publish:
            await self._redis_publish("broadcast", message)

        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for _conn_list in self.section_connections.values():
            for _conn in _conn_list:
                await _conn.send_text(message)
