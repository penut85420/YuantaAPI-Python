# 行情資料記錄檔欄位名稱與解釋

## 欄位名稱
+ 每一筆行情資料由左至右分別為：
  1. [接收時間](#接收時間)
  2. [開盤價](#開盤價)
  3. [最高價](#最高價)
  4. [最低價](#最低價)
  5. [最後撮合時間](#最後撮合時間)
  6. [最後撮合價格](#最後撮合價格)
  7. [最後撮合量](#最後撮合量)
  8. [總交易量](#總交易量)
  9. 最佳五檔買量 1
  10. 最佳五檔買量 2
  11. 最佳五檔買量 3
  12. 最佳五檔買量 4
  13. 最佳五檔買量 5
  14. 最佳五檔買價 1
  15. 最佳五檔買價 2
  16. 最佳五檔買價 3
  17. 最佳五檔買價 4
  18. 最佳五檔買價 5
  19. 最佳五檔賣量 1
  20. 最佳五檔賣量 2
  21. 最佳五檔賣量 3
  22. 最佳五檔賣量 4
  23. 最佳五檔賣量 5
  24. 最佳五檔賣價 1
  25. 最佳五檔賣價 2
  26. 最佳五檔賣價 3
  27. 最佳五檔賣價 4
  28. 最佳五檔賣價 5

## 欄位解釋
### 接收時間
+ 為主機接收到這筆行情資訊的時間。

### 開盤價
+ 為這段交易時間內此商品的開盤價。

### 最高價
+ 為這段交易時間內此商品的最高價。

### 最低價
+ 為這段交易時間內此商品的最低價。

### 最後撮合時間
+ 為此商品最後一次撮合的時間。

### 最後撮合價格
+ 為此商品最後一次撮合時的價格。

### 最後撮合量
+ 為此商品最後一次撮合時的交易量。

### 總交易量
+ 為這段交易時間內此商品的總交易量。

## CSV Header
+ 因為本系統並沒有把 CSV 的 Column Header 加上去，所以在這邊附上：
  + Snake Case
    ```
    time,open_price,high_price,low_price,match_time,match_price,match_quantity,total_match_quantity,best_buy_quantity1,best_buy_quantity2,best_buy_quantity3,best_buy_quantity4,best_buy_quantity5,best_buy_price1,best_buy_price2,best_buy_price3,best_buy_price4,best_buy_price5,best_sell_quantity1,best_sell_quantity2,best_sell_quantity3,best_sell_quantity4,best_sell_quantity5,best_sell_price1,best_sell_price2,best_sell_price3,best_sell_price4,best_sell_price5
    ```
  + Pascal Case
    ```
    Time,OpenPrice,HighPrice,LowPrice,MatchTime,MatchPrice,MatchQuantity,TotalMatchQuantity,BestBuyQuantity1,BestBuyQuantity2,BestBuyQuantity3,BestBuyQuantity4,BestBuyQuantity5,BestBuyPrice1,BestBuyPrice2,BestBuyPrice3,BestBuyPrice4,BestBuyPrice5,BestSellQuantity1,BestSellQuantity2,BestSellQuantity3,BestSellQuantity4,BestSellQuantity5,BestSellPrice1,BestSellPrice2,BestSellPrice3,BestSellPrice4,BestSellPrice5
    ```
+ 附上 Header List 方便宣告：
  + Snake Case
    ```
    "time", "open_price", "high_price", "low_price", "match_time", "match_price", "match_quantity", "total_match_quantity", "best_buy_quantity1", "best_buy_quantity2", "best_buy_quantity3", "best_buy_quantity4", "best_buy_quantity5", "best_buy_price1", "best_buy_price2", "best_buy_price3", "best_buy_price4", "best_buy_price5", "best_sell_quantity1", "best_sell_quantity2", "best_sell_quantity3", "best_sell_quantity4", "best_sell_quantity5", "best_sell_price1", "best_sell_price2", "best_sell_price3", "best_sell_price4", "best_sell_price5"
    ```
  + Pascal Case
    ```
    "Time", "OpenPrice", "HighPrice", "LowPrice", "MatchTime", "MatchPrice", "MatchQuantity", "TotalMatchQuantity", "BestBuyQuantity1", "BestBuyQuantity2", "BestBuyQuantity3", "BestBuyQuantity4", "BestBuyQuantity5", "BestBuyPrice1", "BestBuyPrice2", "BestBuyPrice3", "BestBuyPrice4", "BestBuyPrice5", "BestSellQuantity1", "BestSellQuantity2", "BestSellQuantity3", "BestSellQuantity4", "BestSellQuantity5", "BestSellPrice1","BestSellPrice2", "BestSellPrice3", "BestSellPrice4", "BestSellPrice5"
    ```
+ Python List
  ```python
  [
    'time',
    'open_price',
    'high_price',
    'low_price',
    'match_time',
    'match_price',
    'match_quantity',
    'total_match_quantity',
    'best_buy_quantity1',
    'best_buy_quantity2',
    'best_buy_quantity3',
    'best_buy_quantity4',
    'best_buy_quantity5',
    'best_buy_price1',
    'best_buy_price2',
    'best_buy_price3',
    'best_buy_price4',
    'best_buy_price5',
    'best_sell_quantity1',
    'best_sell_quantity2',
    'best_sell_quantity3',
    'best_sell_quantity4',
    'best_sell_quantity5',
    'best_sell_price1',
    'best_sell_price2',
    'best_sell_price3',
    'best_sell_price4',
    'best_sell_price5'
  ]
  ```
