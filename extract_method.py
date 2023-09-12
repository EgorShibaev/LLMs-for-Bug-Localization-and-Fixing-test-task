import os
import re
import sys

def extract_method_code(repository_path: str, full_method_name: str, language: str) -> str:
    """
    Extracts the code of the method with the given name from the repository
    :param repository_path: path to the repository
    :param method_name: name of the method to extract
    :param language: language of the method - java or kotlin
    :return: code of the method
    """
    if language == "java":
        # in case of java there is only one file 
        # that can contain the method - the file with the same name as the class
        # so we can just find function with the given name in the file with the same name as the class
        package, class_name, method_name = full_method_name.rsplit(".", 2)
        package_path = package.replace(".", os.path.sep)
        file_path = os.path.join(repository_path, "src", "main", language, package_path, f"{class_name}.java")

        with open(file_path, "r") as file:
            content = file.read()

        method_code = extract_method_code_from_code(content, method_name, language)
        return method_code
    else: # kotlin
        # first case package.class.method - function is method of some class
        if full_method_name.count(".") >= 2:
            package, class_name, method_name = full_method_name.rsplit(".", 2)
        elif full_method_name.count(".") == 1:
            class_name, method_name = full_method_name.rsplit(".", 1)
            package = ""
        package_path = package.replace(".", os.path.sep)
        file_path = os.path.join(repository_path, "src", "main", language, package_path)
        for file in os.listdir(file_path):
            if file.endswith(".kt"):
                with open(os.path.join(file_path, file), "r") as f:
                    content = f.read()
                
                # find the class inside the content
                class_pattern = re.compile(rf"class\s+{class_name}")
                match = class_pattern.search(content)
                if not match:
                    continue
                # extract the code of the class
                class_code = extract_code_block(content, match.start())[0]
                # when we found class we know for sure that the method is inside this class
                method_code = extract_method_code_from_code(class_code, method_name, language)
                return method_code
        
        # second case package.method - function is method of some file

        if full_method_name.count(".") >= 1:
            package, method_name = full_method_name.rsplit(".", 1)
        else:
            package = ""
            method_name = full_method_name

        package_path = package.replace(".", os.path.sep)
        file_path = os.path.join(repository_path, "src", "main", language, package_path)
        for file in os.listdir(file_path):

            if file.endswith(".kt"):
                with open(os.path.join(file_path, file), "r") as f:
                    content = f.read()
                # now we should not look inside the classes because 
                # we are looking for method outside any class
                # so content of each class is deleted from the code

                # find all classes inside the content
                class_pattern = re.compile(rf"\s+class\s+")
            
                match = class_pattern.search(content)
                while match != None:
                    # extract the code of the class
                    class_code, end_position = extract_code_block(content, match.start())
                    content = content[:match.start()] + content[end_position:]

                    match = class_pattern.search(content)

                # find the method inside the content without classes
                method_code = extract_method_code_from_code(content, method_name, language)
                if method_code != None:
                    return method_code
        return None


def extract_method_code_from_code(code, method_name, language):
    """
    Extracts the code of the method with the given name from the Java code
    :param code: Java or Kotlin code
    :param method_name: name of the method to extract
    :param language: language of the method - java or kotlin
    :return: code of the method
    """

    if language == "java":
        method_pattern = re.compile(rf"\n\s*(\w+\s+)*{method_name}\s*\([^\)]*\)(\s*throws\s+[\w,]+)?\s*\{{")
    else:
        method_pattern = re.compile(rf"\n\s*(\w+\s+)*fun\s+{method_name}\s*\([^\)]*\)[^\n]*\{{")

    match = method_pattern.search(code)
    if not match:
        return None

    return extract_code_block(code, match.start())[0]


def extract_code_block(code, start_position):
    """
    Extracts the code block starting at the given position according to the opening and closing braces
    :param code: Java or Kotlin code
    :param start_position: position of the opening brace of the code block
    :return: code block and end position of the code block
    """
    open_braces = 0
    code_block_start = start_position
    code_block_end = -1

    for i in range(start_position, len(code)):
        if code[i] == "{":
            open_braces += 1
        elif code[i] == "}":
            open_braces -= 1
            if open_braces == 0:
                code_block_end = i + 1
                break

    if code_block_end == -1:
        raise ValueError(f"Code block extraction failed")

    while code[code_block_start] == "\n":
        code_block_start += 1

    return code[code_block_start:code_block_end], code_block_end


def main(repository_path, fully_qualified_method_name, language):
    try:
        method_code = extract_method_code(repository_path, fully_qualified_method_name, language)
        if method_code == None:
            print(f"Method {fully_qualified_method_name} not found")
        else:
            print(f"Method code for {fully_qualified_method_name}:\n\n{method_code}")
    except ValueError as e:
        print(f"Method extraction failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_method.py java/kotlin <repository_path> <fully_qualified_method_name>")
    else:
        main(sys.argv[2], sys.argv[3], sys.argv[1])