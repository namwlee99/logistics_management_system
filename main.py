import sys
import time
import RPi.GPIO as GPIO
import cv2
import pyzbar.pyzbar as pyzbar
import pigpio
import dht11
import spidev
from multiprocessing import Process
from RPi_I2C_LCD_driver import RPi_I2C_driver

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

cap = cv2.VideoCapture(0)

motor1_pin = (16, 20, 21)                 #ENA, IN1, IN2
motor2_pin = (13, 19, 26)                    #IN3, IN4, ENB
GPIO.setup(motor1_pin, GPIO.OUT)
GPIO.setup(motor2_pin, GPIO.OUT)
pwm1 = GPIO.PWM(motor1_pin[0], 50)
pwm2 = GPIO.PWM(motor2_pin[2], 50)
pwm1.start(50)
pwm2.start(50)
motor_spe, motor_dur = 0, 0
motor_state = 0

ir_pin = (12)
GPIO.setup(ir_pin, GPIO.IN)
ir_sta = 0

pi = pigpio.pi()

buzzer_pin = (17)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, False)

lcd = RPi_I2C_driver.lcd(0x27)
lcd.clear()
lcd_celsius_symbol = (0b00111, 0b00101, 0b00111, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000)
crisis_string = ['', '', '', '']
state_temp = 0

dht11_pin = dht11.DHT11(pin = 18)
dht11 = dht11_pin.read()
dht11_state = [0, 0]

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 250000
spi_channel = (0)
flood_state = ''

flame_pin = (27)
GPIO.setup(flame_pin, GPIO.IN)
flame_state = 0

gas_pin = (22)
GPIO.setup(gas_pin, GPIO.IN)
gas_state = 0

object_list = ('1001', '1002', '1003')
object_num = [0, 0, 0, 0]                 #All Storage, First Storage, Second Storage, Third Storage
iden_obj = 0
object_order = []
print_text = ''

def motor_start(motor_spe):
    #모터 작동 함수
    pwm1.ChangeDutyCycle(motor_spe)
    pwm2.ChangeDutyCycle(motor_spe)
    GPIO.output(motor1_pin[1], True)
    GPIO.output(motor1_pin[2], False)
    GPIO.output(motor2_pin[0], True)
    GPIO.output(motor2_pin[1], False)
    
def motor_stop(motor_dur):
    #모터 정지 함수
    time.sleep(motor_dur)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
  
def buzzer(buzzer_num):
    #경고음 알림 함수
    for i in range(0, buzzer_num):
        GPIO.output(buzzer_pin, True)
        time.sleep(0.0625)
        GPIO.output(buzzer_pin, False)
        time.sleep(0.0625)
  
def flood():
    #Water Sensor 작동에 필요한 함수
    assert 0 <= spi_channel <= 0
        
    if spi_channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    r = spi.xfer2([1, cbyte, 0])
    
    return ((r[1] & 31) << 6) + (r[2] >> 2)

def motor_action(motor_state, iden_obj):
    #모터, 서보모터 작동 함수
    if motor_state == 1:
        motor_start(35)
    if not(GPIO.input(ir_pin)):
        if iden_obj == 1001:
            pi.set_servo_pulsewidth(25, 1600)    #1번 창고
        elif iden_obj == 1002:
            pi.set_servo_pulsewidth(25, 1250)    #2번 창고
        elif iden_obj == 1003:
            pi.set_servo_pulsewidth(25, 1000)    #3번 창고
        motor_start(80)
        motor_stop(3)
        pi.set_servo_pulsewidth(25, 1000)
        motor_state = 0
        return motor_state

def state_print(state_mode, crisis_string):
    #LCD 상태 출력 함수
    global dht11, dht11_state
    print("--------------------------------------------------")
    print("%s\n%s\n%s\n%s" % (crisis_string[0], crisis_string[1], crisis_string[2], crisis_string[3]))
    print(motor_state)
    if state_mode < 3:
        for i in range(0, 2):
            lcd.setCursor(0,i)
            lcd.print(crisis_string[i])
        for i in range(2, 3):
            lcd.setCursor(4,i)
            lcd.print(crisis_string[i])
        lcd.setCursor(4,3)
        lcd.print("Tem: %-3.1f" % dht11_state[0])
        lcd.createChar(0, lcd_celsius_symbol)
        lcd.setCursor(13,3)
        lcd.write(0)
        lcd.setCursor(14,3)
        lcd.print("C Hum: %d%%" % dht11_state[1])
            
    else:
        for i in range(0, 2):
            lcd.setCursor(0,i)
            lcd.print(crisis_string[i])
        for i in range(2, 4):
            lcd.setCursor(4,i)
            lcd.print(crisis_string[i])

