import type { IdeaVariantItem } from '../../../types/idea'
import { Button } from '../../../components/shared/ui/Button'
import { Spinner } from '../../../components/shared/ui/Spinner'

interface VariantCardProps {
  variant: IdeaVariantItem
  isSelecting: boolean
  onSelect: (variantId: string) => void
}

function getVariantStyle(type: string) {
  switch (type) {
    case 'expansion':
      return {
        border: 'border-blue-200',
        badge: 'bg-blue-100 text-blue-700',
      }
    case 'focus':
      return {
        border: 'border-emerald-200',
        badge: 'bg-emerald-100 text-emerald-700',
      }
    case 'creative_twist':
      return {
        border: 'border-purple-200',
        badge: 'bg-purple-100 text-purple-700',
      }
    default:
      return {
        border: 'border-slate-200',
        badge: 'bg-slate-100 text-slate-700',
      }
  }
}

export function VariantCard({
  variant,
  isSelecting,
  onSelect,
}: VariantCardProps) {
  const styles = getVariantStyle(variant.variant_type)

  return (
    <article
      className={`
        group rounded-2xl border ${styles.border}
        bg-white/80 backdrop-blur-sm
        p-6 transition-all duration-300
        hover:shadow-lg hover:-translate-y-1
      `}
    >
      <div className="flex items-center justify-between gap-3">
        <h4 className="text-lg font-semibold text-slate-900">
          {variant.title}
        </h4>

        <span
          className={`px-3 py-1 text-xs rounded-full font-medium ${styles.badge}`}
        >
          {variant.variant_type.replace('_', ' ')}
        </span>
      </div>

      <p className="mt-4 text-sm leading-6 text-slate-700">
        {variant.content}
      </p>

      <div className="mt-6 flex justify-end">
        <Button
          type="button"
          variant="secondary"
          onClick={() => onSelect(variant.variant_id)}
          disabled={isSelecting}
          loading={isSelecting}
          className="rounded-full px-4 py-2"
        >
          <span className="inline-flex items-center gap-2">
            {isSelecting && <Spinner size="sm" />}
            {isSelecting ? 'Selecting...' : 'Choose direction'}
          </span>
        </Button>
      </div>
    </article>
  )
}