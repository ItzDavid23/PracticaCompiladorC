"""Pruebas del analizador léxico de Mini C según SKILL.md."""

from minic.diagnostics import diagnostic_code
from minic.lexer.lexer import Lexer
from minic.lexer.token import Token
from minic.lexer.token_type import TokenType
from minic.output.diagnostic_printer import format_diagnostic
from minic.output.token_printer import format_token


def test_skill_section_7_valid_source() -> None:
    source = "int2 = 12abc;\nwhilex == -5"
    lexer = Lexer(source)
    result = lexer.scan()

    assert len(result.diagnostics) == 0

    expected_tokens = [
        Token(TokenType.IDENTIFIER, "int2", None, 1, 1),
        Token(TokenType.ASSIGN, "=", None, 1, 6),
        Token(TokenType.INTEGER_LITERAL, "12", 12, 1, 8),
        Token(TokenType.IDENTIFIER, "abc", None, 1, 10),
        Token(TokenType.SEMICOLON, ";", None, 1, 13),
        Token(TokenType.IDENTIFIER, "whilex", None, 2, 1),
        Token(TokenType.EQUAL_EQUAL, "==", None, 2, 8),
        Token(TokenType.MINUS, "-", None, 2, 11),
        Token(TokenType.INTEGER_LITERAL, "5", 5, 2, 12),
        Token(TokenType.EOF, "", None, 2, 13),
    ]

    assert result.tokens == expected_tokens

    formatted_output = [format_token(t) for t in result.tokens]
    expected_formatted = [
        "IDENTIFIER 'int2' 1 1",
        "ASSIGN '=' 1 6",
        "INTEGER_LITERAL '12' 1 8",
        "IDENTIFIER 'abc' 1 10",
        "SEMICOLON ';' 1 13",
        "IDENTIFIER 'whilex' 2 1",
        "EQUAL_EQUAL '==' 2 8",
        "MINUS '-' 2 11",
        "INTEGER_LITERAL '5' 2 12",
        "EOF '' 2 13",
    ]
    assert formatted_output == expected_formatted


def test_skill_section_7_errors_source() -> None:
    source = "int x = @;\nx ! = 0; // fin"
    lexer = Lexer(source)
    result = lexer.scan()

    expected_tokens = [
        Token(TokenType.KW_INT, "int", None, 1, 1),
        Token(TokenType.IDENTIFIER, "x", None, 1, 5),
        Token(TokenType.ASSIGN, "=", None, 1, 7),
        Token(TokenType.SEMICOLON, ";", None, 1, 10),
        Token(TokenType.IDENTIFIER, "x", None, 2, 1),
        Token(TokenType.ASSIGN, "=", None, 2, 5),
        Token(TokenType.INTEGER_LITERAL, "0", 0, 2, 7),
        Token(TokenType.SEMICOLON, ";", None, 2, 8),
        Token(TokenType.IDENTIFIER, "fin", None, 2, 13),
        Token(TokenType.EOF, "", None, 2, 16),
    ]
    assert result.tokens == expected_tokens

    expected_diagnostics_formatted = [
        "LEX001 error 1:9 Carácter no reconocido: '@'",
        "LEX001 error 2:3 Carácter no reconocido: '!'",
        "LEX001 error 2:10 Carácter no reconocido: '/'",
        "LEX001 error 2:11 Carácter no reconocido: '/'",
    ]
    formatted_diagnostics = [format_diagnostic(d) for d in result.diagnostics]
    assert formatted_diagnostics == expected_diagnostics_formatted


def test_empty_source() -> None:
    result = Lexer("").scan()
    assert result.diagnostics == []
    assert len(result.tokens) == 1
    assert result.tokens[0] == Token(TokenType.EOF, "", None, 1, 1)


def test_operators_and_delimiters() -> None:
    source = "+ - == != = ( ) { } ;"
    result = Lexer(source).scan()
    assert result.diagnostics == []
    types = [t.type for t in result.tokens]
    assert types == [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.EQUAL_EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.ASSIGN,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]


def test_integer_literal_values() -> None:
    source = "007 0 42 12345678901234567890"
    result = Lexer(source).scan()
    assert result.diagnostics == []
    assert [t.literal for t in result.tokens[:-1]] == [7, 0, 42, 12345678901234567890]
