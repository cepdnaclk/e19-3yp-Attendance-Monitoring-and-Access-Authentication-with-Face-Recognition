import os


def create_folder(folder_name):

    if folder_name:
        script_path = os.path.abspath(__file__)  # Get the absolute path of the script
        root_path = os.path.dirname(os.path.dirname(script_path))  # Navigate up one level to the project root
        fr_path = os.path.join(root_path, "face_detection")
        datasets_path = os.path.join(fr_path, "datasets")
        folder_path = os.path.join(datasets_path, folder_name)

        # Check if the folder exists
        if not os.path.exists(folder_path):
            # If the folder doesn't exist, create it
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created in 'face_detection' folder.")
        else:
            print(f"Folder '{folder_name}' already exists in 'face_detection/datasets' folder.")
    else:
        print("Invalid or missing folder name in the JSON payload.")