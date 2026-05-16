import * as React from "react"
import { cn } from "@/lib/utils"

const Progress = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { value?: number }
>(({ className, value, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "relative h-1.5 w-full overflow-hidden rounded-full bg-zinc-800",
      className
    )}
    {...props}
  >
    <div
      className="h-full flex-1 bg-gradient-to-r from-[#A855F7] to-[#EAB308] transition-all duration-500"
      style={{ width: `${value || 0}%` }}
    />
  </div>
))
Progress.displayName = "Progress"

export { Progress }
