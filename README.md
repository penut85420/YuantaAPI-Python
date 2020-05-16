# Yuanda Quote API using Python

## Table of Contents
+ [Introduction](#introduction)
+ [Features](#features)
+ [Environment](#environment)
+ [Installation](#installation)
+ [Usage](#usage)
+ [Port](#port)
+ [Columns Name](#columns-name)
+ [Scripts](#scripts)
+ [To-Do](#to-do)
+ [Security Issue](#security-issue)
+ [Reference](#reference)

## Introduction
+ 這是使用 Python 串接元大行情 API 的程式。
+ 這份程式碼修改自 [這篇文章](https://tinyurl.com/yxgffpo6)，請各位一定要去按個讚！

## Features
+ 啟動程式後，會將行情資料記錄成 csv 檔。
  + 只要有撮合、五檔跳動皆會新增一筆資料。
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
+ `$ python quote.py [-h] [-v VERBOSE]`
  + `-h, --help` - 顯示說明訊息。
  + `-v, --verbose` - 設定 Log 檔的 Logging Level，請參考 [Severity Levels](https://tinyurl.com/y4p2a25l)。
  + `--no-option` - 選擇不要接收選擇權的行情

## Port
+ 使用 80 或 443 為日盤的行情。
+ 使用 82 或 442 為夜盤的行情。

## Columns Name
+ 關於行情資料欄位的名稱與解釋請參考 [`COLSNAME.md`](https://git.io/Jf00M)。

## Scripts
+ `do_compress.py`
  + 壓縮行情資料，建議使用 Bash 執行。
+ `log_cls.py`
  + 清除 `./Logs` 下的紀錄檔。
+ `quote.py`
  + 接收行情資料的主程式。
+ `retrieve_file.py`
  + 從行情資料夾內提取目標商品的資料。
+ `std_analysis.py`
  + 分析行情價格標準差變動的相關資訊。
+ `switch_battery_plan.py`
  + 切換電腦的電源狀態。
+ `utils.py`
  + 系統相關程式庫。
+ `ping.sh`
  + 執行 Ping 元大行情主機的指令。
  + 必須使用 Bash 執行。

## To-Do
+ 選擇權商品的部分並不算太完整，目前只有針對個人需求抓取台指的部分。

## Security Issue
+ 元大 API 會在連接伺服器的時候自動產生一個 `Logs\event.log` 的檔案，會將使用者的帳密以明碼的方式寫入，程式執行結束時請務必手動刪除這個檔案。
  + 本系統會每隔五分鐘清除一次這個資料夾下的檔案
  + 也可以手動執行 `log_cls.py` 這個程式來清除

## Reference
+ [Python 程式交易 30 天新手入門](https://tinyurl.com/y3ycw3ms)
