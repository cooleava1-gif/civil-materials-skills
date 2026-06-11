# Civil Materials Skills — Nature Skills Architecture Upgrade Plan

> **Goal:** 将 civil-materials-skills 全面升级为 nature-skills 的土木工程版本，采用相同的架构设计、目录结构和使用模式，同时保留土木材料领域的专业内容。

---

## 📋 对比分析：当前状态 vs 目标状态

### 架构对比

| 维度 | nature-skills | civil-materials-skills (当前) | 升级目标 |
|---|---|---|---|
| **SKILL.md 格式** | YAML frontmatter (name, description, version, author) + Markdown body | 有 frontmatter 但格式不统一 | 统一为 nature-skills 格式 |
| **manifest.yaml** | 声明式轴检测 + 文件映射 | 有 manifest.yaml 但格式不同 | 对齐 nature-skills 格式 |
| **Static/Dynamic 分层** | static/ 放可复用片段，SKILL.md 做路由 | 有 static/ 但结构不一致 | 对齐目录结构 |
| **_shared 目录** | core/ + journal-formats/ | core/ + journal-formats/ + paper-production/ | 保留额外内容，对齐基础结构 |
| **插件支持** | .claude-plugin/ + plugins/ | 只有 plugins/ | 添加 .claude-plugin/ |
| **触发描述** | 详细的触发关键词（中英文） | 有但不够详细 | 增强触发描述 |

### 目录结构对比

```
nature-skills/                      civil-materials-skills/
├── skills/                         ├── skills/
│   ├── _shared/                    │   ├── _shared/
│   │   ├── core/                   │   │   ├── core/
│   │   └── journal-formats/        │   │   ├── journal-formats/
│   └── nature-*/                   │   │   └── paper-production/
│       ├── SKILL.md                │   └── civil-materials-*/
│       ├── manifest.yaml           │       ├── SKILL.md
│       ├── README.md               │       ├── manifest.yaml
│       ├── static/                 │       ├── README.md
│       │   ├── core/               │       ├── static/
│       │   └── fragments/          │       │   ├── core/
│       ├── references/             │       │   └── fragments/
│       ├── scripts/                │       ├── references/
│       ├── tests/                  │       ├── scripts/
│       └── examples/               │       ├── tests/
├── plugins/                        │       └── examples/
├── .claude-plugin/                 ├── plugins/
├── scripts/                        ├── .claude-plugin/ (新增)
├── docs/                           ├── scripts/
└── README.md                       ├── docs/
                                    └── README.md
```

---

## 🎯 升级任务清单

### Phase 1: 基础架构对齐

#### Task 1: 统一 SKILL.md Frontmatter 格式

**目标:** 所有技能的 SKILL.md 使用统一的 YAML frontmatter 格式

**当前格式:**
```yaml
---
name: civil-materials-reader
version: "1.1.0"
stability: stable
description: Use when reading...
---
```

**目标格式 (对齐 nature-skills):**
```yaml
---
name: civil-materials-reader
description: >-
  Build source-grounded civil materials reading artifacts...
  Use whenever the user asks to read a paper, translate,
  extract figures/tables, build evidence chains...
  Also trigger on 中文触发词...
version: 2.0.0
author: Civil Materials Team, refactored into static/dynamic layers
---
```

**需要修改的文件:**
- [ ] `skills/civil-materials-research/SKILL.md`
- [ ] `skills/civil-materials-reader/SKILL.md`
- [ ] `skills/civil-materials-citation/SKILL.md`
- [ ] `skills/civil-materials-writing/SKILL.md`
- [ ] `skills/civil-materials-polishing/SKILL.md`
- [ ] `skills/civil-materials-figure/SKILL.md`
- [ ] `skills/civil-materials-data/SKILL.md`
- [ ] `skills/civil-materials-reviewer/SKILL.md`
- [ ] `skills/civil-materials-response/SKILL.md`
- [ ] `skills/civil-materials-paper2ppt/SKILL.md`
- [ ] `skills/civil-materials-pptx/SKILL.md`

**验证命令:**
```bash
python -c "
from pathlib import Path
import yaml
for skill_dir in Path('skills').glob('civil-materials-*'):
    skill_md = skill_dir / 'SKILL.md'
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')
        if content.startswith('---'):
            frontmatter = content.split('---')[1]
            data = yaml.safe_load(frontmatter)
            required = ['name', 'description', 'version']
            missing = [k for k in required if k not in data]
            if missing:
                print(f'{skill_dir.name}: MISSING {missing}')
            else:
                print(f'{skill_dir.name}: OK')
"
```

