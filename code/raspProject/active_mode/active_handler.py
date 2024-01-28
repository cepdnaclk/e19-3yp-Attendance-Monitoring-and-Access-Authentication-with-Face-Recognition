import os
from components import fingerprint, keypad, camera, doorlock
from active_mode import send_request

from dotenv import load_dotenv, set_key

# Adjust the path to point to the root folder
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

security_level = os.environ.get('SECURITY_LEVEL')

def attendance_handler(queue):
    print('Level1')
    emp_id, state = camera.capture_face_detection()
    
    if emp_id == 'Unknown':
        print('Attendance Marked Unsuccessfull!')
        queue.put('Not Registered')
        return
    
    if state == True and emp_id != 0:
        print('Attendance Marked for emp_id:', emp_id)
        queue.put('Attendence Marked')
        

        if security_level == 'level2':
            print('Taking Fingerprint...')
            queue.put('Enter The Fingerprint...')
            fp_id, state = fingerprint.find_print()
            if not state:
                queue.put('No Match')
                print('Fingerprint is not match...')
                print('Door Unlock Failed!')
            elif state:
                if int(fp_id) == int(emp_id):
                    queue.put('Fingerprint correct')
                    print('Fingerprint correct')
                    doorlock.open_lock(queue)

        elif security_level == 'level3':
            print('Enter The Fingerprint...')
            queue.put('Taking Fingerprint...')
            fp_id, state = fingerprint.find_print()
            print(fp_id, state)
            if state == False:
                queue.put('No Match')
                print('Fingerprint is not match...')
                print('Door Unlock Failed!')
            elif state == True:
                if int(fp_id) == int(emp_id):
                    print('Fingerprint Identified')
                    print('Entre the pincode...')
                    queue.put('Fingerprint Identified')
                    queue.put('Enter Pincode')

                    ent_pincode = keypad.get_pin()
                    url = 'https://facesecure.azurewebsites.net/attendanceManagement/check-pin/'
                    state = send_request.check_pincode(ent_pincode, emp_id, url)
                    print(state)
                    if state == True:
                        print('Pincode Is Correct...!')
                        doorlock.open_lock(queue)
                        
                    elif state == False:
                        print('Pincode Is Not Correct...!')
                        print('Door Unlock Failed')
                        queue.put('Pincode Is Not Correct...! Door Unlock Failed!')
    else:
        print('Attendance Marked unsuccessfully')
        queue.put('Unsuccessful')
