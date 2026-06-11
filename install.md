# Install Civil Materials Skills

本文档说明如何安装和配置 civil-materials-skills 技能包。

## Option 1: Codex Plugin

**通过插件市场安装（推荐）：**

```bash
codex plugin marketplace add https://github.com/cooleava1-gif/civil-materials-skills.git --ref main
codex plugin add civil-materials-skills@civil-materials-skills
```

**Codex Desktop 用户：**

1. 打开 Codex Desktop 设置
2. 添加自定义插件市场：
   - 市场源：`https://github.com/cooleava1-gif/civil-materials-skills.git`
   - 分支/ref：`main`
3. 安装插件：`civil-materials-skills`

安装后，所有 `civil-materials-*` 技能将通过插件作为完整包提供。如果技能未立即显示，请刷新插件页面或启动新的 Codex 会话。

## Option 2: Manual Skills Install

**克隆仓库：**

```bash
git clone https://github.com/cooleava1-gif/civil-materials-skills.git
cd civil-materials-skills
```

**安装单个技能：**

```bash
mkdir -p ~/.codex/skills
cp -R skills/_shared ~/.codex/skills/
cp -R skills/civil-materials-reader ~/.codex/skills/
```

**安装所有技能：**

```bash
mkdir -p ~/.codex/skills
cp -R skills/_shared ~/.codex/skills/
for d in skills/civil-materials-*; do
  cp -R "$d" ~/.codex/skills/
done
```

**使用 PowerShell 安装（Windows）：**

```powershell
.\scripts\install.ps1
```

## Option 3: Claude Code Plugin

**通过插件市场安装（推荐）：**

```bash
claude plugin marketplace add cooleava1-gif/civil-materials-skills
claude plugin install civil-materials-skills@civil-materials-skills
```

**备选：子代理/包装器安装**

如果插件市场不可用，可以使用子代理包装器：

```bash
mkdir -p ~/ai-skills
cd ~/ai-skills
git clone https://github.com/cooleava1-gif/civil-materials-skills.git
```

创建用户级子代理包装器：

```bash
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/civil-materials-reader.md <<'EOF'
---
name: civil-materials-reader
description: Full-paper bilingual, figure-aware, source-grounded Markdown reader for civil engineering papers.
---

When invoked, first read `~/ai-skills/civil-materials-skills/skills/civil-materials-reader/SKILL.md`.
Treat that file as the governing workflow.
If the skill references supporting files, read only the specific files you need from
`~/ai-skills/civil-materials-skills/skills/civil-materials-reader/` and
`~/ai-skills/civil-materials-skills/skills/_shared/`.
Do not replace the skill with a generic paper-summary response.
EOF
```

## Verify The Install

运行发布检查脚本验证安装：

```bash
python scripts/run_release_checks.py --json
```

预期输出：`"status": "pass"`

运行架构检查：

```bash
python scripts/check_skill_architecture.py --json
```

预期输出：根目录/插件镜像差异为空或仅有已知例外。

## Five-Minute Walkthrough

### 路径 A：WER-EA 综述工作流

```
Help me run a WER-EA mini-review workflow from screening to figure planning.
```

**预期流程：**
1. `civil-materials-research` 路由工作流
2. `civil-materials-citation` 规划搜索和筛选矩阵
3. `civil-materials-reader` 构建证据链交接
4. `civil-materials-writing` 构建大纲
5. `civil-materials-figure` 规划综述图表

### 路径 B：实验论文

```
Audit this experimental manuscript for evidence gaps before I draft the discussion.
```

**预期流程：**
1. `civil-materials-research` 框定阶段、证据水平和路由
2. `civil-materials-data` 和 `civil-materials-figure` 紧缩支撑数据
3. `civil-materials-writing` 和 `civil-materials-polishing` 重建有界文本
4. `civil-materials-reviewer` 检查修订包

### 路径 C：论文→PPT

```
Turn this paper package into a journal-club slide outline and then a real PPTX.
```

**预期流程：**
1. `civil-materials-paper2ppt` 创建幻灯片就绪 Markdown
2. `civil-materials-pptx` 将大纲转换为实际 PowerPoint 文件

## Guided Demo Routes

如果你想要一个引导式的首次使用路径，可以从这里开始：

1. [WER-EA 综述](docs/workflows/wer-ea-mini-review.md)
2. [实验论文](docs/workflows/experimental-manuscript.md)
3. [修回循环](docs/workflows/revision-loop.md)
4. [论文→演讲](docs/workflows/paper-to-presentation.md)

## Showcase Shortcuts

如果你已经清楚交付物是什么，可以直接跳到结果形状：

- [投稿包](docs/showcases/submission-package.md)
- [审稿回复](docs/showcases/reviewer-response.md)
- [FAIR 数据包](docs/showcases/fair-data-package.md)

完整索引请查看 [docs/showcases/README.md](docs/showcases/README.md)。

## 更新技能

**通过 Git 更新：**

```bash
cd civil-materials-skills
git pull
cp -R skills/_shared ~/.codex/skills/
for d in skills/civil-materials-*; do
  cp -R "$d" ~/.codex/skills/
done
```

**通过 PowerShell 更新（Windows）：**

```powershell
git pull
.\scripts\install.ps1
```

更新后重启 Codex 或 Claude Code 以加载新技能。

## 故障排除

### 技能未显示

1. 确认技能已复制到正确目录（`~/.codex/skills/`）
2. 重启 Codex 或 Claude Code
3. 检查 `_shared` 目录是否与技能目录在同一层级

### 路径错误

确保 `_shared` 目录与 `civil-materials-*` 技能目录在同一父目录下：

```
~/.codex/skills/
├── _shared/              # 共享支持目录
├── civil-materials-research/
├── civil-materials-reader/
└── ...
```

## 环境变量（可选）

学术搜索 MCP 功能需要以下环境变量：

- `OPENALEX_API_KEY` - OpenAlex API 密钥
- `SEMANTIC_SCHOLAR_API_KEY` - Semantic Scholar API 密钥
- `CIVIL_MATERIALS_CONTACT_EMAIL` - 联系邮箱（用于 API 请求）
- `NCBI_API_KEY` - NCBI API 密钥（用于 PubMed 搜索）

## 下一步

安装完成后，可以尝试：

1. [WER-EA 综述工作流](docs/workflows/wer-ea-mini-review.md)
2. [实验论文工作流](docs/workflows/experimental-manuscript.md)
3. [修回循环工作流](docs/workflows/revision-loop.md)
4. [论文→PPT 工作流](docs/workflows/paper-to-presentation.md)

如有问题，请提交 [Issue](https://github.com/cooleava1-gif/civil-materials-skills/issues)。
