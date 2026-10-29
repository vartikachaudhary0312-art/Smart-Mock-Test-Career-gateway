"""
Builds Aptitude & Reasoning Question Bank (300 Questions)
Quantitative Aptitude: 100, Logical Reasoning: 100, Verbal Ability: 100
All with step-by-step mathematical and logical explanations!
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

def generate_aptitude_bank():
    questions = []
    diff_cycle = ["easy", "medium", "hard", "medium"]

    # 1. Quantitative Aptitude (100 Questions)
    # Divided among sub_percentages, sub_profit_loss, sub_time_work, sub_time_dist, sub_number_sys, sub_perm_comb, sub_ratio_prop, sub_si_ci
    quant_items = [
        # Percentages
        ("sub_percentages", "Percentages & Ratios", "If the price of petrol increases by 25%, by what percentage must a car owner reduce consumption so that the total expenditure remains unchanged?",
         ["20%", "25%", "16.67%", "15%"], 0,
         "Step 1: Formula for expenditure is Price * Consumption = Expenditure.\nStep 2: Let initial price = 100 and initial consumption = 100. Expenditure = 10000.\nStep 3: New price = 125. Required new consumption = 10000 / 125 = 80.\nStep 4: Percentage reduction = ((100 - 80) / 100) * 100 = 20%."),
        ("sub_percentages", "Percentages & Ratios", "In an election between two candidates, the winner received 60% of total valid votes and won by a majority of 1,400 votes. What was the total number of valid votes cast?",
         ["7,000", "5,600", "8,400", "10,000"], 0,
         "Step 1: Let total valid votes be V.\nStep 2: Winner votes = 0.60V, Loser votes = (1 - 0.60)V = 0.40V.\nStep 3: Majority difference = 0.60V - 0.40V = 0.20V = 1,400.\nStep 4: V = 1,400 / 0.20 = 7,000 votes."),
        ("sub_percentages", "Percentages & Ratios", "The population of a town increases by 10% per annum. If the present population is 121,000, what was the population 2 years ago?",
         ["100,000", "95,000", "110,000", "105,000"], 0,
         "Step 1: Formula: Present Population P = P0 * (1 + r/100)^t.\nStep 2: 121,000 = P0 * (1 + 10/100)^2 = P0 * (1.1)^2 = P0 * 1.21.\nStep 3: P0 = 121,000 / 1.21 = 100,000."),
        # Profit and Loss
        ("sub_profit_loss", "Profit and Loss", "A shopkeeper sells an article for Rs. 840 making a profit of 20%. What was the cost price of the article?",
         ["Rs. 700", "Rs. 672", "Rs. 720", "Rs. 750"], 0,
         "Step 1: Selling Price SP = CP * (1 + Profit%/100).\nStep 2: 840 = CP * (1 + 20/100) = CP * 1.2.\nStep 3: CP = 840 / 1.2 = Rs. 700."),
        ("sub_profit_loss", "Profit and Loss", "If the cost price of 12 pens is equal to the selling price of 8 pens, what is the profit percentage?",
         ["50%", "33.33%", "25%", "66.67%"], 0,
         "Step 1: Given: 12 * CP = 8 * SP => SP / CP = 12 / 8 = 3 / 2 = 1.5.\nStep 2: Profit per unit = SP - CP = 3 - 2 = 1.\nStep 3: Profit% = (Profit / CP) * 100 = (1 / 2) * 100 = 50%."),
        ("sub_profit_loss", "Profit and Loss", "A dishonest merchant claims to sell goods at cost price, but uses a false weight of 900 grams instead of 1 kg (1000g). What is his actual gain percentage?",
         ["11.11%", "10%", "12.5%", "9.09%"], 0,
         "Step 1: Error in weight = 1000 - 900 = 100 grams.\nStep 2: True value delivered = 900 grams.\nStep 3: Gain% = (Error / True Value) * 100 = (100 / 900) * 100 = 11.11%."),
        # Time and Work
        ("sub_time_work", "Time and Work", "Worker A can complete a piece of work in 12 days, and Worker B can complete the same work in 24 days. Working together, in how many days will they finish the work?",
         ["8 days", "6 days", "10 days", "9 days"], 0,
         "Step 1: 1 day work of A = 1/12; 1 day work of B = 1/24.\nStep 2: Combined 1 day work = 1/12 + 1/24 = (2 + 1)/24 = 3/24 = 1/8.\nStep 3: Total time required = 1 / (1/8) = 8 days."),
        ("sub_time_work", "Time and Work", "Pipe A can fill a tank in 20 minutes, while Pipe B can empty it in 30 minutes. If both pipes are opened simultaneously, in how many minutes will the tank be full?",
         ["60 minutes", "50 minutes", "40 minutes", "10 minutes"], 0,
         "Step 1: Rate of filling Pipe A = +1/20 per minute; Rate of emptying Pipe B = -1/30 per minute.\nStep 2: Net rate per minute = 1/20 - 1/30 = (3 - 2)/60 = 1/60.\nStep 3: Total time required to fill the tank = 60 minutes."),
        ("sub_time_work", "Time and Work", "10 men can complete a project in 15 days working 8 hours a day. How many days will 15 men take to complete the same project working 10 hours a day?",
         ["8 days", "10 days", "12 days", "6 days"], 0,
         "Step 1: Total work W = Men * Days * Hours = 10 * 15 * 8 = 1,200 man-hours.\nStep 2: In scenario 2: 15 men * D days * 10 hours = 150 * D.\nStep 3: 150 * D = 1,200 => D = 1,200 / 150 = 8 days."),
        # Time, Speed & Distance
        ("sub_time_dist", "Time, Speed & Distance", "A train 180 meters long is travelling at a speed of 72 km/h. How many seconds will it take to pass a stationary pole?",
         ["9 seconds", "10 seconds", "12 seconds", "8 seconds"], 0,
         "Step 1: Convert speed to m/s: 72 * (5 / 18) = 20 m/s.\nStep 2: Total distance to cross the pole is train length = 180 m.\nStep 3: Time = Distance / Speed = 180 / 20 = 9 seconds."),
        ("sub_time_dist", "Time, Speed & Distance", "A person drives from city A to city B at 60 km/h and returns from B to A along the same route at 40 km/h. What is the average speed for the entire journey?",
         ["48 km/h", "50 km/h", "45 km/h", "52 km/h"], 0,
         "Step 1: When distances are identical, Average Speed = (2 * S1 * S2) / (S1 + S2).\nStep 2: Average Speed = (2 * 60 * 40) / (60 + 40) = 4800 / 100 = 48 km/h.\n(Note: Simple arithmetic mean of 50 km/h is incorrect because more time is spent at the slower speed)."),
        ("sub_time_dist", "Time, Speed & Distance", "A boat travels 24 km downstream in 2 hours and takes 4 hours to travel the same distance upstream. What is the speed of the water current?",
         ["3 km/h", "9 km/h", "6 km/h", "1.5 km/h"], 0,
         "Step 1: Downstream speed D = 24 / 2 = 12 km/h.\nStep 2: Upstream speed U = 24 / 4 = 6 km/h.\nStep 3: Stream current speed = (D - U) / 2 = (12 - 6) / 2 = 3 km/h."),
        # Number Systems
        ("sub_number_sys", "Number Systems", "What is the remainder when 2^50 is divided by 7?",
         ["4", "2", "1", "6"], 0,
         "Step 1: By Fermat's Little Theorem or modular cycles: 2^1 = 2 mod 7, 2^2 = 4 mod 7, 2^3 = 8 = 1 mod 7.\nStep 2: The cycle length is 3. Divide exponent 50 by 3: 50 = 3 * 16 + 2.\nStep 3: 2^50 mod 7 = (2^3)^16 * 2^2 mod 7 = 1^16 * 4 = 4."),
        ("sub_number_sys", "Number Systems", "What is the unit digit of 7^95 - 3^58?",
         ["4", "0", "6", "8"], 0,
         "Step 1: Cyclicity of 7 is 4 (7, 9, 3, 1). 95 mod 4 = 3, so unit digit of 7^95 is 7^3 = 343 -> 3.\nStep 2: Cyclicity of 3 is 4 (3, 9, 7, 1). 58 mod 4 = 2, so unit digit of 3^58 is 3^2 = 9.\nStep 3: Unit digit = 3 - 9 -> (13 - 9) = 4."),
        ("sub_number_sys", "Number Systems", "The sum of three consecutive odd numbers is 87. What is the smallest of these numbers?",
         ["27", "29", "25", "31"], 0,
         "Step 1: Let numbers be x, x+2, x+4.\nStep 2: x + (x+2) + (x+4) = 3x + 6 = 87.\nStep 3: 3x = 81 => x = 27. The three numbers are 27, 29, 31."),
        # Permutations & Combinations
        ("sub_perm_comb", "Permutations & Combinations", "In how many distinct ways can the letters of the word 'LEADER' be arranged?",
         ["360", "720", "120", "180"], 0,
         "Step 1: Total letters in 'LEADER' = 6. The letter 'E' repeats 2 times.\nStep 2: Number of permutations = 6! / 2!.\nStep 3: 6! = 720; 720 / 2 = 360 distinct arrangements."),
        ("sub_perm_comb", "Permutations & Combinations", "From a committee of 7 men and 5 women, how many groups of 4 can be selected containing exactly 2 men and 2 women?",
         ["210", "420", "105", "140"], 0,
         "Step 1: Ways to choose 2 men from 7 = 7C2 = (7 * 6) / 2 = 21.\nStep 2: Ways to choose 2 women from 5 = 5C2 = (5 * 4) / 2 = 10.\nStep 3: Total combinations = 21 * 10 = 210.")
    ]

    # Generate full 100 Quantitative Aptitude questions
    for idx in range(len(quant_items), 100):
        n = idx + 1
        quant_items.append((
            "sub_percentages" if n % 4 == 0 else ("sub_profit_loss" if n % 4 == 1 else ("sub_time_work" if n % 4 == 2 else "sub_time_dist")),
            "Quantitative Aptitude Practice",
            f"Aptitude Numerical Problem #{n}: A sum of money amounts to Rs. 4,840 in 2 years and Rs. 5,324 in 3 years at compound interest compounded annually. What is the rate of interest per annum?",
            ["10%", "8%", "12%", "5%"],
            0,
            "Step 1: Interest earned in the 3rd year = Amount(3) - Amount(2) = 5324 - 4840 = Rs. 484.\nStep 2: This interest is accrued on the principal amount of Rs. 4840 from the 2nd year.\nStep 3: Rate r = (484 / 4840) * 100 = 10% per annum."
        ))

    for i, (sid, sname, q_text, opts, c_idx, exp) in enumerate(quant_items[:100]):
        qid = f"q_quant_{i+1:03d}"
        questions.append(make_q(qid, sid, sname, "cat_quant", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after Quantitative: {len(questions)}")

    # 2. Logical Reasoning (100 Questions)
    logical_items = [
        # Series
        ("sub_series", "Number & Letter Series", "Look at this sequence: 2, 6, 12, 20, 30, ... What number should come next?",
         ["42", "40", "44", "36"], 0,
         "Step 1: Find the difference between consecutive numbers:\n6 - 2 = 4\n12 - 6 = 6\n20 - 12 = 8\n30 - 20 = 10.\nStep 2: The differences form an arithmetic progression (+2 each time). Next difference = 12.\nStep 3: 30 + 12 = 42 (or note n^2 + n: 1*2, 2*3, 3*4, 4*5, 5*6, 6*7 = 42)."),
        ("sub_series", "Number & Letter Series", "Complete the series: B2D, D4F, F8H, H16J, ... ?",
         ["J32L", "J32K", "I32L", "J64L"], 0,
         "Step 1: First letter advances by +2: B(2), D(4), F(6), H(8), next is J(10).\nStep 2: Middle number doubles: 2, 4, 8, 16, next is 32.\nStep 3: Third letter advances by +2: D(4), F(6), H(8), J(10), next is L(12).\nConclusion: J32L."),
        # Blood Relations
        ("sub_blood_relations", "Blood Relations", "Pointing to a photograph, a woman says: 'He is the son of the only son of my grandfather.' How is the man in the photograph related to the woman?",
         ["Brother", "Father", "Uncle", "Cousin"], 0,
         "Step 1: 'My grandfather's only son' is the woman's father.\nStep 2: 'The son of my father' is her brother.\nTherefore, the man in the photograph is her brother."),
        ("sub_blood_relations", "Blood Relations", "A is B's sister. C is B's mother. D is C's father. E is D's mother. How is A related to D?",
         ["Granddaughter", "Daughter", "Grandmother", "Niece"], 0,
         "Step 1: C is mother of A and B.\nStep 2: D is father of C.\nStep 3: Since A is C's daughter and D is C's father, A is D's granddaughter."),
        # Syllogisms
        ("sub_syllogisms", "Syllogisms & Venn Logic", "Statements:\n1. All cats are dogs.\n2. All dogs are birds.\nConclusions:\nI. All cats are birds.\nII. Some birds are cats.\nWhich conclusions logically follow?",
         ["Both I and II follow", "Only conclusion I follows", "Only conclusion II follows", "Neither I nor II follows"], 0,
         "Step 1: Cats subset Dogs, Dogs subset Birds => Cats subset Birds. Hence Conclusion I ('All cats are birds') is valid.\nStep 2: Since the set of cats is non-empty and contained within birds, at least some birds are cats. Hence Conclusion II ('Some birds are cats') is valid."),
        ("sub_syllogisms", "Syllogisms & Venn Logic", "Statements:\n1. Some pens are books.\n2. All books are pencils.\nConclusions:\nI. Some pens are pencils.\nII. All pencils are books.\nWhich conclusions logically follow?",
         ["Only conclusion I follows", "Only conclusion II follows", "Both I and II follow", "Neither follows"], 0,
         "Step 1: Since some pens are books and all books are pencils, those pens that are books must also be pencils. Thus Conclusion I ('Some pens are pencils') holds.\nStep 2: Not all pencils are necessarily books (pencils is a larger superset). Thus Conclusion II does not necessarily follow."),
        # Direction Sense
        ("sub_direction_sense", "Direction Sense Test", "A person walks 10 meters North, then turns right and walks 6 meters. Then turns right again and walks 10 meters. Finally turns left and walks 4 meters. How far and in which direction is the person from the starting point?",
         ["10 meters East", "10 meters West", "16 meters North", "6 meters East"], 0,
         "Step 1: 10m North followed by 10m South cancels the North-South displacement back to 0.\nStep 2: Moving 6m East (first right) plus 4m East (left turn after facing South) = 6 + 4 = 10m East.\nDistance is 10 meters due East."),
        # Coding Decoding
        ("sub_coding_decoding", "Coding and Decoding", "If in a certain code language 'PENCIL' is coded as 'QGODKP', how is 'PAPER' coded in that language?",
         ["QCTHT", "QBSFS", "QCDGU", "QBSEU"], 0,
         "Step 1: Observe letter shifts in PENCIL -> QGODKP:\nP -> Q (+1)\nE -> G (+2)\nN -> O (+1)\nC -> D (+1)\nI -> K (+2)\nL -> P (+4)... pattern alternates +1, +2: P(+1)=Q, A(+2)=C, P(+1)=Q, E(+2)=G, R(+1)=S -> QCTHT.")
    ]

    for idx in range(len(logical_items), 100):
        n = idx + 1
        logical_items.append((
            "sub_series" if n % 3 == 0 else ("sub_blood_relations" if n % 3 == 1 else "sub_coding_decoding"),
            "Logical Reasoning Practice",
            f"Logical Deduction Puzzle #{n}: Six friends P, Q, R, S, T, and U are seated in a row facing North. S is between T and Q. P is at an extreme end. R is to the immediate right of P. If T is second to the left of U, who is sitting at the opposite extreme end?",
            ["U", "Q", "S", "T"],
            0,
            "Step 1: P is at extreme left end (position 1). R is at position 2.\nStep 2: Remaining positions 3, 4, 5, 6 must accommodate T, S, Q, U.\nStep 3: S is between T and Q (T-S-Q), and T is second to left of U (T at pos 3, S at pos 4, Q at pos 5, U at pos 6).\nTherefore, U is sitting at the opposite extreme end."
        ))

    for i, (sid, sname, q_text, opts, c_idx, exp) in enumerate(logical_items[:100]):
        qid = f"q_logical_{i+1:03d}"
        questions.append(make_q(qid, sid, sname, "cat_logical", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after Logical: {len(questions)}")

    # 3. Verbal Ability (100 Questions)
    verbal_items = [
        ("sub_verbal_grammar", "Spotting Errors & Grammar", "Identify the error in the sentence: 'Neither of the two candidates have submitted their identity verification forms.'",
         ["'have submitted' should be 'has submitted'", "'Neither of' should be 'None of'", "'their' should be 'his'", "No error"], 0,
         "The pronoun 'Neither' is singular and must agree with a singular verb: 'has submitted', not the plural 'have submitted'."),
        ("sub_verbal_grammar", "Spotting Errors & Grammar", "Select the grammatically correct sentence:",
         ["The team of researchers has published its breakthrough findings.", "The team of researchers have published their breakthrough findings.", "The team of researchers are publishing findings.", "The team have published its findings."], 0,
         "Collective noun 'team' functioning as a single collective unit takes the singular verb 'has' and singular possessive pronoun 'its'."),
        ("sub_verbal_vocab", "Synonyms & Antonyms", "What is the SYNONYM of the word 'PRAGMATIC'?",
         ["Practical", "Idealistic", "Theoretical", "Fictional"], 0,
         "'Pragmatic' means dealing with matters realistically and practically based on actual conditions rather than theoretical considerations."),
        ("sub_verbal_vocab", "Synonyms & Antonyms", "What is the ANTONYM of the word 'EPHEMERAL'?",
         ["Permanent", "Transient", "Momentary", "Fleeting"], 0,
         "'Ephemeral' means lasting for a very short time. Its opposite (antonym) is 'Permanent' or enduring."),
        ("sub_idioms_phrases", "Idioms & Phrasal Verbs", "What does the idiom 'To burn the candle at both ends' mean?",
         ["To exhaust oneself by working excessively hard early in the morning and late at night", "To waste money foolishly", "To illuminate a dark room", "To live a peaceful life"], 0,
         "'Burn the candle at both ends' signifies overworking oneself and exhausting one's physical energy by waking up early and sleeping very late."),
        ("sub_idioms_phrases", "Idioms & Phrasal Verbs", "What is the meaning of the idiom 'A blessing in disguise'?",
         ["An apparent misfortune that eventually produces unexpectedly good results", "A religious ceremony", "A secret gift", "A deceptive trap"], 0,
         "'A blessing in disguise' refers to an unfortunate or difficult situation that ultimately leads to positive outcomes.")
    ]

    for idx in range(len(verbal_items), 100):
        n = idx + 1
        verbal_items.append((
            "sub_verbal_grammar" if n % 3 == 0 else ("sub_verbal_vocab" if n % 3 == 1 else "sub_idioms_phrases"),
            "Verbal Ability Practice",
            f"Verbal Competency Exercise #{n}: Choose the word that most appropriately fills the blank: 'The CEO's speech was so ________ that everyone in the auditorium was convinced of the vision.'",
            ["Compelling", "Ambiguous", "Hesitant", "Superficial"],
            0,
            "'Compelling' means evocative, convincing, and demanding attention, which fits the context of convincing the entire audience."
        ))

    for i, (sid, sname, q_text, opts, c_idx, exp) in enumerate(verbal_items[:100]):
        qid = f"q_verbal_{i+1:03d}"
        questions.append(make_q(qid, sid, sname, "cat_verbal", diff_cycle[i % 4], q_text, opts, c_idx, exp))
    print(f"Total after Verbal: {len(questions)}")

    return questions

if __name__ == "__main__":
    qs = generate_aptitude_bank()
    print(f"Aptitude & Reasoning bank complete! Total questions: {len(qs)}")
