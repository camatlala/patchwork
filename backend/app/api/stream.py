from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/sessions/{session_id}/stream")
async def session_stream(websocket: WebSocket, session_id: int):
    await websocket.accept()
    await websocket.send_json({"type": "connected", "session_id": session_id})
    await websocket.close()
