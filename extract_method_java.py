import sys
import javalang
import os
from code_extraction import extract_code_block


def extract_method_code(java_source, class_name, method_name):
    """
    This function extracts the code of the method with the
    given name and class from the Java source code
    :param java_source: Java source code
    :param class_name: name of the class
    :param method_name: name of the method
    :return: code of the method
    """
    tree = javalang.parse.parse(java_source)

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        if class_name == path[1][0].name and method_name == node.name:
            start_line = node.position.line - 1
            start_position = sum(len(line) + 1 for line in java_source.splitlines()[:start_line]) \
                             + node.position.column - 1
            return extract_code_block(java_source, start_position)[0]

    return None


def main(repository_path, fully_qualified_method_name):
    try:
        if fully_qualified_method_name.count(".") >= 2:
            package, class_name, method_name = fully_qualified_method_name.rsplit(".", 2)
        else:
            class_name, method_name = fully_qualified_method_name.rsplit(".", 1)
            package = ""

        package_path = package.replace(".", os.path.sep)
        file_path = os.path.join(repository_path, "src", "main", "java", package_path, f"{class_name}.java")

        with open(file_path, "r") as java_file:
            java_source = java_file.read()

        # Extract the method code
        method_code = extract_method_code(java_source, class_name, method_name)

        if method_code:
            print(f"Method code for {fully_qualified_method_name}:")
            print(method_code)
        else:
            print(f"Method {fully_qualified_method_name} not found.")

    except ValueError as e:
        print(f"Method extraction failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_method_java.py <repository_path> <fully_qualified_method_name>")
    else:
        main(sys.argv[1], sys.argv[2])
