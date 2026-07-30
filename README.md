# Codex Doc-First Development Skill (v2.1.0 正式版)

> **专为 AI Agent 打造的工业级“文档优先 + 密码学物理门禁”软件工程技能包**  
> **An Industrial-Grade Document-First Software Engineering Skill for AI Agents**

---

## 💡 核心背景：为什么需要本项目？

在当前的 AI 辅助软件开发中，大语言模型（如 OpenAI Codex、Claude Engineer、Antigravity 等）在自主编写代码时经常面临以下 5 大致命痛点：

1. **暗箱操作与随意改码**：Agent 在未经用户许可的情况下，直接改动主干代码、删除已有配置文件或改动无关模块。
2. **黑盒死循环与 Token 浪费**：遇到编译或测试报错时，Agent 盲目反复修改、陷入死循环，消耗大量 Token 却无法解决问题。
3. **伪测试与虚假报告**：Agent 编写空断言（如 `assert True`）或把测试断言注释掉，欺骗主控程序并虚报成功。
4. **历史凭证篡改**：Agent 在修改失败后，偷改审计日志以掩盖错误。
5. **开局一次性越权授权**：传统的静态授权要么导致 Agent 中途频繁询问被打扰，要么开局一次性授权导致风险失控。

`codex-doc-first-development` 技能包就是为了**彻底解决上述痛点**而生的工业级治理方案。

---

## 🛡️ 核心治理机制 (v2.1.0 重磅升级)

本项目不仅是一套指导 Agent 行为的“文档规范”，更是一套拥有**物理 Python 脚本硬门禁**的防御体系：

- **离线 JSON Schema 机器校验**：将 Schema 从 Markdown 锚点解析解耦，独立存放于 `references/schemas/*.json`（标准 JSON Schema 规范），并保留 Markdown 提取的降级兼容。
- **跨平台 Advisory Lock & 锁抢占清理**：在代码写入阶段，通过 `lock_manager.py` 对 `docs/delivery/.log.lock` 进行基于 OS-level 咨询锁 (`fcntl`/`msvcrt`) 的互斥锁定，支持基于 PID 存活检查与 TTL 超时的死锁自动清理。
- **密码学 Merkle 链防篡改与 Artifact SHA-256 哈希审计**：所有授权与意图记录写入 `permission-audit.log`，支持多模态与二进制文件 Artifact SHA-256 哈希比对。
- **伪测试与假占位符启发式检测**：`check_task_pack.py` 内置静态分析算子，自动拦截 `assert True`、`self.assertTrue(True)`、注释断言与空 `pass` 测试块。
- **Exit Code 确定性物理退出码 (0–6)**：提供确定性、Fail-Close 机制的 CLI 退出码与 JSON 输出体。

---

## 🔄 全生命周期工作流程图 (Mermaid)

下图展示了从 `S0 启动握手` 到 `S22 阶段归档` 的完整控制流、决策门禁与分支路线：

