import { useState } from "react";

export function RepoInput({ onSubmit }: { onSubmit: (repoUrl: string, task: string) => void }) {
  const [repoUrl, setRepoUrl] = useState("");
  const [task, setTask] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(repoUrl, task);
      }}
    >
      <input placeholder="git repo URL" value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} />
      <input placeholder="task" value={task} onChange={(e) => setTask(e.target.value)} />
      <button type="submit">Start session</button>
    </form>
  );
}
