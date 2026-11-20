'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import curriculumData from '@/data/curriculum.json';
import {
  GraduationCap, CheckCircle2, Calendar, Users, Award, ShieldCheck,
  Terminal, Sparkles, ExternalLink, ChevronDown, ChevronUp, Copy, Check,
  ArrowRight, BookOpen, Clock, AlertCircle, Send, Code, Database, Bot, Layers
} from 'lucide-react';

interface EnrollmentStats {
  total_enrolled: number;
  live_cohort_enrolled: number;
  self_paced_enrolled: number;
  total_live_seats: number;
  seats_remaining: number;
  is_cohort_open: boolean;
  next_cohort_start: string;
  curriculum_version: string;
}

interface WeekSchedule {
  week: number;
  title: string;
  part: string;
  chapterId?: string;
  studioLab?: string;
  concepts: string[];
  deliverable: string;
  colabUrl?: string;
}

const WEEKS_DATA: WeekSchedule[] = [
  {
    week: 1,
    title: 'The Builder Launchpad',
    part: 'Part I: Foundations',
    chapterId: 'ch00',
    concepts: ['Python for AI', 'OOP System Modeling', 'REST APIs with FastAPI', 'Git Hygiene', 'Linux CLI'],
    deliverable: 'Configure verified local Python 3.11+ environment with zero paid API dependencies and implement a typed REST microservice with SQLite persistence.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part1-foundations/ch00-builder-launchpad.ipynb'
  },
  {
    week: 2,
    title: 'Math & Stats Intuition for AI',
    part: 'Part I: Foundations',
    chapterId: 'ch01',
    concepts: ['Vector Embeddings', 'Dot Products', 'Cosine Similarity', 'Gradients & Backprop', 'Bayes Theorem'],
    deliverable: 'Implement vector distance and similarity functions from scratch in pure NumPy and verify numerical stability against PyTorch.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part1-foundations/ch01-math-and-stats-intuition.ipynb'
  },
  {
    week: 3,
    title: 'The Classical ML Bridge',
    part: 'Part I: Foundations',
    chapterId: 'ch02',
    concepts: ['Supervised vs Unsupervised', 'Loss Curves', 'Bias-Variance Tradeoff', 'L1/L2 Regularization', 'Cross-Validation'],
    deliverable: 'Train, evaluate, and benchmark a classical tabular model with scikit-learn; profile training loss convergence and feature importances.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part1-foundations/ch02-classical-ml-bridge.ipynb'
  },
  {
    week: 4,
    title: 'Generative AI Foundations',
    part: 'Part II: Core Generative AI & LLMs',
    chapterId: 'ch03',
    concepts: ['Generative vs Discriminative', 'Self-Attention Mechanism', 'Transformer Architecture', 'Tokenization', 'RLHF & Safety'],
    deliverable: 'Build a minimal PyTorch multi-head self-attention module and inspect attention weight matrices across sequence tokens.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part2-core-genai/ch03-generative-ai-foundations.ipynb'
  },
  {
    week: 5,
    title: 'Inside Large Language Models',
    part: 'Part II: Core Generative AI & LLMs',
    chapterId: 'ch04',
    concepts: ['BPE Tokenization', 'RoPE Positional Embeddings', 'KV Caching', 'LoRA Fine-Tuning', 'Quantization (AWQ/GGUF)'],
    deliverable: 'Profile KV cache memory consumption across sequence lengths and quantify 4-bit quantization speed vs perplexity tradeoffs.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part2-core-genai/ch04-inside-large-language-models.ipynb'
  },
  {
    week: 6,
    title: 'Studio Lab 1: Tokenizer & Embedding Mechanics',
    part: 'Part II: Core Generative AI & LLMs',
    studioLab: 'Tab 1: Tokenizer & Embedding Explorer',
    concepts: ['Token Boundary Effects', 'Subword Vocabularies', 'Semantic Vector Clustering', '2D PCA / t-SNE Projections'],
    deliverable: 'Run live interactive tokenization scans and explore cosine similarity geometry directly in the companion studio UI.',
  },
  {
    week: 7,
    title: 'Prompt & Context Engineering',
    part: 'Part II: Core Generative AI & LLMs',
    chapterId: 'ch05',
    concepts: ['Prompt Anatomy', 'Few-Shot Conditioning', 'Chain-of-Thought (CoT)', 'Pydantic JSON Mode', 'Prompt Injection Defense'],
    deliverable: 'Construct an adversarial-tested prompt pipeline with defensive sanitizers and automated schema enforcement.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part2-core-genai/ch05-prompt-and-context-engineering.ipynb'
  },
  {
    week: 8,
    title: 'Vector Databases & Similarity Search',
    part: 'Part III: Vector DBs, Data & Production RAG',
    chapterId: 'ch06',
    concepts: ['ANN Search', 'HNSW Graph Indexes', 'IVF Voronoi Centroids', 'Product Quantization', 'pgvector & Qdrant'],
    deliverable: 'Benchmark recall vs QPS latency curves across index configurations using local pgvector and ChromaDB.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part3-rag-data/ch06-vector-databases-and-search.ipynb'
  },
  {
    week: 9,
    title: 'Data Engineering for AI Systems',
    part: 'Part III: Vector DBs, Data & Production RAG',
    chapterId: 'ch07',
    concepts: ['ETL / ELT Pipelines', 'Document Ingestion', 'Chunk Deduplication', 'Feature Stores', 'Data Versioning (DVC)'],
    deliverable: 'Implement an idempotent document ingestion pipeline that extracts, normalizes, and versions unstructured PDFs.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part3-rag-data/ch07-data-engineering-for-ai.ipynb'
  },
  {
    week: 10,
    title: 'Production RAG Systems',
    part: 'Part III: Vector DBs, Data & Production RAG',
    chapterId: 'ch08',
    concepts: ['Hybrid Search (Dense + BM25)', 'Reciprocal Rank Fusion (RRF)', 'Cross-Encoder Reranking', 'Context Grounding', 'Citations'],
    deliverable: 'Build an end-to-end production RAG microservice with hybrid retrieval and verified citation grounding.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part3-rag-data/ch08-production-rag-systems.ipynb'
  },
  {
    week: 11,
    title: 'Studio Lab 2: RAG Chunking & Hybrid Retrieval Debugger',
    part: 'Part III: Vector DBs, Data & Production RAG',
    studioLab: 'Tab 2: RAG Chunking & Retrieval Debugger',
    concepts: ['Sliding Window Overlap', 'Dense vs Sparse Weighting (Alpha)', 'RRF k-parameter Tuning'],
    deliverable: 'Interactively benchmark retrieval precision across ambiguous enterprise queries using the live studio debugger.',
  },
  {
    week: 12,
    title: 'Autonomous AI Agents',
    part: 'Part IV: Autonomous Agents, MCP & Production MLOps',
    chapterId: 'ch09',
    concepts: ['ReAct Loop (Reason + Act)', 'Tool Invocation', 'Task Decomposition', 'Episodic Memory', 'Multi-Agent Orchestrator'],
    deliverable: 'Implement an autonomous multi-step research agent with sandboxed python execution and error recovery.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part4-agents-prod/ch09-autonomous-ai-agents.ipynb'
  },
  {
    week: 13,
    title: 'Model Context Protocol (MCP)',
    part: 'Part IV: Autonomous Agents, MCP & Production MLOps',
    chapterId: 'ch10',
    concepts: ['N×M Integration Solution', 'JSON-RPC 2.0 Transport', 'MCP Tools & Resources', 'Sampling', 'Capability Negotiation'],
    deliverable: 'Build and deploy a compliant MCP Server using the official Python SDK exposing custom enterprise tools and resources.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part4-agents-prod/ch10-model-context-protocol-mcp.ipynb'
  },
  {
    week: 14,
    title: 'Studio Labs 3 & 4: LangGraph & MCP Inspector',
    part: 'Part IV: Autonomous Agents, MCP & Production MLOps',
    studioLab: 'Tabs 3 & 4: LangGraph Flows + Live JSON-RPC Inspector',
    concepts: ['Cyclical State Graphs', 'Human-in-the-Loop Checkpoints', 'Live JSON-RPC Frame Inspection'],
    deliverable: 'Trace multi-agent execution graphs and inspect raw JSON-RPC protocol messages live in the companion UI.',
  },
  {
    week: 15,
    title: 'Production Systems & MLOps',
    part: 'Part IV: Autonomous Agents, MCP & Production MLOps',
    chapterId: 'ch11',
    concepts: ['Semantic Caching', 'Async Celery Workers', 'vLLM / Ollama Serving', 'Docker Multi-Stage Builds', 'GitHub Actions CI/CD'],
    deliverable: 'Deploy a multi-container Docker Compose stack featuring backend, caching layer, vector store, and monitoring probes.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part4-agents-prod/ch11-production-systems-and-mlops.ipynb'
  },
  {
    week: 16,
    title: 'Evals, Observability, AI Safety & Capstone Defense',
    part: 'Part IV: Autonomous Agents, MCP & Production MLOps',
    chapterId: 'ch12',
    concepts: ['RAG Triad (Faithfulness, Relevance, Precision)', 'Hallucination Detection', 'OpenTelemetry Tracing', 'Capstone Defense'],
    deliverable: 'Submit production-grade Capstone Project and complete live defense against the 100-Point Grading Rubric.',
    colabUrl: 'https://colab.research.google.com/github/abda-dc/ai-engineering-zero-to-hero/blob/main/book/chapters/part4-agents-prod/ch12-evals-observability-and-safety.ipynb'
  }
];

