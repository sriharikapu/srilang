import ast as python_ast
from typing import Any, Optional, Sequence, Type, Union

from .natspec import parse_natspec as parse_natspec
from .utils import ast_to_dict as ast_to_dict
from .utils import parse_to_ast as parse_to_ast

NODE_BASE_ATTRIBUTES: Any
NODE_SRC_ATTRIBUTES: Any
DICT_AST_SKIPLIST: Any

def get_node(
    ast_struct: Union[dict, python_ast.AST], parent: Optional[srilangNode] = ...
) -> srilangNode: ...

class srilangNode:
    full_source_code: str = ...
    def __init__(self, parent: Optional[srilangNode] = ..., **kwargs: dict) -> None: ...
    def __hash__(self) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...
    @property
    def description(self): ...
    @classmethod
    def get_fields(cls: Any) -> set: ...
    def evaluate(self) -> srilangNode: ...
    @classmethod
    def from_node(cls, node: srilangNode, **kwargs: Any) -> Any: ...
    def to_dict(self) -> dict: ...
    def get_children(
        self,
        node_type: Union[Type[srilangNode], Sequence[Type[srilangNode]], None] = ...,
        filters: Optional[dict] = ...,
        reverse: bool = ...,
    ) -> Sequence: ...
    def get_descendants(
        self,
        node_type: Union[Type[srilangNode], Sequence[Type[srilangNode]], None] = ...,
        filters: Optional[dict] = ...,
        include_self: bool = ...,
        reverse: bool = ...,
    ) -> Sequence: ...
    def get_ancestor(
        self, node_type: Union[Type[srilangNode], Sequence[Type[srilangNode]], None] = ...
    ) -> srilangNode: ...
    def get(self, field_str: str) -> Any: ...

class TopLevel(srilangNode):
    doc_string: Str = ...
    body: list = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __getitem__(self, key: Any) -> Any: ...
    def __iter__(self) -> Any: ...
    def __len__(self) -> int: ...
    def __contains__(self, obj: Any) -> bool: ...

class Module(TopLevel):
    def replace_in_tree(self, old_node: srilangNode, new_node: srilangNode) -> None: ...

class FunctionDef(TopLevel):
    name: str = ...
    args: arguments = ...
    returns: srilangNode = ...

class arguments(srilangNode):
    args: list = ...
    defaults: list = ...

class arg(srilangNode): ...
class Return(srilangNode): ...

class ClassDef(srilangNode):
    body: list = ...
    name: str = ...
    class_type: str = ...

class Constant(srilangNode):
    value: Any = ...

class Num(Constant):
    @property
    def n(self): ...

class Int(Num):
    value: int = ...

class Decimal(Num): ...
class Hex(Num): ...

class Str(Constant):
    @property
    def s(self): ...

class Bytes(Constant):
    @property
    def s(self): ...

class List(srilangNode):
    elts: list = ...

class Tuple(srilangNode):
    elts: list = ...

class Dict(srilangNode):
    keys: list = ...

class NameConstant(Constant): ...

class Name(srilangNode):
    id: str = ...

class Expr(srilangNode): ...

class UnaryOp(srilangNode):
    op: srilangNode = ...

class USub(srilangNode): ...
class Not(srilangNode): ...

class BinOp(srilangNode):
    op: srilangNode = ...

class Add(srilangNode): ...
class Sub(srilangNode): ...
class Mult(srilangNode): ...
class Div(srilangNode): ...
class Mod(srilangNode): ...
class Pow(srilangNode): ...
class BoolOp(srilangNode): ...
class And(srilangNode): ...
class Or(srilangNode): ...

class Compare(srilangNode):
    op: srilangNode = ...

class Eq(srilangNode): ...
class NotEq(srilangNode): ...
class Lt(srilangNode): ...
class LtE(srilangNode): ...
class Gt(srilangNode): ...
class GtE(srilangNode): ...
class In(srilangNode): ...

class Call(srilangNode):
    args: list = ...
    keywords: list = ...
    func: Name = ...

class keyword(srilangNode): ...
class Attribute(srilangNode): ...

class Subscript(srilangNode):
    slice: Index = ...

class Index(srilangNode):
    value: Constant = ...

class Assign(srilangNode): ...

class AnnAssign(srilangNode):
    target: srilangNode = ...
    value: srilangNode = ...
    annotation: srilangNode = ...

class AugAssign(srilangNode): ...
class Raise(srilangNode): ...
class Assert(srilangNode): ...
class Pass(srilangNode): ...

class Import(srilangNode):
    names: list = ...

class ImportFrom(srilangNode):
    level: int = ...
    module: str = ...
    names: list = ...

class alias(srilangNode): ...

class If(srilangNode):
    body: list = ...
    orelse: list = ...

class For(srilangNode): ...
class Break(srilangNode): ...
class Continue(srilangNode): ...