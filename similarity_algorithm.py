import codecs
from os import walk
import parso
import re
import javac_parser
import sctokenizer
import sqlparse

resultListCount = []


def getResultListCount():
    return resultListCount


# Walk the given directory and store the names of all the files in it.
def walk_dir(start_directory):
    f_names = []
    for (dirpath, dirnames, filenames) in walk(start_directory):
        f_names.append(filenames)
    return f_names


# The method to check Python file similarity
def check_python(rep_path):
    names = walk_dir(rep_path)
    try:
        names[0].remove('.DS_Store')
    except:
        names[0] = names[0]

    code_dict = openfile(rep_path, names)[0]
    pos_dict = openfile(rep_path, names)[1]

    mark, matches_list = greedy_tiling(code_dict, names, 12)

    mark_dict = mark

    match_dict = {}
    for i in matches_list:
        try:
            match_dict[i[3]].append((pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]]))
        except:
            match_dict[i[3]] = [(pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]])]

        try:
            match_dict[i[4]].append((pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]]))

        except:
            match_dict[i[4]] = [(pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]])]

    return mark_dict, match_dict



# Open a python file and tokenize it
def openfile(filepath, f_names):
    code_dict = {}
    pos_dict = {}
    for i in range(0, (len(f_names[0]))):
        with codecs.open(filepath + f_names[0][i], 'r', encoding='utf-8', errors='ignore') as f:
            token_list = []
            lines = f.readlines()
            text = ''
            for line in lines:
                text = text + line
            for e in parso.parse(text, version="3.9").children:
                token_list.append(e)
            counter = 0
            check = 1
            while counter != check:
                check = counter
                temp = []
                for e in token_list:
                    try:
                        temp = temp + e.children
                        counter = counter + 1

                    except:
                        temp.append(e)
                token_list = temp
            pos_list = []
            final_list = []
            for a in token_list:
                if a.type == 'keyword':
                    final_list.append(a)
                    pos_list.append(a.start_pos)
                elif str(a) == '<Operator: =>':
                    final_list.append('assign')
                    pos_list.append(a.start_pos)
                elif re.match('<Name: print@', str(a)) is not None:
                    final_list.append('out')
                    pos_list.append(a.start_pos)
                elif re.match('<Name: write@', str(a)) is not None:
                    final_list.append('out')
                    pos_list.append(a.start_pos)
                elif re.match('<Name: read@', str(a)) is not None:
                    final_list.append('in')
                    pos_list.append(a.start_pos)
                elif re.match('<Name: readline@', str(a)) is not None:
                    final_list.append('in')
                    pos_list.append(a.start_pos)
                elif re.match('<Name: readlines@', str(a)) is not None:
                    final_list.append('in')
                    pos_list.append(a.start_pos)

            code_dict[f_names[0][i]] = final_list
            pos_dict[f_names[0][i]] = pos_list

    return code_dict, pos_dict


# Loop through all the files and calculate their similarity
def greedy_tiling(code_dict, f_names, max):
    mark = {}
    duplicate = {}
    matches_list = []
    for i in range(0, (len(f_names[0]))):
        temp = []
        for e in code_dict[f_names[0][i]]:
            temp.append('0')
        mark[f_names[0][i]] = temp

    for i in f_names[0]:

        mark[i] = ['0'] * len(mark[i])

        for a in f_names[0]:
            if a != i:

                mark[a] = ['0'] * len(mark[a])
                maxMatch = max
                while maxMatch >= max:
                    matches = []
                    count = 0

                    for t in range(0, len(code_dict[i])):
                        if mark[i][t] == '0':
                            for b in range(0, len(code_dict[a])):

                                if mark[a][b] == '0' and str(code_dict[i][t]) == str(code_dict[a][b]):

                                    j = 0
                                    flag = True

                                    while str(code_dict[a][b + j]) == str(code_dict[i][t + j]) and flag:

                                        if ((b + j + 1) < len(code_dict[a])) and ((t + j + 1) < len(code_dict[i])):
                                            if mark[a][b + j] == '0' and mark[i][t + j] == '0':
                                                j = j + 1
                                            else:
                                                flag = False
                                        else:
                                            flag = False

                                    if j > count:
                                        count = j
                                        matches = [(t, b, j, i, a)]
                                    elif j == count:
                                        matches.append((t, b, j, i, a))

                    maxMatch = count

                    if maxMatch >= max:

                        for f in matches:
                            matches_list.append(f)
                        for m in matches:
                            for c in range(0, m[2]):
                                mark[i][m[0] + c] = a


        count = 0
        for n in mark[i]:
            if n != '0':
                count = count + 1
        score = count / len(mark[i])
        duplicate[i] = str(score)

    return duplicate, matches_list


