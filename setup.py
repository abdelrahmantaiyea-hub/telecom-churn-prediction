from setuptools import find_packages, setup
from typing import List

# This is our 'Magic String' constant
HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    This function acts as the 'Bridge' between your Shopping List (requirements.txt)
    and the Project Identity (setup.py).
    '''
    requirements = []
    
    try:
        with open(file_path) as file_obj:
            # 1. Read all lines from the text file
            requirements = file_obj.readlines()
            
            # 2. Use list comprehension to remove the invisible '\n' (new line) 
            # characters that Python picks up when reading text files.
            requirements = [req.replace("\n", "") for req in requirements]

            # 3. The Filter: If '-e .' is in the list, we remove it.
            # We do this because '-e .' is a command for pip to RUN this setup.py,
            # and we don't want the setup.py to try to install itself as a library!
            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
                
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure it exists in the root directory.")

    return requirements

# This is the 'Ingredients Label' of your project
setup(
    name='Telecom_Churn_Project',          # The name of your 'Product'
    version='0.0.1',                       # Versioning for tracking updates
    author='Abdelrahman',                  # The lead engineer
    author_email='abdelrahmantaiyea@gmail.com', # Contact for the dev team
    packages=find_packages(),              # The 'Portal' that finds the 'src' folder (via __init__.py)
    install_requires=get_requirements('requirements.txt') # The 'Automatic Shopper'
)
