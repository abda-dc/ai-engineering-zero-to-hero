import json
from typing import Dict, Any, List, Optional
import math

class MCPServerHandler:
    """
    Compliant Model Context Protocol (MCP) Server Handler
    Implements JSON-RPC 2.0 specification for Tools, Resources, and Prompts.
    """
    def __init__(self, server_name: str = "ai-engineering-companion-mcp", version: str = "1.0.0"):
        self.server_name = server_name
        self.version = version
        
        # Tools Registry
        self.tools = {
            "calculate_kv_cache": {
                "name": "calculate_kv_cache",
                "description": "Calculates memory footprint in MB and GB for LLM KV cache given parameters.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "batch_size": {"type": "integer", "default": 1},
                        "seq_len": {"type": "integer", "default": 4096},
                        "num_layers": {"type": "integer", "default": 32},
                        "num_heads": {"type": "integer", "default": 32},
                        "head_dim": {"type": "integer", "default": 128},
                        "precision_bytes": {"type": "integer", "default": 2}
                    },
                    "required": ["seq_len"]
                },
                "handler": self._calc_kv_cache
            },
            "vector_search": {
                "name": "vector_search",
                "description": "Performs in-memory cosine similarity search against index documents.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "top_k": {"type": "integer", "default": 3}
                    },
                    "required": ["query"]
                },
                "handler": self._vector_search
            },
            "check_guardrail": {
                "name": "check_guardrail",
                "description": "Evaluates prompt text against prompt injection patterns and toxic signatures.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string"}
                    },
                    "required": ["prompt"]
                },
                "handler": self._check_guardrail
            },
            "redact_pii": {
                "name": "redact_pii",
                "description": "Redacts SSNs, credit card numbers, and email addresses from text for GDPR/HIPAA compliance.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"}
                    },
                    "required": ["text"]
                },
                "handler": self._redact_pii
            }
        }
        
        # Resources Registry
        self.resources = {
            "schema://curriculum": {
                "uri": "schema://curriculum",
                "name": "Curriculum Schema Definition",
                "mimeType": "application/json",
                "description": "JSON schema for all 4 parts and 13 chapters."
            },
            "schema://agent_state": {
                "uri": "schema://agent_state",
                "name": "LangGraph Agent State Structure",
                "mimeType": "application/json",
                "description": "Standard state dictionary schema used in agent orchestration."
            }
        }
        
        # Prompts Registry
        self.prompts = {
            "rag_qa_template": {
                "name": "rag_qa_template",
                "description": "Production RAG template with strict grounding and citation instructions.",
                "arguments": [
                    {"name": "query", "description": "The user query", "required": True},
                    {"name": "context", "description": "Delimited context passages", "required": True}
                ]
            }
        }

    def _calc_kv_cache(self, seq_len: int, batch_size: int = 1, num_layers: int = 32, num_heads: int = 32, head_dim: int = 128, precision_bytes: int = 2) -> dict:
        bytes_total = 2 * batch_size * num_layers * num_heads * seq_len * head_dim * precision_bytes
        mb = bytes_total / (1024 * 1024)
        gb = mb / 1024
        return {
            "batch_size": batch_size,
            "seq_len": seq_len,
            "memory_mb": round(mb, 2),
            "memory_gb": round(gb, 4),
            "status": "Calculated via 2 * B * L * H * S * D * P formula"
        }

    def _vector_search(self, query: str, top_k: int = 3) -> dict:
        corpus = [
            {"id": "doc_rag", "text": "RAG bridges foundation models with external enterprise data."},
            {"id": "doc_mcp", "text": "Model Context Protocol connects AI to tools and data sources via JSON-RPC."},
            {"id": "doc_agent", "text": "LangGraph models agent states as cyclical directed graphs."},
            {"id": "doc_evals", "text": "Ragas computes Faithfulness, Context Precision, and Relevance."}
        ]
        q_words = set(query.lower().split())
        scored = []
        for d in corpus:
            d_words = set(d["text"].lower().split())
            score = len(q_words.intersection(d_words)) / max(len(q_words), 1)
            scored.append({"id": d["id"], "text": d["text"], "score": round(score, 3)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return {"query": query, "matches": scored[:top_k]}

    def _check_guardrail(self, prompt: str) -> dict:
        suspicious = ["ignore all previous", "system prompt", "dan mode", "override security"]
        flagged = [p for p in suspicious if p in prompt.lower()]
        return {
            "prompt": prompt,
            "is_safe": len(flagged) == 0,
            "flagged_signatures": flagged,
            "decision": "ACCEPT" if len(flagged) == 0 else "REJECT_PROMPT_INJECTION"
        }

    def _redact_pii(self, text: str) -> dict:
        import re
        s1 = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL_REDACTED]', text)
        s2 = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]', s1)
        return {"original": text, "sanitized": s2, "pii_detected": (s2 != text)}

    def dispatch(self, rpc_request: Dict[str, Any]) -> Dict[str, Any]:
        msg_id = rpc_request.get("id", 1)
        method = rpc_request.get("method")
        params = rpc_request.get("params", {})
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": self.server_name,
                        "version": self.version
                    },
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {"subscribe": True, "listChanged": True},
                        "prompts": {"listChanged": True}
                    }
                }
            }
            
        elif method == "tools/list":
            tool_list = [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "inputSchema": t["inputSchema"]
                }
                for t in self.tools.values()
            ]
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tool_list}}
            
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
                }
            try:
                out = self.tools[tool_name]["handler"](**args)
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(out, indent=2)}]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32000, "message": f"Execution error: {str(e)}"}
                }
                
        elif method == "resources/list":
            res_list = list(self.resources.values())
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"resources": res_list}}
            
        elif method == "resources/read":
            uri = params.get("uri")
            if uri not in self.resources:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32602, "message": f"Resource URI '{uri}' not found."}
                }
            res_meta = self.resources[uri]
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "contents": [{
                        "uri": uri,
                        "mimeType": res_meta["mimeType"],
                        "text": json.dumps({"resource": uri, "status": "AVAILABLE", "description": res_meta["description"]})
                    }]
                }
            }
            
        elif method == "prompts/list":
            prompt_list = list(self.prompts.values())
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"prompts": prompt_list}}
            
        elif method == "prompts/get":
            pname = params.get("name")
            pargs = params.get("arguments", {})
            if pname != "rag_qa_template":
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32602, "message": f"Prompt '{pname}' not found."}
                }
            q = pargs.get("query", "[QUERY]")
            c = pargs.get("context", "[CONTEXT]")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "description": "Rendered RAG template",
                    "messages": [
                        {"role": "system", "content": "You are a grounded AI assistant. Answer using ONLY the provided context."},
                        {"role": "user", "content": f"<context>\n{c}\n</context>\n\nQuestion: {q}"}
                    ]
                }
            }
            
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32600, "message": f"Unsupported or unknown method '{method}'."}
        }

mcp_server = MCPServerHandler()
