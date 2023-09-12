# Test task

File extract_method.py contains a script that extracts method code, given its fully qualified name and path to the repository. This program supports both Java and Kotlin languages.

**Usage:** `python extract_method.py <language> <path> <fully qualified method name>`

For Java language, the program just looks inside the file with the class name. Then, the method with the given name is searched inside this class. 

For Kotlin language, it is assumed that the directory structure follows the package structure (it is only a recommended naming convention in Kotlin). Two cases are considered:
- Method is inside the class. In this case, all files in the package directory are considered and the class with the given name is searched inside them. As soon as the class with the given name is found, the method with the given name is searched inside this class.
- This function does not belong to any particular class. In this case, all files in the directory are considered, all classes in the code are deleted and the method with the given name is searched inside code without classes. This code may provide a reason for such an approach:

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

## Example of usage for Java:
```
python .\extract_method.py java ..\IdeaProjects\csc-java-course-spring-2023-key-value-store-EgorShibaev\ org.csc.java.spring2023.KeyValueStoreImplementation.getIndexManager
```
output:
```java
Method code for org.csc.java.spring2023.KeyValueStoreImplementation.getIndexManager:

  public IndexManager getIndexManager() {
    check_closed();

    return indexManager;
  }
```
## Example of usage for Kotlin:
```
python .\extract_method.py kotlin ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.StatisticHandler.addIntermediateZeros
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

```
 python .\extract_method.py kotlin ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.main
```
output:
```kotlin
Method code for ru.senin.kotlin.wiki.main:

fun main(args: Array<String>) {
        println("Hello world!")
}
```

```
 python .\extract_method.py kotlin ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.A.bar
```
output:
```kotlin
Method code for ru.senin.kotlin.wiki.A.bar:

        protected suspend fun bar(): Map<Int, List<Int>> {
                return emptyMap()
        }
```

In this example function belong to class A. If fully qualified name in query is `ru.senin.kotlin.wiki.bar`, then this method will not be found:
```
 python .\extract_method.py kotlin ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.bar
```
output:
```
Method ru.senin.kotlin.wiki.bar not found
```