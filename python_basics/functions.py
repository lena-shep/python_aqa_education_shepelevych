# Functions
def list_benefits():
    return "More organized code", "More readable code", "Easier code reuse", "Allowing programmers to share and connect code together"


# Modify this function to concatenate to each benefit - " is a benefit of functions!"
def build_sentence(benefit):
    return "%s, is a benefit of functions" % benefit


def name_the_benefits_of_functions():
    """Print sentence from two functions"""
    list_of_benefits = list_benefits()
    for benefit in list_of_benefits:
        print(build_sentence(benefit))


name_the_benefits_of_functions()


# Multiple Function Arguments
def foo(a, b, c, *more):
    """Function for variable numbers of arguments"""
    return len(more)


def bar(a, b, c, **more):
    """Function for variable numbers of arguments with keyword."""
    if more.get("magicnumber") == 7:
        return True
    else:
        return False


if foo(1, 2, 3, 4) == 1:
    print("Good.")
if foo(1, 2, 3, 4, 5) == 2:
    print("Better.")
if bar(1, 2, 3, magicnumber=6) == False:
    print("Great.")
if bar(1, 2, 3, magicnumber=7) == True:
    print("Awesome!")