def state_check(state_mode, print_text, flood_state, flame_state, gas_state):
    #상태 체크 및 출력 전처리 함수
    global dht11, dht11_state, motor_state
    if flood_state and flame_state and gas_state:                    #홍수 발생
        crisis_string[1] = '###### FLOOD #######'
        crisis_string[2] = '##### OUTBREAK #####'
    elif (not(flood_state)) and (not(flame_state)) and gas_state:    #화재 발생
        crisis_string[1] = '###### FLAME #######'
        crisis_string[2] = '##### OUTBREAK #####'
    elif (not(flood_state)) and flame_state and (not(gas_state)):    #가스 누출 발생
        crisis_string[1] = '####### GAS ########'
        crisis_string[2] = '####### LEAK #######'
    elif flood_state and (not(flame_state)) and gas_state:            #홍수, 화재 발생
        crisis_string[1] = '### FLOOD FLAME ####'
        crisis_string[2] = '##### OUTBREAK #####'
    elif flood_state and flame_state and (not(gas_state)):            #홍수, 가스 누출 발생
        crisis_string[1] = '## FLOOD OUTBREAK ##'
        crisis_string[2] = '##### GAS LEAK #####'  
    elif (not(flood_state)) and (not(flame_state)) and (not(gas_state)):    #화재, 가스 누출 발생
        crisis_string[1] = '## FLAME OUTBREAK ##'
        crisis_string[2] = '##### GAS LEAK #####'
    elif flood_state and (not(flame_state)) and (not(gas_state)):            #홍수, 화재, 가스 누출 발생
        crisis_string[1] = 'FLOOD FLAME OUTBREAK'
        crisis_string[2] = '##### GAS LEAK #####'
    else:
        if state_mode == 0  and (dht11.is_valid() and ((dht11_state[0] != dht11.temperature) or (dht11_state[1] != dht11.humidity))):
            #온습도가 갱신되었을 때
            crisis_string[0] = '  Camera is Ready   '
            crisis_string[1] = '1st St: %d 2st St: %d ' %(object_num[1], object_num[2])
            crisis_string[2] = '3st St: %d All St: %d ' %(object_num[3], object_num[0])
            crisis_string[3] = 'Tem: %-3.1f°C Hum: %d%%' % (dht11.temperature, dht11.humidity)
            dht11_state[0] = dht11.temperature
            dht11_state[1] = dht11.humidity
            state_print(state_mode, crisis_string)
        elif state_mode == 0 and crisis_string[0] != '  Camera is Ready   ':
            #창고 재고가 변경되었을 때
            crisis_string[0] = '  Camera is Ready   '
            crisis_string[1] = '1st St: %d 2st St: %d ' %(object_num[1], object_num[2])
            crisis_string[2] = '3st St: %d All St: %d ' %(object_num[3], object_num[0])
            crisis_string[3] = 'Tem: %-3.1f°C Hum: %d%%' % (dht11.temperature, dht11.humidity)
            dht11_state[0] = dht11.temperature
            dht11_state[1] = dht11.humidity
            state_print(state_mode, crisis_string)
        elif state_mode == 0 and motor_state == 1:
            #모터가 작동될 때
            crisis_string[0] = '    Motor   Move     '
            crisis_string[1] = '1st St: %d 2st St: %d ' %(object_num[1], object_num[2])
            crisis_string[2] = '3st St: %d All St: %d ' %(object_num[3], object_num[0])
            crisis_string[3] = 'Tem: %-3.1f°C Hum: %d%%' % (dht11.temperature, dht11.humidity)
            dht11_state[0] = dht11.temperature
            dht11_state[1] = dht11.humidity
            state_print(state_mode, crisis_string)   
        elif state_mode > 0:
            #QR코드가 인식되었을 때
            crisis_string[0] = str(print_text)
            crisis_string[1] = '1st St: %d 2st St: %d ' %(object_num[1], object_num[2])
            crisis_string[2] = '3st St: %d All St: %d ' %(object_num[3], object_num[0])
            if dht11.is_valid() and ((dht11_state[0] != dht11.temperature) or (dht11_state[1] != dht11.humidity)):
                crisis_string[3] = 'Tem: %-3.1f°C Hum: %d%%' % (dht11.temperature, dht11.humidity)
                dht11_state[0] = dht11.temperature
                dht11_state[1] = dht11.humidity
            state_print(state_mode, crisis_string)
            buzzer(state_mode)
        
    if flood_state or (not(flame_state)) or (not(gas_state)):
        #재난 상황 발생시 경고 문고
        crisis_string[0] = '########## WARNING #'
        crisis_string[3] = '# WARNING ##########'
        state_print(5, crisis_string)
        buzzer(3)
        crisis_string[0] = '# WARNING ##########'
        crisis_string[3] = '########## WARNING #'
        state_print(5, crisis_string)
            
    dht11 = dht11_pin.read()
        
