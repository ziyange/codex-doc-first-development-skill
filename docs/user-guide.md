# Codex Doc-First Development Skill 用户使用手册

文档状态：与当前仓库实现同步
Skill 名称：`codex-doc-first-development`

## 1. 定位

这个 Skill 是一套工程化的 Codex 文档优先软件开发工作流。它不是简单提示词，而是一个可复用的 Codex Skill 包，用于把原始想法或已有项目变更，转换成可执行、可验证、可归档的软件工程流程。

它覆盖：

1. 从 0 捕获项目想法。
2. 判断快速档、标准档、严格档。
3. 生成产品、需求、架构、阶段计划、Task Pack。
4. 规划 Codex 子智能体并行协作。
5. 管理分支、文件所有权、锁协议和 Git 冲突。
6. 执行 TDD、测试质量审查、本地验证、CI/PR 验收。
7. 进行文档回写、合并准备和阶段归档。

## 2. 当前仓库内容

可安装的 Skill 位于仓库根目录下的 `codex-doc-first-development/`。本手册位于 `docs/user-guide.md`。仓库不承诺预生成 `outputs/` 目录或 ZIP 包；如需打包，应以可安装 Skill 目录为输入自行生成。

## 3. Skill 包结构

```text
codex-doc-first-development/
  SKILL.md
  agents/
    openai.yaml
  references/
    methodology.md
    templates.md
    prompts.md
    review-gates.md
    agent-git-ci.md
    examples.md
  scripts/
    scaffold_docs.py
    check_task_pack.py
```

`SKILL.md` 是 Codex 触发后首先读取的核心工作流。

`references/methodology.md` 是完整 S0-S22 生命周期。

`references/templates.md` 是文档、Task Pack、PR、归档模板。

`references/prompts.md` 是主控、评审、worker、验收、变更控制提示词。

`references/review-gates.md` 是评审、测试、验收、合并门禁。

`references/agent-git-ci.md` 是子智能体、分支、锁、CI、PR、冲突处理规范。

`references/examples.md` 是新项目、已有功能、Bug、重构、多 Agent 阶段示例。

`scripts/scaffold_docs.py` 可以生成项目 docs 脚手架。

`scripts/check_task_pack.py` 可以检查 Task Pack 基础完整性。

## 4. 推荐安装方式：把 GitHub 地址发给 Codex

正常安装不需要用户手动复制文件。你只需要把下面这段话发给 Codex：

```text
使用 $skill-installer 安装这个 Codex Skill：
https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

Codex Agent 应使用 `skill-installer` 的 GitHub 安装脚本，把 skill 安装到 `$CODEX_HOME/skills`；如果未设置 `CODEX_HOME`，则安装到 `~/.codex/skills`。

如果已经安装 `skill-installer`，其内部安装命令应等价于下列形式；这不是本仓库自带脚本：

```bash
scripts/install-skill-from-github.py --url https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

如果安装后当前客户端没有立即发现 Skill，Codex 应提醒重启或刷新：

```text
Restart Codex to pick up new skills.
```

重启或刷新后即可使用：

```text
Use $codex-doc-first-development to turn my software idea into a Codex-ready engineering plan.
```

中文：

```text
使用 $codex-doc-first-development，从这个项目想法开始，帮我生成需求、docs 事实源、阶段计划、Task Pack、验证门禁和归档流程：
<<<粘贴项目想法>>>
```

## 5. 手动安装方式，仅作为 fallback

如果 Codex 无法联网安装，或你想从本地目录安装，可以手动复制 skill 目录：

```powershell
Copy-Item `
  -LiteralPath "<workspace>\codex-doc-first-development" `
  -Destination "$env:USERPROFILE\.codex\skills\codex-doc-first-development" `
  -Recurse `
  -Force
```

手动复制后同样需要重启 Codex。

## 6. 基础调用

从 0 开始：

```text
使用 $codex-doc-first-development，从 0 开始协助我完成这个软件项目。

项目想法：
<<<粘贴项目想法>>>

授权：
- 允许修改文件：是/否
- 允许创建 Git 分支：是/否
- 允许创建子智能体：是/否
- 允许使用 GitHub/PR/CI：是/否
- 允许安装依赖或联网：是/否
- 允许提交 commit：是/否
- 允许创建 draft PR：是/否

请先输出项目理解、流程档位、必须确认问题、可默认假设、docs 结构建议、阶段计划草案。
```

已有项目功能：

