功能說明

    場景設置：
        一個籃框（HOOP）位於高度 1.5 米，半徑 0.45 米。
        一個網（NET）作為傳感器，檢測球是否通過籃框。
        一個籃球（BALL）從高度 3 米自由落下，半徑 0.12 米，質量 0.625 千克。
        一個地板（FLOOR）防止球無限下落。
        一個顯示器（DISPLAY）顯示得分，初始為 0，每次球通過籃框加 2 分。
        一個監督者節點（SUPERVISOR）管理球的消失與重新生成。
    得分機制：
        當球通過 NET（傳感器區域）時，控制器檢測到並在 DISPLAY 上增加 2 分。
    球的重生：
        球通過籃框後，當其高度低於某個閾值（例如 0.5 米）時，監督者移除該球。
        同時在初始位置 (0, 3, 0) 生成一個新球，繼續下落。
    按鍵控制：
        按 p 暫停模擬（Webots 的時間步進停止）。
        按 q 終止模擬（退出 Webots）。
        按 s 恢復模擬（從暫停狀態繼續）。

控制器邏輯（概要）

由於 .wbt 文件本身不包含邏輯，需搭配一個控制器（例如 Python 腳本 basketball_controller.py）。以下是控制器應實現的功能：

    初始化：啟用鍵盤輸入、傳感器（NET）、顯示器（DISPLAY）。
    主循環：
        檢測球是否進入 NET（通過檢查球的坐標或傳感器觸發）。
        若進入，更新顯示器得分（+2）。
        監控球高度，若低於閾值，使用監督者 API 移除球並在 (0, 3, 0) 生成新球。
        監控鍵盤：
            p：暫停模擬（wb_supervisor_simulation_set_mode(WB_SUPERVISOR_SIMULATION_MODE_PAUSE)）。
            q：終止模擬（wb_supervisor_simulation_quit()）。
            s：恢復模擬（wb_supervisor_simulation_set_mode(WB_SUPERVISOR_SIMULATION_MODE_RUN)）。
    顯示器更新：使用 wb_display_draw_text 在顯示器上渲染當前得分。

使用方法

    將上述內容保存為 basketball.wbt。
    創建一個控制器文件（例如 basketball_controller.py），實現上述邏輯。
    在 Webots 中打開 basketball.wbt，確保控制器正確關聯到 SUPERVISOR 節點。
    運行模擬，觀察球下落、得分、消失與重生，並使用 p、q、s 鍵控制。