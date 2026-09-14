const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface SessionDetail {
  session_id: number;
  status: string;
  messages: { role: string; content: string }[];
}

export async function createSession(
  repoUrl: string,
  task: string,
  authToken?: string
): Promise<{ session_id: number; status: string }> {
  const res = await fetch(`${BASE_URL}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl, task, auth_token: authToken ?? null }),
  });
  return res.json();
}

export async function getSession(id: number): Promise<SessionDetail> {
  const res = await fetch(`${BASE_URL}/sessions/${id}`);
  return res.json();
}

export function openSessionStream(id: number, onEvent: (event: any) => void): WebSocket {
  const wsUrl = BASE_URL.replace(/^http/, "ws") + `/sessions/${id}/stream`;
  const ws = new WebSocket(wsUrl);
  ws.onmessage = (msg) => onEvent(JSON.parse(msg.data));
  return ws;
}
