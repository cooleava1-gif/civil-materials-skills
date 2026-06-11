# 贡献指南

感谢你对 civil-materials-skills 的关注！本文档说明如何贡献新技能或改进现有技能。

## 目录

- [技能目录结构](#技能目录结构)
- [SKILL.md 格式规范](#skillmd-格式规范)
- [manifest.yaml 编写指南](#manifestyaml-编写指南)
- [static/ 目录结构](#static-目录结构)
- [测试要求](#测试要求)
- [PR 提交流程](#pr-提交流程)

---

## 技能目录结构

每个技能必须遵循以下目录结构：

```
skills/civil-materials-<name>/
├── SKILL.md                    # 技能主文件（必需）
├── manifest.yaml               # 声明式路由配置（必需）
├── README.md                   # 人类可读说明（必需）
├── static/                     # 静态内容片段
│   ├── core/                   # 核心文件
│   │   ├── principles.md       # 核心原则
│   │   ├── workflow.md         # 工作流程
│   │   └── output-contract.md  # 输出契约
│   └── fragments/              # 可复用片段
│       ├── domain/             # 领域片段
│       ├── journal/            # 期刊片段
│       └── task/               # 任务片段
├── references/                 # 详细参考文档
├── scripts/                    # 自动化脚本
├── tests/                      # 测试文件
│   ├── test_*.py              # 单元测试
│   └── pressure-tests/        # 压力测试
├── examples/                   # 示例输出
├── assets/                     # 资源文件
│   └── templates/             # 模板文件
└── agents/                     # 代理配置
    └── openai.yaml            # OpenAI 代理配置
```

---

## SKILL.md 格式规范

每个 SKILL.md 必须包含 YAML frontmatter 和 Markdown body：

```yaml
---
name: civil-materials-<name>
description: >-
  详细的功能描述...
  
  Also trigger on:
  - English: trigger keywords...
  - Chinese: 触发关键词...
  
  Specializes in:
  - 专业领域 1
  - 专业领域 2
version: 2.0.0
author: Your Name, refactored into static/dynamic layers
---
```

### Frontmatter 字段说明

| 字段 | 必需 | 说明 |
|---|---|---|
| `name` | ✓ | 技能名称，格式为 `civil-materials-<name>` |
| `description` | ✓ | 详细描述，包含触发关键词（中英文） |
| `version` | ✓ | 语义化版本号（推荐 2.0.0） |
| `author` | ✓ | 作者信息 |

### Body 结构

```markdown
# Civil Materials <Name>

一句话描述技能的核心功能。

## Routing protocol

### 1. Load the manifest and the core layer
读取 manifest.yaml 和核心文件。

### 2. Detect the axis values
检测用户请求的轴值。

### 3. Load the matching fragment(s)
加载匹配的片段。

### 4. Build the output
使用加载的材料构建输出。

### 5. Validate and hand off
验证输出并交接给下一个技能。
```

---

## manifest.yaml 编写指南

manifest.yaml 使用声明式格式定义技能的路由逻辑：

```yaml
name: civil-materials-<name>
version: 2.0.0
description: >
  Declarative manifest for the static/dynamic split...

always_load:
  # 共享层
  - ../_shared/core/terminology-ledger.md
  # 技能本地核心
  - static/core/principles.md
  - static/core/workflow.md
  - static/core/output-contract.md

axes:
  <axis_name>:
    detect: |
      描述如何检测这个轴的值...
    values:
      <value1>: static/fragments/<category>/<value1>.md
      <value2>: static/fragments/<category>/<value2>.md
    default: <value1>
    multi: false
```

### 轴（Axes）说明

轴是技能路由的维度，每个轴有：
- `detect`：如何从用户请求中检测值
- `values`：允许的值及其对应的文件路径
- `default`：默认值
- `multi`：是否允许多选

---

## static/ 目录结构

### core/ 文件

| 文件 | 用途 |
|---|---|
| `principles.md` | 核心原则和立场 |
| `workflow.md` | 标准工作流程 |
| `output-contract.md` | 输出格式契约 |

### fragments/ 目录

按类别组织可复用片段：

```
fragments/
├── domain/           # 领域特定内容
│   ├── asphalt-pavement.md
│   ├── cement-concrete.md
│   └── ...
├── journal/          # 期刊特定格式
│   ├── cbm.md
│   ├── ccc.md
│   └── ...
└── task/             # 任务特定指导
    ├── reading.md
    ├── writing.md
    └── ...
```

---

## 测试要求

每个技能必须包含：

### 单元测试

```python
# tests/test_<skill>.py
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

class <Skill>Tests(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue((ROOT / "skills" / "civil-materials-<name>" / "SKILL.md").is_file())
    
    def test_manifest_exists(self):
        self.assertTrue((ROOT / "skills" / "civil-materials-<name>" / "manifest.yaml").is_file())
    
    def test_static_core_exists(self):
        static_core = ROOT / "skills" / "civil-materials-<name>" / "static" / "core"
        self.assertTrue(static_core.is_dir())
```

### 压力测试

在 `tests/pressure-tests/` 目录下添加边界条件测试：

```markdown
# tests/pressure-tests/<scenario>.md

## Scenario
描述压力测试场景

## Expected Behavior
描述预期行为
```

---

## PR 提交流程

### 1. Fork 并克隆仓库

```bash
git clone https://github.com/<your-username>/civil-materials-skills.git
cd civil-materials-skills
```

### 2. 创建功能分支

```bash
git checkout -b feature/civil-materials-<new-skill>
```

### 3. 实现技能

按照上述规范创建技能目录和文件。

### 4. 运行测试

```bash
# 运行单元测试
python -m unittest discover -s skills/civil-materials-<name>/tests -v

# 运行发布检查
python scripts/run_release_checks.py --json

# 运行架构检查
python scripts/check_skill_architecture.py --json
```

### 5. 同步插件镜像

```bash
# 复制到插件镜像
cp -R skills/civil-materials-<name> plugins/civil-materials-skills/skills/
cp -R skills/_shared plugins/civil-materials-skills/skills/
```

### 6. 提交 PR

```bash
git add .
git commit -m "feat: add civil-materials-<name> skill"
git push origin feature/civil-materials-<new-skill>
```

### PR 描述模板

```markdown
## 新技能描述
简要描述新技能的功能。

## 触发关键词
- English: keyword1, keyword2
- Chinese: 关键词1, 关键词2

## 测试覆盖
- [ ] 单元测试通过
- [ ] 压力测试添加
- [ ] 发布检查通过
- [ ] 架构检查通过

## 文档
- [ ] SKILL.md 完整
- [ ] manifest.yaml 正确
- [ ] README.md 添加
```

---

## 代码风格

- **Markdown**：使用 UTF-8 编码，行尾使用 LF
- **Python**：遵循 PEP 8，使用 4 空格缩进
- **YAML**：使用 2 空格缩进，避免制表符
- **提交信息**：使用 Conventional Commits 格式

---

## 问题反馈

如有问题或建议，请提交 Issue 或联系维护者。

感谢你的贡献！🎉
