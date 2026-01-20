#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from std_msgs.msg import String

import cv2, json, numpy as np
from ultralytics import YOLO

import os

class AINode(Node):
    def __init__(self):
        super().__init__('ai_node')
        self.model = YOLO('yolov8n.pt') 
        self.publisher_ = self.create_publisher(String, 'vision_data', 10)
        
        home_dir = os.path.expanduser('~')
        video_path = os.path.join(home_dir, 'ros2_ws/src/my_robot_system/scripts/test_people.mp4')
        
        self.get_logger().info(f"영상 로드 시도: {video_path}")
        
        self.cap = cv2.VideoCapture(video_path)
        
        # 파일이 정상적으로 열렸는지 확인
        if not self.cap.isOpened():
            self.get_logger().error(f"영상 파일을 열 수 없습니다. 경로를 확인하세요: {video_path}")
        else:
            self.get_logger().info("영상 파일 로드 성공!")
            
        self.create_timer(0.1, self.run_ai)
        self.get_logger().info("Python AI 노드가 시작되었습니다.")

    def run_ai(self):
        ret, frame = self.cap.read()
        
        if not ret or frame is None:
            self.get_logger().warn('프레임 읽기 실패. 영상을 처음으로 되돌립니다.')
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        results = self.model.predict(frame, device='0', verbose=False)
        
        coords = []
        for box in results[0].boxes:
            if int(box.cls) == 0:
                x, y, w, h = box.xywh[0].tolist()
                coords.append({"x": round(x, 2), "y": round(y, 2)})

        msg = String()
        msg.data = json.dumps(coords)
        self.publisher_.publish(msg)
        
        if len(coords) > 0:
            self.get_logger().info(f"데이터 전송 중: {len(coords)}명 발견")

def main(args=None):
    rclpy.init(args=args)

    node = AINode() 
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()