```mermaid
flowchart TD
    S0["S0: 启动与权限握手 (Startup & Handshake)"]
    S0_Handshake["建立安全基线并选择模式 (Goal / Plan / Build)"]
    S1_Intake["S1: 需求捕获与 CoT 难点反思"]
    S1_CardMatch{"计算难点卡置信度 S(C)"}
    S1_HighConf["高置信度: 强行加载领域排查清单"]
    S1_MidConf["中置信度: 需用户显式确认"]
    S1_NoMatch["无命中: 执行标准 CoT 反思"]
    S2_Scan["S2: 项目上下文扫描 (scaffold_docs.py)"]
    S3_Draft["S3 - S5: 正式方案与架构设计"]
    S6_Docs["S6 - S8: 建立文档事实源 (AGENTS.md, README.md)"]
    S7_CheckLinks{"check_docs_links.py 链接校验"}
    S9_Phase["S9 - S10: 阶段计划与 Task Pack 拆解"]
    S10_CheckTask{"check_task_pack.py Task Pack 门禁"}
    S11_Strat["S11 - S12: 执行策略与互斥锁配置 (lock_manager.py)"]
    S13_Exec["S13: 代码修改与事务写入 (两阶段提交)"]
    S13_AuditLog["写入 AuditLog (PENDING) 并计算 Merkle 链"]
    S13_WriteLock{"互斥锁内写入物理文件"}
    S13_CleanLock["清理文件并翻转 AuditLog 为 ABORTED"]
    S13_Commit["AuditLog 翻转 COMMITTED, 写入 execution-trace.json"]
    S14_TestQuality["S14: 单元测试质量审查 (拒绝假测试)"]
    S15_TraceVerify["S15: 物理门禁校验 (verify_runtime_trace.py --json)"]
    ExitBranch{"解析退出码 Exit Code (0 - 6)"}
    S16_Acceptance["S16: 主控验收通过 (PASS)"]
    Exit1_Halt["熔断终止: 轮次超过 MAX_ITERATIONS -> 标记 BLOCKED"]
    Exit2_Check{"检查 runtime_event_reason"}
    Exit2_Fuse["扩界超过 2 次: 强行将 Goal 模式降级为 Plan 模式"]
    Exit2_Expand["解析 offending_files, 发起单次扩界申请"]
    Exit3_Halt["Fail-Close: Schema 缺失或日志损坏 -> 强行终止"]
    Exit4_Check{"检查 (4, runtime_event_reason)"}
    Exit4_Retry["安全作废: 提示已安全作废, 允许重新尝试"]
    Exit4_ParseReason{"解析 reason_details 字典"}
    Exit4_Pending["提示重试动作或翻转为 ABORTED"]
    Exit4_MissingTrace["仅补写 Result 凭证, 严格禁止重试代码写入!"]
    Exit5_Halt["安全警报 (短路): Merkle 链断链或 Hash 篡改 -> 强行终止!"]
    Exit6_Halt["数据审计 (短路): PENDING/ABORTED 带有 Result -> 强行终止!"]
    S17_Git["S17 - S19: Git 冲突处理与阶段集成验收"]
    S20_DFX["S20: 文档写回与 DFX 知识库沉淀 (写回 pain-points.md)"]
    S21_PR["S21: 合并 / PR / 发布准备 (需人工显式确认)"]
    S22_Archive["S22: 阶段归档 (docs/archive/)"]

    S0 --> S0_Handshake
    S0_Handshake --> S1_Intake
    S1_Intake --> S1_CardMatch
    S1_CardMatch -- "S(C) >= 0.8" --> S1_HighConf
    S1_CardMatch -- "0.5 <= S(C) < 0.8" --> S1_MidConf
    S1_CardMatch -- "S(C) < 0.5" --> S1_NoMatch
    S1_HighConf --> S2_Scan
    S1_MidConf --> S2_Scan
    S1_NoMatch --> S2_Scan
    S2_Scan --> S3_Draft
    S3_Draft --> S6_Docs
    S6_Docs --> S7_CheckLinks
    S7_CheckLinks -- "存在坏链/坏锚点" --> S6_Docs
    S7_CheckLinks -- "校验通过" --> S9_Phase
    S9_Phase --> S10_CheckTask
    S10_CheckTask -- "包含通配符或伪测试" --> S9_Phase
    S10_CheckTask -- "校验通过" --> S11_Strat
    S11_Strat --> S13_Exec
    S13_Exec --> S13_AuditLog
    S13_AuditLog --> S13_WriteLock
    S13_WriteLock -- "写入异常 (如磁盘满/中断)" --> S13_CleanLock
    S13_CleanLock --> S15_TraceVerify
    S13_WriteLock -- "写入成功" --> S13_Commit
    S13_Commit --> S14_TestQuality
    S14_TestQuality --> S15_TraceVerify
    S15_TraceVerify --> ExitBranch
    ExitBranch -- "Exit 0: SUCCESS" --> S16_Acceptance
    ExitBranch -- "Exit 1: ITERATION_EXCEEDED" --> Exit1_Halt
    ExitBranch -- "Exit 2: OFF_BOUNDARY_VIOLATION" --> Exit2_Check
    Exit2_Check -- "EXPANSION_LIMIT_EXCEEDED" --> Exit2_Fuse
    Exit2_Check -- "null (普通文件越界)" --> Exit2_Expand
    Exit2_Fuse --> S9_Phase
    Exit2_Expand --> S9_Phase
    ExitBranch -- "Exit 3: SCHEMA_OR_PARSE_FAILURE" --> Exit3_Halt
    ExitBranch -- "Exit 4: UNCOMMITTED_TRANSACTION" --> Exit4_Check
    Exit4_Check -- "SAFELY_ABORTED_OPERATION" --> Exit4_Retry
    Exit4_Check -- "null (静态链节点缺漏)" --> Exit4_ParseReason
    Exit4_ParseReason -- "UNCOMMITTED_PENDING" --> Exit4_Pending
    Exit4_ParseReason -- "COMMITTED_RESULT_MISSING" --> Exit4_MissingTrace
    Exit4_Retry --> S13_Exec
    Exit4_Pending --> S13_Exec
    Exit4_MissingTrace --> S13_Commit
    ExitBranch -- "Exit 5: TAMPER_OR_HASH_MISMATCH" --> Exit5_Halt
    ExitBranch -- "Exit 6: ILLEGAL_TRANSACTION_STATE" --> Exit6_Halt
    S16_Acceptance --> S17_Git
    S17_Git --> S20_DFX
    S20_DFX --> S21_PR
    S21_PR --> S22_Archive
```

