"""
Read Sample.py and find imported libraries
Find required Libraries from requirements.txt
"""

file_path = 'sample.py'
req='requirements.txt'

def findimport(file_path):

    with open(file_path, 'r') as file:
        first_lines=[]

        for line in file:
                if 'import' in line:
                    first_lines.append(line.strip()[7:]) #only keep library name in list (remove 'import ')
                else: 
                    break 

    return first_lines


def findreqlines(req):
    reqlines=[]
    libraries= findimport(file_path)

    for lib in libraries:

        with open(req, 'r') as file2:
            line_number=0

            for line in file2:
                line_number+=1
                if (lib.lower())==(line[:len(lib)].lower()):  #Search if Library is there in requirements.txt
                    reqlines.append(line_number)
                    
    return reqlines

print(findreqlines(req))

    
                    
                    
                    