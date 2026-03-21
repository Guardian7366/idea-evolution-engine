interface FlowStatusPanelProps {
  sessionId: string
  ideaId: string
  variantsCount: number
}

export function FlowStatusPanel({
  sessionId,
  ideaId,
  variantsCount,
}: FlowStatusPanelProps) {
  return (
    <section className="grid gap-4 md:grid-cols-2">
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="text-lg font-semibold">Current session</h3>
        <p className="mt-3 text-sm text-slate-600">
          <span className="font-medium text-slate-800">Session ID:</span>{' '}
          {sessionId || 'Not created yet'}
        </p>
        <p className="mt-2 text-sm text-slate-600">
          <span className="font-medium text-slate-800">Idea ID:</span>{' '}
          {ideaId || 'Not created yet'}
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="text-lg font-semibold">Flow status</h3>
        <p className="mt-3 text-sm text-slate-600">
          Variants generated: {variantsCount}
        </p>
      </div>
    </section>
  )
}