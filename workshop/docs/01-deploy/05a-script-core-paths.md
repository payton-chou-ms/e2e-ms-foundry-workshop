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

如果你想回到 Foundry portal 做 guided demo，請看 [Microsoft Foundry 手動 Demo](04a-manual-experiments.md)。
如果你想手動驗證 Lakehouse、tables 與 ontology，請看 [Microsoft Fabric 手動驗證](04b-fabric-manual-validation.md)。

---

[← 腳本用途與執行順序總覽](05-script-sequence.md) | [主流程腳本 01-08 →](05b-script-core-pipeline.md)