export function TokenUsageDashboard({ promptTokens, completionTokens }: { promptTokens: number; completionTokens: number }) {
  return (
    <div>
      <span>Prompt tokens: {promptTokens}</span>
      <span>Completion tokens: {completionTokens}</span>
    </div>
  );
}
