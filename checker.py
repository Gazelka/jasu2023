import sympy
#global
open_brackets=['(','{','[']
close_brackets=[')','}',']']

def get_type_of_brackets(c):
    if c in open_brackets:
        return open_brackets.index(c)
    elif c in close_brackets:
        return close_brackets.index(c)

def syntax_validator(s):
    a=[]
    for i in s:
        if i in open_brackets:
            a.append(i)
        elif i in close_brackets:
            if len(a)==0:
                return False
            if get_type_of_brackets(i)==get_type_of_brackets(a[len(a)-1]):
                a.pop()
            else:
                return False
    if len(a)==0:
        return True
    return False
    pass

if __name__ == '__main__':
    s = input()
    if not syntax_validator(s):
        print("Invalid")
        exit()
    
    expr = sympy.sympify(s)
    print(expr)

