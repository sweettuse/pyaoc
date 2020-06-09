The problem: You're given a mapping that's like the following:

'a' -> 1

'b' -> 2

'c' -> 3

...

'z' -> 26

With this mapping, if you're given a string, for example, "ab", you can convert it to another string using the map. So "ab" -> "12" In the problem, you're given the converted version of the string (like "12"). The problem asks you to write an algorithm that takes the converted version of the string and returns the number of messages that could have been the original message. So if you're given "12" as the input, the output should be 2. It could be "ab" or "l"