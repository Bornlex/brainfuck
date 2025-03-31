prompt = """
You are a programming problem teacher, you provide with problems and their solutions.

The problems need to be simple so a Turing incomplete programming language is enough to solve them.

It is very important that you follow this format when outputing a problem:
{"problem": "Print the sum of 3 and 5.", "solution": "8"}

The output format is a JSON object made of two keys:
- problem: a string containing the problem
- solution: a string containing the solution.
"""

examples = [
    '{"problem": "compute the sum of 3 and 5", "solution": "8"}',
    '{"problem": "multiply 56 by 2", "solution": "112"}',
    '{"problem": "compute the sum of 3 and 5", "solution": "8"}',
    '{"problem": "Print 7 times the letter a.", "solution": "aaaaaaa"}',
    '{"problem": "Display Hello world on screen", "solution": "Hello world"}',
    '{"problem": "Reverse the string banana", "solution": "ananab"}',
    '{"problem": "count the characters in the word solution", "solution": "8"}',
    '{"problem": "Return the maximum of 5 and 12", "solution": "12"}',
    '{"problem": "Divide 17 by 5", "solution": "3.4"}',
    '{"problem": "Concatenate the following strings: \"welcome\" and \"home\"", "solution": "welcome home"}',
    '{"problem": "say hi", "solution": "hi"}',
    '{"problem": "what is the letter after g", "solution": "h"}',
    '{"problem": "subtract 33 from 20", "solution": "-13"}',
]
