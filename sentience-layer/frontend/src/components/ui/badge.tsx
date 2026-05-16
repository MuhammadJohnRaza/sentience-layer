import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-[#A855F7] focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-[#EAB308] text-black shadow hover:bg-[#EAB308]/80",
        secondary:
          "border-zinc-700 bg-zinc-800 text-slate-200 hover:bg-zinc-700",
        destructive:
          "border-transparent bg-red-900/70 text-red-300 shadow hover:bg-red-900",
        outline:
          "border-zinc-700 text-[#A855F7] bg-transparent hover:bg-purple-900/20",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
