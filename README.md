# 물류관리 시스템

## 작품소개
물류관리 시스템은 프로세서인 Raspberry PI를 기반으로 IR센서, 화재 감지 센서, 물 감지 센서 등을 활용하여 효율적으로 창고를 관리하고 현장에서는 LCD와 Buzzer로 창고의 상태를 확인할 수 있다.

## 팀구성
H/W: 정승훈   
S/W: **이남웅**

## 개발기간
22. 06. 24. ~ 22. 09. 28.

## 사용한 부품
PI카메라: QR코드를 인식
DHT11 Sensor: 스토리지 온습도를 측정
Water Sensor: 물이 닿으면 센서가 작동
Gas Sensor: 가스가 근처에 발생할 경우 작동
Flame Sensor: 불이 근처에 있을 경우 센서가 작동
Buzzer: 재난 감지 센서 작동시 경보
LCD2004: 평시 스토리지 적재량과 온습도를 알려줌 / 재난 발생시 경고 문구 알림
TT Motor: 컨베이어 벨트를 조작하기 위해 양 끝단에 설치
MCP3008: Water Sensor와 같이 아날로그 신호를 받는 센서를 디지털 신호로 변환
IR Sensor: 컨베이어 벨트 위 물체를 인식
Servo Motor: 물체를 스토리지 별로 분류

## 동작방식
물류관리 시스템은 PI카메라를 통해 제품에 있는 바코드를 읽어 위치정보를 불러들여 제품이 있는 컨베이어 벨트가 작동하게 되고, 제품이 교차점에 도달하게 되면 교차점에 있는 IR센서가 제품 위치를 인식하게 되고, 제품을 이도시킬지 판별한다. PI카메라에서 바코드 인식을 못할 경우 Buzzer가 작동하여 경적음을 울린다.
만약 해당 교차점에서 이동하려고 하면 서브모터가 제품을 이동시키게 되고, 컨베이어 벨트에서 지정된 위치로 이동시키게 된다. 제품의 효율적 관리를 위해 Flame센서와 Gas센서, Water센서, 온습도 센서를 내장하게 되고 LCD와 Buzzer를 통해 물류창고 상태를 확인할 수 있다.

## 블록도
<img width="824" alt="image" src="https://github.com/namwlee99/logistics_management_system/assets/123155552/6d6c7c4e-d2ca-4e3c-8f4c-d260321d49e8">

## 회로도
![KakaoTalk_Photo_2023-06-25-16-59-58](https://github.com/namwlee99/logistics_management_system/assets/123155552/410ccaf1-d42c-47a2-957a-2a70ad10f449)


## 전면도
![KakaoTalk_Photo_2023-06-25-16-47-03](https://github.com/namwlee99/logistics_management_system/assets/123155552/e48b2da5-87a5-4a3a-a539-f853676af3a0)

## 작동영상
유튜브영상1
유튜브영상2
