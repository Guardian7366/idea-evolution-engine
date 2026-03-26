import type { TextareaHTMLAttributes } from "react"

type TextAreaVariant = 'primary' | 'secondary'

type TextAreaProps = {
    variant?: TextAreaVariant
} & TextareaHTMLAttributes<HTMLTextAreaElement>

export function TextArea({
    variant = 'primary',
    ...props
}: TextAreaProps) {
    const baseClasses =
        'w-full rounded-lg border border-slate-300 p-3 outline-none focus:border-slate-500'
    
    const variantClasses =
    variant === 'primary'
        ? 'min-h-[140px]'
        : 'min-h-[120px]'

    return (
        <textarea
        {...props}
        className={`${baseClasses} ${variantClasses}`}/>
    )
}
