# 快速建置與測試

如果你現在只想知道該跑哪兩個命令，這一頁就夠了。

## Path 1: Foundry IQ only

適合先做文件問答，不接 Fabric。

建置：

```bash
python scripts/00_build_solution.py --foundry-only
```

測試：

```bash
python scripts/08_test_foundry_agent.py --foundry-only
```

## Path 2: Foundry IQ + Fabric IQ

適合同時做文件問答和資料問答。

建置：

```bash
python scripts/00_build_solution.py --from 02
```

測試：

```bash
python scripts/08_test_foundry_agent.py
```

## 如果你還想知道背後有哪些 script

接著看 [主流程腳本 01-08](05b-script-core-pipeline.md)。

如果你想改走 Foundry portal 內比較原生的文件型 agent，請看 [Microsoft Foundry / Fabric 手動實驗流程](04a-manual-experiments.md)。

---

[← 腳本用途與執行順序總覽](05-script-sequence.md) | [主流程腳本 01-08 →](05b-script-core-pipeline.md)