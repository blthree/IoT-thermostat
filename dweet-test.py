from Adafruit_IO import Client

aio = Client('14737421b335461c9a194995f9b537af')
aio.send('photocell', 'ON')
