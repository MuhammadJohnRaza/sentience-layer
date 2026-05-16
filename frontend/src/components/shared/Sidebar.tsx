"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useStore } from "@/store/useStore";
import { NAV_ITEMS } from "@/lib/constants";
import { Button } from "@/components/ui/button";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 flex h-16 w-full items-center justify-between border-b-2 border-border bg-background px-4 text-foreground">
      {/* Left: Logo */}
      <div className="flex items-center gap-2 pr-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-border text-background">
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <span className="text-xl font-bold tracking-tight text-primary-foreground hidden md:block">
          Sentience Layer
        </span>
      </div>

      {/* Center: Scrollable Nav */}
      <nav className="flex-1 overflow-x-auto no-scrollbar">
        <ul className="flex items-center gap-1 min-w-max px-2">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium transition-all duration-200",
                    isActive
                      ? "text-primary-foreground border-b-2 border-border bg-border/20 shadow-[0_0_10px_rgba(124,58,237,0.3)]"
                      : "text-muted-foreground hover:bg-border/10 hover:text-foreground",
                  )}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Right: Actions */}
      <div className="flex items-center gap-2 pl-4">
        <Button variant="ghost" size="icon" className="text-primary-foreground hover:bg-border/20">
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </Button>
        <div className="h-8 w-8 rounded-full bg-border/30 border border-border flex items-center justify-center text-primary-foreground">
          U
        </div>
      </div>
    </header>
  );
}