---

## 🚦 确定性 0–6 退出码硬门禁协议表

校验 CLI `scripts/verify_runtime_trace.py` 输出确定性退出码，主控 Agent 严格按照以下**完备分发表**进行动作处置：

| 退出码 | 标识符 | 运行时事件原因 | 场景说明 | 主控 SKILL.md 处置动作 |
|:---:|---|:---:|---|---|
| `0` | `SUCCESS` | `null` | 审计日志、执行轨迹与 Merkle 链完全合法自洽 | **通过放行**：允许执行本轮代码或进入下一阶段 |
| `1` | `ITERATION_EXCEEDED` | `null` | 自动自愈循环轮次超过设定的上限 | **熔断终止**：强行终止自愈循环，标记阻塞并提交报告 |
| `2` | `OFF_BOUNDARY_VIOLATION` | `"EXPANSION_LIMIT_EXCEEDED"` | 扩界申请次数超过上限 (最多 2 次) | **降级融合**：强行将 Goal 模式降级为 Plan 模式 |
| `2` | `OFF_BOUNDARY_VIOLATION` | `null` | 拟改动文件超出白名单授权范围 | **发起扩界**：解析越界文件清单，向用户申请单次扩界 |
| `3` | `SCHEMA_OR_PARSE_FAILURE` | `null` | Schema 配置文件缺失、日志坏损或解析失败 | **Fail-Close**：强行卡死，提示人工修复环境 |
| `4` | `UNCOMMITTED_TRANSACTION` | `"SAFELY_ABORTED_OPERATION"` | 写入异常已在互斥锁内安全回滚为作废状态 | **安全重试**：提示本次写入已安全作废，允许重新尝试 |
| `4` | `UNCOMMITTED_TRANSACTION` | `null` | 静态链节点存在未提交或缺凭证记录 | **字典解析**：未完成事务允许重试；缺凭证事务**仅补写凭证，严禁重试代码写入** |
| `5` | `TAMPER_OR_HASH_MISMATCH` | `null` | Merkle 链断链、Hash 校验不符或轨迹伪造 | **安全警报 (短路)**：提示审计日志遭破坏，强行终止 |
| `6` | `ILLEGAL_TRANSACTION_STATE` | `null` | 未提交或已作废节点带有执行凭证的数据矛盾 | **数据审计 (短路)**：提示数据非法，强行终止人工介入 |

---

## 📂 仓库目录结构