const RUBRIC_DIMENSIONS = [
  {
    id: 'arch',
    title: '1. Architectural Rigor & System Design',
    points: 20,
    description: 'Decoupled services, asynchronous streaming I/O, robust Docker containerization, and local-first zero-cost fallbacks.',
    criteria: [
      'Clean separation between ingestion, indexing, retrieval, and inference services.',
      'Resilient database fallback: PostgreSQL + pgvector primary, SQLite local fallback for zero-Docker dev.',
      'Asynchronous non-blocking streaming token generation with low Time-to-First-Token (TTFT).',
      'Production-ready docker-compose.yml configuration with health checks and restart policies.'
    ]
  },
  {
    id: 'mcp',
    title: '2. Model Context Protocol (MCP) & Agents',
    points: 20,
    description: 'Compliant MCP Server implementation, bidirectional JSON-RPC 2.0 communication, and cyclical agent workflows.',
    criteria: [
      'Standard-compliant MCP Server implementation exposing typed tools, resources, and prompt templates.',
      'Bidirectional JSON-RPC 2.0 transport handling initialize handshakes and error handling.',
      'Multi-agent graph orchestration (e.g. LangGraph) with cyclical state propagation.',
      'Human-in-the-loop review checkpoints for sensitive database writes or high-cost tool calls.'
    ]
  },
  {
    id: 'rag',
    title: '3. RAG Retrieval Quality & Grounding',
    points: 20,
    description: 'Hybrid sparse/dense retrieval, cross-encoder reranking, and citation-grounded generation without hallucinations.',
    criteria: [
      'Dual-stream hybrid retrieval harmonizing BM25 lexical search with dense vector ANN search.',
      'Reciprocal Rank Fusion (RRF) with cross-encoder reranking stage for optimal top-k precision.',
      'Context compression and strict bracketed citation generation [1][2] tied to source passages.',
      'Empirical validation demonstrating zero hallucinated facts across ambiguous test queries.'
    ]
  },
  {
    id: 'prod',
    title: '4. Production Engineering & Caching',
    points: 20,
    description: 'Multi-tier semantic caching, high-throughput batching, sub-100ms response targets, and thorough test coverage.',
    criteria: [
      'Two-tier caching: Exact hash match (<1ms) and semantic cosine distance thresholding (<15ms).',
      'Idempotent document ingestion pipeline handling duplicates, chunk splitting, and metadata enrichment.',
      'High-throughput model serving configuration with local Ollama or vLLM backends.',
      'Automated test suite passing with high branch coverage (pytest unit and integration tests).'
    ]
  },
  {
    id: 'evals',
    title: '5. Safety, Evals & Observability',
    points: 20,
    description: 'Automated RAG Triad benchmarking, distributed OpenTelemetry tracing, and defensive prompt security.',
    criteria: [
      'Automated evaluation pipeline measuring Context Precision, Faithfulness, and Answer Relevance.',
      'Full OpenTelemetry distributed tracing across all LLM inference and tool invocation spans.',
      'Defensive prompt injection sanitization, PII redaction, and strict JSON schema output validation.',
      'Complete documentation: Architectural diagrams, setup instructions, and audit log.'
    ]
  }
];

