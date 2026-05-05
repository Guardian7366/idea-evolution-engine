import { useState } from 'react'
import type { IdeaVariantItem } from '../../../types/idea'
import { Button } from '../../../components/shared/ui/Button'
import { Spinner } from '../../../components/shared/ui/Spinner'

interface VariantCardProps {
  variant: IdeaVariantItem
  isSelecting: boolean
  isSelected: boolean
  hasSelectedVariant: boolean
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
  isSelected,
  hasSelectedVariant,
  onSelect,
}: VariantCardProps) {
  const styles = getVariantStyle(variant.variant_type)

  const [showConfirm, setShowConfirm] = useState(false)

  const isDisabled = isSelecting || hasSelectedVariant

  return (
    <article
      className={`
        rounded-2xl border ${styles.border}
        bg-white/80 backdrop-blur-sm
        p-6 transition-all duration-300
        ${!hasSelectedVariant ? 'hover:shadow-lg hover:-translate-y-1' : ''}
        ${isSelected ? 'ring-2 ring-slate-900 shadow-lg' : ''}
        ${hasSelectedVariant && !isSelected ? 'opacity-60' : ''}
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

      {hasSelectedVariant ? (
        <div className="mt-6 flex justify-end">
          {isSelected ? (
            <span className="text-sm font-medium text-emerald-600">
              ✓ Selected
            </span>
          ) : (
            <span className="text-sm text-slate-400">
              Not selected
            </span>
          )}
        </div>
      ) : (
        <div className="mt-6 flex justify-end">
          {!showConfirm ? (
            <Button
              type="button"
              variant="secondary"
              onClick={() => setShowConfirm(true)}
              disabled={isDisabled}
              className="rounded-full px-4 py-2"
            >
              Choose direction
            </Button>
          ) : (
            <div className="flex items-center gap-2">
              <Button
                type="button"
                onClick={() => onSelect(variant.variant_id)}
                disabled={isSelecting}
                loading={isSelecting}
                className="rounded-full px-4 py-2"
              >
                <span className="inline-flex items-center gap-2">
                  {isSelecting && <Spinner size="sm" />}
                  Confirm
                  
                </span>
              </Button>

              <Button
                type="button"
                variant="secondary"
                onClick={() => setShowConfirm(false)}
                disabled={isSelecting}
                className="rounded-full px-4 py-2"
              >
                Cancel
              </Button>
            </div>
          )}
        </div>
      )}
    </article>
  )
}