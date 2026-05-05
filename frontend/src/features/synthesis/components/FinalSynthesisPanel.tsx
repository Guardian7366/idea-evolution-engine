import type { FinalSynthesisResult } from '../../../types/idea'
import { Button } from '../../../components/shared/ui/Button'
import { EmptyState } from '../../../components/shared/EmptyState'
import { Spinner } from '../../../components/shared/ui/Spinner'

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
  const isDisabled = isGenerating

  return (
    <section className="mx-auto w-full max-w-5xl rounded-2xl border border-slate-200 bg-white/80 p-6 shadow-sm backdrop-blur-sm">
      <div className="mb-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Step 5
          </span>
          <h3 className="text-2xl font-semibold text-slate-900">
            Final synthesis
          </h3>
        </div>

        <p className="max-w-2xl text-sm leading-6 text-slate-600">
          Generate a structured synthesis from the current active version to
          capture the core concept, value proposition, and recommended next step.
        </p>
      </div>

      {!hasActiveVersion ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6">
          <EmptyState>
            You need an active version before generating a final synthesis.
          </EmptyState>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-xs text-slate-500">
              Use this as the closing step to summarize the evolved idea.
            </p>

            <Button
              type="button"
              onClick={onGenerate}
              disabled={isDisabled}
              loading={isGenerating}
              className="inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5"
            >
              <span className="inline-flex items-center gap-2">
                {isGenerating && <Spinner size="sm" />}
                {isGenerating ? 'Generating...' : 'Generate synthesis'}
              </span>
            </Button>
          </div>

          {synthesisResult ? (
            <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="rounded-xl bg-slate-50 p-4">
                <h4 className="text-base font-semibold text-slate-900">Title</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.title}
                </p>
              </div>

              <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                <h4 className="text-base font-semibold text-slate-900">
                  Core concept
                </h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.core_concept}
                </p>
              </div>

              <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                <h4 className="text-base font-semibold text-slate-900">
                  Value proposition
                </h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {synthesisResult.value_proposition}
                </p>
              </div>

              <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4">
                <h4 className="text-base font-semibold text-emerald-900">
                  Recommended next step
                </h4>
                <p className="mt-2 text-sm leading-6 text-emerald-950">
                  {synthesisResult.recommended_next_step}
                </p>
              </div>

              <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                <h4 className="text-base font-semibold text-slate-900">Notes</h4>
                <ul className="mt-3 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-700">
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