# Open Java file and tokenize them
def openfile_java(filepath, f_names):
    java = javac_parser.Java()
    code_dict = {}
    pos_dict = {}
    for i in range(0, (len(f_names[0]))):
        with codecs.open(filepath + f_names[0][i], 'r', encoding='utf-8', errors='ignore') as f:
            token_list = []
            lines = f.readlines()
            text = ''
            for line in lines:
                text = text + line
            for e in java.lex(text):
                token_list.append(e)

            pos_list = []
            final_list = []
            reservedWord = ['CLASS', 'PACKAGE', 'IMPORT', 'WHILE', 'FOR', 'SWITCH', 'CASE', 'TRY',
                            'CATCH', 'FINALLY', 'IF', 'ELSE', 'RETURN', 'BREAK', 'CONTINUE', 'VOID',
                            'LBRACE', 'RBRACE', 'EQ', 'INT', 'BOOLEAN', 'DOUBLE', 'STRING', 'CHARACTER', 'IDENTIFIER',
                            'System']
            for a in token_list:
                # print(a.start_pos)
                for word in reservedWord:
                    if a[0] == word:
                        if word == 'INT':
                            final_list.append('CreateVar')
                            pos_list.append((a[2][0], a[2][1]))
                        elif word == 'BOOLEAN':
                            final_list.append('CreateVar')
                            pos_list.append((a[2][0], a[2][1]))
                        elif word == 'DOUBLE':
                            final_list.append('CreateVar')
                            pos_list.append((a[2][0], a[2][1]))
                        elif word == 'STRING':
                            final_list.append('CreateVar')
                            pos_list.append((a[2][0], a[2][1]))
                        elif word == 'CHARACTER':
                            final_list.append('CreateVar')
                            pos_list.append((a[2][0], a[2][1]))
                        elif word == 'IDENTIFIER':
                            if a[1] == 'System':
                                final_list.append(a[0])
                                pos_list.append((a[2][0], a[2][1]))
                        else:
                            final_list.append(a[0])
                            pos_list.append((a[2][0], a[2][1]))

            code_dict[f_names[0][i]] = final_list
            pos_dict[f_names[0][i]] = pos_list

    return code_dict, pos_dict


# Open CPP file and tokenize them
def openfile_cpp(filepath, f_names):
    code_dict = {}
    pos_dict = {}
    for i in range(0, (len(f_names[0]))):
        pos_list = []
        final_list = []
        tokens = sctokenizer.tokenize_file(filepath=filepath + f_names[0][i], lang='cpp')
        for t in tokens:
            if str(t.token_type) == 'TokenType.KEYWORD':
                final_list.append(t.token_value)
                pos_list.append((t.line, t.column))
            elif str(t.token_type) == 'TokenType.SPECIAL_SYMBOL':
                if t.token_value == '{':
                    final_list.append('Block_Begin')
                    pos_list.append((t.line, t.column))
                elif t.token_value == '}':
                    final_list.append('Block_End')
                    pos_list.append((t.line, t.column))
            elif str(t.token_type) == 'TokenType.OPERATOR':
                if t.token_value == '=':
                    final_list.append('Assign')
                    pos_list.append((t.line, t.column))

        code_dict[f_names[0][i]] = final_list
        pos_dict[f_names[0][i]] = pos_list

    return code_dict, pos_dict


# Open PHP file and tokenize them
def open_PHP(filepath, f_names):
    code_dict = {}
    pos_dict = {}
    for i in range(0, (len(f_names[0]))):
        pos_list = []
        final_list = []
        tokens = sctokenizer.tokenize_file(filepath=filepath + f_names[0][i], lang='php')
        for t in tokens:
            if str(t.token_type) == 'TokenType.KEYWORD':
                final_list.append(t.token_value)
                pos_list.append((t.line, t.column))
            elif str(t.token_type) == 'TokenType.SPECIAL_SYMBOL':
                final_list.append(t.token_value)
                pos_list.append((t.line, t.column))
            elif str(t.token_type) == 'TokenType.OPERATOR':
                if t.token_value == '=':
                    final_list.append('ASSIGN')
                    pos_list.append((t.line, t.column))

        code_dict[f_names[0][i]] = final_list
        pos_dict[f_names[0][i]] = pos_list

    return code_dict, pos_dict


# Open C file and tokenize them
def openfile_c(filepath, f_names):
    code_dict = {}
    pos_dict = {}
    for i in range(0, (len(f_names[0]))):
        pos_list = []
        final_list = []
        tokens = sctokenizer.tokenize_file(filepath=filepath + f_names[0][i], lang='c')
        for t in tokens:
            if str(t.token_type) == 'TokenType.KEYWORD':
                final_list.append(t.token_value)
                pos_list.append((t.line, t.column))
            elif str(t.token_type) == 'TokenType.SPECIAL_SYMBOL':
                if t.token_value == '{':
                    final_list.append('Block_Begin')
                    pos_list.append((t.line, t.column))
                elif t.token_value == '}':
                    final_list.append('Block_End')
                    pos_list.append((t.line, t.column))
            elif str(t.token_type) == 'TokenType.OPERATOR':
                if t.token_value == '=':
                    final_list.append('Assign')
                    pos_list.append((t.line, t.column))
        code_dict[f_names[0][i]] = final_list
        pos_dict[f_names[0][i]] = pos_list

    return code_dict, pos_dict


