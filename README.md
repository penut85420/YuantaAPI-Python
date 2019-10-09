# Yuanda Quote API using Python

## Introduction
+ 這是使用 Python 串接元大行情 API 的程式。
+ 這份程式碼修改自 [這篇文章](https://tinyurl.com/yxgffpo6)，請各位一定要去按個讚！

## Features
+ 啟動程式後，會將行情資料記錄成 csv 檔。
+ 支援股票、期貨和選擇權商品。
+ 自動切換日夜盤。
+ 自動更新選擇權商品代碼。

## Environment
+ OS: Windows 10 x64 1903
+ Python Version: **3.6 x86**
  + 必須使用 x86 版本的 Python 才能正常運作。

## Installation
+ 安裝元大行情 API，請參考 [這篇文章](https://tinyurl.com/y6xsdnq5)。
+ 安裝 Python 環境：
  + `pip install -r requirements.txt`

## Usage
+ `$ python quote.py [-h] [-p PORT] [--night] [-v VERBOSE]`
  + `-h, --help` - 顯示說明訊息。
  + `-p, --port` - 設定連接 API 的 Port。
  + `-n, --night` - 設定是否為夜盤。
  + `-v, --verbose` - 設定 Log 檔的 Logging Level，請參考 [Severity Levels](https://tinyurl.com/y4p2a25l)。
+ Example
  + 普通獲取日盤行情
    + `$ python quote.py`
  + 獲取夜盤行情
    + `$ python quote.py -n`

## Port
+ 使用 80 或 443 為日盤的行情。
+ 使用 82 或 442 為夜盤的行情。

## Security
+ 元大 API 會在連接伺服器的時候自動產生一個 `Logs\event.log` 的檔案，會將使用者的帳密寫進去，程式執行結束時請務必手動刪除這個檔案。

## Reference
+ [Python 程式交易 30 天新手入門](https://tinyurl.com/y3ycw3ms)
