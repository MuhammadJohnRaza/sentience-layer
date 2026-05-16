/** * Loading Screen with animated logo */
export function LoadingScreen() {
  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-white dark:bg-background">
      {" "}
      <div className="relative">
        {" "}
        <div className="h-16 w-16 animate-spin rounded-full border-4 border-border border-t-slate-900 dark:border-border dark:border-t-slate-50" />{" "}
        <div className="absolute inset-0 flex items-center justify-center">
          {" "}
          <div className="h-8 w-8 rounded-full bg-card dark:bg-background" />{" "}
        </div>{" "}
      </div>{" "}
      <p className="mt-6 text-lg font-medium text-foreground dark:text-foreground">
        Sentience Layer
      </p>{" "}
      <p className="text-sm text-foreground0">
        Initializing cognitive architecture...
      </p>{" "}
    </div>
  );
}
