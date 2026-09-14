import { useEffect, useState } from "react";
import { getSession, openSessionStream, SessionDetail } from "../api/client";

export function SessionView({ sessionId }: { sessionId: number }) {
  const [session, setSession] = useState<SessionDetail | null>(null);
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    getSession(sessionId).then(setSession);
    const ws = openSessionStream(sessionId, (event) => setEvents((prev) => [...prev, event]));
    return () => ws.close();
  }, [sessionId]);

  return (
    <div>
      <h3>Session {sessionId}: {session?.status}</h3>
      <ul>
        {events.map((e, i) => (
          <li key={i}>{JSON.stringify(e)}</li>
        ))}
      </ul>
    </div>
  );
}
