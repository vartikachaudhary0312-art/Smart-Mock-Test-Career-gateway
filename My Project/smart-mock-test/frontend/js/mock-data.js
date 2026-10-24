/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Seed Mock Data Store for Stage 1 (Frontend Demonstration)
 */

const DEFAULT_MOCK_DATA = {
  users: [
    {
      id: "usr_student_01",
      name: "Rahul Sharma",
      email: "student@example.com",
      password: "Student@123",
      role: "student",
      phone: "+91 9876543210",
      location: "Bangalore, India",
      education: "MCA 4th Sem, ABC Institute of Technology",
      skills: ["Java", "Python", "SQL", "HTML/CSS", "Data Structures"],
      registeredAt: "2026-01-15"
    },
    {
      id: "usr_admin_01",
      name: "System Admin",
      email: "vartikachaudhary0312@gmail.com",
      password: "Vartika1234@",
      role: "admin",
      phone: "+91 9876543211",
      location: "New Delhi, India",
      registeredAt: "2025-11-01"
    }
  ],

  subjects: [
    { id: "sub_cse_comprehensive", name: "CSE Comprehensive Assessment", icon: "bi-mortarboard", questionCount: 50, category: "All CSE Subjects", description: "A 50-question assessment spanning the complete computer science subject bank." },
    { id: "sub_c", name: "C Programming", icon: "bi-braces", questionCount: 2, category: "Programming" },
    { id: "sub_java", name: "Java Programming", icon: "bi-cup-hot", questionCount: 3, category: "Programming" },
    { id: "sub_python", name: "Python Core", icon: "bi-filetype-py", questionCount: 3, category: "Programming" },
    { id: "sub_dsa", name: "Data Structures & Algorithms", icon: "bi-diagram-3", questionCount: 3, category: "Computer Science" },
    { id: "sub_discrete", name: "Discrete Mathematics", icon: "bi-calculator", questionCount: 2, category: "Mathematics" },
    { id: "sub_dbms", name: "DBMS & SQL", icon: "bi-database", questionCount: 3, category: "Database" },
    { id: "sub_os", name: "Operating Systems", icon: "bi-cpu", questionCount: 2, category: "Core CS" },
    { id: "sub_networks", name: "Computer Networks", icon: "bi-diagram-3-fill", questionCount: 2, category: "Core CS" },
    { id: "sub_coa", name: "Computer Organization & Architecture", icon: "bi-motherboard", questionCount: 2, category: "Core CS" },
    { id: "sub_toc", name: "Theory of Computation", icon: "bi-diagram-2", questionCount: 2, category: "Core CS" },
    { id: "sub_compiler", name: "Compiler Design", icon: "bi-code-square", questionCount: 2, category: "Core CS" },
    { id: "sub_se", name: "Software Engineering", icon: "bi-kanban", questionCount: 2, category: "Software" },
    { id: "sub_web", name: "Web Development (HTML/CSS/JS)", icon: "bi-code-slash", questionCount: 2, category: "Web Tech" },
    { id: "sub_ai", name: "Artificial Intelligence & Machine Learning", icon: "bi-robot", questionCount: 2, category: "Emerging Tech" },
    { id: "sub_security", name: "Cybersecurity", icon: "bi-shield-lock", questionCount: 2, category: "Security" }
  ],

  questions: [
    {
      id: "q_j1",
      subjectId: "sub_java",
      difficulty: "Medium",
      question: "Which feature of OOP allows creating a new class from an existing class?",
      options: ["Polymorphism", "Inheritance", "Encapsulation", "Abstraction"],
      correctIndex: 1,
      explanation: "Inheritance is the OOP mechanism where a subclass derives attributes and methods from a superclass."
    },
    {
      id: "q_j2",
      subjectId: "sub_java",
      difficulty: "Easy",
      question: "Which keyword is used to declare a constant variable in Java?",
      options: ["static", "const", "final", "immutable"],
      correctIndex: 2,
      explanation: "The 'final' keyword in Java prevents modification of a variable's value."
    },
    {
      id: "q_j3",
      subjectId: "sub_java",
      difficulty: "Hard",
      question: "What is the memory area allocated for Java Objects?",
      options: ["Stack", "Heap", "Class Area", "Method Area"],
      correctIndex: 1,
      explanation: "All objects in Java are dynamically allocated on the Heap memory."
    },
    {
      id: "q_p1",
      subjectId: "sub_python",
      difficulty: "Easy",
      question: "Which of the following data types is IMMUTABLE in Python?",
      options: ["List", "Dictionary", "Tuple", "Set"],
      correctIndex: 2,
      explanation: "Tuples cannot be altered once created, making them immutable in Python."
    },
    {
      id: "q_p2",
      subjectId: "sub_python",
      difficulty: "Medium",
      question: "What is the output of bool([]) in Python?",
      options: ["True", "False", "None", "TypeError"],
      correctIndex: 1,
      explanation: "Empty sequences (like empty lists) evaluate to False in boolean context."
    },
    {
      id: "q_d1",
      subjectId: "sub_dsa",
      difficulty: "Medium",
      question: "What is the worst-case time complexity of QuickSort?",
      options: ["O(N log N)", "O(N)", "O(N²)", "O(1)"],
      correctIndex: 2,
      explanation: "QuickSort exhibits O(N²) worst-case complexity when the pivot selection is unbalanced (e.g., sorted array with first element pivot)."
    },
    {
      id: "q_d2",
      subjectId: "sub_dsa",
      difficulty: "Hard",
      question: "Which data structure is primarily used to implement Breadth-First Search (BFS) on graphs?",
      options: ["Stack", "Queue", "Priority Queue", "Hash Table"],
      correctIndex: 1,
      explanation: "BFS explores neighbors level-by-level using a FIFO Queue."
    },
    {
      id: "q_db1",
      subjectId: "sub_dbms",
      difficulty: "Medium",
      question: "Which SQL clause is used to filter records AFTER an aggregation GROUP BY?",
      options: ["WHERE", "HAVING", "ORDER BY", "FILTER"],
      correctIndex: 1,
      explanation: "HAVING filters aggregated groups, whereas WHERE filters individual rows before grouping."
    },
    {
      id: "q_p3",
      subjectId: "sub_python",
      difficulty: "Hard",
      question: "Which Python feature guarantees cleanup code runs whether an exception occurs or not?",
      options: ["except block", "finally block", "raise statement", "assert statement"],
      correctIndex: 1,
      explanation: "A finally block runs after try/except processing, including when an exception is raised."
    },
    {
      id: "q_d3",
      subjectId: "sub_dsa",
      difficulty: "Easy",
      question: "What is the time complexity of binary search on a sorted array?",
      options: ["O(log n)", "O(n)", "O(n log n)", "O(1)"],
      correctIndex: 0,
      explanation: "Binary search halves the remaining search interval at each step."
    },
    {
      id: "q_db2",
      subjectId: "sub_dbms",
      difficulty: "Easy",
      question: "Which key uniquely identifies each row in a relational table?",
      options: ["Foreign key", "Primary key", "Composite index", "View key"],
      correctIndex: 1,
      explanation: "A primary key uniquely identifies each row and cannot contain a null value."
    },
    {
      id: "q_os1",
      subjectId: "sub_os",
      difficulty: "Easy",
      question: "Which operating system component selects the next process to run?",
      options: ["Scheduler", "Assembler", "Linker", "Loader"],
      correctIndex: 0,
      explanation: "The CPU scheduler chooses a process from the ready queue for execution."
    },
    {
      id: "q_os2",
      subjectId: "sub_os",
      difficulty: "Medium",
      question: "Which condition is required for deadlock?",
      options: ["Preemption", "Circular wait", "Process termination", "Priority aging"],
      correctIndex: 1,
      explanation: "Circular wait is one of the four necessary Coffman conditions for deadlock."
    },
    {
      id: "q_web1",
      subjectId: "sub_web",
      difficulty: "Easy",
      question: "Which HTML element represents the primary content of a page?",
      options: ["<main>", "<aside>", "<footer>", "<summary>"],
      correctIndex: 0,
      explanation: "The main element identifies the dominant content of the document body."
    },
    {
      id: "q_web2",
      subjectId: "sub_web",
      difficulty: "Medium",
      question: "Which CSS selector has the highest specificity?",
      options: [".menu", "#menu", "nav a", "*"],
      correctIndex: 1,
      explanation: "An ID selector has higher specificity than a class, element, or universal selector."
    },
    {
      id: "q_c1",
      subjectId: "sub_c",
      difficulty: "Easy",
      question: "What does sizeof(char) return in C?",
      options: ["1 byte", "Always 2 bytes", "The pointer size", "The string length"],
      correctIndex: 0,
      explanation: "The C standard defines sizeof(char) as exactly 1 byte."
    },
    {
      id: "q_c2",
      subjectId: "sub_c",
      difficulty: "Medium",
      question: "What value does malloc return when allocation fails?",
      options: ["-1", "NULL", "0 bytes", "An empty string"],
      correctIndex: 1,
      explanation: "malloc returns a null pointer when it cannot allocate the requested memory."
    },
    {
      id: "q_discrete1",
      subjectId: "sub_discrete",
      difficulty: "Easy",
      question: "How many elements are in the power set of a set with 3 elements?",
      options: ["3", "6", "8", "9"],
      correctIndex: 2,
      explanation: "A set with n elements has 2^n subsets, so 2^3 = 8."
    },
    {
      id: "q_discrete2",
      subjectId: "sub_discrete",
      difficulty: "Medium",
      question: "A connected graph with n vertices and n - 1 edges is necessarily a:",
      options: ["Complete graph", "Tree", "Bipartite graph", "Cycle"],
      correctIndex: 1,
      explanation: "A connected, acyclic graph with n vertices has exactly n - 1 edges."
    },
    {
      id: "q_network1",
      subjectId: "sub_networks",
      difficulty: "Easy",
      question: "Which protocol translates domain names into IP addresses?",
      options: ["DNS", "FTP", "SMTP", "ARP"],
      correctIndex: 0,
      explanation: "The Domain Name System resolves human-readable domain names to IP addresses."
    },
    {
      id: "q_network2",
      subjectId: "sub_networks",
      difficulty: "Medium",
      question: "Which transport protocol provides reliable, ordered delivery?",
      options: ["UDP", "IP", "TCP", "ICMP"],
      correctIndex: 2,
      explanation: "TCP uses acknowledgements and sequencing to provide reliable, ordered delivery."
    },
    {
      id: "q_coa1",
      subjectId: "sub_coa",
      difficulty: "Easy",
      question: "Which CPU component performs arithmetic and logical operations?",
      options: ["ALU", "Control unit", "Program counter", "Cache controller"],
      correctIndex: 0,
      explanation: "The arithmetic logic unit performs arithmetic calculations and Boolean operations."
    },
    {
      id: "q_coa2",
      subjectId: "sub_coa",
      difficulty: "Medium",
      question: "Which cache principle describes reusing recently accessed data?",
      options: ["Spatial locality", "Temporal locality", "Sequential consistency", "Virtual addressing"],
      correctIndex: 1,
      explanation: "Temporal locality means data accessed recently is likely to be accessed again soon."
    },
    {
      id: "q_toc1",
      subjectId: "sub_toc",
      difficulty: "Easy",
      question: "Which machine recognizes regular languages?",
      options: ["Finite automaton", "Turing machine only", "SQL engine", "Assembler"],
      correctIndex: 0,
      explanation: "Deterministic and nondeterministic finite automata recognize regular languages."
    },
    {
      id: "q_toc2",
      subjectId: "sub_toc",
      difficulty: "Medium",
      question: "Which abstract machine recognizes context-free languages?",
      options: ["Finite automaton", "Pushdown automaton", "Register only", "Boolean circuit"],
      correctIndex: 1,
      explanation: "A pushdown automaton uses a stack and recognizes context-free languages."
    },
    {
      id: "q_compiler1",
      subjectId: "sub_compiler",
      difficulty: "Easy",
      question: "Which compiler phase groups characters into tokens?",
      options: ["Lexical analysis", "Code generation", "Linking", "Optimization"],
      correctIndex: 0,
      explanation: "The lexical analyzer converts the input character stream into tokens."
    },
    {
      id: "q_compiler2",
      subjectId: "sub_compiler",
      difficulty: "Medium",
      question: "Which compiler phase checks whether tokens follow grammar rules?",
      options: ["Parsing", "Register allocation", "Linking", "Loading"],
      correctIndex: 0,
      explanation: "The parser checks token sequences against the language grammar."
    },
    {
      id: "q_se1",
      subjectId: "sub_se",
      difficulty: "Easy",
      question: "What is the main purpose of requirements analysis?",
      options: ["Understand stakeholder needs", "Compile source code", "Allocate CPU registers", "Encrypt database rows"],
      correctIndex: 0,
      explanation: "Requirements analysis identifies and documents what the system must do."
    },
    {
      id: "q_se2",
      subjectId: "sub_se",
      difficulty: "Medium",
      question: "Which test checks a single function or module in isolation?",
      options: ["Acceptance test", "Unit test", "Load test", "System test"],
      correctIndex: 1,
      explanation: "Unit tests validate small units of code independently."
    },
    {
      id: "q_ai1",
      subjectId: "sub_ai",
      difficulty: "Easy",
      question: "Which learning approach trains a model using labeled examples?",
      options: ["Supervised learning", "Unsupervised learning", "Random search", "Reinforcement only"],
      correctIndex: 0,
      explanation: "Supervised learning uses input examples paired with known target labels."
    },
    {
      id: "q_ai2",
      subjectId: "sub_ai",
      difficulty: "Medium",
      question: "A model performs well on training data but poorly on new data. This is:",
      options: ["Underflow", "Overfitting", "Normalization", "Clustering"],
      correctIndex: 1,
      explanation: "Overfitting occurs when a model memorizes training patterns and generalizes poorly."
    },
    {
      id: "q_security1",
      subjectId: "sub_security",
      difficulty: "Easy",
      question: "Which practice is recommended for storing user passwords?",
      options: ["Store plaintext", "Hash with a salt", "Encode with Base64", "Reuse an encryption key"],
      correctIndex: 1,
      explanation: "Passwords should be stored as salted, one-way password hashes."
    },
    {
      id: "q_security2",
      subjectId: "sub_security",
      difficulty: "Medium",
      question: "What is the best defense against SQL injection in database queries?",
      options: ["Parameterized queries", "Longer table names", "Client-side validation only", "Hiding error messages"],
      correctIndex: 0,
      explanation: "Parameterized queries keep untrusted input separate from SQL syntax."
    },
    {
      id: "q_c3",
      subjectId: "sub_c",
      difficulty: "Medium",
      question: "What is the purpose of the #include directive in C?",
      options: ["Run a loop", "Include a header before compilation", "Allocate heap memory", "Declare a function body"],
      correctIndex: 1,
      explanation: "The preprocessor handles #include by inserting the requested header contents before compilation."
    },
    {
      id: "q_c4",
      subjectId: "sub_c",
      difficulty: "Hard",
      question: "What is the result of modifying the same scalar twice without sequencing in one C expression?",
      options: ["Always zero", "Implementation-defined result", "Undefined behavior", "Compile-time constant"],
      correctIndex: 2,
      explanation: "Unsequenced conflicting side effects on a scalar produce undefined behavior in C."
    },
    {
      id: "q_java4",
      subjectId: "sub_java",
      difficulty: "Medium",
      question: "What is the average time complexity of a HashMap lookup?",
      options: ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
      correctIndex: 0,
      explanation: "HashMap lookups are average O(1), assuming a well-distributed hash function."
    },
    {
      id: "q_python4",
      subjectId: "sub_python",
      difficulty: "Medium",
      question: "Which standard-library tool creates a shallow copy of an object?",
      options: ["copy.copy", "copy.deepcopy only", "json.loads", "itertools.chain"],
      correctIndex: 0,
      explanation: "copy.copy creates a shallow copy while retaining references to nested objects."
    },
    {
      id: "q_dsa4",
      subjectId: "sub_dsa",
      difficulty: "Hard",
      question: "Which shortest-path algorithm is not generally correct when edges may have negative weights?",
      options: ["Dijkstra's algorithm", "Bellman-Ford", "Floyd-Warshall", "Topological relaxation on a DAG"],
      correctIndex: 0,
      explanation: "Dijkstra's greedy choice assumes non-negative edge weights."
    },
    {
      id: "q_discrete3",
      subjectId: "sub_discrete",
      difficulty: "Hard",
      question: "How many edges does the complete graph K5 contain?",
      options: ["5", "8", "10", "20"],
      correctIndex: 2,
      explanation: "A complete graph K_n has n(n - 1)/2 edges; K5 has 10."
    },
    {
      id: "q_db4",
      subjectId: "sub_dbms",
      difficulty: "Hard",
      question: "Which ACID property ensures a transaction is all-or-nothing?",
      options: ["Consistency", "Isolation", "Durability", "Atomicity"],
      correctIndex: 3,
      explanation: "Atomicity ensures all operations in a transaction succeed together or are rolled back."
    },
    {
      id: "q_os3",
      subjectId: "sub_os",
      difficulty: "Hard",
      question: "Paging primarily eliminates which kind of memory fragmentation?",
      options: ["Internal fragmentation", "External fragmentation", "Code fragmentation", "Cache fragmentation"],
      correctIndex: 1,
      explanation: "Fixed-size pages and frames eliminate external fragmentation, though internal fragmentation can remain."
    },
    {
      id: "q_os4",
      subjectId: "sub_os",
      difficulty: "Medium",
      question: "Which synchronization primitive allows only one thread into a critical section at a time?",
      options: ["Mutex", "Page table", "Scheduler queue", "System call"],
      correctIndex: 0,
      explanation: "A mutex provides mutual exclusion for access to a shared critical section."
    },
    {
      id: "q_network3",
      subjectId: "sub_networks",
      difficulty: "Hard",
      question: "How many usable host addresses are in a conventional IPv4 /24 subnet?",
      options: ["24", "128", "254", "256"],
      correctIndex: 2,
      explanation: "A /24 has 256 addresses; the network and broadcast addresses are not assignable to hosts."
    },
    {
      id: "q_coa3",
      subjectId: "sub_coa",
      difficulty: "Hard",
      question: "A pipeline instruction needs a result not yet written by an earlier instruction. This is a:",
      options: ["Structural hazard", "Data hazard", "Control hazard", "Cache miss"],
      correctIndex: 1,
      explanation: "A data hazard occurs when an instruction depends on the result of an earlier instruction."
    },
    {
      id: "q_toc3",
      subjectId: "sub_toc",
      difficulty: "Hard",
      question: "Which classic problem is undecidable for a general-purpose Turing machine?",
      options: ["Finding a DFA transition", "The halting problem", "Checking a finite string", "Sorting a finite list"],
      correctIndex: 1,
      explanation: "The halting problem has no algorithm that decides termination for every program and input."
    },
    {
      id: "q_compiler3",
      subjectId: "sub_compiler",
      difficulty: "Hard",
      question: "Which compiler phase checks that an expression uses compatible types?",
      options: ["Lexical analysis", "Semantic analysis", "Linking", "Code loading"],
      correctIndex: 1,
      explanation: "Semantic analysis checks meaning-related rules, including type compatibility."
    },
    {
      id: "q_se3",
      subjectId: "sub_se",
      difficulty: "Hard",
      question: "Which design goal makes a module easier to change without affecting unrelated modules?",
      options: ["High coupling", "Low cohesion", "Low coupling", "Global state"],
      correctIndex: 2,
      explanation: "Low coupling limits dependencies between modules and reduces change impact."
    },
    {
      id: "q_web3",
      subjectId: "sub_web",
      difficulty: "Hard",
      question: "Which HTTP status code means the requested resource was not found?",
      options: ["200", "301", "403", "404"],
      correctIndex: 3,
      explanation: "HTTP 404 indicates that the requested resource could not be found."
    },
    {
      id: "q_ai3",
      subjectId: "sub_ai",
      difficulty: "Hard",
      question: "Which metric is the harmonic mean of precision and recall?",
      options: ["Accuracy", "F1 score", "Mean squared error", "R-squared"],
      correctIndex: 1,
      explanation: "The F1 score is the harmonic mean of precision and recall."
    },
    {
      id: "q_security3",
      subjectId: "sub_security",
      difficulty: "Hard",
      question: "What does the principle of least privilege require?",
      options: ["Give every user administrator access", "Grant only the access needed for a task", "Share one account across a team", "Disable audit logging"],
      correctIndex: 1,
      explanation: "Least privilege limits each account to the minimum permissions required."
    }
  ],

  results: [
    {
      id: "res_101",
      userId: "usr_student_01",
      subjectId: "sub_java",
      subjectName: "Java Programming",
      difficulty: "Medium",
      totalQuestions: 10,
      correct: 8,
      incorrect: 1,
      skipped: 1,
      scorePct: 80,
      timeSpentMinutes: 12,
      completedAt: "2026-02-10 14:30"
    },
    {
      id: "res_102",
      userId: "usr_student_01",
      subjectId: "sub_dsa",
      subjectName: "Data Structures",
      difficulty: "Hard",
      totalQuestions: 10,
      correct: 7,
      incorrect: 2,
      skipped: 1,
      scorePct: 70,
      timeSpentMinutes: 15,
      completedAt: "2026-02-18 11:15"
    }
  ],

  jobs: [
    {
      id: "job_01",
      company: "TechCorp Solutions",
      title: "Graduate Software Engineer Trainee",
      location: "Bangalore (Hybrid)",
      type: "Full-Time",
      experience: "0 - 1 Years",
      salary: "₹6.5 LPA - ₹8.0 LPA",
      skillsRequired: ["Java", "SQL", "OOP", "Data Structures"],
      description: "We are seeking proactive MCA/B.Tech freshers with strong Java fundamentals and problem-solving skills to join our core backend development team.",
      postedDate: "2026-02-20",
      status: "Active"
    },
    {
      id: "job_02",
      company: "CloudScale Systems",
      title: "Associate Python Developer",
      location: "Pune / Remote",
      type: "Full-Time",
      experience: "0 - 2 Years",
      salary: "₹7.0 LPA - ₹9.5 LPA",
      skillsRequired: ["Python", "Flask", "REST API", "PostgreSQL"],
      description: "Build robust REST APIs and scalable backend microservices using Python and Flask.",
      postedDate: "2026-02-22",
      status: "Active"
    },
    {
      id: "job_03",
      company: "NexGen Innovations",
      title: "Frontend Web Engineer (Junior)",
      location: "Hyderabad",
      type: "Full-Time",
      experience: "0 - 1 Years",
      salary: "₹5.5 LPA - ₹7.2 LPA",
      skillsRequired: ["JavaScript", "HTML5", "CSS3", "Bootstrap"],
      description: "Develop responsive and performant enterprise web applications with modern UX/UI standards.",
      postedDate: "2026-02-25",
      status: "Active"
    },
    {
      id: "job_04",
      company: "Vector Insights",
      title: "Junior Data Analyst",
      location: "Bengaluru / Hybrid",
      type: "Full-Time",
      experience: "0 - 1 Years",
      salary: "₹5.0 LPA - ₹7.0 LPA",
      skillsRequired: ["SQL", "Python", "Excel", "Data Visualization"],
      description: "Prepare data reports and dashboards that help product teams make informed decisions.",
      postedDate: "2026-03-02",
      status: "Active"
    },
    {
      id: "job_05",
      company: "QualityHub Technologies",
      title: "Associate Quality Assurance Engineer",
      location: "Chennai",
      type: "Full-Time",
      experience: "0 - 1 Years",
      salary: "₹4.5 LPA - ₹6.5 LPA",
      skillsRequired: ["Software Testing", "Java", "Selenium", "API Testing"],
      description: "Build test cases and help validate reliable web applications across releases.",
      postedDate: "2026-03-04",
      status: "Active"
    },
    {
      id: "job_06",
      company: "ByteCloud Services",
      title: "Cloud and DevOps Trainee",
      location: "Pune / Remote",
      type: "Full-Time",
      experience: "Fresher",
      salary: "₹6.0 LPA - ₹8.0 LPA",
      skillsRequired: ["Linux", "Docker", "AWS", "CI/CD"],
      description: "Support cloud deployments and automate repeatable build and release workflows.",
      postedDate: "2026-03-06",
      status: "Active"
    },
    {
      id: "job_07",
      company: "InsightAI Labs",
      title: "AI and Machine Learning Engineer Trainee",
      location: "Hyderabad / Hybrid",
      type: "Full-Time",
      experience: "0 - 1 Years",
      salary: "₹7.0 LPA - ₹10.0 LPA",
      skillsRequired: ["Python", "Machine Learning", "Statistics", "Pandas"],
      description: "Assist with data preparation, model experiments, and evaluation for applied AI products.",
      postedDate: "2026-03-08",
      status: "Active"
    },
    {
      id: "job_08",
      company: "Sentinel Security",
      title: "Cybersecurity Analyst Associate",
      location: "New Delhi",
      type: "Full-Time",
      experience: "0 - 2 Years",
      salary: "₹5.5 LPA - ₹8.0 LPA",
      skillsRequired: ["Networking", "Linux", "Security Monitoring", "Incident Response"],
      description: "Monitor security events and support vulnerability assessment and incident response.",
      postedDate: "2026-03-10",
      status: "Active"
    }
  ],

  applications: [
    {
      id: "app_01",
      userId: "usr_student_01",
      jobId: "job_01",
      company: "TechCorp Solutions",
      jobTitle: "Graduate Software Engineer Trainee",
      appliedDate: "2026-02-24",
      status: "Under Review"
    }
  ],

  notifications: [
    {
      id: "notif_01",
      userId: "usr_student_01",
      title: "Mock Test Completed",
      message: "You scored 80% on Java Programming (Medium). Great job!",
      time: "2 hours ago",
      read: false
    },
    {
      id: "notif_02",
      userId: "usr_student_01",
      title: "New Career Match",
      message: "CloudScale Systems posted a job matching your Python skills.",
      time: "1 day ago",
      read: true
    }
  ]
};

