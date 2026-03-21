import type { ActiveIdeaVersion } from '../../../types/idea'

interface ActiveVersionPanelProps {
  activeVersion: ActiveIdeaVersion | null
}

export function ActiveVersionPanel({
  activeVersion,
}: ActiveVersionPanelProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-semibold">Active version</h3>

      {!activeVersion ? (
        <div className="mt-4 rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
          No active version yet. Select one variant to create version 1.
        </div>
      ) : (
        <div className="mt-4 space-y-4">
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

          <div>
            <h4 className="text-lg font-semibold">{activeVersion.title}</h4>
            <p className="mt-3 text-sm leading-6 text-slate-700">
              {activeVersion.content}
            </p>
          </div>

          <div className="grid gap-3 text-sm text-slate-600 md:grid-cols-2">
            <p>
              <span className="font-medium text-slate-800">Version ID:</span>{' '}
              {activeVersion.version_id}
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
              {activeVersion.idea_id}
            </p>
          </div>
        </div>
      )}
    </section>
  )
}