import type { ButtonHTMLAttributes, PropsWithChildren } from "react";

type ButtonVariant = "primary" | "secondary" | "success" | "warning";

type ButtonProps = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: ButtonVariant;
    fullWidth?: boolean;
  }
>;

const baseClasses =
  "button-shell inline-flex min-h-[46px] items-center justify-center rounded-2xl px-4 py-3 text-sm font-semibold tracking-[0.01em] transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-60 disabled:shadow-none";

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    "button-shell--primary border border-cyan-200/28 bg-[linear-gradient(180deg,rgba(171,247,255,0.97),rgba(91,205,255,0.84))] text-slate-950 shadow-[inset_0_1px_0_rgba(255,255,255,0.76),0_10px_24px_rgba(38,147,199,0.26)] hover:-translate-y-[1px] hover:brightness-[1.03] hover:shadow-[inset_0_1px_0_rgba(255,255,255,0.8),0_14px_30px_rgba(38,147,199,0.32)]",
  secondary:
    "button-shell--secondary border border-white/10 bg-[linear-gradient(180deg,rgba(255,255,255,0.11),rgba(255,255,255,0.035))] text-slate-100 shadow-[inset_0_1px_0_rgba(255,255,255,0.08),0_10px_22px_rgba(0,0,0,0.16)] backdrop-blur-md hover:-translate-y-[1px] hover:border-cyan-200/18 hover:bg-white/[0.09]",
  success:
    "button-shell--success border border-emerald-200/26 bg-[linear-gradient(180deg,rgba(171,255,205,0.96),rgba(91,232,156,0.85))] text-slate-950 shadow-[inset_0_1px_0_rgba(255,255,255,0.72),0_10px_24px_rgba(36,145,98,0.26)] hover:-translate-y-[1px] hover:brightness-[1.03] hover:shadow-[inset_0_1px_0_rgba(255,255,255,0.78),0_14px_30px_rgba(36,145,98,0.3)]",
  warning:
    "button-shell--warning border border-amber-200/28 bg-[linear-gradient(180deg,rgba(255,232,166,0.98),rgba(255,190,88,0.88))] text-slate-950 shadow-[inset_0_1px_0_rgba(255,255,255,0.68),0_10px_24px_rgba(184,118,20,0.24)] hover:-translate-y-[1px] hover:brightness-[1.03] hover:shadow-[inset_0_1px_0_rgba(255,255,255,0.74),0_14px_30px_rgba(184,118,20,0.28)]",
};

export default function Button({
  variant = "primary",
  fullWidth = false,
  className = "",
  children,
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
      type={type}
      className={[
        baseClasses,
        variantClasses[variant],
        fullWidth ? "w-full" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <span className="relative z-[1] flex items-center justify-center gap-2 text-center">
        {children}
      </span>
      <span className="button-shell__shine" />
      <span className="button-shell__rim" />
      <span className="button-shell__glow" />
    </button>
  );
}