// Initialize Mock Data in LocalStorage if missing
(function initLocalStorage() {
  const mergeMissingRecords = (storageKey, defaults) => {
    const existing = JSON.parse(localStorage.getItem(storageKey) || "[]");
    const existingIds = new Set(existing.map(item => item.id));
    const additions = defaults.filter(item => !existingIds.has(item.id));
    const merged = [...existing, ...additions];
    if (additions.length) localStorage.setItem(storageKey, JSON.stringify(merged));
    return merged;
  };

  if (!localStorage.getItem("smt_users")) {
    localStorage.setItem("smt_users", JSON.stringify(DEFAULT_MOCK_DATA.users));
  }
  const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
  const admin = users.find(user => user.id === "usr_admin_01");
  if (admin) {
    admin.email = "vartikachaudhary0312@gmail.com";
    admin.password = "Vartika1234@";
    localStorage.setItem("smt_users", JSON.stringify(users));
  }
  const subjects = mergeMissingRecords("smt_subjects", DEFAULT_MOCK_DATA.subjects);
  const questions = mergeMissingRecords("smt_questions", DEFAULT_MOCK_DATA.questions);
  subjects.forEach(subject => {
    subject.questionCount = subject.id === "sub_cse_comprehensive"
      ? 50
      : questions.filter(question => question.subjectId === subject.id).length;
  });
  localStorage.setItem("smt_subjects", JSON.stringify(subjects));
  if (!localStorage.getItem("smt_results")) {
    localStorage.setItem("smt_results", JSON.stringify(DEFAULT_MOCK_DATA.results));
  }
  mergeMissingRecords("smt_jobs", DEFAULT_MOCK_DATA.jobs);
  if (!localStorage.getItem("smt_applications")) {
    localStorage.setItem("smt_applications", JSON.stringify(DEFAULT_MOCK_DATA.applications));
  }
  if (!localStorage.getItem("smt_notifications")) {
    localStorage.setItem("smt_notifications", JSON.stringify(DEFAULT_MOCK_DATA.notifications));
  }
})();
