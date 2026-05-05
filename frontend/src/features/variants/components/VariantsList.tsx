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
    <section className="mx-auto w-full max-w-5xl space-y-6">
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-semibold text-slate-900">
          Explore initial directions
        </h3>
        <p className="text-sm text-slate-600 max-w-2xl mx-auto">
          Each variant represents a different way to approach your idea. Select one to continue evolving it.
        </p>
      </div>

      {variants.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white/60 p-6 text-sm text-slate-500 text-center">
          No variants yet. Start the flow to see generated options.
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
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