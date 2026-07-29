1. AI 的限制通常不是能力，而是環境不完整

文章提到，初期進展比預期慢，不是 Codex 不會寫，而是：

規格不清楚。
缺少可執行工具。
缺少架構邊界。
缺少可驗證結果。
缺少足夠的 repository context。

因此，遇到 AI 一直做錯時，不應只是換一句 prompt 再試一次，而要問：

AI 缺少哪一項資訊？
缺少哪個工具？
哪個規則無法被自動驗證？
哪個結果無法被觀察？

這正是 Harness Engineering 的核心。

2. 工程師角色從「寫程式」變成「設計系統」

文章中的工程師主要工作變成：

把大型需求拆成小型基礎能力。
建立 AI 能使用的工具。
定義清楚的模組邊界。
建立驗收標準。
建立自動測試。
讓 AI 可以自行查看錯誤。
將人工經驗寫回系統。

也就是：

以前：
工程師 → 撰寫功能

AI Agent 模式：
工程師 → 設計開發工廠
AI       → 在工廠內完成開發

因此，真正的效率來自「開發系統」，不是單次生成程式碼。

3. AGENTS.md 應該是地圖，不是百科全書

OpenAI 一開始曾嘗試把所有規則都放在一個大型 AGENTS.md，結果失敗。

原因包括：

太長會占用上下文。
所有規則都說重要，就沒有優先順序。
文件容易過時。
AI 不知道哪些規則仍然有效。
很難自動檢查文件是否完整。

後來他們把 AGENTS.md 縮短成約 100 行，只作為「導航入口」，詳細知識放入結構化的 docs/。

例如：

AGENTS.md
ARCHITECTURE.md
docs/
├─ design-docs/
├─ exec-plans/
│  ├─ active/
│  └─ completed/
├─ product-specs/
├─ references/
├─ RELIABILITY.md
├─ SECURITY.md
└─ QUALITY_SCORE.md
