import type {
  ActiveIdeaVersion,
  VersionComparisonResult,
} from '../../../types/idea'

import { Button } from '../../../components/shared/ui/Button'
import { EmptyState } from '../../../components/shared/EmptyState'
import { Spinner } from '../../../components/shared/ui/Spinner'

interface VersionComparisonPanelProps {
  baseVersion: ActiveIdeaVersion | null
  activeVersion: ActiveIdeaVersion | null
  comparisonResult: VersionComparisonResult | null
  isComparing: boolean
  onCompare: () => void
}

export function VersionComparisonPanel({
  baseVersion,
  activeVersion,
  comparisonResult,
  isComparing,
  onCompare,
}: VersionComparisonPanelProps) {
  const canCompare =
    Boolean(baseVersion) &&
    Boolean(activeVersion) &&
    baseVersion?.version_id !== activeVersion?.version_id

  return (
    <section className="mx-auto w-full max-w-5xl rounded-2xl border border-slate-200 bg-white/80 p-6 shadow-sm backdrop-blur-sm">
      <div className="mb-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Step 3
          </span>
          <h3 className="text-2xl font-semibold text-slate-900">
            Compare versions
          </h3>
        </div>

        <p className="max-w-2xl text-sm leading-6 text-slate-600">
          Compare the original selected version with the current active version to
          see what changed and which direction is stronger.
        </p>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-4">
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
            Version A
          </p>
          <p className="mt-2 text-sm font-semibold text-slate-900">
            {baseVersion?.title ?? 'Not available'}
          </p>
          <p className="mt-1 break-all text-xs text-slate-500">
            {baseVersion?.version_id ?? 'No version selected'}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4">
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
            Version B
          </p>
          <p className="mt-2 text-sm font-semibold text-slate-900">
            {activeVersion?.title ?? 'Not available'}
          </p>
          <p className="mt-1 break-all text-xs text-slate-500">
            {activeVersion?.version_id ?? 'No active version'}
          </p>
        </div>
      </div>

      {!canCompare ? (
        <div className="mt-5 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6">
          <EmptyState>
            Select a variant and then transform the active version to enable comparison.
          </EmptyState>
        </div>
      ) : (
        <div className="mt-5 space-y-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-xs text-slate-500">
              Compare once you have at least two different versions.
            </p>

            <Button
              type="button"
              onClick={onCompare}
              disabled={isComparing}
              loading={isComparing}
              className="inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5"
            >
              {isComparing && <Spinner size="sm" />}
              {isComparing ? 'Comparing...' : 'Compare versions'}
            </Button>
          </div>

          {comparisonResult ? (
            <div className="space-y-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="rounded-xl bg-slate-50 p-4">
                <h4 className="text-base font-semibold text-slate-900">Summary</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {comparisonResult.summary}
                </p>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                  <h5 className="text-sm font-semibold text-slate-900">
                    Strengths of Version A
                  </h5>
                  <ul className="mt-3 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-700">
                    {comparisonResult.strengths_version_a.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                  <h5 className="text-sm font-semibold text-slate-900">
                    Strengths of Version B
                  </h5>
                  <ul className="mt-3 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-700">
                    {comparisonResult.strengths_version_b.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                <h5 className="text-sm font-semibold text-slate-900">
                  Key differences
                </h5>
                <ul className="mt-3 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-700">
                  {comparisonResult.key_differences.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4">
                <h5 className="text-sm font-semibold text-emerald-900">
                  Recommendation
                </h5>
                <p className="mt-2 text-sm leading-6 text-emerald-950">
                  {comparisonResult.recommendation}
                </p>
              </div>
            </div>
          ) : null}
        </div>
      )}
    </section>
  )
}