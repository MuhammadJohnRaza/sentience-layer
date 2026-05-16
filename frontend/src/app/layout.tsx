/** * Root Layout */
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/shared/Sidebar";
import { TopBar } from "@/components/shared/TopBar";
import { ErrorBoundary } from "@/components/shared/ErrorBoundary";
import { useStore } from "@/store/useStore";
const inter = Inter({
  subsets: ["latin"],
});
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
      {" "}
      <body
        className={`${inter.className}
bg-background text-foreground`}
      >
        {" "}
        <ErrorBoundary>
          {" "}
          <div className="flex min-h-screen flex-col bg-background">
            {" "}
            <Sidebar /> <TopBar />{" "}
            <main className="flex-1 p-6"> {children}</main>{" "}
          </div>{" "}
        </ErrorBoundary>{" "}
      </body>{" "}
    </html>
  );
}
