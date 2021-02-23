# Reverse-sheet-sky-children-of-the-light

我想要彈更多的音樂 ((っ･ω･)っ  
I want to play more music in Sky ((っ･ω･)っ

這個程式可以從 sky 影片中逆向出文字譜面  
This program can reverse the sheet from the sky video

**該程式盡量遵守** [pep8](https://www.python.org/dev/peps/pep-0008/)、[gitmoji](https://gitmoji.dev/)

---

## 教學影片 teach video

⚠️⚠️⚠️ 拜託! 我決定之後重錄了 自己看就好 我不想讓黑歷史讓太多人知道 qwq⚠️⚠️⚠️  
⚠️⚠️⚠️plz don't share to other people, i know this video is very bad Orz , i will make a new⚠️⚠️⚠️  
[https://youtu.be/8r4bcis4C_s](https://youtu.be/8r4bcis4C_s)  
[![待補的URL](http://img.youtube.com/vi/8r4bcis4C_s/0.jpg)](https://youtu.be/8r4bcis4C_s)

## 譜面 sheets

這裡有一些已經轉好的譜面  
Here have some sky sheet can play

- http://bit.ly/3qy6aZ1 (from [不用登入 google](https://forms.gle/q11xptKWeZkbFU687))
- http://bit.ly/38RwvuO (from [需要登入 google](https://forms.gle/cNgn23CM3FDkR5Tg7))

## 貢獻譜面 contribute sheets

**歡迎透過表單貢獻給所有光之子**  
**Welcome to contribute to skykids through this form**

如果可以的話還是希望你能夠提供有譜面檔的版本  
如此一來對方可以輕鬆的將譜面轉成他所喜歡的格式  
If possible, I hope you do provide the version with the score file.  
In this way, the skykids can easily convert the score to his preferred format

Need to login google. 需要登入 google  
[https://forms.gle/PrwRa1BoavDcfvp77](https://forms.gle/PrwRa1BoavDcfvp77)  
Not need to login google. 不用登入 google  
[https://forms.gle/cNgn23CM3FDkR5Tg7](https://forms.gle/cNgn23CM3FDkR5Tg7)

## 程式執行環境安裝 environment install

**⚠️python version require >= 3.5⚠️**

```allowEmpty
pip install -r requirements.txt
```

## 如何使用 How to use

目前只有教學影片，歡迎貢獻 PR  
Now just have teach video，welcome PR

### 鍵盤功能

![鍵盤功能](https://imgur.com/9e58sw1.png)

## 待做功能 ToDo

- 4_play_sheet_video 應該要加個 X 軸向長條狀態列在影片下方，藉此告知目前所有換行符的位置
- ~~4_play_sheet_video 考慮做在轉換影片中，如果該鍵盤正被播放，要給一個紅色框框提示~~
- 4_play_sheet_video 要做音符時間輸出 每個行首一個
- 4_play_sheet_video 要做自動換行，隔幾秒空白就一個
- 新增 自動打包並替代所有 win x64 的東東(不想用複雜的環境，想一鍵解決) 目前候選用 [PyUpdater](https://github.com/Digital-Sapphire/PyUpdater)
- 新增 轉換格式的程式，讓 user 可以用於 "Sky Studio" or "Sky Music"
- analysis 要做極高峰植濾波
- 增加短時間連續演奏符號 "-", ex:【B4-C4】

## 已知問題 issues

- 4_play_sheet_video 換行(a 鍵)時間**好像**比影片畫面會再晚一點點。目前不知道會不會跟電腦環境有關，有關的話較難排除。
- 4_play_sheet_video 輸出的換行符 '\\n' 有時候會失效，不確定觸發機制，如果遇上可以改 '\\r\\n' 看看。

## 資料來源 + 授權 data source + authorize

- 鍵盤圖片([可免費商用授權](https://www.pexels.com/zh-tw/photo/698808/))
- [Shelter (Porter Robinson & Madeon) | 避難所 | Sky: Children of the Light 光遇 COVER](https://www.youtube.com/watch?v=Rf_DHuEkdY4)
- 感謝 [Y C](https://www.youtube.com/watch?v=leOckppuFkY&lc=Ugw3kpea7BD0LvKWLEt4AaABAg.9BJJCPqBs-N9ISCkLZAPiw) 大大授權使用影片

## 作者 Author

![](https://avatars3.githubusercontent.com/u/22027801?s=460&v=4)

[永格天](https://we684123.carrd.co/)  
一個~~中二病~~水瓶座男子  
不太擅長塗鴉 (看大頭貼就知道 Orz...)
