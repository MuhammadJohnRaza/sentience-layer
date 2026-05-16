/** * Message Bubble Component */
import { Message } from "@/types";
import { cn, formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  return (
    <div className={cn("flex", isUser ? "justify-end" : "justify-start")}>
      {" "}
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-3",
          isUser
            ? "bg-card text-white"
            : isSystem
              ? "bg-red-100 text-red-800"
              : "bg-border/10 dark:bg-border/30",
        )}
      >
        {" "}
        <p className="text-sm leading-relaxed">{message.content}</p>{" "}
        {message.metadata?.actions && message.metadata.actions.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {" "}
            {message.metadata.actions.map((action: any) => (
              <Badge
                key={action.id}
                variant="outline"
                className="text-xs cursor-pointer hover:bg-slate-200"
              >
                {" "}
                {action.title}
              </Badge>
            ))}
          </div>
        )}
        <p
          className={cn(
            "mt-1 text-[10px]",
            isUser ? "text-slate-300" : "text-muted-foreground",
          )}
        >
          {" "}
          {formatDate(message.timestamp)}
          {message.metadata?.confidence && (
            <span className="ml-2">
              • {(message.metadata.confidence * 100).toFixed(0)}% confidence
            </span>
          )}
        </p>{" "}
      </div>{" "}
    </div>
  );
}
