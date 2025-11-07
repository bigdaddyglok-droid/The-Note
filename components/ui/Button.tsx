import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "../../utils/cn";

type ButtonVariant = "primary" | "secondary" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  loading?: boolean;
}

const variants: Record<ButtonVariant, string> = {
  primary:
    "bg-accent text-white hover:bg-accent/90 focus-visible:shadow-focus disabled:bg-accent/40",
  secondary:
    "bg-white/10 text-white hover:bg-white/20 focus-visible:shadow-focus disabled:bg-white/10",
  ghost: "bg-transparent text-white/70 hover:text-white focus-visible:shadow-focus"
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", loading, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 font-medium transition disabled:cursor-not-allowed",
        variants[variant],
        className
      )}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading && (
        <span className="inline-flex h-4 w-4 animate-spin rounded-full border-2 border-white/70 border-t-transparent" />
      )}
      {children}
    </button>
  )
);

Button.displayName = "Button";
