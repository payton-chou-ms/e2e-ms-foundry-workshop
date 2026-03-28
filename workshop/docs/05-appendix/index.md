# 附錄：Fabric 延伸

這一章刻意放在主線之後。

建議順序是：先把 Foundry 線跑通，再回來補 Fabric 線。也就是先完成 Azure 部署、Foundry agent 建立與驗證，確認文件路徑穩定後，再處理 Fabric workspace、Lakehouse、Ontology 與 SQL grounding。

## 這一章適合什麼時候看

- 你已經完成 Foundry 主線，現在要把 PoC 擴充到結構化資料問答
- 你需要建立或檢查 Fabric workspace、Lakehouse、Ontology
- 你要驗證 `execute_sql` 路徑或解釋 Fabric IQ 背後怎麼運作

## 建議閱讀順序

1. [建立 Fabric 工作區](01-setup-fabric.md)
2. [Fabric 詳細設定](02-workspace-settings.md)
3. [Microsoft Fabric 手動驗證](03-manual-validation.md)
4. [Fabric IQ：資料](04-fabric-iq.md)
5. [維護者：資料腳本對照](05-maintainer-data-scripts.md)

## 主線與附錄的分工

- 主線：先完成 Foundry 文件路徑、agent 建立、驗證與教學示範
- 附錄：再補上 Fabric 資料層、手動驗證與 IQ 資料 grounding

如果你現在只是要把 workshop 跑通，先回到 [部署方案](../01-deploy/index.md) 或 [深入解析](../03-understand/index.md)。

---

[← 深入解析](../03-understand/index.md) | [建立 Fabric 工作區 →](01-setup-fabric.md)