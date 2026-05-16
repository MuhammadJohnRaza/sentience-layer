/**
 * Root Layout — Horizontal top navbar, black background
 */

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/shared/Sidebar";
import { ErrorBoundary } from "@/components/shared/ErrorBoundary";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Sentience Layer v4.0",
  description: "Cognitive Operating System powered by Google Antigravity",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.className} bg-black text-slate-100 antialiased`}>
        <ErrorBoundary>
          {/* Top navbar */}
          <Sidebar />

          {/* Main content — push down by navbar height (h-14 = 3.5rem) */}
          <main className="pt-14 min-h-screen">
            <div className="px-6 py-6">
              {children}
            </div>
          </main>
        </ErrorBoundary>
      </body>
    </html>
  );
}