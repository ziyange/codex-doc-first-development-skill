# Codex Doc-First Development Skill (v2.3.0)

一个 skill 完成文档优先开发：需求梳理、任务拆解、实现、文档同步、UI/UX 对齐和可执行验证。

**只安装 `codex-doc-first-development/` 一个目录。** 所有参考文档、检查脚本和 Schema 都在其中，不再需要分别安装入口、文档同步、Task Pack 或 UI/UX skill。

> 标题版本表示已发布的版本。当前主分支已收敛为单 skill；脚本路径迁移属于破坏性变更，将通过[版本 PR](https://github.com/ziyange/codex-doc-first-development-skill/pull/1)统一升级版本。安装 `main` 可使用当前代码。

## 安装一次即可使用

在支持 skill-installer 的 Codex 中发送：

```text
安装这个 skill：
https://github.com/ziyange/codex-doc-first-development-skill/tree/main/codex-doc-first-development
```

也可以复制仓库中的整个 `codex-doc-first-development/` 到用户 skill 目录。Codex 的常见位置是 `~/.codex/skills/`；若配置了 `CODEX_HOME`，则使用其 `skills/` 子目录。

安装后下一轮对话可以使用：

```text
使用 $codex-doc-first-development，帮我修复导出功能。
先查看项目已有文档和测试，在现有授权范围内完成修改并验证。
```

也可描述新项目、现有功能或文档问题，由智能体按任务选择该 skill。内部模块按需读取，不需要用户再选择或安装子 skill。

## 按任务轻重执行

| 档位 | 适用情况 | 最低产物与验证 |
|---|---|---|
| Quick | 范围明确、低风险的小修复或文案调整 | 复用已有任务/文档；缺少记录时补目标、文件范围、验收与验证记录 |
| Standard | 超出 Quick 范围的一般功能、行为变化或跨模块修改 | 受影响的需求/契约、Task Pack 与测试；多任务时再准备阶段计划 |
| Strict | 权限、安全、迁移、公共契约或重大架构/生产风险 | 完整适用文档、Task Pack、风险评审、运行时审计及测试 |

风险按影响判断，单文件权限修改也可能是 Strict。Quick/Standard/Strict 与 Goal/Plan/Build 是两条独立轴；已选择的执行协议不会因为 Quick 而省略白名单、审计或迭代限制。

智能体复用已有授权，只询问影响方向的缺失信息或新增权限。S0–S22 是生命周期索引，小任务不必生成完整文档树。

## 一个 skill 内部包含什么

| 能力 | 内部参考 | 内置脚本 |
|---|---|---|
| 启动与需求梳理 | `references/session-start.md` | `scripts/scaffold_docs.py`（按需初始化） |
| 文档同步与链接检查 | `references/doc-sync.md` | `scripts/check_docs_links.py` |
| Task Pack 结构检查 | `references/task-pack.md` | `scripts/check_task_pack.py` |
| 图形界面设计对齐 | `references/ui-ux-prototyping.md` | 使用可用的设计/生图工具，无额外 skill 依赖 |
| 运行时验证与审计 | `references/review-gates.md`、`references/schemas.md` | `scripts/verify_runtime_trace.py`、`scripts/check_permission_log.py`、`scripts/lock_manager.py` |

主入口保持不超过 150 行，详细规则放在本目录的 `references/` 中。模块化体现在内部文件组织，不体现为多个安装单元。

## 关键行为

- **文档与实现同步**：需求、架构、API、布局或交互事实变化时，在实现前或同一步更新所属文档；未改变事实的内部重构无需机械改文档。
- **设计门禁按变化适用**：仅对图形界面变化对齐布局和状态；复用已确认设计。CLI、后端、脚本没有图形界面变化时跳过视觉原型。本地界面记录事件、状态和结果，不虚构 API。
- **避免重复请求逻辑**：复用公共服务/客户端；字段投影仅在真实需求或性能要求明确时引入。
- **区分结构与授权**：Task Pack Exit 0 仅表示结构检查通过，不代表用户许可、依赖就绪或测试通过。`warnings` 是建议项。
- **失败关闭**：必需审计输入缺失或损坏返回 Exit 3。Merkle 链检查验证提交给它的记录一致性，不证明所有外部操作均已被记录。

## 运行检查

依赖 Python >= 3.9 和 `jsonschema`。在本仓库根目录执行：

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python codex-doc-first-development/scripts/check_docs_links.py . --json
python codex-doc-first-development/scripts/check_task_pack.py tests/fixtures/valid_task_pack.md --json
python codex-doc-first-development/scripts/verify_runtime_trace.py --trace tests/fixtures/valid_trace.json --permission-log tests/fixtures/valid_audit.log --task-pack tests/fixtures/valid_task_pack.md --mode goal --json
```

在目标项目运行时，用安装目录定位脚本，用项目目录定位工件。Schema 默认随 skill 安装位置解析。示例中的 `TASK-001.md` 应替换为当前 Task Pack。

## 从旧多 skill 布局迁移

1. 用当前 `codex-doc-first-development/` 整目录更新主 skill，先备份原安装。
2. 两项检查脚本现在位于主 skill 的 `scripts/`；更新项目 CI 或脚本中的旧路径，不保留第二份脚本副本。
3. 删除或移出 skill 发现目录中旧的入口、文档同步、Task Pack、UI/UX 独立安装，防止重复触发。详细旧目录名称及路径见[用户指南](docs/user-guide.md)。
4. 下一轮对话只使用 `$codex-doc-first-development`。

## 仓库结构

```text
codex-doc-first-development/
  SKILL.md
  agents/openai.yaml
  references/               # 内部指南、模板、Schema
  scripts/                  # 六个检查与辅助脚本
tests/                      # unittest 与 fixtures，含单目录隔离安装测试
.github/                    # 三平台 CI 与非 npm 发布工具
.changeset/                 # 待处理的版本变更记录
docs/user-guide.md          # 中文操作手册
docs/releasing.md           # 发布维护说明
CHANGELOG.md                # 历史记录
```

## 文档与发布

- [用户指南](docs/user-guide.md)：使用示例、验证方式与旧安装迁移。
- [任务适配策略](codex-doc-first-development/references/adaptive-workflow.md)：如何选择档位及适用门禁。
- [贡献范围](SCOPE.md)与[仓库约定](AGENTS.md)：贡献需有可复现的问题和验证证据。
- [发布维护](docs/releasing.md)：保留 changeset 格式，由 Python 同步版本、README、CHANGELOG，并创建版本 PR；无需 npm 包。合并和 tag 发布保持显式操作。
- [变更历史](CHANGELOG.md)：历史上的多 skill 拆分记录保留，当前安装方式以本页为准。

项目采用 [MIT License](LICENSE)。
