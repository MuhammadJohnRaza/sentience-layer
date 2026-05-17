/** * Top Navigation Bar */ "use client";
import { useStore } from "@/store/useStore";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useWebSocket } from "@/hooks/useWebSocket";
export function TopBar() {
  const { user, notifications, clearNotifications } = useStore();
  const { isConnected } = useWebSocket();
  return (
    <header className="fixed left-0 right-0 top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-white/80 px-6 backdrop-blur-md dark:border-border dark:bg-background/80">
      {" "}
      <div className="flex items-center gap-4">
        {" "}
        <div className="flex items-center gap-2">
          {" "}
          <div
            className={cn(
              "h-2 w-2 rounded-full",
              isConnected ? "bg-primary" : "bg-destructive",
            )}
          />{" "}
          <span className="text-xs text-foreground0">
            {isConnected ? "Live" : "Offline"}
          </span>{" "}
        </div>{" "}
      </div>{" "}
      <div className="flex items-center gap-4">
        {" "}
        {notifications.length > 0 && (
          <div className="relative">
            {" "}
            <Badge
              variant="destructive"
              className="cursor-pointer"
              onClick={clearNotifications}
            >
              {" "}
              {notifications.length}
            </Badge>{" "}
          </div>
        )}
        <div className="flex items-center gap-3">
          {" "}
          <div className="text-right">
            {" "}
            <p className="text-sm font-medium">{user?.name || "Guest"}</p>{" "}
            <p className="text-xs text-foreground0">
              {user?.email || "Not signed in"}
            </p>{" "}
          </div>{" "}
          <div className="h-8 w-8 rounded-full bg-slate-200 dark:bg-slate-700" />{" "}
        </div>{" "}
      </div>{" "}
    </header>
  );
}
import { cn } from "@/lib/utils";
