import type { IdeaVariantItem } from '../../../types/idea'

interface VariantCardProps {
  variant: IdeaVariantItem
  isSelecting: boolean
  onSelect: (variantId: string) => void
}

export function VariantCard({
  variant,
  isSelecting,
  onSelect,
}: VariantCardProps) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <h4 className="text-lg font-semibold">{variant.title}</h4>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
          {variant.variant_type}
        </span>
      </div>

      <p className="mt-3 text-sm leading-6 text-slate-700">{variant.content}</p>

      <div className="mt-4">
        <button
          type="button"
          onClick={() => onSelect(variant.variant_id)}
          disabled={isSelecting}
          className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-800 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isSelecting ? 'Selecting...' : 'Select Variant'}
        </button>
      </div>
    </article>
  )
}