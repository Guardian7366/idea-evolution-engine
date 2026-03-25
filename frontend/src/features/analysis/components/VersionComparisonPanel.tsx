import type {
  ActiveIdeaVersion,
  VersionComparisonResult,
} from '../../../types/idea'

import { Button } from '../../../components/shared/Button'
import { EmptyState } from '../../../components/shared/EmptyState'

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
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-semibold">Compare versions</h3>
      <p className="mt-2 text-sm text-slate-600">
        Compare the initial selected version against the current active version.
      </p>

      <div className="mt-4 grid gap-3 text-sm text-slate-600 md:grid-cols-2">
        <p>
          <span className="font-medium text-slate-800">Version A:</span>{' '}
          {baseVersion?.version_id ?? 'Not available'}
        </p>
        <p>
          <span className="font-medium text-slate-800">Version B:</span>{' '}
          {activeVersion?.version_id ?? 'Not available'}
        </p>
      </div>

      {!canCompare ? (
        <EmptyState>
          Select a variant and then transform the active version to enable
          comparison.
        </EmptyState>
      ) : (
        <div className="mt-4 space-y-4">
          <Button type="button" onClick={onCompare} disabled={isComparing} loading={isComparing}>
            {isComparing ? 'Comparing...' : 'Compare Versions'}
          </Button>

          {comparisonResult ? (
            <div className="space-y-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div>
                <h4 className="text-base font-semibold">Summary</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {comparisonResult.summary}
                </p>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <h5 className="text-sm font-semibold text-slate-800">
                    Strengths of Version A
                  </h5>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                    {comparisonResult.strengths_version_a.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h5 className="text-sm font-semibold text-slate-800">
                    Strengths of Version B
                  </h5>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                    {comparisonResult.strengths_version_b.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div>
                <h5 className="text-sm font-semibold text-slate-800">
                  Key differences
                </h5>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                  {comparisonResult.key_differences.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h5 className="text-sm font-semibold text-slate-800">
                  Recommendation
                </h5>
                <p className="mt-2 text-sm leading-6 text-slate-700">
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