```text
codex-doc-first-development-skill/
├── README.md                             # 项目使用说明与流程图
├── CHANGELOG.md                          # 版本变更新鲜事
├── LICENSE                               # 开源许可协议 (MIT)
├── pyproject.toml                        # 项目打包与依赖声明
├── requirements.txt                      # 依赖列表 (jsonschema, pytest)
├── .github/
│   └── workflows/
│       └── ci.yml                        # GitHub Actions CI 跨平台自动化构建流程
├── tests/                                # 单元测试与端到端集成测试套件
│   ├── fixtures/                         # 标准集成测试数据 (valid, tampered, unauthorized)
│   ├── test_check_task_pack.py           # 基准用例 TC-C01 ~ TC-C02 及伪测试检测
│   ├── test_lock_manager.py              # LockManager Advisory Lock 单元测试
│   ├── test_skill.py                     # Skill 完整性与链路测试
│   ├── test_verify_runtime_trace.py      # 基准用例 TC-V01 ~ TC-V19
│   └── test_verify_runtime_trace_end2end.py # CLI 端到端 Exit Codes (0, 2, 5) 校验
└── codex-doc-first-development/
    ├── SKILL.md                          # Skill 核心主控指南 (v2.1.0)
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── schemas/                      # 离线独立 JSON Schema 文件
    │   │   ├── AuditLogSchema.json
    │   │   ├── ExecutionTraceSchema.json
    │   │   ├── ExpansionSchema.json
    │   │   ├── PainPointCardSchema.json
    │   │   └── TaskPackSchema.json
    │   ├── schemas.md                    # JSON Schema 人类可读说明文档
    │   ├── capabilities-matrix.md        # S0-S22 阶段资产映射表
    │   ├── pain-points.md                # 6 大领域工程难点卡片库
    │   ├── methodology.md                # S0-S22 完整方法论指南
    │   ├── templates.md                  # 标准文档模板
    │   ├── review-gates.md               # 评审门禁与退出码表
    │   └── agent-git-ci.md               # 分支与 Agent 协作规约
    └── scripts/
        ├── verify_runtime_trace.py       # 物理硬门禁校验 CLI (Exit 0-6)
        ├── check_permission_log.py       # Merkle 链与 Artifact Hash 静态校验模块
        ├── lock_manager.py               # 跨平台 Advisory Lock 锁管理器
        ├── check_task_pack.py            # Task Pack 规范与伪测试校验器
        ├── check_docs_links.py           # Markdown 链接与锚点校验器
        └── scaffold_docs.py              # 文档脚手架生成器
```

---

## ⚡ 快速安装与使用指南

### 1. 环境准备与依赖安装

克隆仓库后，推荐安装必要依赖（`jsonschema` 等）：

```bash
pip install -r requirements.txt
```

### 2. 使用 Codex Skill Installer 自动安装（推荐）

直接将本仓库的 GitHub Skill URL 发送给 AI 助手：

```text
Use $skill-installer to install this Codex skill:
https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

### 3. 本地手动拷贝安装

```powershell
Copy-Item `
  -LiteralPath ".\codex-doc-first-development" `
  -Destination "$env:USERPROFILE\.codex\skills\codex-doc-first-development" `
  -Recurse `
  -Force
```

### 4. 触发指令 Prompt

```text
使用 $codex-doc-first-development，从这个项目想法开始，帮我生成需求、docs 事实源、阶段计划、Task Pack、验证门禁和归档流程：
<<<粘贴你的项目想法或需求描述>>>
```

---

## 🧪 单元测试与端到端验证

在技能包根目录下运行以下命令，验证全量 48 项单元与集成测试：

```bash
python -m unittest discover -s tests -v
```

你也可以直接使用 Fixtures 测试 `verify_runtime_trace.py` 物理门禁 CLI 的 JSON 输出：

```bash
python codex-doc-first-development/scripts/verify_runtime_trace.py \
  --trace tests/fixtures/valid_trace.json \
  --permission-log tests/fixtures/valid_audit.log \
  --task-pack tests/fixtures/valid_task_pack.md \
  --schemas codex-doc-first-development/references/schemas.md \
  --mode goal \
  --next-iteration 1 \
  --json
```

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 协议开源。
