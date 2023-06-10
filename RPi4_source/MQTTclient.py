##################################################
# REF: https://github.com/jiteshsaini/mqtt-demo/
##################################################

import time
import paho.mqtt.client as mqtt

class MQTTclient():
	
	def __init__(self, client_name):
		self.client = mqtt.Client(client_name)
		# states for checking sent from pub and recv by sub
		self.is_sent = 0
		self.is_recv = 0
		
	############### PUBLISHER ###############
	
	def on_publish(self, client, userdata, mid):
		print("message published")
	
	def publish(self, topic='rpi/broadcast', msg=''):
		self.client.on_publish = self.on_publish
		self.client.connect('127.0.0.1', 1883)
		self.client.loop_start()
		# test code
		# k = "5"
		while True:
			# k = k + 1
			# if (k > 20):
				# k = 1
			try:
				# msg = str(k)
				pub_msg = self.client.publish(	topic=topic, 
												payload=msg.encode('utf-8'), 
												qos=0,	)
				pub_msg.wait_for_publish()
				# print(pub_msg.is_published())
				if (pub_msg.is_published() == True):
					self.is_sent = 1
					# time.sleep(60)
					break
			except Exception as e:
				print(e)
			time.sleep(2)
	
	############### SUBSCRIBER ###############
	
	def on_connect(self, client, userdata, flags, rc):
		global flag_connected
		flag_connected = 1
		# self.client_subscriptions(client)
		print("Connected to MQTT server")
	
	def on_disconnect(self, client, userdata, rc):
		global flag_connected
		flag_connected = 0
		print("Disconnected from MQTT server")
	
	def sub_callback(self, client, userdata, msg):
		print(str(msg.payload.decode('utf-8')))
		self.is_recv = 1
	
	def client_subscriptions(self, client, topic):
		client.subscribe(topic)
		# client.subscribe("rpi/broadcast")
		
	def subscribe(self, topic='rpi/broadcast'):
		flag_connected = 0
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.message_callback_add(topic, self.sub_callback)
		self.client.connect('127.0.0.1', 1883)
		self.client.loop_start()
		self.client_subscriptions(self.client, topic)
		print("...Client set up complete...")
		# test code
		while True:
			time.sleep(3)
			if (self.is_recv == 1):
				print("Received!!!")
				break
        
