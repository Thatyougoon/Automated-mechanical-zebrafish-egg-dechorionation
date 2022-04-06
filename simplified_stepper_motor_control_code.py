# Uses ticcmd to send and receive data from the Tic over USB.
# Works with either Python 2 or Python 3.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".
# 200 steps = 1 revolution 

import subprocess, yaml, time, numpy
 
def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))

def pos_in(i):
    print("current position is to: " + str(i))
    ticcmd('--exit-safe-start', '--position', str(i))
    return 

def pos_out():
    r = yaml.safe_load(ticcmd('-s', '--full'))['Current position']
    return r

def TX():
    return yaml.safe_load(ticcmd('-s', '--full'))['TX pin']['Digital reading']

def step_setting(): 
    step_mode = {
    'Full step': 1,'1/2 step': 2,'1/4 step': 4,'1/8 step': 8,
    '1/16 step': 16,'1/32 step': 32,'1/64 step': 64,
    '1/128 step': 128,'1/256 step': 256}
    return step_mode[yaml.load(ticcmd('-s', '--full'))['Step mode']]
    
def max_speed_in(speed,pitch):
    if speed > .1 or speed <= 0:
        exit()
    i =2000000000 * speed * step_setting() / pitch 
    print(i)
    ticcmd('--max-speed', str(int(i)))
    return

def max_accel_in(i):
    if i > 2147483647 or i <= 0:
        exit()
    
    print(i)
    ticcmd('--max-accel', str(int(i)))
    return

ticcmd('--exit-safe-start','--max-speed', str(200000000))

# std_vel = 2000000000 standard max velocity
# 200000.0000 pulses/s = 
# 200000 [pulses/s] * 1/step_mode [steps/pulses] * 1/200 [rev/steps] * pitch [mm/rev]
# 1000 * step_mode * pitch  [mm/s] = 1/step_mode * pitch  [m/s] = speed max 
# 2000000000 * x * step_mode / pitch  =  x [m/s]


# max max accerlation = 21474836.47 pulses/s^2
# to have the same accerlation everywhere, we have to consider the
# highest pitch ratio. This should leave enough dynamic range to equalize
# the accerlation for all. 


pitch_array = [1,12] # all the pitches in mm
pitch = pitch_array[1] # mm 
scaling =  pitch/(200*step_setting())
dia_tube = .8 # mm
dia_plunger = 8.5 # mm

# motor block will move backwards,be detected by sensor and move forward

Range = 37 #mm
buffer = 0 #mm
flow_speed = 4.23 * 2 ** (-3) # [0,1,2,3,4] m/s speed of flow in smallest tube, 
# not to confuse with the speed of the motor

speed = .01 # m/s. Max speed should be .01 m/s.  for the motor 
max_speed_in(speed,pitch)

#-----------------------------------------------------------------

max_accel_in( numpy.floor(2147483647*pitch)/max(pitch_array) )
margin_forward = int(Range/scaling)

if TX() == 1: #1 = no detection, 0 = detection
    max_speed_in(flow_speed * (dia_tube/dia_plunger)**2,pitch)
    pos_in(int(buffer/scaling)+pos_out())
    time.sleep(1)
    
time.sleep(1)
if TX() == 0: 
    print('Terminated program for safety')
    exit()
else:
    while TX() == 1:
        i = pos_out()- int(1.1*Range/scaling)
        pos_in(i)
        time.sleep(2)
        print("Setting target position to {}.".format(i))
    
print("Enter any symbol to start push")
input()
pos_in(margin_forward+pos_out())
time.sleep(3)

