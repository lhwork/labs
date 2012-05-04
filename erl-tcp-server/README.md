### Erlang连接压力测试程序
=========================

### 性能优化

1. 编译erlang，支持epoll

        ./configure --enable-threads --enable-kernel-poll
        make && make install

2. 修改erlang环境变量

        vim ~/.bashrc
        set ERL_MAX_PORTS=102400
        export ERL_MAX_PORTS

3. 修改文件描述符数量

        ulimit -n 102400

4. 修改端口范围

		echo 1024 65535 > /proc/sys/net/ipv4/ip_local_port_range

5. 启动

        $erl -noshell +P 102400 +K true +S 2 -smp -s echo_server start

