from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    This function acts as the 'Bridge' between (requirements.txt)
    and the Project Identity (setup.py).
    '''
    requirements = []
    
    try:
        with open(file_path) as file_obj:
            # 1. Read all lines from the text file
            requirements = file_obj.readlines()
            
            # to remove characters that Python picks up when reading text files.
            requirements = [req.strip() for req in requirements]

            
            # and we don't want the setup.py to try to install itself as a library!
            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
                
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure it exists in the root directory.")

    return requirements

# This is the 'Ingredients Label
setup(
    name='Telecom_Churn_Project',          
    version='0.0.1',                       
    author='Abdelrahman',                  
    author_email='abdelrahmantaiyea@gmail.com', # Contact 
    packages=find_packages(),              # this finds the 'src' folder (via __init__.py)
    install_requires=get_requirements('requirements.txt') # The 'Automatic Shopper'
)
