type SpinnerProps = {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  const sizeClasses =
    size === 'sm' ? 'h-4 w-4 border-2' : size === 'lg' ? 'h-8 w-8 border-4' : 'h-5 w-5 border-2'

  return (
    <span
      className={`inline-block animate-spin rounded-full border-slate-300 border-t-slate-900 ${sizeClasses} ${className}`}
      aria-hidden="true"
    />
  )
}