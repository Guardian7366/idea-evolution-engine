import type {
  PerspectiveAnalysisResult,
  PerspectiveType,
} from '../../../types/idea'

import { Button } from '../../../components/shared/ui/Button'
import { EmptyState } from '../../../components/shared/EmptyState'

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
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-semibold">Explore perspective</h3>
      <p className="mt-2 text-sm text-slate-600">
        Analyze the current active version from one controlled MVP perspective.
      </p>

      {!hasActiveVersion ? (
        <EmptyState>
          You need an active version before exploring perspectives.
        </EmptyState>
      ) : (
        <div className="mt-4 space-y-4">
          <div className="space-y-2">
            <label
              htmlFor="perspective-select"
              className="text-sm font-medium text-slate-800"
            >
              Perspective type
            </label>

            <select
              id="perspective-select"
              value={selectedPerspective}
              onChange={(event) =>
                onPerspectiveChange(event.target.value as PerspectiveType)
              }
              className="w-full rounded-lg border border-slate-300 bg-white p-3 outline-none focus:border-slate-500"
            >
              {perspectiveOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <Button type="button" onClick={onExplore} disabled={isExploring} loading={isExploring}>
            {isExploring ? 'Exploring...' : 'Explore Perspective'}
          </Button>

          {perspectiveResult ? (
            <div className="space-y-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div>
                <h4 className="text-base font-semibold">Summary</h4>
                <p className="mt-2 text-sm leading-6 text-slate-700">
                  {perspectiveResult.summary}
                </p>
              </div>

              <div>
                <h5 className="text-sm font-semibold text-slate-800">
                  Observations
                </h5>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                  {perspectiveResult.observations.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h5 className="text-sm font-semibold text-slate-800">
                  Suggestion
                </h5>
                <p className="mt-2 text-sm leading-6 text-slate-700">
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