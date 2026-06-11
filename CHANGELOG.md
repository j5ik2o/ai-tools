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

