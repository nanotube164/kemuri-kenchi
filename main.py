from mox.smoke_detection import Detector as dt
import time

index = 0
run = dt.smoke_detection()
while run:
    run = dt.smoke_detection()
    #time.sleep(1)