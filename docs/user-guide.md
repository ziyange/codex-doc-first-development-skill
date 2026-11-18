# Codex 文档优先开发 Skill 使用指南

## 1. 安装和调用

当前只有一个安装单元：`codex-doc-first-development/`。它包含启动、需求梳理、文档同步、Task Pack、UI/UX 对齐和验证脚本，内部参考文档不需要单独安装。

向 Codex 发送：

```text
安装 https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

手动安装时，将该目录完整复制到 `~/.codex/skills/` 或所配置的 `CODEX_HOME/skills/`。安装目录要保留 `SKILL.md`、`agents/`、`references/`、`scripts/`，不能只复制入口文件。

下一轮对话使用：

```text
使用 $codex-doc-first-development，在现有项目中修复 CSV 导出错误。
先阅读已有文档和相关测试，保持修改范围明确，完成后报告验证结果。
```

不需要另一个启动命令，也不需要选择子 skill。主 skill 同时支持明确调用和自动选择；调用策略见[说明](../.agents/invocation.md)。

## 2. 新项目和已有项目

新项目可以描述目标、用户、核心场景和限制：

```text
使用 $codex-doc-first-development，设计一个本地个人任务管理工具。
先明确需求和验收标准，按照实际风险选择文档深度。
```

已有项目可以直接给出问题、预期行为和允许修改的范围。智能体先检查仓库、当前文档、测试、Git 状态和已有授权，简要说明档位、范围与验证方法。它只询问会改变结果的缺失事实或尚未获得的权限。

确认过的设计、授权和契约直接复用。新增范围或未授权的外部操作仍需满足相应授权要求。

## 3. 风险档位与单点闭环

| 档位 | 判断依据 | 记录与验证 |
|---|---|---|
| Quick | 范围清晰、低风险，无架构或公共契约变化 | 回填现有任务；没有现成记录时，在最终回复交代结果，无需新建文件 |
| Standard | 一般功能、非轻量行为变化或跨模块工作，且不触发 Strict | 复用现有任务或计划，补受影响的契约和行为测试证据 |
| Strict | 安全、权限、迁移、公共契约、重大架构或生产风险 | 使用同一处记录，验证拒绝、兼容性、失败或恢复等相关路径 |

每行计划对应一个可单独验收的结果。开工前在该处写目标、授权范围、验收条件和计划检查；交付前在同一处补实际结果、证据链接和剩余阻塞。已有测试或 CI 检查覆盖同一变更时，直接引用。多个计划点可以放在一张表里，不为命令、文件修改或重试另起日志。

例如：仅修 README 文案时，核对改动即可在最终回复闭环；新增 CLI 的 JSON 输出时，在原任务里补行为测试结果；单文件权限调整仍要验证允许和拒绝的场景。开工前和交付前各合并检查一次，修复后只复查受影响及项目明确要求的检查。

Strict 档不自动启用逐操作审计。项目已使用相关协议、明确选择本 Skill 的 Goal/Plan/Build **运行时审计协议**，或规定必须审计时，按相应协议执行。使用本 Skill 的审计机制时，仍需保留 Task Pack、审计输入、白名单/黑名单及迭代限制；Goal 必须有一条有效的 `MAX_ITERATIONS: N`，N 在 1–10 之间。普通计划、开发或目标跟踪不会自动打开这个协议。

S0–S22 是按需使用的生命周期索引。独立复审、全量 CI 和阶段归档仅在风险或项目要求需要时使用；项目强制的流程和已启用的审计继续有效。

## 4. 文档同步、Task Pack 与 UI

三项能力都由主 skill 内部执行：

- `references/doc-sync.md`：事实变化时同步更新所属文档；未改变文档事实的内部重构无需机械回写。
- `references/task-pack.md`：在项目、用户或审计协议要求正式 Task Pack 时，检查其 16 个必需标题、任务范围和占位符。结构通过不等于用户授权或测试通过。
- `references/ui-ux-prototyping.md`：对图形界面变化检查受影响布局、交互和状态；复用已确认设计。没有图形界面变化时跳过原型，本地界面无需 API 绑定表。

这些文件是主 skill 内部参考，不是需要安装的插件或独立 skill。

## 5. 检查脚本

以下命令在本仓库根目录执行，需要 Python >= 3.9 和 `jsonschema`：

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python codex-doc-first-development/scripts/check_docs_links.py . --json
python codex-doc-first-development/scripts/check_task_pack.py tests/fixtures/valid_task_pack.md --json
python codex-doc-first-development/scripts/verify_runtime_trace.py --trace tests/fixtures/valid_trace.json --permission-log tests/fixtures/valid_audit.log --task-pack tests/fixtures/valid_task_pack.md --mode goal --json
```

