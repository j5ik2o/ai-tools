## [0.5.0](https://github.com/j5ik2o/ai-tools/compare/v0.4.1...v0.5.0) (2026-07-01)


### Features

* add git and github plugins to marketplace ([cce04a0](https://github.com/j5ik2o/ai-tools/commit/cce04a07bc25fb40b61223ab19b11a80bdb8aa48))
* **github:** add deep research README skill ([363eb0d](https://github.com/j5ik2o/ai-tools/commit/363eb0d63192d373078e899089021b0f9d33a40c))
* **plugins:** add codex plugin manifests ([280db66](https://github.com/j5ik2o/ai-tools/commit/280db66faf8322e224a6fbae1bb6d2d176301ea4))
* **plugins:** add codex skill metadata ([54e06e7](https://github.com/j5ik2o/ai-tools/commit/54e06e7949d19d971fe566cb605c901a32740dc2))
* **skill-forge:** generate codex openai metadata ([8f66e4d](https://github.com/j5ik2o/ai-tools/commit/8f66e4dda53d1fb687d8b716aa140471f0787ddc))
* track renames before marking an issue's target as gone ([f46bef7](https://github.com/j5ik2o/ai-tools/commit/f46bef7146d92db35693b60d8c2e56670478ca27))


### Bug Fixes

* aggregate paginated issue pages into a single array ([c12c7f7](https://github.com/j5ik2o/ai-tools/commit/c12c7f7e1c7116bf9831cb331006263e5346d3cc))
* align takt plugin description with workflow-builder rename ([7bcb8cc](https://github.com/j5ik2o/ai-tools/commit/7bcb8cc94838f640833caf0a0d3b67d41cf6da53))
* correct issue classification priority in gh-issue-organizer ([ef3238d](https://github.com/j5ik2o/ai-tools/commit/ef3238d040ff512cd5803dff11c23e6a76535726))
* forward-reference Step 2 criteria from Step 1 summary ([e011bc5](https://github.com/j5ik2o/ai-tools/commit/e011bc57f421623e143382e61c7dcf14cf994d0c))
* guarantee full issue fetch beyond the gh list limit ([ec126a8](https://github.com/j5ik2o/ai-tools/commit/ec126a8b8b6bdd05b63141545f5f83ca941912b0))
* include coderabbit label in CodeRabbit extraction commands ([3fd9c2f](https://github.com/j5ik2o/ai-tools/commit/3fd9c2f2900efa23cbcb4cc23df6154dcb22778e))
* make issue-count and pagination commands actually unbounded ([278e335](https://github.com/j5ik2o/ai-tools/commit/278e3356af69655849e6f3af0ec78e34bb9b925b))
* make その他 a true catch-all and clarify bug detection ([0627e1a](https://github.com/j5ik2o/ai-tools/commit/0627e1a69cb3dc90989e5174e4d227aee7f5f6c5))
* **plugins:** preserve credential commit guard ([e62ba28](https://github.com/j5ik2o/ai-tools/commit/e62ba28b19d13d9f1828be432d9572cc1af84a22))
* **plugins:** reject empty codex capabilities ([a6101b5](https://github.com/j5ik2o/ai-tools/commit/a6101b5fffaa0468fee94231fc5bc89d6ef27349))
* **plugins:** require defaultPrompt array ([10348dd](https://github.com/j5ik2o/ai-tools/commit/10348dd19baae77aaeab7eaa5db3d20e792496b1))
* resolve internal inconsistencies in gh-issue-organizer ([ef33510](https://github.com/j5ik2o/ai-tools/commit/ef335103d02e15d6a854d4ee9a883a6fc55f3f90))
* review staged changes before committing in git-commit ([80f6217](https://github.com/j5ik2o/ai-tools/commit/80f6217d778895ab8ac32f419d092da5aa2310d8))
* scope CodeRabbit category to coderabbitai and coderabbit label ([8073258](https://github.com/j5ik2o/ai-tools/commit/8073258097e1800d5df196d7c1b18d406c69f7c1))
* scope git-commit trigger to explicit commit requests ([c45e5fa](https://github.com/j5ik2o/ai-tools/commit/c45e5fabb66e730f453ecacf34ae89a24b37333d))
* **scripts:** set CLAUDE_IDENTITY for corporate environment ([308ce1e](https://github.com/j5ik2o/ai-tools/commit/308ce1edcda03816027f2034988446b69c9565bd))
* **skill-forge:** add platform-aware skill validation ([701052f](https://github.com/j5ik2o/ai-tools/commit/701052f4a7dd173aec563da9be7211cc116da89f))
* **skill-forge:** document trigger eval boundaries ([76e2d7b](https://github.com/j5ik2o/ai-tools/commit/76e2d7bd5f820019baafd2e9192eca9fb07de53f))
* **skill-forge:** evaluate claude skills via skill layout ([6b48d79](https://github.com/j5ik2o/ai-tools/commit/6b48d79a87ab805b4c4739d635a3e03bc21fcf13))
* **skill-forge:** normalize eval expectations schema ([9c1a693](https://github.com/j5ik2o/ai-tools/commit/9c1a6936d5f90185defaf4b35ef4b07170e3821c))
* **skill-forge:** use agents skills for codex evals ([4d90c8b](https://github.com/j5ik2o/ai-tools/commit/4d90c8b51d38e6f31142677e8dabd6566139b8b5))
* **takt:** align review workflow aggregation ([55ec6da](https://github.com/j5ik2o/ai-tools/commit/55ec6dab8c00ad32f16c0687f55b6353ba69fbd1))
* tighten bug title match and add その他 to summary table ([bfb490d](https://github.com/j5ik2o/ai-tools/commit/bfb490d89b2862950e2b7c6d1b7b57dfd2580043))
* verify committed content after pre-commit hooks run ([1d358cf](https://github.com/j5ik2o/ai-tools/commit/1d358cfefdbb0ceac2251e4099ebd28555eed5a2))

## [0.4.1](https://github.com/j5ik2o/ai-tools/compare/v0.4.0...v0.4.1) (2026-06-17)


### Bug Fixes

* Terraformレビュー集約条件を修正 ([b3883fb](https://github.com/j5ik2o/ai-tools/commit/b3883fb7c7790135d2e31d442d72a13b0a89ad45))


### Reverts

* Terraformレビュー集約条件修正を取り消し ([9864d14](https://github.com/j5ik2o/ai-tools/commit/9864d148a12ee8994639e381e95e286009dce00f))

## [0.4.0](https://github.com/j5ik2o/ai-tools/compare/v0.3.3...v0.4.0) (2026-06-11)


### Features

* **ci:** add takt-skill-auto-update workflow ([bc317da](https://github.com/j5ik2o/ai-tools/commit/bc317da66c734c39079369252713217bc999232c))


### Bug Fixes

* .gitignore ([a133937](https://github.com/j5ik2o/ai-tools/commit/a1339379cf982771369f91912071caf7a9999dd4))
* **ci:** address review findings in takt-skill-auto-update ([0d14685](https://github.com/j5ik2o/ai-tools/commit/0d14685aa5c5a5e58382dc50629bb9183f006df2))
* **ci:** avoid pipe in branch-version check to be pipefail-safe ([b7229f9](https://github.com/j5ik2o/ai-tools/commit/b7229f9f57b5e4c7342814c8861685d3c985c4a4))
* **ci:** disable credential persistence in update job checkout ([d838f31](https://github.com/j5ik2o/ai-tools/commit/d838f31c4701c469161b24964201ee34082e7319))
* **ci:** re-run update when branch exists but PR was never created ([097e5c8](https://github.com/j5ik2o/ai-tools/commit/097e5c8a7b259814f450d689580836aedbb86233))
* **scripts:** clean up shebang and update CODEX_HOME path ([1f51802](https://github.com/j5ik2o/ai-tools/commit/1f518025dff34a29c3a64663f56c28b717c3390f))
* **takt-skill-updater:** Step 0 honors pinned NEW_VERSION ([ea6850f](https://github.com/j5ik2o/ai-tools/commit/ea6850f58ab670814a77550aeb5f1aa9b1d844a3))
* **takt-skills:** correct misleading observability example in synced e2e.md ([ed18c26](https://github.com/j5ik2o/ai-tools/commit/ed18c26ae169b501fc45c8d612ed3d5ed4e9c656))

## [0.3.3](https://github.com/j5ik2o/ai-tools/compare/v0.3.2...v0.3.3) (2026-06-02)


### Bug Fixes

* allow empty changelog releases ([b4cb806](https://github.com/j5ik2o/ai-tools/commit/b4cb806054f7524a3667a5520a461724d630a48c))

## [0.3.2](https://github.com/j5ik2o/ai-tools/compare/v0.3.1...v0.3.2) (2026-04-15)


### Bug Fixes

* **takt-workflow-builder:** update evals and validate script to workflow/step terminology ([a05100c](https://github.com/j5ik2o/ai-tools/commit/a05100c26af5b2f0311b930616d5fed771e649f9))

## [0.3.1](https://github.com/j5ik2o/ai-tools/compare/v0.3.0...v0.3.1) (2026-04-13)


### Bug Fixes

* remaining piece→workflow terminology in SKILL.md/SKILL.en.md ([9ee8edf](https://github.com/j5ik2o/ai-tools/commit/9ee8edf4c3189d0a7503a5f2aa227b46d9095e0c))

## [0.3.0](https://github.com/j5ik2o/ai-tools/compare/v0.2.0...v0.3.0) (2026-04-13)


### Features

* **takt:** sync takt submodule references into each skill's local directory ([6aadf85](https://github.com/j5ik2o/ai-tools/commit/6aadf85c4ffc74e5983456b52964083afa4f2cde))


### Bug Fixes

* **marketplace:** declare plugin skill paths ([72484ba](https://github.com/j5ik2o/ai-tools/commit/72484ba8b99bb7307d9f47a1345a63fb85eecf69))
* **plugin:** add plugin metadata files ([7572185](https://github.com/j5ik2o/ai-tools/commit/7572185f2694df3718c203f84438d58ae06470e3))
* **scripts:** improve skill recognition checks with parallel execution and temporary result directory ([c63f682](https://github.com/j5ik2o/ai-tools/commit/c63f682860a726e5702d9ddba557340cbeae102f))
* **scripts:** prevent nested session detection in test plugin install script ([0d0d927](https://github.com/j5ik2o/ai-tools/commit/0d0d9279992209043bdbd962430afd2e02bde055))
* update marketplace.json for takt-workflow-builder rename and remove $schema ([2be9469](https://github.com/j5ik2o/ai-tools/commit/2be946920aa863bedb5c44b18b89ceb89aaa4a9b))

## [0.2.0](https://github.com/j5ik2o/ai-tools/compare/de1cfee51078d9d55b04077361f335b7af68ba7d...v0.2.0) (2026-03-09)


### Features

* add default `.takt/config.yaml` configuration for Codex ([7544af9](https://github.com/j5ik2o/ai-tools/commit/7544af92dd8c07df78ad76f12a588f623ab24b2b))
* takt-skill-updater にタグ間差分の取得ステップを追加 ([62417b5](https://github.com/j5ik2o/ai-tools/commit/62417b52b8b42388ecd5a4c6811bd319d14dfddb))


### Bug Fixes

* address bugbot review comments ([3aa29bf](https://github.com/j5ik2o/ai-tools/commit/3aa29bfb0c23cef36fb13f076079be5069e23c1a))
* repair broken skill symlinks ([1f82408](https://github.com/j5ik2o/ai-tools/commit/1f8240818e700300b73ec7d358c63cf9a73ec568))
* resolve skill-creator home overrides ([1326f70](https://github.com/j5ik2o/ai-tools/commit/1326f70e9a8127f7e887cf90d8906813c08d3dcd))
* **skill-forge:** tighten trigger boundaries ([7e4131a](https://github.com/j5ik2o/ai-tools/commit/7e4131a50b92209a4e6d55797bf4eb93e503cad3))
* stabilize skill creator ci ([de1cfee](https://github.com/j5ik2o/ai-tools/commit/de1cfee51078d9d55b04077361f335b7af68ba7d))
* takt-skill-updater にパス表記の読み替えルールを追加 ([dfbfe30](https://github.com/j5ik2o/ai-tools/commit/dfbfe30eced27ad3829c01b81b80f981bfebe7ab))
* takt-skill-updater のファセットパスとバージョンを修正 ([1d231eb](https://github.com/j5ik2o/ai-tools/commit/1d231ebc16bfa70911d5f44772f217ebd53fdf40))
* takt-skill-updater の対象スキル名を実際のディレクトリ名に修正 ([ecb9213](https://github.com/j5ik2o/ai-tools/commit/ecb92136bfff24f60281233ebb3698b57aac7680))
* 環境変数プレフィックスを SKILL_CREATOR_ から SKILL_FORGE_ にリネーム ([1713a66](https://github.com/j5ik2o/ai-tools/commit/1713a66d20347783f591460494bc2604b58b6264))

