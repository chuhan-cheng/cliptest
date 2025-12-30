import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 400
    title: "PyQt5 + QML 動畫範例"

    

    Rectangle {
        id: root
        anchors.fill: parent
        color: "#bf3b3bff"

        // 定義一個圓形
        Rectangle {
            id: ball
            width: 70
            height: 70
            color: "blue"
            radius: width / 2
            x: 50
            y: 50

            // 屬性動畫：當 x 座標改變時觸發平滑移動
            Behavior on x {
                NumberAnimation { duration: 600; easing.type: Easing.OutBounce }
            }

            // 屬性動畫：當顏色改變時觸發漸變
            Behavior on color {
                ColorAnimation { duration: 600 }
            }
        }

        // 滑鼠點擊區域
        MouseArea {
            anchors.fill: parent
            onClicked: {
                // 點擊後隨機改變位置與顏色
                ball.x = Math.random() * (root.width - ball.width)
                ball.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
            }
        }

        Text {
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 30
            text: "點擊視窗任意處觸發動畫"
            font.pixelSize: 16
            color: "#666"
        }

        Column {
            anchors.centerIn: parent
            spacing: 20

            TextField {
                id: inputField
                width: parent.width
                placeholderText: "在此輸入文字並按 Enter..."
                focus: true  // 程式開啟時自動聚焦
                
                // 核心：當按下 Enter 鍵時觸發
                onAccepted: {
                    backend.handleInput(inputField.text)
                    // 可選：按下後清空輸入框
                    // inputField.text = ""
                }
            }

            Button {
                text: "點我印出訊息"
                onClicked: {
                    // 直接呼叫 Python 的函數
                    backend.printMessage("哈囉 Python！")
                }
            }

            Button {
                text: "執行後端邏輯"
                onClicked: {
                    backend.doSomething()
                }
            }
        }
    }
}