下游项目使用安装目录定位脚本，使用项目路径定位工件。`<skill-root>`、`<project-root>` 和 `<active-task-pack>` 都要替换为实际路径，有空格时加引号：

```text
python <skill-root>/scripts/check_docs_links.py <project-root>/docs --json
python <skill-root>/scripts/check_task_pack.py <active-task-pack> --json
python <skill-root>/scripts/verify_runtime_trace.py --task-pack <active-task-pack> --mode goal --json
```

运行时命令只在采用本 Skill 的审计协议时执行。在目标项目根目录运行，按需显式提供 `--trace` 和 `--permission-log`，Goal 使用实际迭代号。默认 Schema 随安装目录解析。遇到缺失的必需记录时，应停止并修复输入，不能补空文件绕过门禁。详见[运行时审计](../codex-doc-first-development/references/runtime-audit.md)。

| 检查 | 结果解释 |
|---|---|
| 链接检查 Exit 0 | 相对链接与 GFM 锚点有效，不证明代码契约一致 |
| Task Pack Exit 0 | 结构检查通过，不授予执行权限；`warnings` 仍需审查 |
| 运行时 Exit 0 | 提供的 Trace/AuditLog 与链检查通过，不证明所有外部操作已被记录 |
| 运行时 Exit 3 | 必需输入缺失/损坏、Schema 或解析错误，应修复输入后重试 |
| 运行时 Exit 1/2/4/5/6 | 迭代限制、范围、事务、链完整性或状态问题，按审计文档的分发表处理 |

脚本无法运行时报告依赖或安装问题，不把手工清单检查说成可执行门禁通过。

## 6. 按需初始化

默认复用已有文档。确需创建文档骨架时先预览：

```text
python <skill-root>/scripts/scaffold_docs.py --root <project-root> --mode standard --auto-detect --dry-run
```

检查计划创建的文件和识别的命令后，移除 `--dry-run` 执行。现有文件默认不会被覆盖；不要未经确认使用 `--overwrite` 覆盖用户文档。显式请求 Quick 脚手架时仍保留其原有输出，但小任务通常无需调用它。

## 7. 从旧安装迁移

旧布局包含主 skill 和四个伴随目录，现统一收回主 skill：

| 旧目录 | 新位置 |
|---|---|
| `codex-doc-first-start` | 主入口与 `references/session-start.md` |
| `codex-doc-first-doc-sync` | `references/doc-sync.md` 与 `scripts/check_docs_links.py` |
| `codex-doc-first-task-pack-gate` | `references/task-pack.md` 与 `scripts/check_task_pack.py` |
| `codex-doc-first-ui-ux-prototyping` | `references/ui-ux-prototyping.md` |

迁移步骤：

1. 备份旧安装，将当前主目录完整安装到原主 skill 位置。
2. 将旧的四个伴随目录移出 skill 发现目录，防止旧描述继续自动触发；保留备份以便恢复。
3. 将项目 CI、脚本及文档中的旧检查命令改到主 skill 的 `scripts/`，不保留两份实现。
4. 下一轮对话只调用 `$codex-doc-first-development`。

主 skill 的名称和现有脚本退出码、JSON 输出保持不变。检查脚本位置迁移是破坏性变更，已通过 major changeset 明确记录；正式版本由版本 PR 同步更新，不能仅凭主分支标题判断代码是否已更新。

## 8. 发布与问题定位

README 描述当前主分支的安装方式，标题版本由发布流程同步。Changeset、版本 PR、标签发布及 Actions 权限详见[发布维护](releasing.md)。

GitHub Actions 失败时先看提交 SHA：旧提交的失败记录会保留，不会被新提交的成功覆盖。报告问题时附上任务、实际命令、退出码、预期与实际结果。
