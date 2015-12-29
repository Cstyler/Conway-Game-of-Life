#!/usr/bin/env python3
import sys

def parser():
    f = open('lifecoords', 'r')
    sys.stdin = f
    line_count = 0
    coords = []
    for line in sys.stdin:
        lex_count = 0
        for lex in line:
            if lex == '*':
                coords.append(( lex_count+30,line_count+15))
            lex_count += 1
        line_count += 1
    return coords
