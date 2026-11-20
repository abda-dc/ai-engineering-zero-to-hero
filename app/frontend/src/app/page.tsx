'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import curriculumData from '@/data/curriculum.json';
import { 
  Sparkles, BookOpen, Layers, Terminal, CheckCircle2, ArrowRight, 
  Search, Code2, Cpu, Database, Bot, ShieldCheck, Flame, Compass
} from 'lucide-react';

export default function DashboardPage() {
  const [progressMap, setProgressMap] = useState<Record<string, any>>({});
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('/api/progress')
      .then(res => res.json())
      .then(data => {
        if (data && typeof data === 'object') {
          setProgressMap(data);
        }
      })
      .catch(() => {});
  }, []);

  const totalChapters = curriculumData.total_chapters;
  const totalConcepts = curriculumData.total_concepts;
  const completedCount = Object.values(progressMap).filter(p => p.completed).length;
  const completionPercentage = Math.round((completedCount / totalChapters) * 100);

  const partIcons = [Compass, Cpu, Database, Bot];
  const partColors = [
    'from-blue-500/20 to-cyan-500/10 border-blue-500/30 text-blue-400',
    'from-purple-500/20 to-pink-500/10 border-purple-500/30 text-purple-400',
    'from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400',
    'from-amber-500/20 to-orange-500/10 border-amber-500/30 text-amber-400'
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      {/* Hero Section */}
      <section className="relative rounded-3xl overflow-hidden glass-panel border border-slate-800 p-8 sm:p-12">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 -mb-10 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
            <Flame className="w-3.5 h-3.5" />
            Master Modern AI Engineering
          </div>

          <h1 className="text-4xl sm:text-5xl font-black text-white tracking-tight leading-tight">
            From Python & Math Foundations to{' '}
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-indigo-400 bg-clip-text text-transparent">
              Production RAG, Agents & MCP
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed">
            The definitive engineering-grade curriculum with 13 runnable Jupyter chapters, 140+ core concepts, 
            local CPU/mock fallbacks, hands-on capstone labs, and an interactive developer studio.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              href="/chapters/ch00"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-medium shadow-lg shadow-emerald-500/25 transition-all group"
            >
              Start First Chapter
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>

            <Link
              href="/studio"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-medium transition-all"
            >
              <Terminal className="w-4 h-4 text-emerald-400" />
              Launch Split-Screen Studio
            </Link>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="mt-10 pt-8 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-6">
          <div>
            <div className="text-3xl font-extrabold text-white">4 Parts</div>
            <div className="text-xs text-slate-400 font-medium mt-1">Progressive Roadmap</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-emerald-400">13 Chapters</div>
            <div className="text-xs text-slate-400 font-medium mt-1">Fully Runnable .ipynb</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-indigo-400">{totalConcepts} Concepts</div>
            <div className="text-xs text-slate-400 font-medium mt-1">Exhaustive Coverage</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-amber-400">{completionPercentage}%</div>
            <div className="text-xs text-slate-400 font-medium mt-1">Mastery Progress</div>
          </div>
        </div>
      </section>

      {/* Filter & Search Bar */}
      <section className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search concepts (e.g. MCP, RAG, HNSW, LoRA)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/50"
          />
        </div>

        {selectedConcept && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Filtering by:</span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/40">
              {selectedConcept}
              <button onClick={() => setSelectedConcept(null)} className="hover:text-white">✕</button>
            </span>
          </div>
        )}
      </section>

      {/* Curriculum Parts & Chapters Grid */}
      <div className="space-y-12">
        {curriculumData.parts.map((part, partIdx) => {
          const PartIcon = partIcons[partIdx % partIcons.length];
          const colorClass = partColors[partIdx % partColors.length];

          // Filter chapters by search or selected concept
          const filteredChapters = part.chapters.filter(ch => {
            if (selectedConcept) {
              return ch.concepts.includes(selectedConcept);
            }
            if (searchQuery.trim()) {
              const q = searchQuery.toLowerCase();
              return (
                ch.title.toLowerCase().includes(q) ||
                ch.concepts.some(c => c.toLowerCase().includes(q))
              );
            }
            return true;
          });

          if (filteredChapters.length === 0) return null;

          return (
            <section key={part.id} className="space-y-6">
              {/* Part Header */}
              <div className="flex items-center gap-3">
                <div className={`p-2.5 rounded-xl border bg-gradient-to-br ${colorClass}`}>
                  <PartIcon className="w-6 h-6" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white tracking-tight">{part.title}</h2>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {filteredChapters.length} {filteredChapters.length === 1 ? 'Chapter' : 'Chapters'}
                  </p>
                </div>
              </div>

              {/* Chapters Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredChapters.map((ch) => {
                  const isCompleted = progressMap[ch.id]?.completed;
                  return (
                    <div
                      key={ch.id}
                      className="glass-card rounded-2xl p-6 flex flex-col justify-between border border-slate-800 hover:border-slate-700 group transition-all"
                    >
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-mono font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
                            {ch.id.toUpperCase()}
                          </span>
                          {isCompleted ? (
                            <span className="inline-flex items-center gap-1 text-xs text-emerald-400 font-medium">
                              <CheckCircle2 className="w-3.5 h-3.5" /> Completed
                            </span>
                          ) : (
                            <span className="text-xs text-slate-500">4 Quizzes • 1 Capstone</span>
                          )}
                        </div>

                        <h3 className="text-lg font-bold text-slate-100 group-hover:text-emerald-400 transition-colors">
                          {ch.title}
                        </h3>

                        {/* Concept Badges */}
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {ch.concepts.slice(0, 6).map((concept) => (
                            <button
                              key={concept}
                              onClick={(e) => {
                                e.preventDefault();
                                setSelectedConcept(concept);
                              }}
                              className="text-[11px] px-2 py-0.5 rounded-md bg-slate-900/80 hover:bg-slate-800 text-slate-300 border border-slate-800 transition-colors"
                            >
                              {concept}
                            </button>
                          ))}
                          {ch.concepts.length > 6 && (
                            <span className="text-[11px] px-1.5 py-0.5 text-slate-500">
                              +{ch.concepts.length - 6} more
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="pt-6 mt-6 border-t border-slate-800/80 flex items-center justify-between">
                        <span className="text-xs text-slate-400 truncate max-w-[150px]">
                          {ch.capstone?.title || 'Capstone Lab'}
                        </span>
                        <Link
                          href={`/chapters/${ch.id}`}
                          className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 group/link"
                        >
                          Explore Chapter
                          <ArrowRight className="w-3.5 h-3.5 group-hover/link:translate-x-0.5 transition-transform" />
                        </Link>
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}
