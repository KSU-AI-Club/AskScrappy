# Prototyping
#
# Note to reader: This code partially works at this time -- logic needs to be 
# refined for some paths -- listed in problematic_paths.txt
#
# This code is really rough around the edges and could definitely benefit from
# refactoring, and the current solution is without a doubt not-optimal.
# But first, we have to try to get something that works
#
q1 = "What was your favorite subject in high school? (math, science, literature, history, art):  "
q2 = "How do you derive meaning in your life? (through work, family and friends):  "
q3 = "Do you prefer to work with people or by yourself? (with people, solo):  "
q4_1 = "Would you like to work in education? (yes, no):  "
q4_2 = "Would you rather be wealthy or respected by your peers? (wealthy, respected):  "
q5_1 = "Which age group? (elementary, middle, high, college):  "
q5_2 = "Do you like computers? (yes, no):  "
q5_3 = "Would you like to explore cultures or people in general? (cultures, general):  "

level = 1
ext_flag = False
edu_flag = False
math_flag = False
lit_flag = False
lit_woke_flag = False
hist_flag = False


class TreeNode:
    def __init__(self, question):
        self.question = question
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def get_child(node, index):
    if index < len(node.children):
        return node.children[index]
    else:
        return None

def print_tree(node, level=0):
    print(" " * level + str(node.question))
    for child in node.children:
        print_tree(child, level + 1)

def conditional_traversal(node):
    global level
    global ext_flag
    global edu_flag
    global math_flag
    global lit_flag
    global lit_woke_flag
    global hist_flag

    user_input = input(node.question)
    # Requires Python > 3.10
    match level:
        case 1: 
            match user_input: 
                case "math":
                    math_flag = True
                    # There's probably a more readable way to do this but for MVP sake:
                    level += 1
                    conditional_traversal(get_child(node, 0))

                case "science":
                    level += 1
                    conditional_traversal(get_child(node, 1))

                case "literature":
                    level += 1
                    conditional_traversal(get_child(node, 2))
                    
                case "history":
                    hist_flag = True
                    level += 1
                    conditional_traversal(get_child(node, 3))

                case "art":
                    level += 1
                    conditional_traversal(get_child(node, 4))

                case _ :
                    print("Unable to read user input")
        case 2: 
            match user_input: 
                case "through work":
                    level += 1
                    conditional_traversal(get_child(node, 0))

                case "family and friends":
                    level += 1
                    conditional_traversal(get_child(node, 1))

                case _:
                    print("Unable to read user input")

        case 3: 
            match user_input:
                case "with people":
                    ext_flag = True
                    level += 1
                    conditional_traversal(get_child(node, 0))

                case "solo":
                    level += 1
                    conditional_traversal(get_child(node, 1))

                case _:
                    print("Unable to read user input")
        case 4: 
            if ext_flag: # Education
                match user_input:
                    case "yes":
                        edu_flag = True
                        level += 1
                        conditional_traversal(get_child(node, 0))

                    case "no":
                        if lit_flag:
                            level += 1
                            conditional_traversal(get_child(node, 1))
                        else:
                            print(f"Your major should be: {get_child(node, 1).question}")

                    case _:
                        print("Unable to read user input")
            else:
                match user_input: # Respect or money
                    case "wealthy":
                        if math_flag:
                            conditional_traversal(get_child(node, 0))
                        else:
                            print(f"Your major should be: {get_child(node, 0).question}")

                    case "respected":
                        if lit_flag:
                            level += 1
                            conditional_traversal(get_child(node, 1))
                        else:
                            print(f"Your major should be: {get_child(node, 1).question}")

                    case _:
                        print("Unable to read user input")
        case 5:
            if edu_flag: # age group
                match user_input:
                    case "elementary":
                        print(f"Your major should be: {get_child(node, 0).question}")
                        return

                    case "middle":
                        print(f"Your major should be: {get_child(node, 1).question}")
                        return

                    case "high":
                        print(f"Your major should be: {get_child(node, 2).question}")
                        return

                    case "college":
                        print(f"Your major should be: {get_child(node, 3).question}")
                        return

                    case _:
                        print("Unable to read user input")
            elif (not edu_flag) and math_flag: # Introverted math person interested in computers? 
                match user_input:
                    case "yes":
                        print(f"Your major should be: {get_child(node, 0).question}")
                        return

                    case "no":
                        print(f"Your major should be: {get_child(node, 1).question}")
                        return

                    case _:
                        print("Unable to read user input")
            else:
                match user_input: # In one of lit's longest paths
                    case "wealthy":
                        print(f"Your major should be:{get_child(node, 0).question}")
                        return
                    case "respected":
                        if lit_woke_flag:
                            level += 1
                            conditional_traversal(get_child(node, 1))
                        else: 
                            print(f"Your major should be: {get_child(node, 1).question}")
                            return

                    case _:
                        print("Unable to read user input")
        case 7:
            match user_input: # Still in lit's longest path
                case "cultures":
                    print(f"Your major should be:{get_child(node, 0).question}")
                    return

                case "general":
                    print(f"Your major should be:{get_child(node, 1).question}")
                    return

                case _:
                    print("Unable to read user input")
        case _:
            print("Some unknown error has occurred. Try again")

