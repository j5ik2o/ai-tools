# ai-tools

[English](README.md)

Claude Code と Codex 向けに、AI エージェントスキルとプラグインを配布するマーケットプレイス用リポジトリです。

## Highlights

- `.claude-plugin/marketplace.json` から複数の plugin を公開
- `.agents/plugins/marketplace.json` から Codex plugin を公開
- `marketplace.yml` と生成済み `marketplace.json` で APM marketplace manifest を提供
- `agent-skills`, `takt`, `software-design` などのスキルコレクションを収録
- `skills/` に直接参照用のシンボリックリンクを保持

## インストール

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install agent-skills@ai-tools
/plugin install takt@ai-tools
/plugin install software-design@ai-tools
```

### Codex Plugin

このリポジトリを Codex plugin marketplace として登録し、必要なプラグインをインストールします。

```shell
codex plugin marketplace add j5ik2o/ai-tools --ref main
codex plugin add git@ai-tools
codex plugin add github@ai-tools
codex plugin add agent-skills@ai-tools
codex plugin add takt@ai-tools
codex plugin add software-design@ai-tools
```

インストール結果を確認したら、新しい Codex タスクを開いてプラグインを読み込みます。

```shell
codex plugin list
```

### Agent Package Manager

```shell
apm marketplace add j5ik2o/ai-tools --name ai-tools
apm install software-design@ai-tools
```

APMでインストールできる package 名は `agent-skills`, `takt`, `software-design` です。

### スキルディレクトリベース CLI

```shell
npx skills add j5ik2o/ai-tools
```

## プラグイン

| Plugin | 説明 | 主なスキル | 詳細 |
|--------|------|------------|------|
| [`agent-skills`](plugins/agent-skills) | スキル作成、評価、反復改善のワークフローを示すエージェントスキル集 | [`j5ik2o:skill-forge`](plugins/agent-skills/skills/j5ik2o:skill-forge) | [README](plugins/agent-skills/README.ja.md) |
| [`takt`](plugins/takt) | TAKT piece engine 向けの分析・構築・最適化スキル集 | `j5ik2o:takt-task-builder`, `takt-piece-builder`, `j5ik2o:takt-facet-builder`, `j5ik2o:takt-analyzer`, `j5ik2o:takt-optimizer`, `j5ik2o:takt-skill-updater` | [README](plugins/takt/README.ja.md) |
| [`software-design`](plugins/software-design) | DDD、クリーンアーキテクチャ、エラー処理、パッケージ設計、リファクタリング、保守しやすいドメインモデリングを支援する設計スキル集 | `j5ik2o:ddd-aggregate-design`, `j5ik2o:clean-architecture`, `j5ik2o:error-handling`, `j5ik2o:package-design`, `j5ik2o:refactoring-packages` | [plugin.json](plugins/software-design/.claude-plugin/plugin.json) |

## リポジトリ構成

```text
.claude-plugin/
└── marketplace.json

marketplace.yml
marketplace.json
mise.toml

plugins/
├── agent-skills/
│   ├── README.md
│   └── skills/
│       └── j5ik2o:skill-forge/
├── takt/
│   ├── README.md
│   └── skills/
│       ├── j5ik2o:takt-analyzer/
│       ├── j5ik2o:takt-facet-builder/
│       ├── j5ik2o:takt-optimizer/
│       ├── j5ik2o:takt-skill-updater/
│       └── j5ik2o:takt-task-builder/
└── software-design/
    └── skills/
        ├── j5ik2o:clean-architecture/
        ├── j5ik2o:ddd-aggregate-design/
        ├── j5ik2o:error-handling/
        └── ...

skills/
├── j5ik2o:skill-forge -> ../plugins/agent-skills/skills/j5ik2o:skill-forge
├── j5ik2o:takt-analyzer -> ../plugins/takt/skills/j5ik2o:takt-analyzer
└── ...

template/
└── SKILL.md.template
```

## 新しいスキルの作成方法

1. `template/SKILL.md.template` を `plugins/agent-skills/skills/j5ik2o:<スキル名>/SKILL.md` にコピー
2. フロントマター（`name`, `description`）を編集し、指示を書く
3. 直接参照する CLI でも使いたい場合は `skills/` にシンボリックリンクを作成:
   ```shell
   ln -s ../plugins/agent-skills/skills/j5ik2o:<スキル名> skills/j5ik2o:<スキル名>
   ```
4. 新しい plugin collection を公開する場合は `.claude-plugin/marketplace.json` を更新

## APM Marketplace のメンテナンス

このリポジトリでは、APM authoring 用の編集元として `marketplace.yml` を保持し、利用者向けに生成済みの `marketplace.json` もコミットします。

APM は `mise` で管理します。

```shell
mise install
mise run apm:version
```

ファイルを書き換えずに marketplace の解決結果を確認する場合:

```shell
mise run apm:marketplace:check
```

`marketplace.yml` から `marketplace.json` を再生成する場合:

```shell
mise run apm:marketplace:build
```

`marketplace.yml` の package ref は、再現可能なAPMビルドのためコミットSHAに固定します。新しい marketplace revision を公開する際に ref を更新してください。

## ライセンス

各スキル配下のライセンス情報を参照してください。