def main():
    global iden_obj
    motor_state = 0
    pi.set_servo_pulsewidth(25, 1000)
    while(cap.isOpened()):
            ret, img = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
            decoded = pyzbar.decode(gray)
            
            flood_state = (flood() > 100)        
            flame_state = GPIO.input(flame_pin)
            gas_state = GPIO.input(gas_pin)
            
            state_check_p=Process(target=state_check(0, 0, flood_state, flame_state, gas_state))
            state_check_p.start()
            
            motor_action_p=Process(target=motor_action(motor_state, iden_obj))
            motor_state = motor_action_p.start()
            
            for d in decoded: 
                x, y, w, h = d.rect
                if not((flood_state)) and flame_state and gas_state:
                    if (d.data.decode('utf-8') == object_list[0]) and (object_num[1] < 3) and (object_num[0] < 9):
                        #첫번째 창고 QR코드가 찍혔을 때
                        object_num[1] += 1
                        iden_obj = int(d.data.decode('utf-8'))
                        print_text = '   First Storage    '
                        object_num[0] = object_num[1] + object_num[2] + object_num[3]
                        state_check_p=Process(target=state_check(1, print_text, 0, 1, 1))
                        state_check_p.start()
                        motor_state = 1
                        cap.release()
                        time.sleep(1.5)
                        cap.open(0)
        
                    elif (d.data.decode('utf-8') == object_list[1]) and (object_num[2] < 3) and (object_num[0] < 9):
                        #두번째 창고 QR코드가 찍혔을 때
                        object_num[2] += 1
                        iden_obj = int(d.data.decode('utf-8'))
                        print_text = '   Second Storage   '
                        object_num[0] = object_num[1] + object_num[2] + object_num[3]
                        state_check_p=Process(target=state_check(1, print_text, 0, 1, 1))
                        state_check_p.start()
                        motor_state = 1
                        cap.release()
                        time.sleep(1.5)
                        cap.open(0)
        
                    elif (d.data.decode('utf-8') == object_list[2]) and (object_num[3] < 3) and (object_num[0] < 9):
                        #세번째 창고 QR코드가 찍혔을 때
                        object_num[3] += 1
                        iden_obj = int(d.data.decode('utf-8'))
                        print_text = '   Third Storage    '
                        object_num[0] = object_num[1] + object_num[2] + object_num[3]
                        state_check_p=Process(target=state_check(1, print_text, 0, 1, 1))
                        state_check_p.start()
                        motor_state = 1
                        cap.release()
                        time.sleep(1.5)
                        cap.open(0)
       
                    elif ((d.data.decode('utf-8') == object_list[0]) or (d.data.decode('utf-8') == object_list[1]) or (d.data.decode('utf-8') == object_list[2])) and \
                         (object_num[0] == 9):
                        #물건이 초과되었을 때
                        print_text = '    Object Over     '
                        object_num[0] = object_num[1] + object_num[2] + object_num[3]
                        state_check_p=Process(target=state_check(2, print_text, 0, 1, 1))
                        state_check_p.start()
                        cap.release()
                        time.sleep(1.5)
                        cap.open(0) 
       
                    elif ((d.data.decode('utf-8') == object_list[0]) or (d.data.decode('utf-8') == object_list[1]) or (d.data.decode('utf-8') == object_list[2])) and \
                         ((object_num[1] == 3) or (object_num[2] == 3) or (object_num[3] == 3)):
                        #창고가 꽉찼을 때
                        print_text = '  Storage is full   '
                        object_num[0] = object_num[1] + object_num[2] + object_num[3]
                        state_check_p=Process(target=state_check(2, print_text, 0, 1, 1))
                        state_check_p.start()
                        cap.release()
                        time.sleep(1.5)
                        cap.open(0)
        
                    else:
                        #잘못된 QR코드가 찍혔을 때
                        print_text = '    Wrong QR code   '
                        object_num[0] = object_num[1] + object_num[2] + object_num[3]
                        state_check_p=Process(target=state_check(2, print_text, 0, 1, 1))
                        state_check_p.start()
                        cap.release()
                        time.sleep(1.5)
                        cap.open(0)
                    
try:
    motor_stop(0)                    #모터 초기화
    main_p=Process(target=main())
    main_p.start()
    
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllWindows()
    lcd.clear()
    spi.close() 
    print("--------------------------------------------------\nSystem Shutdown\n--------------------------------------------------")
    sys.exit(0)
