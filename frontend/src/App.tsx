import { useState } from "react";
import { RepoInput } from "./components/RepoInput";
import { SessionView } from "./components/SessionView";
import { createSession } from "./api/client";

export function App() {
  const [sessionId, setSessionId] = useState<number | null>(null);

  const handleSubmit = async (repoUrl: string, task: string) => {
    const { session_id } = await createSession(repoUrl, task);
    setSessionId(session_id);
  };

  return (
    <div>
      <h1>Patchwork</h1>
      {sessionId === null ? <RepoInput onSubmit={handleSubmit} /> : <SessionView sessionId={sessionId} />}
    </div>
  );
}
