"""
1)Read Sample.py and find imported libraries
2)Find required Libraries from requirements.txt
3)Update requirements text file (For now requirements2.txt)
"""

def FindImport(file_path):                                  # To get Initial imports from sample.py

    with open(file_path, 'r') as file:
        first_lines=[]

        for line in file:
            line = line.strip()  # Remove leading/trailing spaces

            if line.startswith('import'):
                first_lines.append(line.split()[1])    # Only keep the library name in the list 

            elif line.startswith('from'):
                first_lines.append(line.split()[1])

    return first_lines


def FindreqLibraries(req,file_path):                    # To get library list from requirements.txt
    reqLibraries=[]
    libraries= FindImport(file_path)

    for lib in libraries:

        with open(req, 'r') as file2:
            line_number=0

            for line in file2:
                line_number+=1

                if (lib.lower())==(line[:len(lib)].lower()):   #Search if Library is there in requirements.txt

                    reqLibraries.append(line[:-1])             # [:-1] is used to remove the '\n' from the line variable

    return reqLibraries


def changereqfile(req2,req,file_path):

    with open(req2, 'w') as file3:
        liblist=FindreqLibraries(req,file_path)

        for i in range(0,len(liblist)):             # To Write into requirements2.txt line by line
            file3.writelines(liblist[i]+'\n')   


file_path = 'sample.py'
req='requirements.txt'
req2='requirements2.txt'

print(FindreqLibraries(req,file_path))           # To see library list

changereqfile(req2,req,file_path)                # To make final changes in requirements2.txt

print(FindImport(file_path))