-module(erserver).

-export([startd/0, start/0, start/1, process/1]).
-define(TCP_OPTIONS, [binary, {packet, 0}, {active, false}]).
-define(Port, 4444).

startd() ->
    register(?MODULE, spawn(?MODULE, start, [])).

start() -> start(?Port).

start(Port) ->
    case gen_tcp:listen(Port, ?TCP_OPTIONS) of
        {ok, LSock} -> server_loop(LSock);
        {error, Reason} -> Reason
    end.

%% main server loop - wait for next connection, spawn child to process it
server_loop(LSock) ->
    case gen_tcp:accept(LSock) of
        {ok, Sock} ->
            spawn(?MODULE, process, [Sock]),
            server_loop(LSock);
        {error, Reason} ->
            Reason
    end.

%% process current connection
process(Sock) ->
    Req = do_recv(Sock),
    io:format("recv data:~p~n.", [Req]),
    Resp = "(erlang) hello world",
    do_send(Sock, Resp),
    gen_tcp:close(Sock).

%% send a line of text to the socket
do_send(Sock,Msg) ->
    case gen_tcp:send(Sock, Msg) of
        ok -> ok;
        {error, Reason} -> Reason
    end.
    
%% receive data from the socket
do_recv(Sock) ->
    case gen_tcp:recv(Sock, 0) of
        {ok, Bin} -> binary_to_list(Bin);
        {error, closed} -> gen_tcp:close(Sock);
        {error, Reason} -> Reason
    end.
