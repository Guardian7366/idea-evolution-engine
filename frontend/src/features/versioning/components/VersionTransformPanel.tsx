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
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-semibold">Transform active version</h3>
      <p className="mt-2 text-sm text-slate-600">
        Apply one transformation to the current active version. For now, this
        frontend step uses the refine action.
      </p>

      {!hasActiveVersion ? (
        <EmptyState>
          Select a variant first to activate version 1 before transforming it.
        </EmptyState>
      ) : (
        <div className="mt-4 space-y-4">
          <TextArea
            value={transformInstruction}
            onChange={(event) => onInstructionChange(event.target.value)}
            placeholder="Example: Make the idea clearer and easier to execute for a first MVP."
            variant='secondary'
          />

          <Button
            type="button"
            onClick={onRefine}
            disabled={isTransforming || transformInstruction.trim().length < 3}
            loading={isTransforming}
          >
            <span className="inline-flex items-center gap-2">
              {isTransforming && <Spinner size="sm" />}
              {isTransforming ? 'Refining...' : 'Refine Active Version'}
            </span>
          </Button>
        </div>
      )}
    </section>
  )
}