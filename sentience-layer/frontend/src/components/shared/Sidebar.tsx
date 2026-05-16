/**
 * Top Navigation Bar (replaces vertical sidebar)
 * Black · Purple · Gold theme
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { NAV_ITEMS } from "@/lib/constants";
import { useWebSocket } from "@/hooks/useWebSocket";

// Compact icon map (SVG paths only)
const ICON_PATHS: Record<string, string> = {
  LayoutDashboard: "M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z",
  MessageSquare: "M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z",
  Trophy: "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z",
  Zap: "M13 10V3L4 14h7v7l9-11h-7z",
  BookOpen: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253",
  Shield: "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z",
  Brain: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
  GitBranch: "M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4",
  FlaskConical: "M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z",
  Rocket: "M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.2-12.64C20.78 1.88 18.43 0 15.83 0c-3.01 0-5.55 2.29-5.83 5.26A14.93 14.93 0 013.66 7.78c-1.04.66-1.66 1.82-1.53 3.04.17 1.66 1.66 2.96 3.37 2.96h.71c-.02.34-.04.68-.04 1.03 0 3.21 1.78 6.01 4.41 7.48.17.1.34.18.52.26l.52-.26c2.63-1.47 4.41-4.27 4.41-7.48 0-.35-.02-.69-.04-1.03h.71c1.71 0 3.2-1.3 3.37-2.96.13-1.22-.49-2.38-1.53-3.04z",
  Network: "M13 10V3L4 14h7v7l9-11h-7z",
  TrendingUp: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
  Moon: "M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z",
  HelpCircle: "M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
  UserCircle: "M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z",
};

function NavIcon({ name }: { name: string }) {
  const d = ICON_PATHS[name] || ICON_PATHS.LayoutDashboard;
  return (
    <svg className="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
      <path strokeLinecap="round" strokeLinejoin="round" d={d} />
    </svg>
  );
}

export function Sidebar() {
  const pathname = usePathname();
  const { isConnected } = useWebSocket();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* ── Top navbar ── */}
      <header className="fixed top-0 left-0 right-0 z-50 h-14 bg-black border-b border-zinc-800 flex items-center px-4 gap-0">

        {/* Brand */}
        <Link href="/dashboard" className="flex items-center gap-2 mr-6 flex-shrink-0">
          <div className="h-6 w-6 rounded-full bg-purple-900/50 border border-[#EAB308]/60 flex items-center justify-center">
            <div className="h-2 w-2 rounded-full bg-[#EAB308] animate-pulse" />
          </div>
          <span className="text-sm font-bold tracking-tight text-[#EAB308] hidden sm:block">Sentience</span>
          <span className="text-[10px] text-zinc-700 hidden lg:block font-mono">v4.0</span>
        </Link>

        {/* Desktop nav links — scrollable */}
        <nav className="hidden md:flex items-center gap-0.5 flex-1 overflow-x-auto scrollbar-none">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                title={item.label}
                className={cn(
                  "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all duration-150",
                  isActive
                    ? "bg-purple-900/40 text-[#EAB308] border border-[#EAB308]/30"
                    : "text-[#A855F7]/70 hover:bg-purple-900/10 hover:text-[#EAB308] border border-transparent"
                )}
              >
                <NavIcon name={item.icon} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Right side — status + mobile toggle */}
        <div className="ml-auto flex items-center gap-3 flex-shrink-0">
          {/* Connection indicator */}
          <div className="hidden sm:flex items-center gap-1.5">
            <div className={cn("h-1.5 w-1.5 rounded-full", isConnected ? "bg-emerald-400 animate-pulse" : "bg-red-500")} />
            <span className="text-[10px] text-zinc-600">{isConnected ? "Live" : "Offline"}</span>
          </div>

          {/* Avatar */}
          <div className="h-7 w-7 rounded-full bg-purple-900/40 border border-[#EAB308]/40 flex items-center justify-center">
            <svg className="h-3.5 w-3.5 text-[#EAB308]/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>

          {/* Mobile hamburger */}
          <button
            className="md:hidden text-[#EAB308]/60 hover:text-[#EAB308] transition-colors"
            onClick={() => setMobileOpen((v) => !v)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? (
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
      </header>

      {/* ── Mobile dropdown menu ── */}
      {mobileOpen && (
        <div className="fixed top-14 left-0 right-0 z-40 bg-black border-b border-zinc-800 md:hidden shadow-xl">
          <nav className="grid grid-cols-2 gap-1 p-3 max-h-[60vh] overflow-y-auto">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                  className={cn(
                    "flex items-center gap-2 px-3 py-2.5 rounded-lg text-xs font-medium transition-all",
                    isActive
                      ? "bg-purple-900/40 text-[#EAB308] border border-[#EAB308]/30"
                      : "text-[#A855F7]/70 hover:bg-purple-900/10 hover:text-[#EAB308] border border-transparent"
                  )}
                >
                  <NavIcon name={item.icon} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      )}
    </>
  );
}