from pylox.parser.ast_printer import AstPrinter
from pylox.parser.expressions import Expression, Binary, Unary, Grouping, Literal
from pylox.token import Token
from pylox.token_types import TokenTypes

expr = Binary(
    Unary(
        Token(TokenTypes.MINUS, "-", None, 1),
        Literal(123)
    ),
    Token(TokenTypes.STAR, "*", None, 1),
    Grouping(Literal(45.67))
)

print(AstPrinter().print(expr))