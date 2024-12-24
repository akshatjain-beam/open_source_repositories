import os
import shutil

def create_feature_structure(parent_folder_name, language):
    # Define the parent folder path
    parent_folder_path = os.path.join(os.getcwd(), parent_folder_name)

    # Create the parent folder if it doesn't exist
    os.makedirs(parent_folder_path, exist_ok=True)

    # Define the features folder path
    features_folder = os.path.join(parent_folder_path, 'features')
    os.makedirs(features_folder, exist_ok=True)

    # Determine the next feature number
    feature_number = 1
    while True:
        feature_folder_name = f'feature_{feature_number}'
        feature_folder_path = os.path.join(features_folder, feature_folder_name)
        if not os.path.exists(feature_folder_path):
            os.makedirs(feature_folder_path)
            break
        feature_number += 1

    # Determine file extensions based on the selected language
    if language.lower() == 'python':
        file_extension = '.py'
    elif language.lower() == 'go':
        file_extension = '.go'
    else:
        print(f"Unsupported language '{language}'. Defaulting to Python (.py).")
        file_extension = '.py'

    # List of files to create with the appropriate extension
    files_to_create = [
        f'with_hole{file_extension}',
        f'with_golden_solution{file_extension}',
        f'with_flawed_solution{file_extension}',
        'holder_and_prompt.txt',
        'flawed_solution_failure_reason.txt'
    ]

    # Create test_images folder
    test_images_path = os.path.join(feature_folder_path, 'test_images')
    
    try:
        os.makedirs(test_images_path)

        # Create specified files with the correct extensions
        for file_name in files_to_create:
            file_path = os.path.join(feature_folder_path, file_name)
            open(file_path, 'w').close()  # Create an empty file

        print(f"Created folder structure in: {feature_folder_path}")

    except Exception as e:
        # Rollback by deleting the feature folder if an error occurs
        shutil.rmtree(feature_folder_path, ignore_errors=True)
        print(f"Error occurred: {e}. Changes have been rolled back.")

# Example usage
nested_folder_name = input("Enter the name of the nested folder: ")
language = input("Enter the programming language (python/go): ").strip()
create_feature_structure(nested_folder_name, language)
