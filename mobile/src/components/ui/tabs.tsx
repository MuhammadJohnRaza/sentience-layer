"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

const TabsContext = React.createContext<{
  value: string;
  onValueChange: (value: string) => void;
}>({
  value: "",
  onValueChange: () => {},
});

export function Tabs({
  value,
  defaultValue,
  onValueChange,
  className,
  children,
  ...props
}: {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  className?: string;
  children: React.ReactNode;
} & React.HTMLAttributes<HTMLDivElement>) {
  const [localValue, setLocalValue] = React.useState(value || defaultValue || "");

  const activeValue = value !== undefined ? value : localValue;

  const handleValueChange = React.useCallback(
    (newValue: string) => {
      if (value === undefined) {
        setLocalValue(newValue);
      }
      onValueChange?.(newValue);
    },
    [value, onValueChange]
  );

  return (
    <TabsContext.Provider value={{ value: activeValue, onValueChange: handleValueChange }}>
      <div className={cn("w-full", className)} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

export const TabsList = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground border border-border/10",
      className
    )}
    {...props}
  />
));
TabsList.displayName = "TabsList";

export const TabsTrigger = React.forwardRef<
  HTMLButtonElement,
  { value: string } & React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ className, value, children, ...props }, ref) => {
  const { value: activeValue, onValueChange } = React.useContext(TabsContext);
  const isActive = activeValue === value;

  return (
    <button
      ref={ref}
      type="button"
      onClick={() => onValueChange(value)}
      className={cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-semibold tracking-wide transition-all duration-300",
        isActive
          ? "bg-card text-primary-foreground shadow-sm border border-border/30"
          : "text-muted-foreground hover:bg-background/20 hover:text-foreground/90",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
});
TabsTrigger.displayName = "TabsTrigger";

export const TabsContent = React.forwardRef<
  HTMLDivElement,
  { value: string } & React.HTMLAttributes<HTMLDivElement>
>(({ className, value, children, ...props }, ref) => {
  const { value: activeValue } = React.useContext(TabsContext);
  const isActive = activeValue === value;

  if (!isActive) return null;

  return (
    <div
      ref={ref}
      className={cn(
        "mt-2 focus-visible:outline-none",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});
TabsContent.displayName = "TabsContent";
