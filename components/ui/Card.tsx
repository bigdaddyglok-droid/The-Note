import { ReactNode } from "react";
import { cn } from "../../utils/cn";

interface CardProps {
  title: string;
  description?: string;
  children: ReactNode;
  actions?: ReactNode;
  className?: string;
}

export const Card = ({ title, description, children, actions, className }: CardProps) => (
  <section className={cn("glass p-6 space-y-4", className)}>
    <header className="flex items-start justify-between gap-4">
      <div>
        <h2 className="text-xl font-semibold text-white">{title}</h2>
        {description && <p className="text-sm text-white/60 mt-1">{description}</p>}
      </div>
      {actions}
    </header>
    <div>{children}</div>
  </section>
);