---

#### Task 2: 对齐 manifest.yaml 格式

**目标:** 所有 manifest.yaml 使用 nature-skills 的声明式格式

**当前格式:**
```yaml
version: "1.1.0"
always_load:
  - static/core/contract.md
axes:
  source_type:
    default: pasted-text
    values:
      pdf:
        path: references/pdf-reading.md
        triggers: ["PDF", "paper file"]
```

**目标格式 (对齐 nature-skills):**
```yaml
name: civil-materials-reader
version: 2.0.0
description: >
  Declarative manifest for the static/dynamic split...

always_load:
  - ../_shared/core/terminology-ledger.md
  - static/core/principles.md
  - static/core/workflow.md
  - static/core/output-contract.md

axes:
  source_format:
    detect: |
      Determine the input form the user provided...
    values:
      pdf-text:     static/fragments/source/pdf-text.md
      scanned-pdf:  static/fragments/source/scanned-pdf.md
      html:         static/fragments/source/html.md
      doi-arxiv:    static/fragments/source/doi-arxiv.md
      pasted-text:  static/fragments/source/pasted-text.md
    default: pdf-text
    multi: true

references:
  on_demand:
    - condition: cropping figures/tables
      path: references/figure-extraction.md
```

**需要修改的文件:** 同 Task 1

---

#### Task 3: 重组 static/ 目录结构

**目标:** 统一 static/ 目录结构为 core/ + fragments/

**当前结构:**
```
static/
├── core/
│   ├── contract.md
│   ├── workflow.md
│   └── stance.md
└── fragments/ (部分技能有)
```

**目标结构:**
```
static/
├── core/
│   ├── principles.md (核心原则)
│   ├── workflow.md (工作流程)
│   ├── output-contract.md (输出契约)
│   └── stance.md (立场声明)
├── fragments/
│   ├── source/ (源格式片段)
│   ├── domain/ (领域片段)
│   ├── journal/ (期刊片段)
│   └── task/ (任务片段)
```

**需要修改的文件:**
- 重命名 `contract.md` → `principles.md` 或 `output-contract.md`
- 确保每个技能都有完整的 fragments/ 子目录

---

### Phase 2: 内容增强

#### Task 4: 增强触发描述

**目标:** 每个技能的 description 包含详细的中英文触发关键词

**示例 (civil-materials-reader):**
```yaml
description: >-
  Build source-grounded civil materials reading artifacts, not shallow summaries.
  Use whenever the user asks to read a paper, translate an academic paper,
  extract figures/tables, build evidence chains, or create literature matrices
  for civil engineering and construction materials research.

  Also trigger on:
  - English: paper reading, literature review, evidence chain, claim-evidence,
    microstructure interpretation, dosage window, mechanism table
  - Chinese: 读论文、精读论文、论文翻译、文献翻译、文献阅读、学术阅读、
    证据链、微观形貌、剂量窗口、机理表、文献矩阵、组会汇报

  Specializes in:
  - Waterborne epoxy modified emulsified asphalt (WER-EA)
  - Asphalt pavement materials
  - Cement and concrete
  - Durability and sustainability
```

---

#### Task 5: 添加 Claude Code 插件支持

**目标:** 添加 `.claude-plugin/` 目录，支持 Claude Code 安装

**创建文件:**
- `.claude-plugin/plugin.json`
- `.claude-plugin/README.md`

**plugin.json 示例:**
```json
{
  "name": "civil-materials-skills",
  "version": "2.0.0",
  "description": "Civil engineering and construction materials research skills",
  "skills": [
    "civil-materials-research",
    "civil-materials-reader",
    "civil-materials-citation",
    "civil-materials-writing",
    "civil-materials-polishing",
    "civil-materials-figure",
    "civil-materials-data",
    "civil-materials-reviewer",
    "civil-materials-response",
    "civil-materials-paper2ppt",
    "civil-materials-pptx"
  ]
}
```

---

#### Task 6: 统一 _shared 目录结构

**目标:** 对齐 nature-skills 的 _shared 结构