def traverse():
    print("Hi there, I'm Scruffy! I'm going to ask you a few questions to help you narrow down your major.")
    print("Please try to remember to enter all your answers in lowercase.")
    print("Let's go!")
    print(" ")
    conditional_traversal(root)

# Define Tree
#
# I could make this much less verbose but for readibility sake, I'll leave the
# variable instantiations
#
# First Level
root = TreeNode(q1)

# Second Level
math = TreeNode(q2)
sci = TreeNode(q2)
lit = TreeNode(q2)
hist = TreeNode(q2)
art = TreeNode(q2)

root.add_child(math)
root.add_child(sci)
root.add_child(lit)
root.add_child(hist)
root.add_child(art)

# Third Level
math_work = TreeNode(q3)
sci_work = TreeNode(q3)
lit_work = TreeNode(q3)
hist_work = TreeNode(q3)
art_work = TreeNode(q3)

math_fam = TreeNode(q3)
sci_fam = TreeNode(q3)
lit_fam = TreeNode(q3)
hist_fam = TreeNode(q3)
art_fam = TreeNode(q3)

math.add_child(math_work)
math.add_child(math_fam)
sci.add_child(sci_work)
sci.add_child(sci_fam)
lit.add_child(lit_work)
lit.add_child(lit_fam)
hist.add_child(hist_work)
hist.add_child(hist_fam)
art.add_child(art_work)
art.add_child(art_fam)

# Fourth Level
math_work_ext = TreeNode(q4_1)
sci_work_ext = TreeNode(q4_1)
lit_work_ext = TreeNode(q4_1)
hist_work_ext = TreeNode(q4_1)
art_work_ext = TreeNode(q4_1)

math_work_int = TreeNode(q4_2)
sci_work_int = TreeNode(q4_2)
lit_work_int = TreeNode(q4_2)
hist_work_int = TreeNode(q4_2)
art_work_int = TreeNode(q4_2)

math_fam_ext = TreeNode(q4_1)
sci_fam_ext = TreeNode(q4_1)
lit_fam_ext = TreeNode(q4_1)
hist_fam_ext = TreeNode(q4_1)
art_fam_ext = TreeNode(q4_1)

math_fam_int = TreeNode(q4_2)
sci_fam_int = TreeNode(q4_2)
lit_fam_int = TreeNode(q4_2)
hist_fam_int = TreeNode(q4_2)
art_fam_int = TreeNode(q4_2)

math_work.add_child(math_work_ext)
math_work.add_child(math_work_int)
math_fam.add_child(math_fam_ext)
math_fam.add_child(math_fam_int)

sci_work.add_child(sci_work_ext)
sci_work.add_child(sci_work_int)
sci_fam.add_child(sci_fam_ext)
sci_fam.add_child(sci_fam_int)

lit_work.add_child(lit_work_ext)
lit_work.add_child(lit_work_int)
lit_fam.add_child(lit_fam_ext)
lit_fam.add_child(lit_fam_int)

hist_work.add_child(hist_work_ext)
hist_work.add_child(hist_work_ext)
hist_fam.add_child(hist_fam_int)
hist_fam.add_child(hist_fam_int)

art_work.add_child(art_work_ext)
art_work.add_child(art_work_ext)
art_fam.add_child(art_fam_int)
art_fam.add_child(art_fam_int)

# Fifth Level
math_work_ext_edu = TreeNode(q5_1)
sci_work_ext_edu = TreeNode(q5_1)
lit_work_ext_edu = TreeNode(q5_1)
hist_work_ext_edu = TreeNode(q5_1)
art_work_ext_edu = TreeNode(q5_1)

