import type { IdeaVariantItem } from '../../../types/idea'
import { Button } from '../../../components/shared/ui/Button'

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
        <Button
          type="button"
          variant="secondary"
          onClick={() => onSelect(variant.variant_id)}
          disabled={isSelecting}
          loading={isSelecting}
        >
          {isSelecting ? 'Selecting...' : 'Select Variant'}
        </Button>
      </div>
    </article>
  )
}