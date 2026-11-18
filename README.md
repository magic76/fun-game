# 薪水小偷俱樂部 — Fun Game
Three.js 3D 惡搞辦公室遊戲測試站（目前 V10.1 修正版）。

## 試玩
GitHub Pages 啟用後固定網址： https://magic76.github.io/fun-game/

入口：根目錄 `index.html`（內嵌 GLB 模型，不需要自行下載額外模型檔）。
首次載入仍需要連線至 jsDelivr 取得 Three.js。

## 第一次啟用 GitHub Pages
1. 開啟本 Repo 的 Settings → Pages。
2. 在 Build and deployment 的 Source 選 **GitHub Actions**。
3. 進入 Actions → Deploy Fun Game to GitHub Pages → Run workflow（選 main）。
4. 工作流程成功後，用上方固定網址開啟。

以後更新 `main` 的遊戲檔，Pages 將自動部署。不必每次重新下載 HTML。

## 版本資訊
- V10.1：修正「正在打卡…」因道具 UI 變數拼寫錯誤而卡住的問題，加入進場失敗重試保護。
- 支援桌面 WASD／方向鍵與手機虛擬搖桿。
- 單機預覽已包含 3D 場景、角色、道具操作與本機留言。
- **尚未接上真正的多人伺服器**。GitHub Pages 只提供靜態遊戲前端，真人多人需要另部署 Cloudflare Worker / Durable Objects。

開發原則：先在這個固定網址驗收進場與遊戲體驗，再修改人物、美術、碰撞與多人互動。