**当前结构:**
```
_shared/
├── core/
│   ├── claim-strength-ladder.md
│   ├── ethics.md
│   ├── evidence-contract.md
│   ├── source-basis.md
│   ├── stance.md
│   └── terminology-ledger.md
├── journal-formats/
│   ├── cbm.md
│   ├── ccc.md
│   ├── jbe.md
│   └── rmpd.md
└── paper-production/ (土木特有)
    ├── audit_paper_production.py
    ├── examples/
    ├── paper-gate-report-template.md
    ├── weakness-routing.md
    └── weakness-routing-template.csv
```

**目标结构 (保留额外内容):**
```
_shared/
├── README.md (新增说明文件)
├── core/
│   ├── terminology-ledger.md
│   ├── ethics.md
│   ├── evidence-contract.md
│   └── stance.md
├── journal-formats/
│   ├── cbm.md
│   ├── ccc.md
│   ├── cscm.md
│   ├── jbe.md
│   ├── rmpd.md
│   └── ijpe.md
└── paper-production/ (土木特有，保留)
    └── ...
```

---

### Phase 3: 文档和测试

#### Task 7: 更新 README.md

**目标:** 对齐 nature-skills 的 README 风格

**关键更新:**
- 添加 Star History 图表
- 添加贡献指南
- 添加技能索引表格
- 添加安装说明（Codex + Claude Code + 手动）

---

#### Task 8: 添加贡献指南

**目标:** 创建 CONTRIBUTING.md，说明如何添加新技能

**内容结构:**
1. 技能目录结构要求
2. SKILL.md 格式规范
3. manifest.yaml 编写指南
4. 测试要求
5. PR 提交流程

---

#### Task 9: 增强测试覆盖

**目标:** 为每个技能添加完整的测试套件

**测试类型:**
- 单元测试 (scripts/)
- 集成测试 (tests/)
- 压力测试 (tests/pressure-tests/)
- 架构契约测试 (tests/test_skill_architecture_contract.py)

---

### Phase 4: 发布准备

#### Task 10: 版本号升级

**目标:** 所有技能版本号统一升级到 2.0.0

**修改文件:**
- 所有 SKILL.md 的 version 字段
- 所有 manifest.yaml 的 version 字段
- 根目录 package.json (如果有)

---

#### Task 11: 发布检查脚本更新

**目标:** 更新 scripts/run_release_checks.py 支持新架构

**新增检查项:**
- SKILL.md frontmatter 格式检查
- manifest.yaml 格式检查
- static/ 目录结构检查
- Claude Code 插件元数据检查

---

#### Task 12: 文档中文化

**目标:** 添加中文版本文档

**创建文件:**
- `README_CN.md`
- `install_CN.md`
- `CONTRIBUTING_CN.md`
- 各技能 `README_CN.md`

---

## 📅 实施时间表

| Phase | 任务 | 预计时间 | 依赖 |
|---|---|---|---|
| Phase 1 | Task 1-3: 基础架构对齐 | 2-3 天 | 无 |
| Phase 2 | Task 4-6: 内容增强 | 2-3 天 | Phase 1 |
| Phase 3 | Task 7-9: 文档和测试 | 2-3 天 | Phase 2 |
| Phase 4 | Task 10-12: 发布准备 | 1-2 天 | Phase 3 |

**总计:** 7-11 天

---

## 🔍 验证清单

### 架构验证
- [ ] 所有 SKILL.md 使用统一 frontmatter 格式
- [ ] 所有 manifest.yaml 使用声明式轴检测格式
- [ ] 所有 static/ 目录遵循 core/ + fragments/ 结构
- [ ] _shared/ 目录结构对齐

### 功能验证
- [ ] 所有技能可以通过关键词触发
- [ ] 路由协议正确加载片段
- [ ] 输出符合 output-contract 定义

### 测试验证
- [ ] 所有单元测试通过
- [ ] 架构契约测试通过
- [ ] 发布检查脚本通过

### 文档验证
- [ ] README.md 完整且准确
- [ ] 每个技能有 README.md
- [ ] 贡献指南完整

---

## 📚 参考资源

- nature-skills 仓库: https://github.com/Yuan1z0825/nature-skills
- nature-skills 架构文档: skills/nature-reader/SKILL.md
- 当前项目文档: docs/architecture/skill-architecture.md

---

## ⚠️ 注意事项

1. **保留土木特有内容:** paper-production/ 目录是土木材料领域的特色，需要保留
2. **向后兼容:** 升级后现有用户的工作流不应中断
3. **渐进式升级:** 可以分阶段实施，先升级核心技能（research, reader, writing）
4. **测试驱动:** 每个任务都应该有对应的测试验证
