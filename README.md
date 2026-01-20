# 🤖 ROS 2 Humble AI-Control Hybrid System

**Windows 11 (WSL 2)** 환경에서 **YOLOv8** 기반의 Python AI 노드와 **C++** 제어 노드 간의 하이브리드 통신을 테스트한 프로젝트. DDS 통신, AI 추론 가속, C++ 노드 설계를 기반으로 테스트 진행.

---

## 1. 개요 (Overview)
- **AI Node (Python):** YOLOv8 모델을 사용하여 영상 내 사람을 감지하고 좌표를 JSON으로 발행.
- **Control Node (C++):** 발행된 토픽을 구독(Subscribe)하여 실시간으로 위험 상황을 판단하고 제어 로그 출력.
---

## 2. 개발 환경 구축 (Environment Setup)

### 2.1 Windows 및 WSL 2 설정
1. **WSL 2 설치:** 터미널(PowerShell)을 관리자 권한으로 실행.
   ```powershell
   wsl --install -d Ubuntu-22.04
2. GPU 드라이버: Windows에 최신 NVIDIA 드라이버가 설치되어 있어야 WSL 내 GPU 가속 가능.

### 2.2 ROS 2 Humble 설치 (Ubuntu 22.04)
  ```bash
  # 리포지토리 설정 및 설치
  sudo apt update && sudo apt install curl gnupg2 lsb-release -y
  sudo curl -sSL [https://raw.githubusercontent.com/ros/rosdistro/master/ros.key](https://raw.githubusercontent.com/ros/rosdistro/master/ros.key) -o /usr/share/keyrings/ros-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] [http://packages.ros.org/ros2/ubuntu](http://packages.ros.org/ros2/ubuntu) $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
  
  sudo apt update
  sudo apt install ros-humble-desktop -y
  
  # 환경 변수 설정
  echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
  source ~/.bashrc
  ```

### 2.3 필수 의존성 설치
  ```bash
  sudo apt install python3-pip python3-colcon-common-extensions -y
  sudo apt install ffmpeg libsm6 libxext6 -y 
  pip3 install ultralytics opencv-python-headless numpy
  ```

## 3. 테스트 및 시뮬레이션 (Simulation)
카메라 하드웨어 없이도 로직을 검증할 수 있도록 동영상 파일 테스트 환경을 추가.

### 3.1 테스트 데이터 준비
  ```bash
  mkdir -p ~/ros2_ws/src/my_robot_system/scripts
  cd ~/ros2_ws/src/my_robot_system/scripts
  # 테스트용 샘플 영상 다운로드
  wget -O test_people.mp4 [https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4](https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4)
  ```

### 3.2 시뮬레이션 가동
ai_node.py에서 위 영상 파일의 절대 경로를 로드하여 AI 추론 및 데이터 발행.

## 4. 빌드 및 실행 (Build & Run)

### 4.1 워크스페이스 빌드
  ```bash
  cd ~/ros2_ws
  colcon build --packages-select my_robot_system
  source install/setup.bash
  ```

### 4.2 노드 실행
- Terminal 1 (AI Node): ros2 run my_robot_system ai_node.py
- Terminal 2 (Control Node): ros2 run my_robot_system control_node
- 통신 확인: rqt_graph 명령어로 노드 간 연결 상태를 시각화하여 확인 가능.

## 5. 최종 시뮬레이션 결과
시뮬레이션 가동 화면: Python 노드의 추론 데이터 전송 및 C++ 노드의 실시간 로그 수신 상황을 확인.
<img width="2559" height="1391" alt="wsl_linux_yolo_ros2_test" src="https://github.com/user-attachments/assets/2e1126e7-73a3-470e-879b-7968294f3677" />





