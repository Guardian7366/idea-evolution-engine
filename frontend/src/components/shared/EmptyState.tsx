import type { ReactNode } from 'react'

type EmptyProps = {
    children : ReactNode
}

export function EmptyState({
  children
}: EmptyProps) {
    const baseClass =
        'mt-4 rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500'

    return (
        <div className={baseClass}>
            {children}
        </div>
    )
}