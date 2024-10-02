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
                    first_lines.append(line.strip()[7:])
                else:  # Exclude lines with 'import'
                    break
        return first_lines


def findreqlines(req):
    a=[]
    libraries= findimport(file_path)
    for lib in libraries:
        with open(req, 'r') as file2:
            line_number=0
            for line in file2:
                line_number+=1
                # print(i,line[:len(i)])
                if (lib.lower())==(line[:len(lib)].lower()):
                    a.append(line_number)
    return a

print(findreqlines(req))

    
                    
                    
                    