import type { ButtonHTMLAttributes, ReactNode } from 'react'

type ButtonVariant = 'primary' | 'secondary'

type ButtonProps = {
  children: ReactNode
  variant?: ButtonVariant
  loading?: boolean
} & ButtonHTMLAttributes<HTMLButtonElement>

export function Button({
  children,
  variant = 'primary',
  loading = false,
  disabled,
  className = '',
  ...props
}: ButtonProps) {
  const baseClasses =
    'rounded-lg px-4 py-2 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50'

  const variantClasses =
    variant === 'primary'
      ? 'bg-slate-900 text-white hover:bg-slate-800'
      : 'border border-slate-300 text-slate-800 hover:bg-slate-50'

  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={`${baseClasses} ${variantClasses} ${className}`}
    >
      {children}
    </button>
  )
}