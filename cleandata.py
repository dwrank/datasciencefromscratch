#!/usr/bin/env python

from __future__ import division

import csv
import dateutil.parser


def parse_row(input_row, parsers):
    '''given a list of parsers (some of which may be None)
    apply the appropriate one to each element of the input_row'''
    
    return [try_or_none(parser)(value) if parser is not None else value
            for value, parser in zip(input_row, parsers)]


def parse_rows_with(reader, parsers):
    '''wrap a reader to apply the parsers to each of it's rows'''
    for row in reader:
        yield parse_row(row, parsers)


def try_or_none(f):
    '''wraps f to return None if f raises an exception
    assume f takes only one input'''
    def f_or_none(x):
        try: return f(x)
        except: return None
    return f_or_none


def try_parse_field(field_name, value, parser_dict):
    '''try to parse value using the appropriate function from parser_dict'''
    parser = parser_dict.get(field_name)
    if parser is not None:
        return try_or_none(parser)(value)
    else:
        return value


def parse_dict(input_dict, parser_dict):
    return {field_name : try_parse_field(field_name, value, parser_dict)
            for field_name, value in input_dict.iteritems()}


if __name__ == '__main__':
    data = []
    
    with open('stock_prices.csv', 'rb') as f:
        reader = csv.reader(f)
        for line in parse_rows_with(reader, [dateutil.parser.parse, None, float]):
            data.append(line)

    for row in data:
        if any(x is None for x in row):
            print row
    
    # try it with a dict reader
    parser_dict = {'date': dateutil.parser.parse,
                   'price': float}
    
    with open('stock_prices.csv', 'rb') as f:
        reader = csv.DictReader(f, delimiter="\t")
        data = [parse_dict(row, parser_dict) for row in reader]

    for row in data:
        print row