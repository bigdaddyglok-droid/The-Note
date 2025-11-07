import { forwardRef, InputHTMLAttributes } from "react";
import { cn } from "../../utils/cn";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-white/40 focus:border-accent focus:outline-none focus:shadow-focus",
        className
      )}
      {...props}
    />
  )
);

Input.displayName = "Input";
