# Reverse-sheet-sky-children-of-the-light

我想要彈更多的音樂 ((っ･ω･)っ  
I want to play more music in Sky ((っ･ω･)っ

這個程式可以從 sky 影片中逆向出文字譜面  
This program can reverse the sheet from the sky video

---

## 教學影片 teach video

[![待補的URL](http://img.youtube.com/vi/E-ofS-MiVzs/0.jpg)](http://bit.ly/3agGXdu)

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
No need to login google. 不用登入 google  
[https://forms.gle/cNgn23CM3FDkR5Tg7](https://forms.gle/cNgn23CM3FDkR5Tg7)

## 程式執行環境安裝 environment install

**⚠️python version require >= 3.5⚠️**

```allowEmpty
pip install -r requirements.txt
```

## 如何使用 How to use

目前只有教學影片，歡迎貢獻 PR  
Now just have teach video，welcome PR

## 待做功能 ToDo

- 4_play_sheet_video 應該要加個 X 軸向長條狀態列在影片下方，藉此告知目前所有換行符的位置
- 4_play_sheet_video 考慮做在轉換影片中，如果該鍵盤正被播放，要給一個紅色框框提示
- 4_play_sheet_video 要做音符時間輸出 每個行首一個
- 4_play_sheet_video 要做自動換行，隔幾秒空白就一個

## 已知問題 issues

- 4_play_sheet_video 換行(a 鍵)時間比影片畫面會再晚一點點。目前不知道會不會跟電腦環境有關，有關的話較難排除。
