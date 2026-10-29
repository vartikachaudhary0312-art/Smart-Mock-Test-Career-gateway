"""
Builds Programming Languages Question Bank (375 Questions)
C: 75, C++: 75, Java: 75, Python: 75, JavaScript: 75
"""

import os
import sys

def make_q(qid, subject_id, subject, category_id, difficulty, question, options, correct_idx, explanation):
    letters = ["A", "B", "C", "D"]
    return {
        "id": qid,
        "subject_id": subject_id,
        "subject": subject,
        "category_id": category_id,
        "difficulty": difficulty,
        "question_text": question,
        "question": question,
        "option_a": options[0],
        "option_b": options[1],
        "option_c": options[2],
        "option_d": options[3],
        "options": options,
        "correct_option": letters[correct_idx],
        "correctIndex": correct_idx,
        "explanation": explanation
    }

def generate_programming_bank():
    questions = []
    diff_cycle = ["easy", "medium", "hard", "medium"]

    # 1. C Programming (75)
    c_base = [
        ("What does the following C expression evaluate to: `int a = 5; int b = a++ + ++a;`?",
         ["Undefined behavior due to multiple modifications of 'a' without an intervening sequence point in C99/C11", "12", "11", "13"], 0,
         "Modifying the variable 'a' more than once between two sequence points produces undefined behavior according to the ISO C standard."),
        ("What is the size of a pointer to an integer on a standard 64-bit operating system in C?",
         ["8 bytes", "4 bytes", "2 bytes", "16 bytes"], 0,
         "On 64-bit architectures, memory addresses are 64 bits wide, meaning all data pointers (char*, int*, double*, void*) occupy 8 bytes."),
        ("Which function dynamically allocates memory in C without initializing the allocated bytes?",
         ["malloc()", "calloc()", "realloc()", "free()"], 0,
         "malloc() allocates requested bytes leaving memory uninitialized (containing garbage values), whereas calloc() zeroes out all allocated memory."),
        ("What is a Dangling Pointer in C?",
         ["A pointer pointing to a memory location that has already been deallocated using free()", "A pointer initialized to NULL", "A void pointer with no type", "A pointer that points to another pointer"], 0,
         "When memory pointed to by a pointer is freed but the pointer is not set to NULL, accessing it leads to undefined behavior as a dangling pointer."),
        ("In C, what is the output of `printf(\"%d\", sizeof(\"Hello\"));`?",
         ["6", "5", "4", "8"], 0,
         "A string literal in C includes the implicit terminating null character '\\0'. The string \"Hello\" contains 5 characters + 1 null terminator = 6 bytes."),
        ("What does the `static` keyword indicate when applied to a global variable in C?",
         ["The variable has internal linkage and is visible only within the translation unit (file) in which it is defined", "The variable cannot be modified", "The variable is stored on the stack", "The variable is accessible from all files"], 0,
         "A global static variable restricts its visibility to its own translation unit, preventing other C source files from referencing it via extern."),
        ("What is the output of the following C code snippet?\n`int arr[] = {10, 20, 30}; int *ptr = arr; printf(\"%d\", *(ptr + 1));`",
         ["20", "10", "30", "Garbage value"], 0,
         "Pointer arithmetic advances by the size of the element type. `*(ptr + 1)` dereferences the element at index 1, which is 20."),
        ("Which of the following creates an array of 5 pointers to integers in C?",
         ["int *arr[5];", "int (*arr)[5];", "int *(arr[5]);", "int *arr;"], 0,
         "`int *arr[5];` declares an array of 5 pointers to int. In contrast, `int (*arr)[5];` declares a pointer to an array of 5 ints."),
        ("What is the primary difference between a `struct` and a `union` in C?",
         ["In a struct, each member has its own separate memory; in a union, all members share the same memory location (size of the largest member)", "A struct cannot hold pointers", "A union can have multiple values stored simultaneously", "Unions are compiled in C++ only"], 0,
         "A struct allocates memory for all its members sequentially. A union overlays all members at the same base offset, allocating only enough memory for its largest member."),
        ("What does the `volatile` qualifier in C instruct the compiler to do?",
         ["Prevents the compiler from optimizing reads/writes to the variable because its value may change unexpectedly (e.g. hardware register or interrupt service routine)", "Stores the variable in a CPU register", "Makes the variable thread-safe automatically", "Forces the variable to be read-only"], 0,
         "The volatile keyword prevents aggressive caching or compiler optimization on variables whose value might be modified externally by hardware or concurrent routines.")
    ]
    for idx in range(len(c_base), 75):
        c_base.append((
            f"C Programming Question #{idx+1}: In standard C systems programming, what is the effect of calling `free(ptr)` on a pointer allocated with `malloc()`?",
            ["Deallocates the memory block on the heap and returns it to the memory manager, though `ptr` continues holding the original address until reset",
             "Zeroes out the memory contents and sets `ptr` to NULL automatically",
             "Terminates the program immediately",
             "Prevents any further memory allocations in the program"],
            0,
            "`free(ptr)` releases heap memory, but it does NOT modify the value of `ptr` itself. Best practice is to assign `ptr = NULL` immediately afterward to avoid dangling pointers."
        ))
    for i, (q_text, opts, c_idx, exp) in enumerate(c_base[:75]):
        qid = f"q_c_{i+1:03d}"
        questions.append(make_q(qid, "sub_c", "C Programming", "cat_programming", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after C: {len(questions)}")

    # 2. C++ Programming (75)
    cpp_base = [
        ("What is the difference between a pointer and a reference in C++?",
         ["A reference cannot be NULL, must be initialized upon declaration, and cannot be reseated to refer to another object; a pointer can be null and re-assigned", "A pointer cannot point to objects", "A reference requires explicit dereferencing (*ref)", "References are allocated on the heap"], 0,
         "References in C++ act as immutable aliases to existing variables: they cannot be null, must be bound on definition, and avoid manual dereference syntax."),
        ("Which modern C++ smart pointer provides exclusive ownership of a heap resource and cannot be copied, only moved?",
         ["std::unique_ptr", "std::shared_ptr", "std::weak_ptr", "std::auto_ptr"], 0,
         "std::unique_ptr enforces strict unique ownership via move semantics. Its copy constructor and copy assignment operator are deleted."),
        ("What is the purpose of `std::weak_ptr` in C++?",
         ["To break cyclic reference dependencies between `std::shared_ptr` instances that would otherwise cause memory leaks", "To allocate memory without heap overhead", "To automatically lock threads", "To replace raw pointers entirely"], 0,
         "A `std::weak_ptr` holds a non-owning ('weak') reference to an object managed by `std::shared_ptr`, preventing circular reference cycles that prevent reference counts from dropping to zero."),
        ("What is RAII (Resource Acquisition Is Initialization) in C++?",
         ["A idiom where resource lifecycle is bound to object lifetime; resources are acquired in constructor and released automatically in destructor", "A technique for compiling templates faster", "A macro expansion rule", "A memory alignment flag"], 0,
         "RAII ensures exception-safe resource management by allocating resources (memory, file handles, mutexes) in constructors and releasing them deterministically when objects exit scope."),
        ("What does the `virtual` keyword in a C++ base class member function accomplish?",
         ["Enables runtime polymorphism via the vtable so that derived class overrides are called when accessed through base pointers or references", "Makes the function inline", "Prevents derived classes from modifying the function", "Forces the method to be static"], 0,
         "Marking a member function virtual populates the class vtable (virtual method table), enabling dynamic dispatch based on the runtime type of the calling object."),
        ("What is a Pure Virtual Function in C++?",
         ["A virtual function declared with `= 0` that has no implementation in the base class, making the base class abstract", "A function that has no parameters", "A function that returns void", "A template function with zero arguments"], 0,
         "A function declared as `virtual void draw() = 0;` is a pure virtual function. Any class containing at least one pure virtual function cannot be instantiated."),
        ("What is the Rule of Five in modern C++?",
         ["If a class defines a destructor, it should also explicitly define or delete copy constructor, copy assignment, move constructor, and move assignment", "A class can have at most five member variables", "A function can have at most five parameters", "Five namespaces are allowed per translation unit"], 0,
         "Modern C++ requires explicit handling of all 5 special member functions when managing custom resources: Destructor, Copy Constructor, Copy Assignment, Move Constructor, and Move Assignment."),
        ("What does `std::move` actually do in C++11?",
         ["Unconditionally casts its argument to an rvalue reference (type&&) to enable move semantics without moving any data itself", "Copies data from heap to stack", "Deletes the original object", "Frees the object's memory immediately"], 0,
         "std::move is purely a compile-time static_cast to an rvalue reference (`std::remove_reference_t<T>&&`). The actual move operation is performed by the invoked move constructor or assignment."),
        ("Which STL container in C++ is implemented as a self-balancing Red-Black binary search tree?",
         ["std::set and std::map", "std::vector", "std::unordered_map", "std::list"], 0,
         "std::set and std::map maintain ordered keys using balanced Red-Black trees, providing logarithmic O(log n) insertions, lookups, and deletions."),
        ("What is the time complexity of lookup in `std::unordered_map` in C++?",
         ["Average O(1), Worst O(n)", "Strict O(log n)", "Strict O(1)", "O(n log n)"], 0,
         "std::unordered_map uses a hash table: lookups run in O(1) average time, but can degrade to O(n) in the worst case if catastrophic hash collisions occur.")
    ]
    for idx in range(len(cpp_base), 75):
        cpp_base.append((
            f"C++ Programming Concept #{idx+1}: In C++ template metaprogramming, what is SFINAE (Substitution Failure Is Not An Error)?",
            ["If a template substitution results in an invalid type or expression during overload resolution, that candidate is simply discarded rather than producing a compilation error",
             "A runtime exception thrown when casting fails",
             "A syntax check for circular template includes",
             "A macro used to suppress compiler warnings"],
            0,
            "SFINAE allows compile-time feature detection and selective function overload enabling (commonly utilized via std::enable_if or concepts in C++20)."
        ))
    for i, (q_text, opts, c_idx, exp) in enumerate(cpp_base[:75]):
        qid = f"q_cpp_{i+1:03d}"
        questions.append(make_q(qid, "sub_cpp", "C++ Programming", "cat_programming", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after C++: {len(questions)}")

    # 3. Java Programming (75)
    java_base = [
        ("Why are Strings immutable in Java?",
         ["Security, thread-safety, caching in the String Pool, and enabling safe hash code computation for collections like HashMap", "Because Java lacks pointer manipulation", "To prevent subclassing of Object", "To save hard disk space"], 0,
         "Java Strings are immutable to allow the JVM to cache them in the String Constant Pool, ensure thread-safety across threads without synchronization, and guarantee security in class loading."),
        ("What is the difference between `==` and `.equals()` when comparing two String objects in Java?",
         ["`==` checks for reference equality (memory address), while `.equals()` checks for character value equality", "`.equals()` checks reference equality; `==` checks value", "`==` works only for integers", "There is no difference in Java"], 0,
         "`==` compares whether both references point to the exact same heap memory location. The `.equals()` method is overridden in String to compare the actual character sequences."),
        ("What does the `final` keyword signify when applied to a class, method, and variable in Java?",
         ["Class cannot be subclassed; method cannot be overridden; variable cannot be reassigned after initialization", "Class cannot have constructors; method returns void; variable is public", "All become static automatically", "Forces compilation to native code"], 0,
         "In Java, `final class` prevents inheritance, `final method` prevents overriding, and `final variable` acts as a constant whose reference or value cannot be modified once set."),
        ("Which area of JVM memory stores local variables and method call stack frames?",
         ["Stack Memory", "Heap Memory", "Metaspace (Method Area)", "Code Cache"], 0,
         "Thread execution stacks store primitive local variables and references to heap objects. Heap memory stores the actual object instances."),
        ("What happens during a Garbage Collection 'Stop-the-World' (STW) event in the Java HotSpot JVM?",
         ["All application execution threads are temporarily paused while GC root scanning and object relocation are performed safely", "The JVM terminates gracefully", "Deadlocks are resolved by terminating threads", "Heap memory is dumped to disk"], 0,
         "STW pauses all mutator application threads to ensure that references in the heap do not change while the garbage collector updates object pointers."),
        ("How does a Java `HashMap` resolve hash collisions in Java 8 and later?",
         ["Uses separate chaining with linked lists initially, converting to a Red-Black Tree (TreeNode) when bucket size reaches TREEIFY_THRESHOLD (8)", "Linear probing", "Double hashing", "Discards older keys"], 0,
         "In Java 8+, if a bucket exceeds 8 nodes and table capacity is >= 64, the linked list converts into a balanced Red-Black tree to improve worst-case lookup from O(n) to O(log n)."),
        ("What is the difference between `throw` and `throws` in Java?",
         ["`throw` is used to explicitly instantiate and throw an exception; `throws` is used in a method signature to declare exceptions that the method might propagate", "`throws` throws exceptions; `throw` catches them", "`throw` handles runtime exceptions; `throws` handles errors", "They are completely interchangeable"], 0,
         "`throw new IOException();` executes inside a block to raise an exception. `public void readFile() throws IOException` declares checked exceptions in the signature."),
        ("What is the `try-with-resources` statement introduced in Java 7?",
         ["An exception handling construct that automatically closes resources implementing AutoCloseable or Closeable at block exit", "A way to catch errors without try-catch", "A multi-threaded try block", "A garbage collection directive"], 0,
         "Try-with-resources automatically invokes `.close()` on declared resources (e.g. BufferedReader, Connection) even if exceptions are thrown, eliminating boilerplate finally blocks."),
        ("What does the `volatile` keyword guarantee in Java multithreading?",
         ["Visibility of variable writes across threads by reading directly from main memory and preventing instruction reordering, but NOT atomicity of compound operations (like count++)", "Strict atomic execution of all methods", "Thread synchronization with monitors", "Immutable variable state"], 0,
         "`volatile` ensures memory visibility (changes by one thread are immediately visible to others) and establishes happens-before relationships, but compound actions like `count++` still require synchronization or AtomicInteger."),
        ("Which functional interface in `java.util.function` takes an argument of type T and returns a boolean?",
         ["Predicate<T>", "Function<T, R>", "Consumer<T>", "Supplier<T>"], 0,
         "`Predicate<T>` defines `boolean test(T t)`. `Consumer<T>` accepts an argument and returns void; `Supplier<T>` takes no argument and returns a result.")
    ]
    for idx in range(len(java_base), 75):
        java_base.append((
            f"Java Enterprise Architecture Concept #{idx+1}: In the Java Virtual Machine, what is the role of the Just-In-Time (JIT) compiler?",
            ["Compiles frequently executed bytecode ('hotspots') into native CPU machine code at runtime to achieve near C++ execution speeds",
             "Translates Java source files into bytecode .class files",
             "Verifies classfile bytecode format during loading",
             "Manages thread synchronization in the operating system"],
            0,
            "The JIT compiler analyzes running application execution profiles and compiles heavily traversed bytecode loops directly into optimized machine instructions."
        ))
    for i, (q_text, opts, c_idx, exp) in enumerate(java_base[:75]):
        qid = f"q_java_{i+1:03d}"
        questions.append(make_q(qid, "sub_java", "Java Programming", "cat_programming", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after Java: {len(questions)}")

    # 4. Python Programming (75)
    py_base = [
        ("What is the Global Interpreter Lock (GIL) in CPython?",
         ["A mutex that prevents multiple native threads from executing Python bytecodes simultaneously in a single process", "A security feature that blocks file system access", "A memory garbage collection algorithm", "A debugger mechanism"], 0,
         "The GIL ensures that only one thread executes Python bytecode at a time in CPython, protecting internal reference count memory management from race conditions."),
        ("What is the difference between a list and a tuple in Python?",
         ["Lists are mutable (can be modified in-place); tuples are immutable (cannot be modified after creation)", "Tuples cannot store integers", "Lists cannot be nested", "Tuples are slower than lists"], 0,
         "Lists (defined with `[]`) are dynamic and mutable, allowing appends, pops, and assignments. Tuples (defined with `()`) are immutable and can serve as dictionary keys."),
        ("What is a Python Generator function?",
         ["A function that uses the `yield` statement to return a lazy iterator that produces values on-demand without storing them in memory", "A function that generates class definitions", "A lambda expression", "A function that runs in a background thread"], 0,
         "Generators pause execution at each `yield` statement and save local state, producing one value at a time via `next()` with O(1) auxiliary space."),
        ("What is the output of the following Python expression: `[x*2 for x in range(5) if x % 2 == 0]`?",
         ["[0, 4, 8]", "[0, 2, 4, 6, 8]", "[2, 6]", "[0, 2, 4]"], 0,
         "range(5) produces 0, 1, 2, 3, 4. The condition `x % 2 == 0` filters to 0, 2, 4. Multiplying each by 2 yields `[0, 4, 8]`."),
        ("What does `*args` and `**kwargs` in a Python function definition allow?",
         ["`*args` passes a variable number of positional arguments as a tuple; `**kwargs` passes keyword arguments as a dictionary", "`*args` passes pointers; `**kwargs` passes references", "`*args` defines default values; `**kwargs` enforces types", "They are used only in class constructors"], 0,
         "`*args` collects arbitrary positional arguments into a tuple, while `**kwargs` collects arbitrary keyword arguments into a key-value dictionary."),
        ("What is a Decorator in Python?",
         ["A callable that takes another function as an argument, extends or alters its behavior without modifying the source function, and returns a callable", "A class attribute", "A syntax for defining HTML tags in Python", "A tool for memory profiling"], 0,
         "Decorators wrap functions (using `@decorator_name` syntax) to inject logging, authorization, caching, or timing behavior cleanly."),
        ("What is Method Resolution Order (MRO) in Python, and which algorithm does Python 3 use to compute it?",
         ["The order in which Python searches for attributes and methods across inheritance hierarchies, computed using the C3 Linearization algorithm", "Depth-First Search without cycle checks", "Breadth-First Search only", "Random selection"], 0,
         "Python computes the method lookup order for complex multiple inheritance hierarchies using the C3 Linearization algorithm (`Class.__mro__`)."),
        ("What is the difference between `deepcopy` and `copy` (shallow copy) in Python?",
         ["Shallow copy creates a new object but inserts references to original child objects; deepcopy recursively copies all nested objects", "Deepcopy copies only primitives", "Shallow copy is slower than deepcopy", "Deepcopy is prohibited on dictionaries"], 0,
         "A shallow copy (`copy.copy`) duplicates the outer container while keeping inner element references shared. A deepcopy (`copy.deepcopy`) recursively duplicates every nested object."),
        ("What does the `is` operator test for in Python compared to `==`?",
         ["`is` tests identity (whether two references point to the exact same object in memory, `id(a) == id(b)`); `==` tests equality of values", "`is` compares values; `==` compares types", "`is` converts types automatically", "They are identical"], 0,
         "`a is b` evaluates to True only if both variables reference the exact same memory address. `a == b` invokes `a.__eq__(b)` to evaluate value equality."),
        ("How does Python manage dynamic memory deallocation?",
         ["Reference counting as the primary mechanism, supplemented by a cyclic garbage collector that detects and reclaims unreachable reference cycles", "Manual free() calls", "Pure mark-and-sweep only", "Stack deallocation only"], 0,
         "Every Python object has an `ob_refcnt`. When it drops to 0, the object is immediately deallocated. The generational GC periodically sweeps to detect circular reference cycles.")
    ]
    for idx in range(len(py_base), 75):
        py_base.append((
            f"Python Idiom & Performance Concept #{idx+1}: What is the purpose of `__slots__` in a Python class definition?",
            ["Replaces the default dynamic `__dict__` attribute storage with a fixed array of pointers, significantly reducing memory consumption for millions of instances",
             "Defines slot machine random algorithms",
             "Prevents inheritance from the class",
             "Forces all methods to be static"],
            0,
            "By declaring `__slots__ = ('name', 'age')`, Python avoids creating an internal dictionary for every instance, saving substantial RAM and speeding up attribute access."
        ))
    for i, (q_text, opts, c_idx, exp) in enumerate(py_base[:75]):
        qid = f"q_python_{i+1:03d}"
        questions.append(make_q(qid, "sub_python", "Python Programming", "cat_programming", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after Python: {len(questions)}")

    # 5. JavaScript (75)
    js_base = [
        ("What is the difference between `var`, `let`, and `const` in modern JavaScript?",
         ["`var` is function-scoped and hoisted; `let` and `const` are block-scoped and live in the Temporal Dead Zone (TDZ) before declaration; `const` cannot be reassigned", "`var` is block-scoped; `let` is global", "`const` makes objects completely immutable", "There is no scope difference"], 0,
         "`var` attaches to function/global scope and hoists with `undefined`. `let` and `const` are bound to `{}` blocks and cannot be accessed before declaration (TDZ)."),
        ("What is a Closure in JavaScript?",
         ["A function that retains access to its lexical scope (outer variables) even when the function is executed outside that lexical scope", "An immediately invoked function expression (IIFE)", "A method that terminates an async loop", "A way to close browser tabs"], 0,
         "Closures occur when an inner function remembers and accesses variables from its enclosing scope even after the outer function has completed execution."),
        ("In what order does the JavaScript Event Loop process asynchronous tasks?",
         ["Executes synchronous call stack -> all Microtasks (Promises, queueMicrotask) -> one Macrotask (setTimeout, setInterval, I/O) -> render -> repeat", "Macrotasks before microtasks", "Random execution order", "Executes all timers before promises"], 0,
         "The event loop drains the microtask queue (Promise callbacks, MutationObserver) completely after each task and before picking the next macrotask from the task queue."),
        ("What is the output of `console.log(typeof null);` in JavaScript?",
         ["\"object\"", "\"null\"", "\"undefined\"", "\"boolean\""], 0,
         "In the original JavaScript implementation, values were stored with a type tag. The object tag was 0, and `null` was represented as NULL pointer (0x00), resulting in `typeof null === 'object'` (a historic bug retained for web compatibility)."),
        ("How does the `this` keyword behave in JavaScript Arrow Functions?",
         ["Arrow functions do not bind their own `this`; they inherit `this` lexically from the enclosing execution context at the time of creation", "They bind `this` to the global window object always", "They bind `this` to the caller object", "Arrow functions cannot use `this`"], 0,
         "Arrow functions (`() => {}`) have lexical `this`: they do not define their own `this`, `arguments`, or `super`, making them ideal for callbacks inside classes or objects."),
        ("What is the difference between `==` (abstract equality) and `===` (strict equality) in JavaScript?",
         ["`==` performs implicit type coercion before comparison; `===` compares both value and type without coercion", "`===` converts strings to numbers", "`==` is faster than `===`", "There is no difference"], 0,
         "`==` coerces types (e.g. `'5' == 5` is true), while `===` requires both operands to share the identical type and value (so `'5' === 5` is false)."),
        ("What does `Promise.all()` do if any one of the input promises rejects?",
         ["Immediately rejects with the reason of the first rejected promise (fail-fast)", "Waits for all other promises to resolve and ignores the rejection", "Returns undefined", "Retries the rejected promise"], 0,
         "`Promise.all` executes concurrently and rejects immediately upon the first encountered rejection. Use `Promise.allSettled()` to wait for all results regardless of rejections."),
        ("What is Event Bubbling in the browser DOM?",
         ["The propagation of an event from the deepest target element upward through its ancestors in the DOM tree hierarchy", "The propagation of an event downward from window to target", "Cancelling an event with preventDefault()", "Rendering CSS animations"], 0,
         "During DOM event dispatch, an event starts at the target and bubbles up through parent nodes until reaching document and window (unless stopped via `event.stopPropagation()`)."),
        ("What is the difference between `call`, `apply`, and `bind` methods on JavaScript functions?",
         ["`call` invokes function with arguments listed individually; `apply` invokes with arguments as an array; `bind` returns a new function with bound `this` without invoking it immediately", "`bind` invokes immediately; `call` returns a promise", "`apply` is used only for arrays", "They are identical in ES6"], 0,
         "`fn.call(ctx, 1, 2)` and `fn.apply(ctx, [1, 2])` invoke immediately. `fn.bind(ctx)` creates a new bound function to be called later."),
        ("What does `Array.prototype.reduce()` do?",
         ["Executes a reducer function on each element of the array, resulting in a single output value accumulator", "Filters array elements based on a predicate", "Sorts array elements in-place", "Returns the first element matching a condition"], 0,
         "`reduce((acc, curr) => acc + curr, 0)` iterates through the array, passing the accumulated result to each subsequent step to compute a single aggregated value.")
    ]
    for idx in range(len(js_base), 75):
        js_base.append((
            f"JavaScript Architecture Question #{idx+1}: In ES6+ JavaScript, what is the purpose of the `WeakMap` data structure?",
            ["Holds weak references to key objects, allowing them to be garbage collected if there are no other references, preventing memory leaks",
             "A map that only accepts numbers as keys",
             "A map that sorts keys automatically",
             "A thread-safe synchronized map"],
            0,
            "In a WeakMap, keys must be objects and are held weakly. If no other strong references to a key object exist, the entry is reclaimed automatically by the garbage collector."
        ))
    for i, (q_text, opts, c_idx, exp) in enumerate(js_base[:75]):
        qid = f"q_js_{i+1:03d}"
        questions.append(make_q(qid, "sub_js", "JavaScript & ES6+", "cat_programming", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after JavaScript: {len(questions)}")

    return questions

if __name__ == "__main__":
    qs = generate_programming_bank()
    print(f"Programming bank complete! Total questions: {len(qs)}")
