# Test task

File extract_method.py contains a script that extracts method code, given its fully qualified name and path to the repository. This program supports both Java and Kotlin languages.

 It is assumed directory structure follows the package structure (it is only a recommended naming convention in Kotlin).In the case of Kotlin, a fully qualified method name is assumed to be {package_name}.{class_name/file_name}.{method_name}. Also, it is assumed that source files are in the `/src/main/java` or `/src/main/kotlin` directories. Usage: ``python extract_method.py {language} {path_to_repository} {fully_qualified_method_name}``. 

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
 python .\extract_method.py kotlin ..\IdeaProjects\kotlin-2022-b10-b11-class6-EgorShibaev\ ru.senin.kotlin.wiki.main.main
```
output:
```kotlin
Method code for ru.senin.kotlin.wiki.main.main:

fun main(args: Array<String>) {
        println("Hello world!")
}
```