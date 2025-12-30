import QtQuick 2.15
import QtQuick.Controls 2.15

Window {
    width: 400
    height: 300
    visible: true
    title: "QML 範例"

    Rectangle {
        id: myRect
        width: 150; height: 150
        color: "blue"
        anchors.centerIn: parent
        radius: 10

        // 點擊事件處理
        MouseArea {
            anchors.fill: parent
            onClicked: {
                myRect.color = (myRect.color == "#0000ff" ? "red" : "blue")
            }
        }

        // 定義屬性動畫
        Behavior on color {
            ColorAnimation { duration: 500 }
        }
        
        Text {
            text: "點擊我"
            anchors.centerIn: parent
            color: "white"
        }
    }
}
