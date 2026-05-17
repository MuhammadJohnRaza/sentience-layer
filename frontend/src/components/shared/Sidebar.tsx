"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useStore } from "@/store/useStore";
import { NAV_ITEMS } from "@/lib/constants";
import { Badge } from "@/components/ui/badge";
import { useWebSocket } from "@/hooks/useWebSocket";

export function Sidebar() {
  const pathname = usePathname();
  const { user, notifications, clearNotifications } = useStore();
  const { isConnected } = useWebSocket();

  return (
    <header className="sticky top-0 z-50 flex h-16 w-full items-center justify-between border-b-2 border-border bg-background px-4 text-foreground shadow-[0_4px_20px_rgba(0,0,0,0.8)]">
      {/* Left: Logo */}
      <div className="flex items-center gap-2 pr-4">
        <div className="flex h-9 w-9 items-center justify-center rounded-md border-2 border-border bg-border/20 text-primary-foreground shadow-[0_0_15px_rgba(124,58,237,0.5)]">
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <span className="text-xl font-black tracking-wider text-primary-foreground bg-gradient-to-r from-primary-foreground via-amber-200 to-primary-foreground bg-clip-text text-transparent hidden sm:block">
          SENTIENCE
        </span>
      </div>

      {/* Center: Scrollable Horizontal Nav */}
      <nav className="flex-1 overflow-x-auto no-scrollbar mx-4">
        <ul className="flex items-center justify-center gap-2 min-w-max px-2">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center whitespace-nowrap rounded-md px-4 py-2 text-sm font-semibold tracking-wide transition-all duration-300",
                    isActive
                      ? "text-primary-foreground border-2 border-border bg-border/30 shadow-[0_0_15px_rgba(124,58,237,0.4)] scale-105"
                      : "text-muted-foreground hover:bg-border/10 hover:text-primary-foreground hover:scale-102",
                  )}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Right: Actions & Profile */}
      <div className="flex items-center gap-4 pl-4">
        {/* Live Status indicator */}
        <div className="flex items-center gap-2">
          <div
            className={cn(
              "h-2..5 w-2.5 rounded-full animate-pulse",
              isConnected 
                ? "bg-primary shadow-[0_0_10px_rgba(124,58,237,0.8)]" 
                : "bg-destructive shadow-[0_0_10px_rgba(239,68,68,0.8)]"
            )}
          />
          <span className="text-xs font-black tracking-widest text-primary-foreground hidden md:inline">
            {isConnected ? "LIVE" : "OFFLINE"}
          </span>
        </div>

        {/* Notifications */}
        {notifications.length > 0 && (
          <div className="relative">
            <Badge
              variant="destructive"
              className="cursor-pointer font-bold border border-destructive bg-destructive text-destructive-foreground hover:bg-destructive/80 shadow-[0_0_10px_rgba(239,68,68,0.5)] animate-bounce"
              onClick={clearNotifications}
            >
              {notifications.length}
            </Badge>
          </div>
        )}

        {/* User Info */}
        <div className="flex items-center gap-3">
          <div className="text-right hidden lg:block">
            <p className="text-sm font-black text-primary-foreground leading-none">{user?.name || "Guest"}</p>
            <p className="text-[10px] font-semibold text-muted-foreground mt-1 tracking-wider leading-none">
              {user?.email || "NOT SIGNED IN"}
            </p>
          </div>
          <div className="h-9 w-9 rounded-full bg-border/20 border-2 border-border flex items-center justify-center font-black text-primary-foreground shadow-[0_0_12px_rgba(124,58,237,0.4)] hover:shadow-[0_0_20px_rgba(124,58,237,0.7)] transition-all duration-300 cursor-pointer">
            {user?.name ? user.name[0].toUpperCase() : "G"}
          </div>
        </div>
      </div>
    </header>
  );
}
