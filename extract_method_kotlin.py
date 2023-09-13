import os
import re
import sys

from code_extraction import extract_code_block


def extract_method_code(repository_path: str, full_method_name: str) -> str | None:
    """
    Extracts the code of the method with the given name from the repository
    :param repository_path: path to the repository
    :param full_method_name: name of the method to extract
    :return: code of the method
    """
    # first case package.class.method - function is method of some class
    package = ""
    class_name = ""
    method_name = ""
    if full_method_name.count(".") >= 2:
        package, class_name, method_name = full_method_name.rsplit(".", 2)
    elif full_method_name.count(".") == 1:
        class_name, method_name = full_method_name.rsplit(".", 1)
    package_path = package.replace(".", os.path.sep)
    file_path = os.path.join(repository_path, "src", "main", "kotlin", package_path)
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
            method_code = extract_method_code_from_code(class_code, method_name)
            return method_code

    # second case package.method - function is method of some file

    if full_method_name.count(".") >= 1:
        package, method_name = full_method_name.rsplit(".", 1)
    else:
        package = ""
        method_name = full_method_name

    package_path = package.replace(".", os.path.sep)
    file_path = os.path.join(repository_path, "src", "main", "kotlin", package_path)
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
            while match is not None:
                # extract the code of the class
                class_code, end_position = extract_code_block(content, match.start())
                content = content[:match.start()] + content[end_position:]

                match = class_pattern.search(content)

            # find the method inside the content without classes
            method_code = extract_method_code_from_code(content, method_name)
            if method_code is not None:
                return method_code
    return None


def extract_method_code_from_code(code: str, method_name: str) -> str | None:
    """
    Extracts the code of the method with the given name from the Kotlin code
    :param code: Kotlin code
    :param method_name: name of the method to extract
    :return: code of the method
    """

    method_pattern = re.compile(rf"\n\s*(\w+\s+)*fun\s+{method_name}\s*\([^\)]*\)[^\n]*\{{")

    match = method_pattern.search(code)
    if not match:
        return None

    return extract_code_block(code, match.start())[0]


def main(repository_path, fully_qualified_method_name):
    try:
        method_code = extract_method_code(repository_path, fully_qualified_method_name)
        if method_code is None:
            print(f"Method {fully_qualified_method_name} not found")
        else:
            print(f"Method code for {fully_qualified_method_name}:\n\n{method_code}")
    except ValueError as e:
        print(f"Method extraction failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_method_kotlin.py <repository_path> <fully_qualified_method_name>")
    else:
        main(sys.argv[1], sys.argv[2])
