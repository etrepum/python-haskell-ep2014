-module(nonsense).
-export([start/0]).

start() ->
    io:format("~p", [1 + "1"]).
