# Test task

In this project, I implemented a program that extracts method code, given its fully qualified name and path to the repository. This program supports both Java and Kotlin languages.
- Java is supported by using `javalang` library for Java code parsing.
- Kotlin is supported by finding method definition in source code using regex.

## Java

**Usage:** `python extract_method_java.py <path to repository> <fully qualified method name>`

For Java language, the program just looks inside the file with the name corresponding to class name. Then, the method with the given name is searched inside this class file (using `javalang` library). 

### Example of usage for Java:
bash command:
```
python .\extract_method_java.py ..\IdeaProjects\csc-java-course-spring-2023-key-value-store-EgorShibaev\ org.csc.java.spring2023.IndexManagerImplementation.add
```
output:
```java
Method code for org.csc.java.spring2023.IndexManagerImplementation.add:
void add(byte[] key, List<FileBlockLocation> writtenBlocks) {
    indexes.put(new ByteWrapper(key), writtenBlocks);
  }
```

bash command:
```
python .\extract_method_java.py ..\IdeaProjects\csc-java-course-spring-2023-key-value-store-EgorShibaev\ org.csc.java.spring2023.KeyValueStoreFactory.create  
```
output:
```java
Method code for org.csc.java.spring2023.KeyValueStoreFactory.create:
KeyValueStore create(Path workingDir, int valueFileSize) throws IOException {
    return new KeyValueStoreImplementation(workingDir, valueFileSize);
  }
```

## Kotlin

**Usage:** `python extract_method_kotlin.py <path to repository> <fully qualified method name>`

For Kotlin language, it is assumed that the directory structure follows the package structure (it is only a recommended naming convention in Kotlin). Two cases are considered:
- __Method is inside the class__. In this case, all files in the package directory are considered and the class with the given name is searched inside them. As soon as the class with the given name is found, the method with the given name is searched inside this class using regex.
- __This function does not belong to any particular class__. In this case, all files in the directory are considered, all classes in the code are deleted and the method with the given name is searched inside code without classes. This code may provide a reason for such an approach:

```kotlin
package com.example

class A {
    fun foo() {
        print("Foo inside class")
    }
}

fun foo() {
    print("Foo outside class")       
}


```
in this code, by request with a fully qualified name `com.example.foo` method outside of class should be found. If the fully qualified name is `com.example.A.foo`, then, the method inside the class should be found. 

### Example of usage for Kotlin:
bash command:
```
python .\extract_method_kotlin.py ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.StatisticHandler.addIntermediateZeros
```
output:
```kotlin
Method code for ru.senin.kotlin.wiki.StatisticHandler.addIntermediateZeros:

                        private override fun addIntermediateZeros(map: Map<Int, Int>): SortedMap<Int, Int> {
                                if (map.isEmpty())
                                        return map.toSortedMap()
                                val min = map.minOf { it.key }
                                val max = map.maxOf { it.key }
                                val result = mutableMapOf<Int, Int>()
                                for (value in min..max)
                                        result[value] = map[value] ?: 0
                                return result.toSortedMap()
                        }
```

bash command:
```
 python .\extract_method_kotlin.py ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.main
```
output:
```kotlin
Method code for ru.senin.kotlin.wiki.main:

fun main(args: Array<String>) {
        println("Hello world!")
}
```

bash command:
```
 python .\extract_method_kotlin.py ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.A.bar
```
output:
```kotlin
Method code for ru.senin.kotlin.wiki.A.bar:

        protected suspend fun bar(): Map<Int, List<Int>> {
                return emptyMap()
        }
```

In this example, function belongs to class A. If fully qualified name in query is `ru.senin.kotlin.wiki.bar`, then this method will not be found:

bash command:
```
 python .\extract_method_kotlin.py ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.bar
```
output:
```
Method ru.senin.kotlin.wiki.bar not found
```