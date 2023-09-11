# Test task

File extract_method.py contains a script that extracts method code, given its fully qualified name and path to the repository. This program supports both Java and Kotlin languages.

**Usage:** `python extract_method.py <language> <path> <fully qualified method name>`

For Java language program just look inside the file with the class name. Then, method with given name is searched inside this class. 

For Kotlin program, it is assumed that directory structure follows the package structure (it is only a recommended naming convention in Kotlin). Two cases are considered:
- method is inside the class. In this case, all files in the directory are considered and the class with given name is searched inside them. Then, method with given name is searched inside this class.
- method is not method of any class. In this case, all files in the directory are considered and method with given name is searched inside them.

So, in the code

```kotlin
package com.example

fun foo() {
    print("Foo outside class")       
}

class A {
    fun foo() {
        print("Foo inside class")
    }
}

```

method with name `com.example.foo` is referred to the first one and method with name `com.example.A.foo` is referred to the second one.



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