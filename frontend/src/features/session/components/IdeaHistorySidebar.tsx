export type IdeaHistoryItem = {
  ideaId: string
  input: string
  createdAt: string
}

type IdeaHistorySidebarProps = {
  isOpen: boolean
  onClose: () => void
  ideas: IdeaHistoryItem[]
  activeIdeaId: string | null
  onSelectIdea: (ideaId: string) => void
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat('es-MX', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export function IdeaHistorySidebar({
  isOpen,
  onClose,
  ideas,
  activeIdeaId,
  onSelectIdea,
}: IdeaHistorySidebarProps) {
  return (
    <>
      <div
        className={`fixed inset-0 z-40 bg-slate-900/40 transition-opacity ${
          isOpen ? 'opacity-100' : 'pointer-events-none opacity-0'
        }`}
        onClick={onClose}
      />

      <aside
        className={`fixed inset-y-0 left-0 z-50 w-[320px] max-w-[90vw] border-r border-slate-200 bg-white shadow-xl transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full flex-col">
          <div className="flex items-center justify-between border-b border-slate-200 p-4">
            <div>
              <h2 className="text-base font-semibold text-slate-900">History</h2>
              <p className="text-sm text-slate-500">Recent ideas in this browser session</p>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900"
              aria-label="Close history"
            >
              X
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4">
            {ideas.length === 0 ? (
              <div className="rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
                No recent ideas yet.
              </div>
            ) : (
              <div className="space-y-3">
                {ideas.map((idea) => {
                  const isActive = idea.ideaId === activeIdeaId

                  return (
                    <button
                      key={idea.ideaId}
                      type="button"
                      onClick={() => onSelectIdea(idea.ideaId)}
                      className={`w-full rounded-lg border p-3 text-left transition ${
                        isActive
                          ? 'border-slate-900 bg-slate-50'
                          : 'border-slate-200 hover:bg-slate-50'
                      }`}
                    >
                      <div className="line-clamp-2 text-sm font-medium text-slate-900">
                        {idea.input}
                      </div>
                      <div className="mt-2 text-xs text-slate-500">
                        {formatDate(idea.createdAt)}
                      </div>
                    </button>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </aside>
    </>
  )
}