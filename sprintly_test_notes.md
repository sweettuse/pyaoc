### overview
 - reiterate reasoning:
     - work on fun problems not strictly work related
     - learn by reviewing the problems as a group and allowing people to ask questions
     - much better if you complete the problems _ahead of time_
 - first problem, rocket stuff, just a good intro to how AOC works and what to expect.
 - the remainder, all about writing your own interpreter, which we will continue
  on in further installments of sprintly tests
 - personal note: i wrote all these things in clojure first to learn, then went back and did python
 - using clojure definitely made me appreciate a more functional style, and you will see some of this here:
    - more map, comp, first, take, juxt
 - all code available at my [personal github](https://github.com/sweettuse/pyaoc2019)


### problem 1: rocket equation
 - simple, straightforward
 - did mine in py38, so wanted to show off the walrus operator :=, which is super cute

### problems 2, 5
 - all centered around building/extending an interpreter
 - key parts:
    - `Program`: conceptually represents a computer
       - has program counter, output register, mem offset, and instructions
    - instructions: what the program can understand
       - ABC base instruction
       - 5 unique instructions for 9 different operations
    - `InstructionInfo`: wraps an individual instruction with meta info and its arity. used by opcode
    - `Opcode`: wraps instruction info with other helpful things, like the program itself


### problem 7: amps
 - this was a cool, if tough to understand question
 - key thought: as soon as "suspending" and "resuming" was mentioned, think generators. that's what they do
 - go over amps/process_map


### problem 6: orbits
 - part 1:
     - recursive, but not tail recursive
     - blows out stack
     - in clojure, basically implemented own stack
     - in python, used the async event loop to flatten out stack
         - demo how this works with a drawing perhaps
     - uses an accumulator to count how many orbits there are (n_parents)
 - part 2:
    - thought process was "find all shared parents, with a distance from each one"
    - find the closest one of those and then sum up those 2 distances
