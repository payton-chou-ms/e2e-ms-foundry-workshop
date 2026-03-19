# 清理資源

完成後請刪除 Azure 資源以管理成本。

## 刪除 Azure 資源

```bash
azd down
```

出現提示時請確認：

```
? Total resources to delete: 8, are you sure? (y/N) y
```

## 驗證刪除

1. 前往 [Azure Portal](https://portal.azure.com/)
2. 檢查 **Resource groups**
3. 確認你的 lab 資源群組已被刪除

!!! warning "重要"
    請務必執行清理以避免持續產生費用！

## 清理 Fabric（選擇性）

如果你建立了 Fabric 產物並希望移除它們：

1. 前往 [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. 開啟你的工作區
3. 刪除為本 workshop 建立的 Lakehouse 和 Warehouse

## 清理本機檔案（選擇性）

移除產生的資料資料夾：

=== "Windows PowerShell"

    ```powershell
    Remove-Item -Recurse -Force data\*_*
    ```

=== "macOS/Linux"

    ```bash
    rm -rf data/*_*/
    ```

---

[後續步驟 →](next-steps.md)
