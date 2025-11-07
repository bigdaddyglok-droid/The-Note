import { forwardRef, SelectHTMLAttributes } from "react";
import { cn } from "../../utils/cn";

export const Select = forwardRef<HTMLSelectElement, SelectHTMLAttributes<HTMLSelectElement>>(
  ({ className, children, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        "w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-white focus:border-accent focus:outline-none focus:shadow-focus",
        className
      )}
      {...props}
    >
      {children}
    </select>
  )
);

Select.displayName = "Select";
