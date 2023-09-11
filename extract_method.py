import os
import re
import sys

def extract_method_code(repository_path: str, method_name: str, language: str) -> str:
    """
    Extracts the code of the method with the given name from the repository
    :param repository_path: path to the repository
    :param method_name: name of the method to extract
    :param language: language of the method - java or kotlin
    :return: code of the method
    """
    
    package, class_name, method_name = method_name.rsplit(".", 2)
    package_path = package.replace(".", os.path.sep)
    file_extension = "java" if language == "java" else "kt"
    file_path = os.path.join(repository_path, "src", "main", language, package_path, f"{class_name}.{file_extension}")

    with open(file_path, "r") as file:
        content = file.read()

    method_code = extract_method_code_from_content(content, method_name, language)
    return method_code

def extract_method_code_from_content(code, method_name, language):
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
        raise ValueError(f"Method {method_name} not found in the code")

    open_braces = 0
    method_start = match.start()
    method_end = -1

    for i in range(method_start, len(code)):
        if code[i] == "{":
            open_braces += 1
        elif code[i] == "}":
            open_braces -= 1
            if open_braces == 0:
                method_end = i + 1
                break

    if method_end == -1:
        raise ValueError(f"Method {method_name} code extraction failed")

    while code[method_start] == "\n":
        method_start += 1

    return code[method_start:method_end]

def main(repository_path, fully_qualified_method_name, language):
    try:
        method_code = extract_method_code(repository_path, fully_qualified_method_name, language)
        print(f"Method code for {fully_qualified_method_name}:\n\n{method_code}")
    except ValueError as e:
        print(f"Method extraction failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_method.py java/kotlin <repository_path> <fully_qualified_method_name>")
    else:
        main(sys.argv[2], sys.argv[3], sys.argv[1])