# 01. NGINX 编译构建体系与排错全解

---

## 🎯 1. 为什么必须/推荐从源码编译 NGINX？

相比直接使用系统的二进制包（如 `apt install nginx` 或 `yum install nginx`），从源码编译是生产高性能优化与二次开发的标准姿势：

```mermaid
flowchart TD
    ROOT["🎯 NGINX 源码编译的 5 大核心原因"]

    ROOT --> P1["⚡ 极致性能与硬件调优"]
    P1 --> P1_1["CPU 专属指令集 (-march=native)"]
    P1 --> P1_2["全程序链接时优化 (-flto)"]
    P1 --> P1_3["高性能内存分配器 (jemalloc/tcmalloc)"]

    ROOT --> P2["🛡️ 模块按需裁剪与瘦身"]
    P2 --> P2_1["剔除无用模块减小体积 (2~3MB)"]
    P2 --> P2_2["降低内存常驻开销"]
    P2 --> P2_3["收敛系统安全攻击面"]

    ROOT --> P3["🔌 集成第三方/自研模块"]
    P3 --> P3_1["OpenResty / Lua 模块"]
    P3 --> P3_2["Brotli / 动态鉴权模块"]
    P3 --> P3_3["自研企业级网关插件"]

    ROOT --> P4["🚀 启用前沿协议特性"]
    P4 --> P4_1["HTTP/3 & QUIC (v3)"]
    P4 --> P4_2["TLS 1.3 / OpenSSL 3.0+"]
    P4 --> P4_3["AIO 线程池卸载阻塞 I/O"]

    ROOT --> P5["🔍 源码调试与可观测性"]
    P5 --> P5_1["--with-debug 毫秒级跟踪"]
    P5 --> P5_2["AddressSanitizer 内存检查"]
    P5 --> P5_3["保留 GDB/LLDB 调试符号 (-O0 -g)"]
```

---

## 🛠️ 2. NGINX 自研构建系统的设计哲学

NGINX 没有采用 `CMake` 或 GNU `Autotools`，而是使用由作者 Igor Sysoev 纯手工编写的基于 POSIX Shell 的 [`auto/`](file:///Users/robot/code/nginx/auto) 脚本体系。

```mermaid
sequenceDiagram
    autonumber
    actor Dev as 开发者
    participant Configure as auto/configure
    participant Probe as 特性探测 (auto/feature, auto/os)
    participant Gen as 代码生成 (auto/modules, auto/make)
    participant Objs as 生成物目录 (objs/)

    Dev->>Configure: 执行 ./auto/configure [参数]
    Configure->>Probe: 探测编译器版本与 C99 特性
    Configure->>Probe: 探测 OS 系统调用 (epoll, kqueue, sendfile 等)
    Configure->>Probe: 探测外部依赖库 (PCRE2, OpenSSL, zlib)
    Probe->>Gen: 汇总特性宏与模块列表
    Gen->>Objs: 1. objs/ngx_auto_config.h (全量特性宏)
    Gen->>Objs: 2. objs/ngx_modules.c (决定模块执行顺序数组)
    Gen->>Objs: 3. objs/Makefile (编译规则)
    Dev->>Objs: make 并行编译
```

### 核心机制精粹：
1. **零外部构建依赖**：仅依赖基础 `/bin/sh`，无需 Python/CMake 等复杂环境。
2. **真实试编测试（Feature Probing）**：在 [`auto/feature`](file:///Users/robot/code/nginx/auto/feature) 中通过现场生成微型 C 代码调用 `cc` 编译测试，而非仅靠系统版本字符串判断。
3. **固化模块执行拓扑（`ngx_modules.c`）**：HTTP 过滤链（Filter Chain）是单向链表，执行顺序由 [`auto/modules`](file:///Users/robot/code/nginx/auto/modules) 输出到 `objs/ngx_modules.c` 的物理数组顺序严格固化，消除运行时查表开销。
4. **预编译宏消除运行时分支**：探测结果全部写入 [`objs/ngx_auto_config.h`](file:///Users/robot/code/nginx/objs/ngx_auto_config.h)，源码通过 `#if (NGX_HAVE_EPOLL)` 条件编译，运行时零多余分支判断。

---

## 🚨 3. 编译失败实战分析与排错（以 PCRE/PCRE2 为例）

### 报错现象：
```text
checking for PCRE2 library ... not found
checking for PCRE library ... not found
...
./auto/configure: error: the HTTP rewrite module requires the PCRE library.
```

### 根本原因剖析：
1. NGINX 默认启用 [`ngx_http_rewrite_module`](file:///Users/robot/code/nginx/src/http/modules/ngx_http_rewrite_module.c)（URL 重写与重定向），该模块强依赖 **PCRE / PCRE2** 正则库。
2. 查看 [`objs/autoconf.err`](file:///Users/robot/code/nginx/objs/autoconf.err) 发现，Clang 试编 `#include <pcre2.h>` 时报错 `fatal error: 'pcre.h' file not found`，系统默认搜索路径缺少该库的头文件与动态库。

### 解决方案：
- **方案 A（快速验证/无需外部依赖）**：
  ```bash
  ./auto/configure --without-http_rewrite_module
  make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu)
  ```
- **方案 B（全功能生产配置，注入 Homebrew 路径）**：
  ```bash
  brew install pcre2 openssl@3 zlib
  ./auto/configure \
      --with-debug \
      --with-http_ssl_module \
      --with-http_v2_module \
      --with-http_stub_status_module \
      --with-http_gzip_static_module \
      --with-cc-opt="-I/opt/homebrew/opt/pcre2/include -I/opt/homebrew/opt/openssl@3/include" \
      --with-ld-opt="-L/opt/homebrew/opt/pcre2/lib -L/opt/homebrew/opt/openssl@3/lib"
  make -j$(sysctl -n hw.ncpu)
  ```
