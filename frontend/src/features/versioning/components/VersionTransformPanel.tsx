import { Button } from '../../../components/shared/ui/Button'
import { EmptyState } from '../../../components/shared/EmptyState'
import { TextArea } from '../../../components/shared/ui/TextArea'
import { Spinner } from '../../../components/shared/ui/Spinner'

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
  const isDisabled = isTransforming || transformInstruction.trim().length < 3

  return (
    <section className="mx-auto w-full max-w-5xl rounded-2xl border border-slate-200 bg-white/80 p-6 shadow-sm backdrop-blur-sm">
      <div className="mb-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Step 2
          </span>
          <h3 className="text-2xl font-semibold text-slate-900">
            Transform active version
          </h3>
        </div>

        <p className="max-w-2xl text-sm leading-6 text-slate-600">
          Apply one transformation to the current active version. Use a short instruction to make the idea clearer, more focused, or more actionable.
        </p>
      </div>

      {!hasActiveVersion ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6">
          <EmptyState>
            Select a variant first to activate version 1 before transforming it.
          </EmptyState>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white shadow-sm transition focus-within:border-slate-300 focus-within:shadow-md">
            <div className="border-b border-slate-100 px-4 py-3">
              <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
                Transformation instruction
              </p>
            </div>

            <div className="px-4 py-4">
              <TextArea
                value={transformInstruction}
                onChange={(event) => onInstructionChange(event.target.value)}
                placeholder="Example: Make the idea clearer and easier to execute for a first MVP."
                variant="secondary"
                className="min-h-[140px] w-full resize-none border-0 bg-transparent p-0 text-sm leading-6 text-slate-800 outline-none placeholder:text-slate-400 focus:border-0 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-xs text-slate-500">
              Tip: one focused instruction works better than multiple changes at once.
            </p>

            <Button
              type="button"
              onClick={onRefine}
              disabled={isDisabled}
              loading={isTransforming}
              className="inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5"
            >
              {isTransforming && <Spinner size="sm" />}
              {isTransforming ? 'Refining...' : 'Refine active version'}
            </Button>
          </div>
        </div>
      )}
    </section>
  )
}