```text
使用 $codex-doc-first-development 为当前仓库规划并实现这个功能：
<<<功能描述>>>

请先扫描 README、docs、AGENTS.md、构建配置、测试、CI 和 git 状态，再输出流程档位、风险、Task Pack、测试策略和分支策略。
```

Bug 修复：

```text
使用 $codex-doc-first-development 修复这个 Bug：
<<<Bug 描述、复现步骤、期望行为>>>

请先补充或设计能复现问题的测试，再做最小修复，并用验收证据证明。
```

重构：

```text
使用 $codex-doc-first-development 重构这个模块：
<<<模块和目标>>>

要求不改变外部行为。请先生成 Task Pack、风险、回滚策略和 characterization tests。
```

## 7. 三种流程档位

快速档：

适用于文案、小 Bug、低风险单文件调整。不强制完整 docs，但需要说明验证方式。

标准档：

适用于普通功能、局部跨模块修改、较重要 Bug。需要最小 docs、阶段计划、Task Pack、验证证据。

严格档：

适用于新项目、架构变更、安全、支付、数据迁移、多 Agent 并发、发布链路。需要完整 docs、评审、TDD、CI/PR、阶段归档。

## 8. docs 脚手架生成

安装后或在 Skill 目录中，可以使用：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001
```

严格档：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode strict --phase 001
```

严格档默认只生成核心文档、锁登记和质量门禁。仅在确有相关事实时选择可选文档，并可先预览：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode strict --phase 001 --include security --include api --dry-run
```

覆盖已有模板：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001 --overwrite
```

默认不会覆盖已有文件。

## 9. Task Pack 检查

检查一个 Task Pack：

```powershell
python scripts/check_task_pack.py "C:\path\to\project\docs\delivery\tasks\TASK-001.md"
```

它会检查：

1. 是否有 `TASK-*` 标题。
2. 是否引用 `REQ-*`。
3. 是否包含 Status、Objective、Allowed Files、Forbidden Files、Test Requirements、Acceptance Criteria 等关键章节。
4. Interfaces、Data、UI、Allowed/Forbidden Files 等执行边界是否存在。
5. 必填章节是否为空或仍包含 `...`、`TODO`、`TBD`、尖括号占位符。
6. 重复标题、任务文件名与标题 ID 是否冲突。

脚手架生成的 Task Pack 有意保留待填写占位符，因此在补全前应当检查失败。

## 10. 多 Agent 使用

只有你明确授权时，Codex 才应该创建子智能体。

授权提示：

```text
我允许你使用子智能体并行开发。
只允许为互不重叠的任务创建 worker。
explorer 只读调查。
主控 Codex 负责复核、集成、测试和最终验收。
```

适合多 Agent：

1. 多模块互不重叠。
2. 一个 Agent 做只读探索，另一个做实现。
3. 测试补充和功能实现可以分离。
4. 文档整理和代码实现可以并行。

不适合多 Agent：

1. 需求未清楚。
2. 写入范围重叠。
3. 共享接口还没设计。
4. 主控无法可靠复核。

## 11. 高风险操作

Codex 必须先征求确认：

1. 合并到主分支。
2. push 到远程主分支。
3. force push。
4. 删除分支或文件。
5. 重置 Git 历史。
6. 发布生产版本。
7. 使用真实密钥、生产数据库或付费外部服务。

## 12. 标准输出状态

`PASS`：满足验收标准，验证证据充分。

`REQUEST_CHANGES`：存在明确可修复问题。

`BLOCKED`：需求、环境、权限、CI、冲突或风险导致无法可靠继续。

## 13. 能力边界

这个 Skill 提供工作流指令、参考材料、脚手架和 Task Pack 校验器。它不会自行提供后台 Agent 调度器、持久锁或死锁检测服务、CI 平台、GitHub 权限、密钥、自动合并或生产发布能力。Agent 必须使用当前环境真实可用且已授权的工具，并区分“计划执行”“本地已执行”“隔离环境已执行”和“外部 CI 已执行”。

如果本地工作区存在被 `.gitignore` 排除的两份长篇中文方法论，它们仅是设计来源，不是安装包内容；运行时事实源是 `codex-doc-first-development/SKILL.md` 及其直接引用。

## 14. 最佳实践

1. 新项目默认严格档。
2. 普通功能默认标准档。
3. 高风险改动自动升级严格档。
4. 不要为小任务制造文档负担。
5. 不要让 worker 在没有 Task Pack 的情况下写代码。
6. 不要把 Agent 自报测试通过当作唯一验收证据。
7. 阶段结束必须归档，降低下一阶段冷启动成本。
