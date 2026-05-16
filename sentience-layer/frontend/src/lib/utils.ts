/**
 * Utility Functions
 */

import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  const d = new Date(date);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatRelativeTime(date: string | Date): string {
  const now = new Date();
  const d = new Date(date);
  const diff = now.getTime() - d.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return formatDate(date);
}

export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + "...";
}

export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
}

export function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.9) return "text-emerald-500 bg-emerald-500/10";
  if (confidence >= 0.7) return "text-amber-500 bg-amber-500/10";
  if (confidence >= 0.5) return "text-orange-500 bg-orange-500/10";
  return "text-red-500 bg-red-500/10";
}

export function getSeverityColor(severity: string): string {
  switch (severity) {
    case "critical": return "text-red-600 bg-red-600/10 border-red-600/20";
    case "high": return "text-orange-500 bg-orange-500/10 border-orange-500/20";
    case "medium": return "text-amber-500 bg-amber-500/10 border-amber-500/20";
    default: return "text-blue-500 bg-blue-500/10 border-blue-500/20";
  }
}