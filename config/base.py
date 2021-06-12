def reverse_config():
    return {
        # 目標資料夾絕對位置
        "aims_folder_path":
            r"C:\Users\we684123\Dropbox\各類專案\Github\Reverse-sheet-sky-children-of-the-light",
        # 影片的位置
        "video_path": "./Shelter.mkv",
        # 譜面輸出目錄
        "output_sheet_path": "./output",
        # 譜面輸出名稱
        "output_file_name": "output_sheet.txt",

        # 棄用，等待某天丟掉
        # # 用 get_boundart.py 轉換出來的圖，整體鍵盤的最左上邊界位置 (可用小畫家看)
        # # use get_boundart.py conversion video to an image
        # # in the image ,keyboard far left and far upper point position
        # "left_upper": [556, 113],
        # # 用 get_boundart.py 轉換出來的圖，整體鍵盤的最右下邊界位置 (可用小畫家看)
        # # use get_boundart.py conversion video to an image
        # # in the image ,keyboard far right and far lower point position
        # "right_lower": [1363, 578],

        # 開始分析時間
        "start_minute": 0,  # 只接受整數 # only integer
        "start_second": 1,  # 只接受整數 # only integer
        # 結束分析時間
        "end_minute": 1,  # 只接受整數 # only integer
        "end_second": 39,  # 只接受整數 # only integer

        # 鍵盤格式。通常是5*3，像是鋼琴，少數是4*2，像是鼓
        # keyboards format, like to piano is 5*3, and drum is 4*2
        # 目前只支援這2種格式("5*3", "4*2")
        # Currently only supports these 2 formats ("5*3", "4*2")
        "keyboards_X_format": 5,  # only 5 or 4
        "keyboards_y_format": 3,  # only 3 or 2
        # 選擇你要輸出的譜面格式，能用的格式在下面 "sheet_formats" 中
        # 如果不滿意預設格式可自己修改或新增
        # 改了之後記得修改 "output_sheet_format" 內容
        # choose output sheet format
        # Available formats are below "sheet_formats"
        # you can modify or add format
        # Remember to modify "output_sheet_format" after changing
        "output_sheet_format": "5_3_sheet_format_mode_2",
        "sheet_formats": {
            "5_3_sheet_format_mode_1": [
                1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
                11, 12, 13, 14, 15
            ],
            "5_3_sheet_format_mode_2": [
                'A1', 'A2', 'A3', 'A4', 'A5',
                'B1', 'B2', 'B3', 'B4', 'B5',
                'C1', 'C2', 'C3', 'C4', 'C5'
            ],
            "4_2_sheet_format_mode_1": [
                1, 2, 3, 4,
                5, 6, 7, 8
            ],
            "4_2_sheet_format_mode_2": [
                'A1', 'A2', 'A3', 'A4',
                'B1', 'B2', 'B3', 'B4'
            ]
        },

        # sync_symbol 同步符號，用於表示符號內是同時按的
        # in the sync_symbol note is simultaneously.
        # 8 4 5 【3 5】 6 6 4
        "sync_symbol": ["【", "】"],
        # 音符間的間隔符號
        # space between notes symbol
        # if "blank_symbol": ","
        # 8,4,5,【3 5】,6,6,4,
        "blank_symbol": " ",
        # 換行符號
        "line_feed_symbol": "\n",
        # 自動由低到高排序音符
        "auto_sort_sync_note": True,  # True False
        # 視為同步的時間區間
        # 單位 ms, unit ms
        "sync_area_time": 70,

        # 音符生成冷去時間 (單位 ms)
        # generate new note cool down time
        "cool_down_time": 330,

        # 譜面生成時，用於閥值的參數
        "trigger_valve_parameter": 2.5,

        # hsv邊界參數
        # hsv boundary parameter
        "hsv": {
            "lower_yellow": [0, 11, 89],
            "upper_yellow": [39, 89, 255],
            "lower_rad": [148, 10, 72],
            "upper_rad": [255, 150, 255]
        },

        # 二值化方法設定
        # set binarization method
        "binarization": {
            # 閥值
            "thresh": 127  # default 127
        },

        # 閉合方法設定
        # set closing
        "closing": {
            # 是否使用closing方法?
            # use closing?
            "use": False,  # True False
            # ⚠️這個我就不用動態生成了，麻煩...
            # 遮罩大小
            # kernel size
            # "kernel": [2, 2] # <- 沒作用 is not work
        },

        # 對於在使用 "4_play_sheet_video.py" 時的特效設定
        # set effect, when you use "4_play_sheet_video.py"
        "play_effect_config": {
            # 是否啟用鍵盤特效
            # use use_keyboard_effect
            "use_keyboard_effect": True,  # True False
            # 鍵盤特效方法
            # 目前有 "center"、"upper_left" 2種
            # keyboard effect
            # now have "center" and "upper_left"
            "keyboard_effect": "upper_left"
        }

    }


def logger_config():
    return {
        "logging_level": "INFO",  # DEBUG # INFO # ERROR # WARNING
        "log_file_path": './logs/Reverse-sheet-sky-children-of-the-light',
        "log_format": '%(asctime)s - %(levelname)s : %(message)s',
        "backupCount": 7,
        "when": 'D',
        "encoding": 'utf-8',
    }
