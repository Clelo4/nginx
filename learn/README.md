# NGINX 源码与高并发架构核心知识库

欢迎来到 NGINX 源码与内核架构进阶知识库！本目录收录了我们在实际源码研读、编译实战、多进程机制、底层数据结构以及开发环境配置等维度的深度技术分析与总结。

---

## 📚 知识库模块目录

| 序号 | 文档名称 | 核心内容提要 |
| :---: | :--- | :--- |
| **01** | [**01. 编译构建体系与排错全解**](file:///Users/robot/code/nginx/learn/01_build_and_troubleshooting.md) | `./auto/configure` 架构设计哲学、特性探测（Feature Probing）、`objs/` 核心生成物解析、PCRE2/OpenSSL 依赖缺失实战排错与编译优化 |
| **02** | [**02. 多进程端口监听与 SO_REUSEPORT 跨平台机制**](file:///Users/robot/code/nginx/learn/02_multiprocess_and_reuseport.md) | 经典 fork 继承模式 vs `SO_REUSEPORT` 独立套接字模式；Linux 四元组哈希负载均衡 vs macOS/传统 BSD 行为差异深度剖析 |
| **03** | [**03. 核心数据结构：ngx_pool_t 内存池深度剖析**](file:///Users/robot/code/nginx/learn/03_ngx_pool_internals.md) | 内存池设计哲学、生命周期化零为整、六大设计巧思（大小头分离、`failed>4` 跳表、Slot 复用、RAII 清理器等）与底层工作原理 |
| **04** | [**04. VS Code 极速开发与断点调试环境指南**](file:///Users/robot/code/nginx/learn/04_vscode_development_guide.md) | Compilation Database（`compile_commands.json`）自动提取、Clangd 秒级跳转、宏展开与 LLDB/GDB 单进程 F5 断点调试 |
| **05** | [**05. NGINX 极简美学 vs Mitmproxy 内存池的“混沌之源”**](file:///Users/robot/code/nginx/learn/05_mitmproxy_vs_nginx_arena.md) | 深度诊断 mitmproxy 内存池架构过度设计问题，通过 Progressive Pedagogy 剖析 NGINX 的树状生命周期与 mitmproxy 的网状引用计数生命周期。 |
| **06** | [**06. 架构师通用思维方法论：避免“过度设计”陷阱**](file:///Users/robot/code/nginx/learn/06_architectural_thinking_methodology.md) | 提炼四大通用架构思维法则（生命周期驱动、零开销隐藏债务、抽象层级预算、错误隔离），建立避免技术自嗨与复杂度的思想防御框架。 |

---

## 🗺️ 全景九阶段学习路线
完整的全局学习规划与 20+ 道大厂高频面试真题，请查阅根目录核心路线图：
📄 [**NGINX_LEARNING_GUIDE.md**](file:///Users/robot/code/nginx/NGINX_LEARNING_GUIDE.md)