export default function EnrollmentPage() {
  const [stats, setStats] = useState<EnrollmentStats>({
    total_enrolled: 14,
    live_cohort_enrolled: 14,
    self_paced_enrolled: 42,
    total_live_seats: 60,
    seats_remaining: 46,
    is_cohort_open: true,
    next_cohort_start: '2026-12-01',
    curriculum_version: '2.0-fullstack'
  });

  const [expandedWeeks, setExpandedWeeks] = useState<Record<number, boolean>>({ 1: true, 6: true, 10: true, 13: true });
  const [selectedRubricId, setSelectedRubricId] = useState<string>('arch');
  const [selectedPartFilter, setSelectedPartFilter] = useState<string>('all');

  // Form State
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    githubUsername: '',
    experienceLevel: 'intermediate',
    track: 'live_cohort',
    goal: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [confirmation, setConfirmation] = useState<any | null>(null);
  const [copiedTicket, setCopiedTicket] = useState(false);
  const [copiedBash, setCopiedBash] = useState(false);

  useEffect(() => {
    fetch('/api/enroll/stats')
      .then(res => res.json())
      .then(data => {
        if (data && data.total_live_seats) {
          setStats(data);
        }
      })
      .catch(() => {});
  }, []);

  const toggleWeek = (weekNum: number) => {
    setExpandedWeeks(prev => ({ ...prev, [weekNum]: !prev[weekNum] }));
  };

  const expandAll = () => {
    const all: Record<number, boolean> = {};
    WEEKS_DATA.forEach(w => { all[w.week] = true; });
    setExpandedWeeks(all);
  };

  const collapseAll = () => {
    setExpandedWeeks({});
  };

  const filteredWeeks = selectedPartFilter === 'all'
    ? WEEKS_DATA
    : WEEKS_DATA.filter(w => w.part.toLowerCase().includes(selectedPartFilter.toLowerCase()));

  const handleEnrollSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      const res = await fetch('/api/enroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: formData.fullName,
          email: formData.email,
          github_username: formData.githubUsername || null,
          experience_level: formData.experienceLevel,
          track: formData.track,
          goal: formData.goal || null
        })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Enrollment failed. Please try again.');
      }

      setConfirmation(data);
      // Refresh stats
      fetch('/api/enroll/stats')
        .then(r => r.json())
        .then(s => setStats(s))
        .catch(() => {});
    } catch (err: any) {
      setErrorMessage(err.message || 'An unexpected error occurred.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const copyToClipboard = (text: string, type: 'ticket' | 'bash') => {
    navigator.clipboard.writeText(text);
    if (type === 'ticket') {
      setCopiedTicket(true);
      setTimeout(() => setCopiedTicket(false), 2000);
    } else {
      setCopiedBash(true);
      setTimeout(() => setCopiedBash(false), 2000);
    }
  };

  const selectedRubric = RUBRIC_DIMENSIONS.find(d => d.id === selectedRubricId) || RUBRIC_DIMENSIONS[0];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-16">
      {/* Hero Section */}
      <section className="relative rounded-3xl overflow-hidden glass-panel border border-slate-800 p-8 sm:p-14">
        <div className="absolute top-0 right-0 -mt-16 -mr-16 w-[420px] h-[420px] bg-gradient-to-br from-indigo-500/20 via-purple-500/10 to-transparent rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/4 -mb-16 w-[360px] h-[360px] bg-emerald-500/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-4xl space-y-6">
          <div className="flex flex-wrap items-center gap-3">
            <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
              <GraduationCap className="w-3.5 h-3.5" />
              16-Week Intensive AI Cohort
            </span>

            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
              <Users className="w-3.5 h-3.5" />
              {stats.seats_remaining} of {stats.total_live_seats} Live Seats Remaining
            </span>

            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-slate-300 text-xs">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              Cohort Starts: {stats.next_cohort_start}
            </span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
            From Python & Math Foundations to{' '}
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-indigo-400 bg-clip-text text-transparent">
              Production LLMs, RAG, Agents & MCP
            </span>
          </h1>

          <p className="text-base sm:text-xl text-slate-300 leading-relaxed max-w-3xl">
            Join the elite hands-on engineering cohort. Build 13 executable Jupyter Book systems, master all 140+ core AI engineering concepts, pass 4 interactive studio labs, and defend your 100-point Capstone Project.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-4">
            <a
              href="#apply"
              className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-600 hover:from-emerald-600 hover:to-indigo-700 text-white font-semibold shadow-xl shadow-emerald-500/25 transition-all group"
            >
              Apply for Cohort
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>

            <a
              href="https://abda-dc.github.io/ai-engineering-zero-to-hero/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700 font-medium transition-all"
            >
              <BookOpen className="w-4 h-4 text-emerald-400" />
              Live Online Textbook
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
            </a>

            <Link
              href="/studio"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700 font-medium transition-all"
            >
              <Terminal className="w-4 h-4 text-indigo-400" />
              Explore /studio Labs
            </Link>
          </div>
        </div>

        {/* Live Cohort Meter */}
        <div className="mt-10 pt-8 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-6">
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Live Seats Left</div>
            <div className="text-3xl font-extrabold text-emerald-400 mt-1">{stats.seats_remaining}</div>
            <div className="text-xs text-slate-500 mt-1">out of {stats.total_live_seats} max seats</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Total Enrolled</div>
            <div className="text-3xl font-extrabold text-indigo-400 mt-1">{stats.total_enrolled}</div>
            <div className="text-xs text-slate-500 mt-1">Live + Self-Paced</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Curriculum Scope</div>
            <div className="text-3xl font-extrabold text-purple-400 mt-1">16 Weeks</div>
            <div className="text-xs text-slate-500 mt-1">13 Ch + 4 Studio Labs</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Capstone Rubric</div>
            <div className="text-3xl font-extrabold text-amber-400 mt-1">100 Pts</div>
            <div className="text-xs text-slate-500 mt-1">5 Core Dimensions</div>
          </div>
        </div>
      </section>

      {/* 16-Week Curriculum Timeline */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <Calendar className="w-3.5 h-3.5" />
              Syllabus Roadmap
            </div>
            <h2 className="text-3xl font-bold text-white tracking-tight">Interactive 16-Week Curriculum</h2>
            <p className="text-sm text-slate-400 mt-1">
              Synchronized with our 13 runnable Jupyter Book chapters and 4 Split-Screen Studio labs.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={expandAll}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-medium text-slate-300 transition-colors"
            >
              Expand All
            </button>
            <button
              onClick={collapseAll}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-medium text-slate-300 transition-colors"
            >
              Collapse All
            </button>
          </div>
        </div>

        {/* Filter Tabs by Part */}
        <div className="flex flex-wrap gap-2 pt-2">
          {[
            { id: 'all', label: 'All 16 Weeks' },
            { id: 'Foundations', label: 'Part I: Foundations (W1-3)' },
            { id: 'Generative AI', label: 'Part II: Core GenAI (W4-7)' },
            { id: 'Vector DBs', label: 'Part III: RAG & Data (W8-11)' },
            { id: 'Agents', label: 'Part IV: Agents & MLOps (W12-16)' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setSelectedPartFilter(tab.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selectedPartFilter === tab.id
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                  : 'bg-slate-900/70 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Week-by-Week Accordion */}
        <div className="space-y-3">
          {filteredWeeks.map(item => {
            const isExpanded = !!expandedWeeks[item.week];
            return (
              <div
                key={item.week}
                className="rounded-2xl glass-panel border border-slate-800/90 overflow-hidden transition-all duration-200 hover:border-slate-700"
              >
                <button
                  onClick={() => toggleWeek(item.week)}
                  className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-900/40 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/20 to-emerald-500/20 border border-slate-700 flex items-center justify-center font-bold text-sm text-emerald-400 shrink-0">
                      W{item.week}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-base font-semibold text-white">{item.title}</span>
                        {item.chapterId && (
                          <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 text-xs font-mono">
                            {item.chapterId}
                          </span>
                        )}
                        {item.studioLab && (
                          <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-medium">
                            Studio Lab
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-slate-400 mt-0.5">{item.part}</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className="hidden sm:inline-block text-xs text-slate-400">
                      {item.concepts.length} Key Concepts
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-5 h-5 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-slate-400" />
                    )}
                  </div>
                </button>

                {isExpanded && (
                  <div className="px-6 py-4 bg-slate-950/50 border-t border-slate-800/80 space-y-4 text-sm">
                    {/* Concept Tags */}
                    <div>
                      <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                        Mastery Topics:
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {item.concepts.map(c => (
                          <span
                            key={c}
                            className="px-2.5 py-1 rounded-md bg-slate-900 text-slate-300 border border-slate-800 text-xs font-medium"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Deliverable Box */}
                    <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                      <div className="text-xs font-semibold text-emerald-400 mb-1 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        Weekly Hands-on Deliverable:
                      </div>
                      <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                        {item.deliverable}
                      </p>
                    </div>

                    {/* Actions & Colab Links */}
                    <div className="flex flex-wrap items-center gap-3 pt-1">
                      {item.chapterId && (
                        <Link
                          href={`/chapters/${item.chapterId}`}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-medium transition-colors"
                        >
                          <BookOpen className="w-3.5 h-3.5" />
                          Open Interactive Reader
                        </Link>
                      )}

                      {item.colabUrl && (
                        <a
                          href={item.colabUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-medium transition-colors"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                          Run in Google Colab
                        </a>
                      )}

                      {item.studioLab && (
                        <Link
                          href="/studio"
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-medium transition-colors"
                        >
                          <Terminal className="w-3.5 h-3.5" />
                          Launch {item.studioLab}
                        </Link>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Capstone Rubric Explorer */}
      <section className="space-y-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 text-purple-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <Award className="w-3.5 h-3.5" />
            Evaluation Standard
          </div>
          <h2 className="text-3xl font-bold text-white tracking-tight">100-Point Capstone Grading Rubric</h2>
          <p className="text-sm text-slate-400 mt-1">
            Every cohort graduate defends a production-grade AI system evaluated across 5 comprehensive engineering dimensions (20 pts each, 80 pts required to certify).
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Dimension Selector List */}
          <div className="space-y-3">
            {RUBRIC_DIMENSIONS.map((dim) => {
              const isSelected = dim.id === selectedRubricId;
              return (
                <button
                  key={dim.id}
                  onClick={() => setSelectedRubricId(dim.id)}
                  className={`w-full p-4 rounded-2xl text-left border transition-all ${
                    isSelected
                      ? 'bg-slate-900/90 border-indigo-500/60 shadow-lg shadow-indigo-500/10 ring-1 ring-indigo-500/40'
                      : 'glass-panel border-slate-800 hover:border-slate-700 hover:bg-slate-900/40'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-sm text-white">{dim.title}</span>
                    <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-mono font-bold">
                      {dim.points} pts
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-2 line-clamp-2">{dim.description}</p>
                </button>
              );
            })}
          </div>

          {/* Dimension Detail Viewer */}
          <div className="lg:col-span-2 rounded-2xl glass-panel border border-slate-800 p-6 sm:p-8 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
              <div>
                <h3 className="text-xl font-bold text-white">{selectedRubric.title}</h3>
                <p className="text-xs text-slate-400 mt-1">{selectedRubric.description}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-black text-indigo-400">{selectedRubric.points}</div>
                <div className="text-xs text-slate-500 uppercase">Max Points</div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Evaluation Benchmarks & Rigor Standards:
              </h4>
              <div className="space-y-2.5">
                {selectedRubric.criteria.map((criterion, idx) => (
                  <div
                    key={idx}
                    className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80"
                  >
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span className="text-xs sm:text-sm text-slate-300 leading-relaxed">{criterion}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Scoring Bands */}
            <div className="pt-2 border-t border-slate-800/80 grid grid-cols-3 gap-3 text-center">
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                <div className="text-xs text-emerald-400 font-semibold">Exemplary</div>
                <div className="text-base font-bold text-white mt-0.5">18 - 20 pts</div>
                <div className="text-[11px] text-slate-400 mt-0.5">Production-ready & tested</div>
              </div>
              <div className="p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
                <div className="text-xs text-indigo-400 font-semibold">Proficient</div>
                <div className="text-base font-bold text-white mt-0.5">14 - 17 pts</div>
                <div className="text-[11px] text-slate-400 mt-0.5">Functional with minor gaps</div>
              </div>
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                <div className="text-xs text-amber-400 font-semibold">Needs Work</div>
                <div className="text-base font-bold text-white mt-0.5">&lt; 14 pts</div>
                <div className="text-[11px] text-slate-400 mt-0.5">Missing fallbacks or tests</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enrollment Application Form */}
      <section id="apply" className="relative rounded-3xl glass-panel border border-slate-800 p-8 sm:p-12 space-y-8">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <Send className="w-3.5 h-3.5" />
            Cohort Application
          </div>
          <h2 className="text-3xl font-bold text-white tracking-tight">Reserve Your Cohort Seat</h2>
          <p className="text-sm text-slate-400 mt-1">
            Submit your information below to register for the upcoming cohort starting {stats.next_cohort_start}. Instant ticket issuance and onboarding packet provided.
          </p>
        </div>

        {confirmation ? (
          /* Confirmation Card */
          <div className="rounded-2xl bg-emerald-950/30 border border-emerald-500/40 p-6 sm:p-8 space-y-6 animate-in fade-in duration-300">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-500/20 pb-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">Enrollment Confirmed!</h3>
                  <p className="text-xs text-emerald-300/80">{confirmation.message}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 bg-slate-900 px-4 py-2 rounded-xl border border-emerald-500/30">
                <div>
                  <div className="text-[10px] text-slate-400 font-mono uppercase">Ticket ID</div>
                  <div className="text-sm font-mono font-bold text-emerald-400">{confirmation.ticket_id}</div>
                </div>
                <button
                  onClick={() => copyToClipboard(confirmation.ticket_id, 'ticket')}
                  className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
                  title="Copy Ticket ID"
                >
                  {copiedTicket ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Onboarding Checklist */}
            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-white flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-emerald-400" />
                Your Day-1 Onboarding Checklist:
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {confirmation.onboarding_steps.map((step: string, idx: number) => (
                  <div
                    key={idx}
                    className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs sm:text-sm text-slate-300 leading-relaxed"
                  >
                    {step}
                  </div>
                ))}
              </div>
            </div>

            {/* Copyable Quickstart Command */}
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="font-mono">Local Ollama Pull Commands (CPU/GPU Zero Cost)</span>
                <button
                  onClick={() => copyToClipboard('ollama pull llama3.2:3b && ollama pull qwen2.5:7b', 'bash')}
                  className="inline-flex items-center gap-1 text-emerald-400 hover:underline"
                >
                  {copiedBash ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copiedBash ? 'Copied' : 'Copy Bash'}</span>
                </button>
              </div>
              <pre className="p-3 rounded-lg bg-slate-900 font-mono text-xs text-emerald-300 overflow-x-auto">
                ollama pull llama3.2:3b && ollama pull qwen2.5:7b
              </pre>
            </div>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link
                href="/chapters/ch00"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-semibold transition-all"
              >
                <BookOpen className="w-4 h-4" />
                Launch Chapter 00: Builder Launchpad
              </Link>
              <Link
                href="/studio"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-semibold transition-all"
              >
                <Terminal className="w-4 h-4 text-indigo-400" />
                Open AI Engineering Studio
              </Link>
            </div>
          </div>
        ) : (
          /* Form Component */
          <form onSubmit={handleEnrollSubmit} className="space-y-6 max-w-2xl">
            {errorMessage && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-semibold">Enrollment Notice</div>
                  <div className="text-xs mt-0.5">{errorMessage}</div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Full Name <span className="text-emerald-400">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.fullName}
                  onChange={e => setFormData({ ...formData, fullName: e.target.value })}
                  placeholder="e.g. Alex Turner"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Work / Personal Email <span className="text-emerald-400">*</span>
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={e => setFormData({ ...formData, email: e.target.value })}
                  placeholder="alex@company.com"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  GitHub Username
                </label>
                <input
                  type="text"
                  value={formData.githubUsername}
                  onChange={e => setFormData({ ...formData, githubUsername: e.target.value })}
                  placeholder="e.g. alexturner"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  Experience Level
                </label>
                <select
                  value={formData.experienceLevel}
                  onChange={e => setFormData({ ...formData, experienceLevel: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-sm focus:outline-none focus:border-emerald-500"
                >
                  <option value="beginner">Foundational (0-1 yrs Python/ML)</option>
                  <option value="intermediate">Mid-Level Engineer (2-4 yrs)</option>
                  <option value="advanced">Senior / Lead Architect (5+ yrs)</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Cohort Track Selection
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <label
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-start gap-3 ${
                    formData.track === 'live_cohort'
                      ? 'bg-emerald-500/10 border-emerald-500/50 text-white'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <input
                    type="radio"
                    name="track"
                    value="live_cohort"
                    checked={formData.track === 'live_cohort'}
                    onChange={() => setFormData({ ...formData, track: 'live_cohort' })}
                    className="mt-1"
                  />
                  <div>
                    <div className="font-semibold text-sm text-white">Live Cohort Track</div>
                    <div className="text-xs text-slate-400 mt-0.5">
                      Weekly peer reviews, live lab walkthroughs, capstone defense.
                    </div>
                  </div>
                </label>

                <label
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-start gap-3 ${
                    formData.track === 'self_paced'
                      ? 'bg-emerald-500/10 border-emerald-500/50 text-white'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <input
                    type="radio"
                    name="track"
                    value="self_paced"
                    checked={formData.track === 'self_paced'}
                    onChange={() => setFormData({ ...formData, track: 'self_paced' })}
                    className="mt-1"
                  />
                  <div>
                    <div className="font-semibold text-sm text-white">Self-Paced Track</div>
                    <div className="text-xs text-slate-400 mt-0.5">
                      Full access to notebooks, studio labs, and automated grading.
                    </div>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Primary Goal / Capstone Project Idea (Optional)
              </label>
              <textarea
                rows={3}
                value={formData.goal}
                onChange={e => setFormData({ ...formData, goal: e.target.value })}
                placeholder="e.g. Build an enterprise MCP server connecting internal SQL schemas to multi-agent LangGraph workflows."
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-emerald-500"
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-600 hover:from-emerald-600 hover:to-indigo-700 text-white font-semibold shadow-lg shadow-emerald-500/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Reserving Seat...</span>
                </>
              ) : (
                <>
                  <span>Confirm Enrollment</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        )}
      </section>
    </div>
  );
}