math_work_ext_noedu = TreeNode("Mathematics, Finance, Mechanical Engineering, or Computer Engineering")
sci_work_ext_noedu = TreeNode("Integrated Health Sciences, Biology, or Nursing")
lit_work_ext_noedu = TreeNode(q4_2)
hist_work_ext_noedu = TreeNode("International Affairs, Political Science, or Media and Entertainment")
art_work_ext_noedu = TreeNode("Media and Entertainment, Digital Animation, or Theatre and Performance Studies")

math_fam_ext_edu = TreeNode(q5_1)
sci_fam_ext_edu = TreeNode(q5_1)
lit_fam_ext_edu = TreeNode(q5_1)
hist_fam_ext_edu = TreeNode(q5_1)
art_fam_ext_edu = TreeNode(q5_1)

math_fam_ext_noedu = TreeNode("Electrical Engineering Technology")
sci_fam_ext_noedu = TreeNode("Public Health Education")
lit_fam_ext_noedu = TreeNode(q4_2)
hist_fam_ext_noedu = TreeNode("Human Services, or Theatre and Performance Studies")
art_fam_ext_noedu = TreeNode("Theatre and Performance Studies")

math_work_int_money = TreeNode(q5_2)
sci_work_int_money = TreeNode("Physics")
lit_work_int_money = TreeNode("Marketing, Hospitality, or Management")
hist_work_int_money = TreeNode("Management, Construction Management, or Entrepreneurship")
art_work_int_money = TreeNode("Architecture")

math_work_int_resp = TreeNode("Mathematics, Physics, Economics, or Accounting")
sci_work_int_resp = TreeNode("Biochemistry, Chemistry, Biology, or Physics")
lit_work_int_resp = TreeNode("English, Modern Language and Culture, Criminal Justice, or Journalism and Emerging Media")
hist_work_int_resp= TreeNode("Antrhopology")
art_work_int_resp = TreeNode("Textile and Surface Design")

math_fam_int_money = TreeNode("Data Science and Analytics")
sci_fam_int_money = TreeNode("Technical Communication")
lit_fam_int_money = TreeNode("Technical Communication")
hist_fam_int_money = TreeNode("International Affairs")
art_fam_int_money = TreeNode("Digital Animation")

math_fam_int_resp = TreeNode("Mathematics")
sci_fam_int_resp = TreeNode("Geospatial Science, or Environmental Engineering")
lit_fam_int_resp = TreeNode("English")
hist_fam_int_resp = TreeNode("Anthropology, Philosophy, or Geography")
art_fam_int_resp = TreeNode("Art, Textile and Surface Design, or Digital Animation")

math_work_ext.add_child(math_work_ext_edu)
math_work_ext.add_child(math_work_ext_noedu)
math_fam_ext.add_child(math_fam_ext_edu)
math_fam_ext.add_child(math_fam_ext_noedu)
math_work_int.add_child(math_work_int_money)
math_work_int.add_child(math_work_int_resp)
math_fam_int.add_child(math_fam_int_money)
math_fam_int.add_child(math_fam_int_money)

sci_work_ext.add_child(sci_work_ext_edu)
sci_work_ext.add_child(sci_work_ext_noedu)
sci_fam_ext.add_child(sci_fam_ext_edu)
sci_fam_ext.add_child(sci_fam_ext_noedu)
sci_work_int.add_child(sci_work_int_money)
sci_work_int.add_child(sci_work_int_resp)
sci_fam_int.add_child(sci_fam_int_money)
sci_fam_int.add_child(sci_fam_int_resp)

lit_work_ext.add_child(lit_work_ext_edu)
lit_work_ext.add_child(lit_work_ext_noedu)
lit_fam_ext.add_child(lit_fam_ext_edu)
lit_fam_ext.add_child(lit_fam_ext_noedu)
lit_work_int.add_child(lit_work_int_money)
lit_work_int.add_child(lit_work_int_resp)
lit_fam_int.add_child(lit_fam_int_money)
lit_fam_int.add_child(lit_fam_int_resp)

