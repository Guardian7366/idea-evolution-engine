import type { IdeaVariantItem } from '../../../types/idea'
import { VariantCard } from './VariantCard'

interface VariantsListProps {
  variants: IdeaVariantItem[]
  isSelecting: boolean
  onSelectVariant: (variantId: string) => void
}

export function VariantsList({
  variants,
  isSelecting,
  onSelectVariant,
}: VariantsListProps) {
  return (
    <section className="space-y-4">
      <h3 className="text-xl font-semibold">Initial variants</h3>

      {variants.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500">
          No variants yet. Start the flow to see generated options.
        </div>
      ) : (
        <div className="grid gap-4">
          {variants.map((variant) => (
            <VariantCard
              key={variant.variant_id}
              variant={variant}
              isSelecting={isSelecting}
              onSelect={onSelectVariant}
            />
          ))}
        </div>
      )}
    </section>
  )
}