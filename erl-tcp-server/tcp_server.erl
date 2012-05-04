%% Copyright (C) 2002, Joe Armstrong  
%% File    : tcp_server.erl  
%% Author  : Joe Armstrong (joe@sics.se)  
%% Purpose : Keeps track of a number of TCP sessions  
%% Last modified: 2002-11-17  
  
-module(tcp_server).  
  
-export([start_raw_server/4, start_client/3,  
     stop/1, children/1]).  
  
-define(KILL_DELAY, 1000).  
  
%% -export([start_child/3]).  
  
%% start_raw_server(Port, Fun, Max)  
%%   This server accepts up to Max connections on Port  
%%   The *first* time a connection is made to Port  
%%   Then Fun(Socket) is called.   
%%   Thereafter messages to the socket result in messsages to the handler.  
  
%% a typical server is usually written like this:  
  
%% To setup a lister  
  
%% start_server(Port) ->      
%%     S = self(),  
%%     process_flag(trap_exit, true),  
%%     tcp_server:start_raw_server(Port,   
%%              fun(Socket) -> input_handler(Socket, S) end,   
%%              15,  
%%                              0)  
%%     loop().  
  
%% The loop() process is a central controller that all  
%% processes can use to synchronize amongst themselfves if necessary  
%% It ends up as the variable "Controller" in the input_handler  
  
%% A typical server is written like this:  
  
%% input_handler(Socket, Controller) ->  
%%     receive  
%%  {tcp, Socket, Bin} ->  
%%      ...  
%%      gen_tcp:send(Socket, ...)  
%%   
%%  {tcp_closed, Socket} ->  
%%  
%%   
%%  Any ->  
%%      ...  
%%   
%%     end.  
  
start_client(Host, Port, Length) ->  
     gen_tcp:connect(Host, Port,  
             [binary,   
              {active, true},   
              {packet, 2},  
              {packet_size, Length}], 30000).  
                       
%% Note when start_raw_server returns, it should be ready to  
%% Immediately accept connections  
%% 作用  
%%      当start_raw_server返回时, 就可以接受连接啦  
%% 参数  
%%      Port    服务器监听端口  
%%      Fun     数据处理函数  
%%      Max     最大连接数  
%%      Length  最大包的长度
start_raw_server(Port, Fun, Max, Length) ->  
    Name = port_name(Port), % 用端口号来命名进程   
    case whereis(Name) of  
    undefined ->            % 如果端口还未定义的话，则启动  
        Self = self(),  
        Pid = spawn_link(fun() ->   % 产生一个新进程  
                     cold_start(Self, Port, Fun, Max, Length)   % 冷启动  
                 end),  
        receive  
        {Pid, ok} ->  
            register(Name, Pid), % 接收到  
            {ok, Pid};  
        {Pid, Error} ->  
            Error  
        end;  
    _Pid ->             % 如果端口已定义，则报错  
        {error, already_started}  
    end.  
  
stop(Port) when integer(Port) ->  
    Name = port_name(Port),  
    case whereis(Name) of  
    undefined ->  
        not_started;  
    Pid ->  
        exit(Pid, kill),  
        (catch unregister(Name)),  
        stopped  
    end.  
  
children(Port) when integer(Port) ->  
    port_name(Port) ! {children, self()},   %   
    receive  
    {session_server, Reply} -> Reply  
    end.  
  
%% 作用  
%%      以端口号做为服务名称  
%% 参数  
%%      端口号  
port_name(Port) when integer(Port) ->  
    list_to_atom("portServer" ++ integer_to_list(Port)).  
  
%% 作用  
%%      启动服务  
%%  参数  
%%      Master      所有者  
%%      Port        端口  
%%      Fun         处理函数  
%%      Max         数大连接数  
%%      Length      最大包的长度
cold_start(Master, Port, Fun, Max, Length) ->  
    process_flag(trap_exit, true),  % 设置退出陷阱  
    io:format("Starting a port server on ~p...~n",[Port]),  
    % 绑定到端口,进行监听  
    case gen_tcp:listen(Port, [binary,  
                   %% {dontroute, true},  
                   {nodelay,true},  
                   {packet_size, Length},  
                   {packet, 2},  
                   {backlog, 1024},  
                   {reuseaddr, true},   
                   {active, false}]) of  
    {ok, Listen} ->  
        %% io:format("Listening on:~p~n",[Listen]),  
        Master ! {self(), ok},  % 发送成功消息  
        New = start_accept(Listen, Fun), % 开始接受连接   
        %% Now we're ready to run  
        socket_loop(Listen, New, [], Fun, Max); % 接受连接后,开始网络通信了   
    Error ->  
        Master ! {self(), Error}  
    end.  
  
%% Don't mess with the following code uless you really know what you're   
%% doing (and Thanks to Magnus for heping me get it right)  
%% 作用  
%%      接受连接后，开始运作  
socket_loop(Listen, New, Active, Fun, Max) ->  
    receive  
    {istarted, New} ->  
        Active1 = [New|Active], % 参见start_child,把新连接加入到活动列表中  
        possibly_start_another(false, Listen, Active1, Fun, Max);  
    {'EXIT', New, _Why} ->  
        %%io:format("Child exit=~p~n",[Why]),  
        possibly_start_another(false, Listen, Active, Fun, Max);  
    {'EXIT', Pid, _Why} ->  
        %%io:format("Child exit=~p~n",[Why]),  
        Active1 = lists:delete(Pid, Active),  
        possibly_start_another(New, Listen, Active1, Fun, Max);  
    {children, From} ->  
        From ! {session_server, Active},  
        socket_loop(Listen, New, Active, Fun, Max);  
    Other ->  
        io:format("Here in loop:~p~n",[Other])  
    end.  
  
possibly_start_another(New, Listen, Active, Fun, Max) when pid(New) ->  
    socket_loop(Listen, New, Active, Fun, Max);  
possibly_start_another(false, Listen, Active, Fun, Max) ->  
    case length(Active) of  
    N when N < Max ->  
        New = start_accept(Listen, Fun),  
        socket_loop(Listen, New, Active, Fun, Max);  
    _ ->  
        error_logger:warning_report(  
          [{module, ?MODULE},  
           {line, ?LINE},  
           {message, "Connections maxed out"},  
           {maximum, Max},  
           {connected, length(Active)},  
           {now, now()}]),  
        socket_loop(Listen, false, Active, Fun, Max)  
    end.  
  
%% 作用  
%%      开始接受连接啦  
%% 参数  
%%      Listen  监听的Socket  
%%      Fun     数据处理函数  
start_accept(Listen, Fun) ->  
    S = self(),  
    spawn_link(fun() -> start_child(S, Listen, Fun) end). % 一个进程处理一个连接  
  
start_child(Parent, Listen, Fun) ->  
    case gen_tcp:accept(Listen) of  % 接受一个连接  
    {ok, Socket} ->  
        Parent ! {istarted,self()}, % 参见socket_loop, tell the controller  
        inet:setopts(Socket, [{nodelay,true},  
                  {packet, 2},  
                  {active, true}]), % before we activate socket  
        Fun(Socket); % 这里应用了数据处理函数Fun  
    _Other ->  
        exit(oops)  
    end.  
