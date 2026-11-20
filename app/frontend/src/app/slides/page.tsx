'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import slidesData from '@/data/slides.json';
import {
  Presentation, ChevronLeft, ChevronRight, Maximize2, Minimize2,
  FileText, ExternalLink, Download, Sparkles, BookOpen, Terminal,
  CheckCircle2, Clock, Code, Monitor, Compass, Eye, EyeOff
} from 'lucide-react';

export default function SlidesPage() {
  const decks = slidesData.decks;
  const [selectedWeek, setSelectedWeek] = useState<number>(1);
  const [currentSlideIndex, setCurrentSlideIndex] = useState<number>(0);
  const [showNotes, setShowNotes] = useState<boolean>(true);
  const [viewMode, setViewMode] = useState<'interactive' | 'iframe'>('interactive');
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const currentDeck = decks.find(d => d.week_number === selectedWeek) || decks[0];
  const slides = currentDeck.slides;
  const currentSlide = slides[currentSlideIndex] || slides[0];

  // Reset slide index when changing week
  const handleSelectWeek = (weekNum: number) => {
    setSelectedWeek(weekNum);
    setCurrentSlideIndex(0);
  };

  const nextSlide = () => {
    if (currentSlideIndex < slides.length - 1) {
      setCurrentSlideIndex(prev => prev + 1);
    }
  };

  const prevSlide = () => {
    if (currentSlideIndex > 0) {
      setCurrentSlideIndex(prev => prev - 1);
    }
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger if user is typing in an input
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;

      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'n' || e.key === 'N' || e.key === 's' || e.key === 'S') {
        setShowNotes(prev => !prev);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentSlideIndex, slides.length]);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  // Format slide markdown for clean visual rendering
  const renderSlideContent = (markdown: string) => {
    const lines = markdown.split('\n');
    const elements: React.ReactNode[] = [];
    let inCodeBlock = false;
    let codeLanguage = '';
    let codeBuffer: string[] = [];

    lines.forEach((line, idx) => {
      if (line.startsWith('```')) {
        if (!inCodeBlock) {
          inCodeBlock = true;
          codeLanguage = line.replace('```', '').trim();
          codeBuffer = [];
        } else {
          inCodeBlock = false;
          elements.push(
            <div key={`code-${idx}`} className="my-4 rounded-xl overflow-hidden border border-slate-800 bg-slate-950">
              {codeLanguage && (
                <div className="px-4 py-1.5 bg-slate-900 border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                  {codeLanguage}
                </div>
              )}
              <pre className="p-4 text-xs sm:text-sm font-mono text-emerald-300 overflow-x-auto leading-relaxed">
                <code>{codeBuffer.join('\n')}</code>
              </pre>
            </div>
          );
        }
        return;
      }

      if (inCodeBlock) {
        codeBuffer.push(line);
        return;
      }

      const trimmed = line.trim();
      if (!trimmed) {
        return;
      }

      if (trimmed.startsWith('# ')) {
        elements.push(
          <h1 key={idx} className="text-3xl sm:text-4xl font-extrabold text-sky-400 tracking-tight mb-4">
            {trimmed.replace('# ', '')}
          </h1>
        );
      } else if (trimmed.startsWith('## ')) {
        elements.push(
          <h2 key={idx} className="text-2xl sm:text-3xl font-bold text-emerald-400 tracking-tight mt-2 mb-3">
            {trimmed.replace('## ', '')}
          </h2>
        );
      } else if (trimmed.startsWith('### ')) {
        elements.push(
          <h3 key={idx} className="text-lg sm:text-xl font-semibold text-purple-400 mt-4 mb-2">
            {trimmed.replace('### ', '')}
          </h3>
        );
      } else if (trimmed.startsWith('> ')) {
        elements.push(
          <blockquote key={idx} className="border-l-4 border-sky-400 bg-slate-900/80 px-4 py-3 rounded-r-xl my-4 text-slate-300 italic text-sm sm:text-base">
            {trimmed.replace('> ', '')}
          </blockquote>
        );
      } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        elements.push(
          <li key={idx} className="ml-5 list-disc text-slate-200 text-sm sm:text-base my-1 leading-relaxed">
            <span dangerouslySetInnerHTML={{ __html: formatInline(trimmed.substring(2)) }} />
          </li>
        );
      } else if (/^\d+\.\s/.test(trimmed)) {
        elements.push(
          <li key={idx} className="ml-5 list-decimal text-slate-200 text-sm sm:text-base my-1 leading-relaxed">
            <span dangerouslySetInnerHTML={{ __html: formatInline(trimmed.replace(/^\d+\.\s/, '')) }} />
          </li>
        );
      } else {
        elements.push(
          <p key={idx} className="text-slate-200 text-sm sm:text-base my-2.5 leading-relaxed"
             dangerouslySetInnerHTML={{ __html: formatInline(trimmed) }}
          />
        );
      }
    });

    return elements;
  };

  const formatInline = (text: string) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="text-slate-300">$1</em>')
      .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-800 text-sky-300 font-mono text-xs">$1</code>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-sky-400 underline hover:text-sky-300">$1</a>');
  };

  const progressPercent = Math.round(((currentSlideIndex + 1) / slides.length) * 100);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Banner & Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <Presentation className="w-3.5 h-3.5" />
            16-Week Instructor Slide Decks
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            Presenter Mode
            <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono font-medium">
              Week {selectedWeek.toString().padStart(2, '0')} of 16
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Complete synchronized slide presentations with architectural diagrams, code walkthroughs, live demo cues, and instructor speaker notes.
          </p>
        </div>

        {/* Global Action Bar */}
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex rounded-xl bg-slate-900 p-1 border border-slate-800">
            <button
              onClick={() => setViewMode('interactive')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
                viewMode === 'interactive'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              Presenter
            </button>
            <button
              onClick={() => setViewMode('iframe')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
                viewMode === 'iframe'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              Marp HTML
            </button>
          </div>

          <button
            onClick={() => setShowNotes(!showNotes)}
            className={`px-3 py-1.5 rounded-xl border text-xs font-medium transition-colors flex items-center gap-1.5 ${
              showNotes
                ? 'bg-purple-500/20 text-purple-300 border-purple-500/40'
                : 'bg-slate-900 text-slate-400 hover:text-white border-slate-800'
            }`}
            title="Toggle Speaker Notes (Hotkeys: S or N)"
          >
            {showNotes ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
            <span>Notes (N)</span>
          </button>

          <a
            href={currentDeck.html_path}
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-medium text-slate-300 transition-colors flex items-center gap-1.5"
            title="Open standalone Marp slide deck in new tab"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Open Standalone</span>
          </a>

          <button
            onClick={toggleFullscreen}
            className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition-colors"
            title="Toggle Fullscreen (F)"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Week Selector Ribbon */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
        {decks.map(deck => {
          const isSelected = deck.week_number === selectedWeek;
          return (
            <button
              key={deck.id}
              onClick={() => handleSelectWeek(deck.week_number)}
              className={`px-3.5 py-2 rounded-xl text-xs font-medium whitespace-nowrap transition-all flex items-center gap-2 ${
                isSelected
                  ? 'bg-gradient-to-r from-emerald-500 to-indigo-600 text-white shadow-md shadow-emerald-500/20'
                  : 'bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800 hover:border-slate-700'
              }`}
            >
              <span className="font-mono font-bold">W{deck.week_number.toString().padStart(2, '0')}</span>
              <span className="hidden sm:inline-block max-w-[140px] truncate">{deck.title.split(':')[1] || deck.title}</span>
            </button>
          );
        })}
      </div>

      {/* Main Presentation Stage */}
      <div ref={containerRef} className={`space-y-4 ${isFullscreen ? 'bg-slate-950 p-6 flex flex-col justify-between h-screen' : ''}`}>
        {viewMode === 'iframe' ? (
          /* Marp Standalone HTML iFrame View */
          <div className="rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 h-[700px] shadow-2xl relative">
            <iframe
              src={currentDeck.html_path}
              className="w-full h-full border-0"
              title={currentDeck.title}
            />
          </div>
        ) : (
          /* Interactive High-Craft Presenter View */
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Slide Canvas */}
            <div className={`${showNotes ? 'lg:col-span-2' : 'lg:col-span-3'} rounded-2xl glass-panel border border-slate-800 p-8 sm:p-12 min-h-[580px] flex flex-col justify-between shadow-2xl relative overflow-hidden`}>
              <div className="absolute top-0 left-0 right-0 h-1 bg-slate-900">
                <div
                  className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-indigo-500 transition-all duration-300"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>

              {/* Slide Content Body */}
              <div className="space-y-4">
                <div className="flex items-center justify-between text-xs text-slate-500 pb-2 border-b border-slate-800/60 font-mono">
                  <span>{currentDeck.title}</span>
                  <span>Slide {currentSlideIndex + 1} of {slides.length}</span>
                </div>

                <div className="pt-2">
                  {renderSlideContent(currentSlide.markdown)}
                </div>
              </div>

              {/* Bottom Canvas Controls */}
              <div className="pt-8 mt-6 border-t border-slate-800/80 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <button
                    onClick={prevSlide}
                    disabled={currentSlideIndex === 0}
                    className="p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 disabled:opacity-30 disabled:pointer-events-none border border-slate-800 transition-colors flex items-center gap-1.5 text-xs font-semibold"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <span>Previous (←)</span>
                  </button>

                  <button
                    onClick={nextSlide}
                    disabled={currentSlideIndex === slides.length - 1}
                    className="p-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white disabled:opacity-30 disabled:pointer-events-none transition-colors flex items-center gap-1.5 text-xs font-semibold shadow-lg shadow-emerald-500/20"
                  >
                    <span>Next (→)</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>

                <div className="text-xs text-slate-400 font-mono">
                  Use <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">←</kbd> <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">→</kbd> or <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">Space</kbd> to step
                </div>
              </div>
            </div>

            {/* Speaker Notes Drawer */}
            {showNotes && (
              <div className="rounded-2xl glass-panel border border-purple-500/30 bg-slate-950/80 p-6 flex flex-col justify-between shadow-xl">
                <div className="space-y-4">
                  <div className="flex items-center justify-between border-b border-purple-500/20 pb-3">
                    <div className="flex items-center gap-2 text-purple-400 font-semibold text-sm">
                      <Sparkles className="w-4 h-4" />
                      <span>Speaker Notes & Pacing</span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-500">Instructor Guide</span>
                  </div>

                  {currentSlide.notes ? (
                    <div className="text-xs sm:text-sm text-slate-300 leading-relaxed space-y-2 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                      {currentSlide.notes}
                    </div>
                  ) : (
                    <div className="text-xs text-slate-500 italic p-4">
                      No specific notes for this slide. Emphasize visual diagram and solicit student questions.
                    </div>
                  )}

                  <div className="space-y-2 pt-2">
                    <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                      Slide Attributes:
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {currentSlide.has_code && (
                        <span className="px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20 text-[11px] font-mono flex items-center gap-1">
                          <Code className="w-3 h-3" /> Code Cell
                        </span>
                      )}
                      {currentSlide.has_demo && (
                        <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20 text-[11px] font-mono flex items-center gap-1">
                          <Terminal className="w-3 h-3" /> Live Demo Cue
                        </span>
                      )}
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[11px] font-mono">
                        Slide {currentSlideIndex + 1}/{slides.length}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500">
                  Tip: Press <kbd className="px-1 rounded bg-slate-800 text-slate-300">N</kbd> to hide this panel for students.
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Quick Chapter & Lab Bridge */}
      <div className="rounded-2xl glass-panel border border-slate-800 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <div className="text-sm font-semibold text-white">Looking for the corresponding Jupyter Chapter?</div>
            <div className="text-xs text-slate-400">Open the interactive runnable reader with mock fallbacks and quizzes.</div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/chapters/ch00"
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-semibold text-slate-200 transition-colors"
          >
            Open Reader
          </Link>
          <Link
            href="/studio"
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-xs font-semibold text-white transition-colors"
          >
            Launch Studio
          </Link>
        </div>
      </div>
    </div>
  );
}
