'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Sparkles, BookOpen, Layers, Terminal, Github, CheckCircle2, GraduationCap, Presentation } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  const [completedCount, setCompletedCount] = useState(0);

  useEffect(() => {
    // Fetch user progress
    fetch('/api/progress')
      .then(res => res.json())
      .then(data => {
        if (data && typeof data === 'object') {
          const count = Object.values(data).filter((p: any) => p.completed).length;
          setCompletedCount(count);
        }
      })
      .catch(() => {});
  }, [pathname]);

  const navLinks = [
    { name: 'Mastery Dashboard', href: '/', icon: Layers },
    { name: 'Chapters', href: '/chapters/ch00', icon: BookOpen },
    { name: 'AI Engineering Studio', href: '/studio', icon: Terminal },
    { name: 'Slides', href: '/slides', icon: Presentation },
    { name: 'Cohort & Syllabus', href: '/enroll', icon: GraduationCap },
  ];

  const progressPct = Math.round((completedCount / 13) * 100);

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="font-bold text-slate-100 tracking-tight flex items-center gap-1.5 text-base">
              AI Engineering
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-mono border border-emerald-500/30">
                Zero to Hero
              </span>
            </div>
            <div className="text-xs text-slate-400">140+ Concepts • 13 Interactive Chapters</div>
          </div>
        </Link>

        {/* Navigation Items */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href.replace('/ch00', '')));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-4 h-4" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Right Actions: Progress & GitHub */}
        <div className="flex items-center gap-3">
          <Link
            href="/enroll"
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-emerald-500 to-indigo-600 hover:from-emerald-600 hover:to-indigo-700 text-white text-xs sm:text-sm font-semibold shadow-md shadow-emerald-500/20 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <GraduationCap className="w-4 h-4" />
            <span>Enroll / Cohort</span>
          </Link>

          <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span className="text-xs font-medium text-slate-300">
              {completedCount}/13 Done ({progressPct}%)
            </span>
            <div className="w-16 h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500"
                style={{ width: `${progressPct}%` }}
              />
            </div>
          </div>

          <a
            href="https://github.com/abda-dc/ai-engineering-zero-to-hero"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition-colors"
            title="GitHub Repository"
          >
            <Github className="w-5 h-5" />
          </a>
        </div>
      </div>
    </header>
  );
}
