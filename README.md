# 물류관리 시스템

## 작품소개
이 작품은 물류관리 시스템으로, Raspberry Pi 프로세서를 기반으로 개발되었습니다. 시스템은 IR 센서, 화재 감지 센서, 물 감지 센서 등을 활용하여 창고를 효율적으로 관리할 수 있습니다. 현장에서는 LCD와 Buzzer를 사용하여 창고의 상태를 실시간으로 확인할 수 있습니다. 이 시스템은 물류 작업 환경에서 보다 효율적인 창고 관리를 지원하며, 사고나 이상 상황을 신속하게 감지하여 조치할 수 있도록 도와줍니다.

## 팀구성
아이디어 제안 및 기획: **이남웅**   
하드웨어 설계 및 구현: 정승훈   
소프트웨어 개발: **이남웅**   
디자인: 정승훈   
시스템 통합 및 테스트: **이남웅**   

## 개발기간
2022/06/24 ~ 2022/09/28

## 사용한 부품
PI 카메라: QR 코드를 식별하여 인식할 수 있는 카메라입니다. 이를 통해 물류 작업에서 중요한 정보를 자동으로 인식하고 처리할 수 있습니다.   
DHT11 센서: 창고의 온도와 습도를 측정하는 센서입니다. 스토리지의 적절한 환경을 유지하기 위해 사용됩니다.
Water Sensor: 물이 센서에 닿으면 작동하는 센서입니다. 누수나 수위 변화를 신속하게 감지하여 관련 문제를 예방하거나 조치할 수 있습니다.   
Gas Sensor: 가스가 근처에 발생할 경우 작동하는 센서입니다. 유해 가스 누출을 신속하게 감지하여 안전에 기여합니다.   
Flame Sensor: 불이 근처에 있을 경우 작동하는 센서입니다. 화재를 조기에 감지하고 경보를 울리거나 조치를 취할 수 있습니다.   
Buzzer: 재난 감지 센서가 작동할 경우 경보를 발생시키는 소리 알림 장치입니다.   
LCD2004: 스토리지의 적재량, 온습도 등의 정보를 표시하는 20x4 문자 LCD입니다. 또한 재난 상황 발생 시 경고 메시지를 표시하여 시각적으로 알릴 수 있습니다.   
TT Motor: 컨베이어 벨트를 조작하기 위해 양 끝단에 설치된 모터입니다. 스토리지 내 물체를 분류하고 이동시키는 역할을 합니다.   
MCP3008: 아날로그 신호를 디지털 신호로 변환해주는 ADC(Analog-to-Digital Converter) 칩입니다.    Water Sensor와 같이 아날로그 입력을 받아서 Raspberry Pi가 처리할 수 있는 디지털 신호로 변환합니다.   
IR Sensor: 컨베이어 벨트 위에 있는 물체를 감지하는 인프라레드(IR) 센서입니다. 물체의 존재를 신속하게 감지하여 작업 프로세스를 제어하거나 인식에 활용할 수 있습니다.   
Servo Motor: 스토리지 내 물체를 분류하기 위해 사용되는 모터입니다. 스토리지 별로 물체를 이동시키거나 배치할 수 있습니다.   

## 동작방식
1. PI 카메라를 통한 바코드 인식: PI 카메라는 제품에 있는 바코드를 인식하여 위치 정보를 가져옵니다. 이 정보를 기반으로 해당 제품이 위치한 컨베이어 벨트가 작동하게 됩니다. 만약 PI 카메라가 바코드를 인식하지 못할 경우 Buzzer가 작동하여 경고음을 울립니다.   
2. IR 센서를 통한 위치 인식: 제품이 교차점에 도달하면 교차점에 있는 IR 센서가 제품의 위치를 감지하여 인식합니다. 이를 통해 제품을 이동시킬지 여부를 판별합니다.   
3. 서브모터를 이용한 제품 이동: 해당 교차점에서 제품을 이동해야 할 경우, 서브모터가 작동하여 제품을 원하는 위치로 이동시킵니다. 이를 통해 제품의 효율적인 관리와 분류가 가능해집니다.   
4. 센서 내장 및 상태 확인: 시스템은 Flame 센서, Gas 센서, Water 센서, 온습도 센서 등을 내장하여 제품의 안전 및 환경 상태를 모니터링합니다. LCD와 Buzzer를 통해 물류창고의 상태를 실시간으로 확인할 수 있습니다.

물류관리 시스템은 PI 카메라를 통해 바코드 인식과 위치 정보를 활용하고, IR 센서와 서브모터를 이용하여 제품의 이동을 제어합니다. 또한 센서를 통해 환경 및 안전 상태를 모니터링하며, LCD와 Buzzer를 통해 사용자에게 정보를 제공합니다.

## 블록도
<img width="768" alt="image" src="https://github.com/namwlee99/logistics_management_system/assets/123155552/e7ba58fe-69ec-4378-99d4-6f4615f3e3cb">


## 회로도
![KakaoTalk_Photo_2023-07-02-10-03-41](https://github.com/namwlee99/logistics_management_system/assets/123155552/1fdc1679-29d2-47a5-b8c3-d5961d5cff7e)


## 사진
![KakaoTalk_Photo_2023-06-25-16-47-12](https://github.com/namwlee99/logistics_management_system/assets/123155552/987fcad2-236b-4408-970e-6b779f5ea6cc)


## 작동 동영상
[![Watch the video](https://img.youtube.com/vi/YHekVKBjydo/0.jpg)](https://youtu.be/YHekVKBjydo)