# Open SQL file and tokenize them
def open_sql(filepath, f_names):
    code_dict = {}
    pos_dict = {}
    for i in range(0, (len(f_names[0]))):
        pos_list = []
        final_list = []
        with codecs.open(filepath + f_names[0][i], 'r', encoding='utf-8', errors='ignore') as f:
            token_list = []
            lines = f.readlines()
            for l in range(0, len(lines)):
                parsed = sqlparse.parse(lines[l])[0]
                for p in parsed:
                    if str(p.ttype) == 'Token.Keyword.DML':
                        final_list.append(str(p))
                        pos_list.append((l + 1, parsed.token_index(p)))
                    elif str(p.ttype) == 'Token.Keyword.DDL':
                        final_list.append(str(p))
                        pos_list.append((l + 1, parsed.token_index(p)))
                    elif str(p.ttype) == 'Token.Keyword':
                        final_list.append(str(p))
                        pos_list.append((l + 1, parsed.token_index(p)))

        code_dict[f_names[0][i]] = final_list
        pos_dict[f_names[0][i]] = pos_list

    return code_dict, pos_dict


# Check the similarity of Java files in a given directory
def check_java(rep_path):
    names = walk_dir(rep_path)
    try:
        names[0].remove('.DS_Store')
    except:
        names[0] = names[0]

    code_dict = openfile_java(rep_path, names)[0]
    pos_dict = openfile_java(rep_path, names)[1]

    mark, matches_list = greedy_tiling(code_dict, names, 12)

    mark_dict = mark

    match_dict = {}
    for i in matches_list:
        try:
            match_dict[i[3]].append((pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]]))
        except:
            match_dict[i[3]] = [(pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]])]

        try:
            match_dict[i[4]].append((pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]]))

        except:
            match_dict[i[4]] = [(pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]])]

    return mark_dict, match_dict


# Check the similarity of C++ files in a given directory
def check_cpp(rep_path):
    names = walk_dir(rep_path)
    try:
        names[0].remove('.DS_Store')
    except:
        names[0] = names[0]

    code_dict = openfile_cpp(rep_path, names)[0]
    pos_dict = openfile_cpp(rep_path, names)[1]

    mark, matches_list = greedy_tiling(code_dict, names, 12)

    mark_dict = mark

    match_dict = {}
    for i in matches_list:
        try:
            match_dict[i[3]].append((pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]]))
        except:
            match_dict[i[3]] = [(pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]])]

        try:
            match_dict[i[4]].append((pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]]))

        except:
            match_dict[i[4]] = [(pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]])]

    return mark_dict, match_dict


# Check the similarity of PHP files in a given directory
def check_PHP(rep_path):
    names = walk_dir(rep_path)
    try:
        names[0].remove('.DS_Store')
    except:
        names[0] = names[0]

    code_dict = open_PHP(rep_path, names)[0]
    pos_dict = open_PHP(rep_path, names)[1]

    mark, matches_list = greedy_tiling(code_dict, names, 12)

    mark_dict = mark

    match_dict = {}
    for i in matches_list:
        try:
            match_dict[i[3]].append((pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]]))
        except:
            match_dict[i[3]] = [(pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]])]

        try:
            match_dict[i[4]].append((pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]]))

        except:
            match_dict[i[4]] = [(pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]])]

    return mark_dict, match_dict


# Check the similarity of C files in a given directory
def check_C(rep_path):
    names = walk_dir(rep_path)
    try:
        names[0].remove('.DS_Store')
    except:
        names[0] = names[0]

    code_dict = openfile_c(rep_path, names)[0]
    pos_dict = openfile_c(rep_path, names)[1]

    mark, matches_list = greedy_tiling(code_dict, names, 12)

    mark_dict = mark

    match_dict = {}
    for i in matches_list:
        try:
            match_dict[i[3]].append((pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]]))
        except:
            match_dict[i[3]] = [(pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]])]

        try:
            match_dict[i[4]].append((pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]]))

        except:
            match_dict[i[4]] = [(pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]])]

    return mark_dict, match_dict


# Check the similarity of SQL files in a given directory
def check_sql(rep_path):
    names = walk_dir(rep_path)
    try:
        names[0].remove('.DS_Store')
    except:
        names[0] = names[0]

    code_dict = open_sql(rep_path, names)[0]
    pos_dict = open_sql(rep_path, names)[1]

    mark, matches_list = greedy_tiling(code_dict, names, 5)

    mark_dict = mark

    match_dict = {}
    for i in matches_list:
        try:
            match_dict[i[3]].append((pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]]))
        except:
            match_dict[i[3]] = [(pos_dict[i[3]][i[0]], pos_dict[i[3]][i[0] + i[2]], i[4], pos_dict[i[4]][i[1]])]

        try:
            match_dict[i[4]].append((pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]]))

        except:
            match_dict[i[4]] = [(pos_dict[i[4]][i[1]], pos_dict[i[4]][i[1] + i[2]], i[3], pos_dict[i[3]][i[0]])]

    return mark_dict, match_dict


