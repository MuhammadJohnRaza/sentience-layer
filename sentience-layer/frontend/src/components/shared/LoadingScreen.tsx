/**
 * Loading Screen with animated logo
 */

export function LoadingScreen() {
  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center bg-white dark:bg-slate-950">
      <div className="relative">
        <div className="h-16 w-16 animate-spin rounded-full border-4 border-slate-200 border-t-slate-900 dark:border-slate-800 dark:border-t-slate-50" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-8 w-8 rounded-full bg-slate-900 dark:bg-slate-50" />
        </div>
      </div>
      <p className="mt-6 text-lg font-medium text-slate-900 dark:text-slate-50">Sentience Layer</p>
      <p className="text-sm text-slate-500">Initializing cognitive architecture...</p>
    </div>
  );
}