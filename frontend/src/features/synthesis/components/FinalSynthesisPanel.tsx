import type { FinalSynthesisResult } from '../../../types/idea'
import { Button } from '../../../components/shared/Button'
import { EmptyState } from '../../../components/shared/EmptyState'

interface FinalSynthesisPanelProps {
  hasActiveVersion: boolean
  synthesisResult: FinalSynthesisResult | null
  isGenerating: boolean
  onGenerate: () => void
}

export function FinalSynthesisPanel({
  hasActiveVersion,
  synthesisResult,
  isGenerating,
  onGenerate,
}: FinalSynthesisPanelProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-semibold">Final synthesis</h3>
      <p className="mt-2 text-sm text-slate-600">
        Generate a final structured synthesis from the current active version.
      </p>

      {!hasActiveVersion ? (
        <EmptyState>
          You need an active version before generating a final synthesis.
        </EmptyState>
      ) : (
        <div className="mt-4 space-y-4">
          <Button
            type="button"
            onClick={onGenerate}
            disabled={isGenerating}
            loading={isGenerating}
          >
            {isGenerating ? 'Generating...' : 'Generate Final Synthesis'}
          </Button>

          {synthesisResult ? (
            <div className="space-y-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div>
                <h4 className="text-base font-semibold">Title</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.title}
                </p>
              </div>

              <div>
                <h4 className="text-base font-semibold">Core concept</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.core_concept}
                </p>
              </div>

              <div>
                <h4 className="text-base font-semibold">Value proposition</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.value_proposition}
                </p>
              </div>

              <div>
                <h4 className="text-base font-semibold">Recommended next step</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.recommended_next_step}
                </p>
              </div>

              <div>
                <h4 className="text-base font-semibold">Notes</h4>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                  {synthesisResult.notes.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          ) : null}
        </div>
      )}
    </section>
  )
}