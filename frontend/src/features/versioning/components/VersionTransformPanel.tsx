interface VersionTransformPanelProps {
  hasActiveVersion: boolean
  transformInstruction: string
  isTransforming: boolean
  onInstructionChange: (value: string) => void
  onRefine: () => void
}

export function VersionTransformPanel({
  hasActiveVersion,
  transformInstruction,
  isTransforming,
  onInstructionChange,
  onRefine,
}: VersionTransformPanelProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-semibold">Transform active version</h3>
      <p className="mt-2 text-sm text-slate-600">
        Apply one transformation to the current active version. For now, this
        frontend step uses the refine action.
      </p>

      {!hasActiveVersion ? (
        <div className="mt-4 rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
          Select a variant first to activate version 1 before transforming it.
        </div>
      ) : (
        <div className="mt-4 space-y-4">
          <textarea
            value={transformInstruction}
            onChange={(event) => onInstructionChange(event.target.value)}
            placeholder="Example: Make the idea clearer and easier to execute for a first MVP."
            className="min-h-[120px] w-full rounded-lg border border-slate-300 p-3 outline-none focus:border-slate-500"
          />

          <button
            type="button"
            onClick={onRefine}
            disabled={isTransforming || transformInstruction.trim().length < 3}
            className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isTransforming ? 'Refining...' : 'Refine Active Version'}
          </button>
        </div>
      )}
    </section>
  )
}