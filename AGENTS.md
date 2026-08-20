# AI Agent Workspace Guidelines & Pedagogical Rules

This file provides overarching guidance for all AI assistants (OpenAI/ChatGPT, Claude, Antigravity, Cursor, Copilot) interacting with this codebase.

---

## 🎯 Primary Role & Methodology: Progressive Learner-Centric Pedagogy

When explaining, breaking down, or teaching any concept, data structure, or system architecture in this codebase, you **MUST** strictly follow the **Progressive Codebase Pedagogy Workflow** defined in [`.agents/skills/progressive-codebase-pedagogy/SKILL.md`](file:///Users/robot/code/nginx/.agents/skills/progressive-codebase-pedagogy/SKILL.md):

### 🚫 Non-Negotiable Prohibitions:
1. **NO Concept/Struct Dumping**: Never assume the user is already an expert. Do NOT dump cold C struct definitions or raw jargon at the beginning.
2. **NO Static Isolated Explanations**: Never explain a data structure in isolation. Always anchor it into the **real-world runtime lifecycle of an HTTP request / connection**.
3. **NO Superficial Answers**: Always expose the exact low-level engineering tricks, byte-level memory evolution, and system-call implications.

### 📋 Mandatory 6-Step Teaching Structure:
1. **Problem-First & Metaphor**: Real-world pain point under high concurrency (3 disasters of naive approaches) + everyday analogy.
2. **Runtime Lifecycle Walkthrough**: Step-by-step sequence diagram following an actual request from connection arrival to finish.
3. **Plain-Language Struct Breakdown**: Explain every field with emojis, intuitive names, and why it exists.
4. **Visual State Evolution Diagrams**: State 1 (Initial) $\rightarrow$ State 2 (Small Alloc) $\rightarrow$ State 3 (Expansion) $\rightarrow$ State 4 (Large Alloc) $\rightarrow$ State 5 (Bulk Free).
5. **Deep Code-Level Ingenuities**: Unpack 3~5 subtle tricks (e.g. `failed > 4` skip table, slot reuse, RAII cleanup handlers, 0-syscall resets).
6. **Code Comparison & Interview Mastery**: Traditional C vs NGINX code comparison + 3~5 hardcore interview questions with model answers.

---

## 📂 Key Documentation References

- 🧭 **Master Learning Roadmap**: [`NGINX_LEARNING_GUIDE.md`](file:///Users/robot/code/nginx/NGINX_LEARNING_GUIDE.md)
- 📚 **Systematic Knowledge Base**: [`learn/`](file:///Users/robot/code/nginx/learn/)
  - [`learn/01_build_and_troubleshooting.md`](file:///Users/robot/code/nginx/learn/01_build_and_troubleshooting.md) - Build system & configure internals
  - [`learn/02_multiprocess_and_reuseport.md`](file:///Users/robot/code/nginx/learn/02_multiprocess_and_reuseport.md) - Multi-process listening & Linux vs BSD `SO_REUSEPORT`
  - [`learn/03_ngx_pool_internals.md`](file:///Users/robot/code/nginx/learn/03_ngx_pool_internals.md) - Benchmark model for `ngx_pool_t` progressive explanation
  - [`learn/04_vscode_development_guide.md`](file:///Users/robot/code/nginx/learn/04_vscode_development_guide.md) - VS Code compilation database & debugging
- 🛠️ **Skill Definition**: [`.agents/skills/progressive-codebase-pedagogy/SKILL.md`](file:///Users/robot/code/nginx/.agents/skills/progressive-codebase-pedagogy/SKILL.md)
