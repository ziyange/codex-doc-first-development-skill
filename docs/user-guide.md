# Codex Doc-First Development Skill 用户使用手册

文档状态：与当前仓库实现同步
Skill 名称：`codex-doc-first-development`

## 1. 定位

这个 Skill 是一套工程化的 Codex 文档优先软件开发工作流。它不是简单提示词，而是一个可复用的 Codex Skill 包，用于把原始想法或已有项目变更，转换成可执行、可验证、可归档的软件工程流程。

它覆盖：

1. 从 0 捕获项目想法并进行强制反思质疑与可行性评估。
2. 在信息澄清充分后，由 Agent 自动触发初始化（创建 AGENTS.md 与 docs 事实源）。
3. 判断快速档、标准档、严格档。
4. 生成产品、需求、架构、阶段计划、Task Pack。
5. 规划 Codex 子智能体并行协作。
6. 管理分支、文件所有权、锁协议和 Git 冲突。
7. 执行 TDD、测试质量审查、本地验证、CI/PR 验收。
8. 进行文档回写、合并准备和阶段归档。

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
    check_docs_links.py
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

重启或刷新后即可使用：

```text
使用 $codex-doc-first-development，从这个项目想法开始，帮我进行反思质疑、自动初始化 docs 事实源、阶段计划、Task Pack 与验证门禁：
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

## 6. 基础调用与自动初始化流程

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

请先对我的想法进行反思质疑（分析缺失信息、代码库冲突与可行性瓶颈），在信息澄清充分后，自动触发初始化并生成 AGENTS.md 与 docs 结构。
```

## 6.1 需求反思、可行性排查与 Agent 自动初始化

为了避免 AI Agent 在需求不明确时盲目生成大量无效文档或错误代码，本 Skill 引入了**强制反思**与**自动初始化**机制：

1. **第 1 步：强制反思（CoT Intake Reflection）**：
   Agent 收到需求想法后，第一个输出 Block 必须为 `## CoT Intake Reflection`，明确包含：
   - **Missing Facts（缺失事实）**：有哪些边界条件或业务规则未交代？
   - **Codebase Conflicts（代码库冲突）**：与现有代码库框架、接口、模式是否存在冲突？
   - **Feasibility Bottlenecks（技术可行性瓶颈）**：在当前约束下，项目目标是否具备技术可行性？
2. **第 2 步：交互澄清与可行性确认**：
   Agent 向用户列出必须澄清的问题与可行性评估结论，协助用户补充必要事实。
3. **第 3 步：信息充分后 Agent 自动初始化**：
   当收集到足够信息且确认可行后，Agent **自动执行初始化动作**（调用 `scaffold_docs.py --auto-detect`），自动扫描根目录及子目录中的复合技术栈与 Monorepo 配置文件（支持 Makefile, Dockerfile, pnpm-workspace.yaml, go.work, Cargo.toml, CMakeLists.txt 等），自动生成预填构建命令的 `AGENTS.md` 和 `docs/` 事实源结构，无需用户手动输入 `/init`。

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

## 8. docs 脚手架生成与 Monorepo / 复合技术栈感知

安装后或在 Skill 目录中，可以使用自动技术栈感知。探针已升级，支持递归扫描根目录及子目录中的 `Makefile` (`make test`), `Dockerfile` / `docker-compose.yml`, `pnpm-workspace.yaml` (`pnpm -r test`), `go.work`, `Cargo.toml` (workspace), `CMakeLists.txt` (`ctest`) 等：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001 --auto-detect
```

严格档：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode strict --phase 001 --auto-detect
```

严格档默认只生成核心文档、锁登记和质量门禁。仅在确有相关事实时选择可选文档，并可先预览：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode strict --phase 001 --include security --include api --dry-run
```

覆盖已有模板：

```powershell
python scripts/scaffold_docs.py --root "C:\path\to\project" --mode standard --phase 001 --overwrite
```

## 9. Task Pack 授权范围与防虚假测试硬门禁

1. **Allowed Files 授权细粒度管控**：
   Task Pack 中的 `Allowed Files` 严禁使用全盘通配符（如 `*`、`**`、`.`）。`scripts/check_task_pack.py` 将会自动拦截过宽授权，强制要求 Agent 列出具体子目录或文件名规则（如 `src/auth/*.ts`）。
2. **防虚假测试与断言质量审计**：
   Test Quality Gate 严格拦截假测试反面模式（如 `assert True`、无断言空测试、纯 HTTP 200 无 payload 断言、过度 Mock 核心逻辑等），强制要求变动逻辑必须覆盖边缘情况与异常路径。

## 10. 静态死链检查器与 CI/CD 结构化 Output 契约

1. **文档相对链接与锚点静态检查器 (`scripts/check_docs_links.py`)**：
   用于自动化解析 Markdown 文档中的相对文件路径 (`[text](relative/path.md)`) 与标题锚点 (`#anchor-name` / `file.md#anchor-name`)，无需启动 HTTP 服务即可进行静态死链阻断：
   ```powershell
   python scripts/check_docs_links.py "C:\path\to\project\docs"
   ```

2. **结构化 JSON Output 与 CI/CD 流水线无缝集成 (`--json`)**：
   所有检查与脚手架工具脚本 (`check_task_pack.py` / `check_docs_links.py` / `scaffold_docs.py`) 均内置 `--json` 选项，可直接输出符合 JSON Schema 契约的机器可读 Payload，便于无缝集成至 GitHub Actions 或 GitLab CI 流水线：
   ```powershell
   python scripts/check_task_pack.py "docs/delivery/tasks/TASK-001.md" --json
   python scripts/check_docs_links.py "docs" --json
   python scripts/scaffold_docs.py --root "." --mode standard --auto-detect --json
   ```
