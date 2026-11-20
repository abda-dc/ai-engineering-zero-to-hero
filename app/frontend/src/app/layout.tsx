import type { Metadata } from 'next';
import './globals.css';
import Navbar from '@/components/Navbar';

export const metadata: Metadata = {
  title: 'AI Engineering: Zero to Hero | Production Curriculum & Companion App',
  description: 'Master 140+ core Generative AI, RAG, Autonomous Agents, and MCP concepts through interactive chapters and live developer studio.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased flex flex-col selection:bg-emerald-500/20 selection:text-emerald-300">
        <Navbar />
        <main className="flex-1">
          {children}
        </main>
        <footer className="border-t border-slate-900 bg-slate-950/90 py-8 px-4 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              AI Engineering: Zero to Hero • Built for Autonomous AI Engineers
            </div>
            <div className="flex items-center gap-4">
              <span>Local-First Execution</span>
              <span>•</span>
              <span>Model Context Protocol</span>
              <span>•</span>
              <span>Production RAG</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