hist_work_ext.add_child(hist_work_ext_edu)
hist_work_ext.add_child(hist_work_ext_noedu)
hist_fam_ext.add_child(hist_fam_ext_edu)
hist_fam_ext.add_child(hist_fam_ext_noedu)
hist_work_int.add_child(hist_work_int_money)
hist_work_int.add_child(hist_work_int_resp)
hist_fam_int.add_child(hist_fam_int_money)
hist_fam_int.add_child(hist_fam_int_resp)

art_work_ext.add_child(art_work_ext_edu)
art_work_ext.add_child(art_work_ext_noedu)
art_fam_ext.add_child(art_fam_ext_edu)
art_fam_ext.add_child(art_fam_ext_noedu)
art_work_int.add_child(art_work_int_money)
art_work_int.add_child(art_work_int_resp)
art_fam_int.add_child(art_fam_int_money)
art_fam_int.add_child(art_fam_int_resp)


# Sixth Level
math_work_ext_edu_elem = TreeNode("Elementary Education")
sci_work_ext_edu_elem = TreeNode("Elementary Education")
lit_work_ext_edu_elem = TreeNode("Elementary Education or English Education")
hist_work_ext_edu_elem = TreeNode("Elementary Education or History Education")
art_work_ext_edu_elem = TreeNode("Elementary Education or Music Education")

math_work_ext_edu_mid = TreeNode("Middle Grades Education")
sci_work_ext_edu_mid = TreeNode("Middle Grades Education")
lit_work_ext_edu_mid = TreeNode("Middle Grades Education or English Education")
hist_work_ext_edu_mid = TreeNode("Middle Grades Education or History Education")
art_work_ext_edu_mid = TreeNode("Middle Grades Education or Music Education")

math_work_ext_edu_high = TreeNode("Secondary Education, Mathematics, or Physics")
sci_work_ext_edu_high = TreeNode("Secondary Education, Physics, Biology, or Chemistry")
lit_work_ext_edu_high = TreeNode("Secondary Education or English Education")
hist_work_ext_edu_high = TreeNode("Secondary Education or History Education")
art_work_ext_edu_high = TreeNode("Secondary Education or Music Education")

math_work_ext_edu_uni = TreeNode("Mathematics or Physics")
sci_work_ext_edu_uni = TreeNode("Physics, Chemistry, Biology, or Biochemistry")
lit_work_ext_edu_uni = TreeNode("English or English Education")
hist_work_ext_edu_uni = TreeNode("Geography, History or History Education")
art_work_ext_edu_uni = TreeNode("Art, Music, or Music Education")

math_fam_ext_edu_elem = TreeNode("Elementary Education")
sci_fam_ext_edu_elem = TreeNode("Elementary Education")
lit_fam_ext_edu_elem = TreeNode("Elementary Education or English Education")
hist_fam_ext_edu_elem = TreeNode("Elementary Education or History Education")
art_fam_ext_edu_elem = TreeNode("Elementary Education or Music Education")

math_fam_ext_edu_mid = TreeNode("Middle Grades Education")
sci_fam_ext_edu_mid = TreeNode("Middle Grades Education")
lit_fam_ext_edu_mid = TreeNode("Middle Grades Education or English Education")
hist_fam_ext_edu_mid = TreeNode("Middle Grades Education or History Education")
art_fam_ext_edu_mid = TreeNode("Middle Grades Education or Music Education")

math_fam_ext_edu_high = TreeNode("Secondary Education, Mathematics, or Physics")
sci_fam_ext_edu_high = TreeNode("Secondary Education, Physics, Biology, or Chemistry")
lit_fam_ext_edu_high = TreeNode("Secondary Education or English Education")
hist_fam_ext_edu_high = TreeNode("Secondary Education or History Education")
art_fam_ext_edu_high = TreeNode("Secondary Education or Music Education")

math_fam_ext_edu_uni = TreeNode("Mathematics or Physics")
sci_fam_ext_edu_uni = TreeNode("Physics, Chemistry, Biology, or Biochemistry")
lit_fam_ext_edu_uni = TreeNode("English or English Education")
hist_fam_ext_edu_uni = TreeNode("Geography, History or History Education")
art_fam_ext_edu_uni = TreeNode("Art, Music, or Music Education")

math_work_int_money_comp = TreeNode("Cybersecurity, Information Technology, Computer Science, Computer Engineering, Electrical Engineering, or Software Engineering")
math_work_int_money_nocomp = TreeNode("Mathematics, Physics")

