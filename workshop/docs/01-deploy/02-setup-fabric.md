# 建立 Fabric 工作區

建立並設定你的 Microsoft Fabric 工作區以使用 Fabric IQ。

!!! info "主要適用對象"
	本頁主要供**管理員部署**路徑使用
	參與者應使用已經準備好並分享給他們的工作區。

## 先決條件

- Microsoft Fabric 容量（建議 F2 或更高）
- 工作區管理員權限
- 工作區已啟用 Ontology / Fabric IQ 所需功能

!!! warning "容量不足不等於功能可用"
	即使工作區已綁定 Fabric 容量，Ontology API 仍可能回傳 `FeatureNotAvailable`。
	如果發生這種情況，代表目前工作區尚未開通本 workshop 所需的 Ontology 功能。此時完整 Fabric 路徑無法執行，請改用已啟用該功能的工作區，或先使用 `--foundry-only` 路徑完成 Search-only workshop。

## 建立 Fabric 工作區

1. 前往 [Microsoft Fabric](https://app.fabric.microsoft.com)
2. 點選 **Workspaces** → **New workspace**
3. 命名，例如 `iq-workshop`
4. 選擇你的 Fabric 容量
5. 點選 **Apply**

## 設定工作區

1. 開啟你新建的工作區
2. 前往 **Settings** → **License info**
3. 確認工作區正在使用 Fabric 容量

## 取得工作區資訊

下一步你將需要以下值：

| 設定項 | 在哪裡找 |
|--------|----------|
| Workspace ID | URL 中 `/groups/` 之後的部分 |
| Workspace name | 工作區設定 |


[← 部署 Azure 資源](01-deploy-azure.md) | [參與者執行與驗證 →](00-participant-run-validate.md)
