module NumAST ( AST(..), eval ) where

data AST = Constant Int
         | Minus AST
         | Add AST AST
         | Multiply AST AST
         deriving (Show, Eq)

eval :: AST -> Int
eval node = case node of
  Constant n   -> n
  Minus n      -> negate (eval n)
  Add a b      -> eval a + eval b
  Multiply a b -> eval a * eval b
