import requests


def check_pincode(pincode, emp_id, backend_url):
    payload = {
        'emp_id': emp_id,
        'image': pincode
    }

    try:
        response = requests.post(backend_url, json=payload)

        if response.status_code == 200:
            result = response.json()
            status = result.get('Status')

            if status == True:
                return True
            if status == False:
                return False
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")