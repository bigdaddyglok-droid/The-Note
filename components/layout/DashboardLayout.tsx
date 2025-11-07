import { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import { Music, Gauge, AudioLines, Sparkles, Mic2, Brain } from "lucide-react";
import { cn } from "../../utils/cn";

interface DashboardLayoutProps {
  children: ReactNode;
}

const navItems = [
  { to: "/session", label: "Session", icon: Gauge },
  { to: "/audio", label: "Audio Pipeline", icon: AudioLines },
  { to: "/lyrics", label: "Lyric Intelligence", icon: Music },
  { to: "/create", label: "Imagination", icon: Sparkles },
  { to: "/voice", label: "Voice", icon: Mic2 },
  { to: "/memory", label: "Memory", icon: Brain }
];

export const DashboardLayout = ({ children }: DashboardLayoutProps) => (
  <div className="min-h-screen grid grid-cols-[280px_1fr] bg-gradient-to-br from-background via-[#0b0d1d] to-[#1c233f] text-white">
    <aside className="border-r border-white/10 glass flex flex-col">
      <div className="px-6 py-8 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-accent/20 flex items-center justify-center">
            <Music className="h-6 w-6 text-accent" />
          </div>
          <div>
            <p className="font-semibold text-lg">The Note</p>
            <p className="text-sm text-white/60 tracking-[0.3em] uppercase">Frequency OS</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-4 py-3 rounded-xl transition",
                "hover:bg-white/10 focus-visible:outline-none focus-visible:shadow-focus",
                isActive ? "bg-white/10 text-accent" : "text-white/70"
              )
            }
          >
            <Icon className="h-5 w-5" />
            <span className="font-medium">{label}</span>
          </NavLink>
        ))}
      </nav>

      <footer className="px-6 py-5 border-t border-white/5 text-xs text-white/50">
        <p>Phase 0 Architecture</p>
        <p>Resonant alignment in progress.</p>
      </footer>
    </aside>
    <main className="p-8 overflow-y-auto">{children}</main>
  </div>
);
