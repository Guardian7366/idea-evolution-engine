import type { PropsWithChildren } from 'react'

export function MainLayout({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen bg-[#E8E8E8] text-slate-900">
      <header className="fixed z-1000 mb-18 w-full border-b border-slate-200 bg-[#B5B5B5]">
        <div className="mx-auto max-w-5xl px-6 py-4 ml-15">
          <h1 className="text-4xl font-bold">Idea Evolution Engine</h1>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
    </div>
  )
}