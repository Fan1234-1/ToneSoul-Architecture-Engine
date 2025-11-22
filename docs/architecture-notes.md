# Architecture Notes

This document offers two complementary perspectives on the ToneSoul Architecture Engine (TAE-01): a philosophical lens and an engineering lens.  Both views are essential for understanding why the system looks the way it does.

## Part A: The Philosopher's View (給哲學家看)

### 時間島（Time-Island）為何必要？

在自然語言交流中，語境是流動的。  為了確保每一次對話都能在穩定的語境中運作，我們將記憶劃分為一座一座的「時間島」。  每座島島都保存了一個連續的事件序列及其上下文摘要，阻止新信息倒濱舊紀錄。  這是一種對抗流動性的策略，確保不可逆、可迴潜的對話歷史。

### 誓言物件（VowObject）是什麼？

語言不是軟跺的文字。  在 ToneSoul 框架中，每一句話都被封裝為一個帶有 `responsibility_score` 的誓言物件。  發出誓言就像簽約：它有時間戳、內容散列和責任度。  誓言物件讓 AI 的輸出具有重量，能夠迴潜和審評，形成道德約束力。

## Part B: The Engineer's View (給工程師看)

### Middleware 設計模式

TAE-01 的核心采用中介層（Middleware）設計模式。  用戶的輸入首先經過 `Agent` 模組生成草稿，再由 `EthicalFilter` 進行安全與風險評估，最後所有結果寫入 `StepLedger`。  每個層次只關注自己的職責，从而降低耰合度，提高可測試性與可維護性。

### StepLedger 如何實現不可變日誌？

`StepLedger` 是一個 append-only 的日誌系統。  每一條記錄都有獨立的 `step_id`、`trace_id` 和 `context_hash`。  `context_hash` 由輸入、輸出和模組標識組合後哈希得到，任何試圖修改既有記錄的行為都會導致哈希不一致，從而被發現。  此設計確保歷史不可編變，為審評和問責提供堅實基礎。
