import os
from components import fingerprint, keypad, camera
from active_mode import send_request

security_level = os.getenv('SECURITY_LEVEL')


def attendance_handler():
    print('Level1')
    emp_id, state = camera.capture_face_detection()
    if state == True and emp_id != 0:
        print('Attendance Marked for emp_id:', emp_id)

        if security_level == 'level2':
            print('Taking Fingerprint...')
            fp_id, state = fingerprint.find_print()
            if not state:
                print('Fingerprint is not match...')
                print('Door Unlock Failed!')
            elif state:
                if fp_id == emp_id:
                    print('Fingerprint correct')
                    print('Door Unlocked!')

        elif security_level == 'level3':
            print('Taking Fingerprint...')
            fp_id, state = fingerprint.find_print()
            if not state:
                print('Fingerprint is not match...')
                print('Door Unlock Failed!')
            elif state:
                if fp_id == emp_id:
                    print('Fingerprint correct')
                    print('Entre the pincode...')

                    ent_pincode = keypad.get_pin()
                    url = 'https://face-secure.azurewebsites.net/attendanceManagement/check-pin/'
                    state = send_request.check_pincode(ent_pincode, emp_id, url)
                    if state == True:
                        print('Pincode Correct...!')
                        print('Door Unlocked!')
                    elif state == False:
                        print('Pincode Not Correct...!')
                        print('Door Unlock Failed')
    else:
        print('Attendance Marked unsuccessfully')
