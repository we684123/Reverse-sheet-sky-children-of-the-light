# Reverse-sheet-sky-children-of-the-light
我想要彈更多的音樂 ((っ･ω･)っ

## 影片
[Shelter (Porter Robinson & Madeon) | 避難所 | Sky: Children of the Light 光遇 COVER](https://www.youtube.com/watch?v=Rf_DHuEkdY4)

## 筆記
由於鍵盤本身就會跳動，因此要做變化值檢測
然後設定閥值，當突波時就是點下去的時機，連續點擊同一鍵時(高於閥值時要再做第二次斜率變化偵測)

目前 code_flow 程式 logger 沒說多好，要再修改，且要再做防呆。

- 要做 可以即時檢測的東西 最少要知道譜面是否生成正確
做一半了，不能及時檢測


2021/1/11
~~！！！警告 目前 pygame 播放有問題 不能信~~
~~自是是不是鎖同音重複時間~~
~~還是檔案~~
已增加通道數解決
