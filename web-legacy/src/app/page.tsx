import Dashboard from "../components/Dashboard";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <h1 className="text-3xl font-bold mb-8 tracking-tight text-white">Sentience Layer (Legacy)</h1>
      <Dashboard />
    </main>
  );
}
