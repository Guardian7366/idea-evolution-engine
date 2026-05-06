import type {
  PerspectiveAnalysisResult,
  PerspectiveType,
} from '../../../types/idea'

import { Button } from '../../../components/shared/ui/Button'
import { EmptyState } from '../../../components/shared/EmptyState'
import { Spinner } from '../../../components/shared/ui/Spinner'

interface PerspectiveExplorerPanelProps {
  hasActiveVersion: boolean
  selectedPerspective: PerspectiveType
  perspectiveResult: PerspectiveAnalysisResult | null
  isExploring: boolean
  onPerspectiveChange: (value: PerspectiveType) => void
  onExplore: () => void
}

const perspectiveOptions: Array<{
  value: PerspectiveType
  label: string
}> = [
  { value: 'feasibility', label: 'Feasibility' },
  { value: 'innovation', label: 'Innovation' },
  { value: 'user_value', label: 'User Value' },
  { value: 'risks', label: 'Risks' },
]

export function PerspectiveExplorerPanel({
  hasActiveVersion,
  selectedPerspective,
  perspectiveResult,
  isExploring,
  onPerspectiveChange,
  onExplore,
}: PerspectiveExplorerPanelProps) {
  const isDisabled = isExploring

  return (
    <section className="mx-auto w-full max-w-5xl rounded-2xl border border-slate-200 bg-white/80 p-6 shadow-sm backdrop-blur-sm">
      <div className="mb-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Step 4
          </span>
          <h3 className="text-2xl font-semibold text-slate-900">
            Explore perspective
          </h3>
        </div>

        <p className="max-w-2xl text-sm leading-6 text-slate-600">
          Review the active version from one specific angle to uncover strengths,
          risks, or opportunities that may not be obvious at first glance.
        </p>
      </div>

      {!hasActiveVersion ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6">
          <EmptyState>
            You need an active version before exploring perspectives.
          </EmptyState>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <label
              htmlFor="perspective-select"
              className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500"
            >
              Perspective type
            </label>

            <select
              id="perspective-select"
              value={selectedPerspective}
              onChange={(event) =>
                onPerspectiveChange(event.target.value as PerspectiveType)
              }
              className="
                mt-3 w-full rounded-xl border border-slate-300 bg-white
                px-4 py-3 text-sm text-slate-800 outline-none
                transition focus:border-slate-500
              "
            >
              {perspectiveOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>

            <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-xs text-slate-500">
                Choose a lens and generate one focused review at a time.
              </p>

              <Button
                type="button"
                onClick={onExplore}
                disabled={isDisabled}
                loading={isExploring}
                className="inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5"
              >
                <span className="inline-flex items-center gap-2">
                  {isExploring && <Spinner size="sm" />}
                  {isExploring ? 'Exploring...' : 'Explore perspective'}
                </span>
              </Button>
            </div>
          </div>

          {perspectiveResult ? (
            <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="rounded-xl bg-slate-50 p-4">
                <h4 className="text-base font-semibold text-slate-900">Summary</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {perspectiveResult.summary}
                </p>
              </div>

              <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                <h5 className="text-sm font-semibold text-slate-900">
                  Observations
                </h5>
                <ul className="mt-3 list-disc space-y-1 pl-5 text-sm leading-6 text-slate-700">
                  {perspectiveResult.observations.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4">
                <h5 className="text-sm font-semibold text-emerald-900">
                  Suggestion
                </h5>
                <p className="mt-2 text-sm leading-6 text-emerald-950">
                  {perspectiveResult.suggestion}
                </p>
              </div>
            </div>
          ) : null}
        </div>
      )}
    </section>
  )
}