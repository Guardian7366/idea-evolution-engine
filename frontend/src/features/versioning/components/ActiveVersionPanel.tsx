import { useState } from 'react'
import type { ActiveIdeaVersion } from '../../../types/idea'
import { EmptyState } from '../../../components/shared/EmptyState'

interface ActiveVersionPanelProps {
  activeVersion: ActiveIdeaVersion | null
}

export function ActiveVersionPanel({
  activeVersion,
}: ActiveVersionPanelProps) {
  const [isExpanded, setIsExpanded] = useState(true)

  return (
    <section
      className="
        sticky top-24 z-20
        rounded-2xl border border-slate-200
        bg-zinc-300 backdrop-blur-sm
        shadow-lg
      "
      aria-live="polite"
    >
      <button
        type="button"
        onClick={() => setIsExpanded((prev) => !prev)}
        aria-expanded={isExpanded}
        className="
          flex w-full items-center justify-between gap-3
          px-5 py-4 text-left
          transition hover:bg-slate-50 hover:rounded-2xl
        "
      >
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold text-slate-900">
              Active version
            </h3>

            {activeVersion ? (
              <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-[11px] font-medium text-emerald-700">
                Live
              </span>
            ) : null}
          </div>

          <p className="mt-1 text-sm text-slate-500">
            {activeVersion
              ? `${activeVersion.title} • Version ${activeVersion.version_number}`
              : 'No active version yet'}
          </p>
        </div>

        <span
          className={`
            grid h-9 w-9 place-items-center rounded-full
            border border-slate-200 bg-white text-slate-700
            transition-transform duration-200
            ${isExpanded ? 'rotate-180' : 'rotate-0'}
          `}
          aria-hidden="true"
        >
          ▾
        </span>
      </button>

      {isExpanded ? (
        <div className="border-t border-slate-100 px-5 py-4">
          {!activeVersion ? (
            <EmptyState>
              No active version yet. Select one variant to create version 1.
            </EmptyState>
          ) : (
            <div className="space-y-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-medium text-white">
                  Version {activeVersion.version_number}
                </span>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                  {activeVersion.transformation_type}
                </span>
                <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
                  {activeVersion.status}
                </span>
              </div>

              <div className="rounded-xl border border-slate-100 bg-zinc-200 p-4">
                <h4 className="text-lg font-semibold text-slate-900">
                  {activeVersion.title}
                </h4>
                <p className="mt-3 text-sm leading-6 text-slate-700">
                  {activeVersion.content}
                </p>
              </div>

              <div className="grid gap-3 text-sm text-slate-600">
                <p>
                  <span className="font-medium text-slate-800">Version ID:</span>{' '}
                  <span className="break-all">{activeVersion.version_id}</span>
                </p>
                <p>
                  <span className="font-medium text-slate-800">Source Variant:</span>{' '}
                  {activeVersion.source_variant_id ?? 'N/A'}
                </p>
                <p>
                  <span className="font-medium text-slate-800">Parent Version:</span>{' '}
                  {activeVersion.parent_version_id ?? 'None'}
                </p>
                <p>
                  <span className="font-medium text-slate-800">Idea ID:</span>{' '}
                  <span className="break-all">{activeVersion.idea_id}</span>
                </p>
              </div>
            </div>
          )}
        </div>
      ) : null}
    </section>
  )
}