lit_work_ext_noedu_money = TreeNode("Entrepreneurship, Management, Marketing, or Professional Sales")
lit_work_ext_noedu_resp = TreeNode("Organizational and Professional Communication, Marketing, Human Services, Criminal Justice, or Journalism and Emerging Media")
lit_fam_ext_noedu_money = TreeNode("Marketing or Psychology")
lit_fam_ext_noedu_resp = TreeNode(q5_3)

math_work_ext_edu.add_child(math_work_ext_edu_elem)
math_work_ext_edu.add_child(math_work_ext_edu_mid)
math_work_ext_edu.add_child(math_work_ext_edu_high)
math_work_ext_edu.add_child(math_work_ext_edu_uni)

math_fam_ext_edu.add_child(math_fam_ext_edu_elem)
math_fam_ext_edu.add_child(math_fam_ext_edu_mid)
math_fam_ext_edu.add_child(math_fam_ext_edu_high)
math_fam_ext_edu.add_child(math_fam_ext_edu_uni)

sci_work_ext_edu.add_child(sci_work_ext_edu_elem)
sci_work_ext_edu.add_child(sci_work_ext_edu_mid)
sci_work_ext_edu.add_child(sci_work_ext_edu_high)
sci_work_ext_edu.add_child(sci_work_ext_edu_uni)

sci_fam_ext_edu.add_child(sci_fam_ext_edu_elem)
sci_fam_ext_edu.add_child(sci_fam_ext_edu_mid)
sci_fam_ext_edu.add_child(sci_fam_ext_edu_high)
sci_fam_ext_edu.add_child(sci_fam_ext_edu_uni)

lit_work_ext_edu.add_child(lit_work_ext_edu_elem)
lit_work_ext_edu.add_child(lit_work_ext_edu_mid)
lit_work_ext_edu.add_child(lit_work_ext_edu_high)
lit_work_ext_edu.add_child(lit_work_ext_edu_uni)

lit_fam_ext_edu.add_child(lit_fam_ext_edu_elem)
lit_fam_ext_edu.add_child(lit_fam_ext_edu_mid)
lit_fam_ext_edu.add_child(lit_fam_ext_edu_high)
lit_fam_ext_edu.add_child(lit_fam_ext_edu_uni)

hist_work_ext_edu.add_child(hist_work_ext_edu_elem)
hist_work_ext_edu.add_child(hist_work_ext_edu_mid)
hist_work_ext_edu.add_child(hist_work_ext_edu_high)
hist_work_ext_edu.add_child(hist_work_ext_edu_uni)

hist_fam_ext_edu.add_child(hist_fam_ext_edu_elem)
hist_fam_ext_edu.add_child(hist_fam_ext_edu_mid)
hist_fam_ext_edu.add_child(hist_fam_ext_edu_high)
hist_fam_ext_edu.add_child(hist_fam_ext_edu_uni)

art_work_ext_edu.add_child(art_work_ext_edu_elem)
art_work_ext_edu.add_child(art_work_ext_edu_mid)
art_work_ext_edu.add_child(art_work_ext_edu_high)
art_work_ext_edu.add_child(art_work_ext_edu_uni)

art_fam_ext_edu.add_child(art_fam_ext_edu_elem)
art_fam_ext_edu.add_child(art_fam_ext_edu_mid)
art_fam_ext_edu.add_child(art_fam_ext_edu_high)
art_fam_ext_edu.add_child(art_fam_ext_edu_uni)

math_work_int_money.add_child(math_work_int_money_comp)
math_work_int_money.add_child(math_work_int_money_nocomp)

lit_work_ext_noedu.add_child(lit_work_ext_noedu_money)
lit_work_ext_noedu.add_child(lit_work_ext_noedu_resp)
lit_fam_ext_noedu.add_child(lit_fam_ext_noedu_money)
lit_fam_ext_noedu.add_child(lit_fam_ext_noedu_resp)


# Seventh Level
lit_fam_ext_noedu_resp_gen = TreeNode("Psychology, Sociology, Exercise Science, or Health and Physical Activities Leadership")
lit_fam_ext_noedu_resp_cult = TreeNode("Asian Studies, Black Studies, or Modern Language and Culture")

lit_fam_ext_noedu_resp.add_child(lit_fam_ext_noedu_resp_gen)
lit_fam_ext_noedu_resp.add_child(lit_fam_ext_noedu_resp_cult)
