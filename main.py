import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json
import atexit


class MQTT:
	def __init__(self):
		self.ip = '116.62.153.244'
		self.port = 1883
		pins = [29, 38]
		GPIO.setmode(GPIO.BOARD)
		for pin in range(pins[0], pins[1], 2):
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, GPIO.LOW)
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message

	def on_connect(self, client, userdata, flags, rc):
		print("Connected with result code" + str(rc))
		self.client.subscribe("gpio")

	def on_message(self, client, userdata, msg):
		print(msg.topic + " " + str(msg.payload))
		gpio = json.loads(bytes(msg.payload).decode('utf-8'))
		key = False
		for item in gpio.items():
			if item[0] == 'pin':
				key = True
		if key:
			if gpio['value'] == 0:
				GPIO.output(gpio['pin'], GPIO.LOW)
			else:
				GPIO.output(gpio['pin'], GPIO.HIGH)

	def mqtt_connect(self):
		self.client.connect(self.ip, self.port, 60)
		self.client.loop_forever()


if __name__ == '__main__':
	atexit.register(GPIO.cleanup)
	m = MQTT()
	m.mqtt_connect()
