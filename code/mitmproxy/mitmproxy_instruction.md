[toc]

#####1，mitmproxy和mitmdump
* mitmproxy：一个交互式的控制台程序，允许信息流被截获，检查、修改和回放。
* mitmdump：提供给http命令，与mitmproxy没有多余的装饰相同的功能。

#####2，安装mitmproxy

    pip install mitmproxy
    

#####3，mitmproxy源码

    github.com/mitmproxy/mitmproxy
    
#####4，相关模块介绍

pathod
    
    一个病态的Web后台程序，和不正当的HTTP客户端。开始提供mitmproxy更好的测试，它现在已经采取了自己的罪恶的生命。
    
netograph
    
    隐私分析项目，采用libmproxy库建成。 mitmproxy的高性能服务器端应用程序的一个例子。
    
tamper

    一个基于mitmproxy扩展devtools，可以让你在本地编辑远程文件并直接为他们服务到Chrome浏览器。
    
bdfproxy

    BackDoor的工厂+ mitmproxy - 修补程序二进制文件在飞行shell代码。
    
mastermind

    来自ustmo的一个项目，提供了一个简单的方法来模拟服务（如API，网站）。
    
#####5，Inline Scripts

mitmproxy有一个强大的脚本API，可以让你修改即时流量或本地改写先前保存的流动。

######5.1，示例

mitmproxy脚本api是事件驱动的。一个脚本是一个Python模块，它公开了一组事件的方法。下面是完整的mitmproxy脚本，为每个http响应增加一个新的header，在它返回客户端之前。

examples/add_header.py¶

```
def response(context, flow):
    flow.response.headers["newheader"] = "foo"
```

第一个参数context，是ScriptContext的一个实例，让脚本与全球mitmproxy状态进行交互。响应事件，也得到一个ScriptContext实例，我们可以用它来操作响应本身。

我们可以用mitmdump或者mitmproxy运行脚本:

```
>>> mitmdump -s add_header.py
```

这样，所有通过proxy的响应，都将被加上新的header。

mitmproxy自带了多种例如内嵌脚本，可以演示许多基本操作。建议你在本地或者gitlab阅读阅读相关内容。

######5.2，Events

传到每个方法中的参数context，始终是ScriptContext的一个实例。它在脚本的生命周期中，保证是同一个对象，且不在多个inline脚本之间共享。您可以放心地使用它来存储您需要的、任何形式的状态。

#######5.2.1，Script Lifecycle Events(脚本生命周期事件)

    start(context, argv)：
        在启动时调用一次，任何其他事件之前。
        Parameters:	argv (List[str]) – 内嵌脚本的参数. 
            例如mitmproxy -s 'example.py --foo 42' sets argv to ["--foo", "42"].
            
    done(context)：
        脚本结束时调用，在所有其他脚本之后。
        
#######5.2.2，Connection Events(连接事件)

    clientconnect(context, root_layer)：
        当一个客户端向proxy发起一个连接时被调用。请注意，一个连接可以对应多个HTTP请求。(0.14版本)
        参数root_layer：根层(具体解释见协议)，他提供了一个对所有RootContext的属性的透明访问。
        比如，root_layer.client_conn.address可以获得连接客户端的远程地址。
        
    clientdisconnect(context, root_layer)：
        当客户端从proxy断开连接时，被调用。
        
    serverconnect(context, server_conn)：
        在proxy向目标服务器发起连接之前被调用。请注意，一个连接可以对应多个HTTP请求。
        参数server_conn：服务的连接对象，它保证有一个非空的地址属性。
        
    serverdisconnect(context, server_conn)：
        在proxy关闭服务的连接时，被调用。
        
#######5.2.3，HTTP Events(HTTP事件) 
        
    request(context, flow)：
        当一个终端request被接受的时候调用，flow对象保证有一个非空的request请求。
        参数flow：flow包含已经接收到的请求，且该对象保证request属性非空。
        
    responseheaders(context, flow)：
        当一个服务响应被接收时被调用。在响应被hook之前它将一直被调用。
        参数flow：flow包含已经接收到的请求，且该对象保证request和response非空。response.content是空的，作为响应身体没有读入。
        
    response(context, flow)：
        当一个response被接受时，被调用。
        参数flow：flow包含已经接收到的请求，且该对象保证request和response非空。response.body将包含原始响应主体，除非响应流已启用。
        
    error(context, flow)：
        当调用发生流量误差，例如无效的服务器响应，或中断连接。这是一个有效的服务器的HTTP错误响应，返回http错误码。
        参数flow：flow包含错误信息，且保证非空。
        
#######5.2.4，TCP Events(HTTP事件) 
           
    tcp_message(context, tcp_msg)：
        如果代理是TCP模式，当它接收到来自客户端或服务器的TCP有效载荷，该事件被调用。
        发送器和接收器是可识别的。该消息是用户可修改。
        参数tcp_msg：参见examples/tcp_message.py？        

######5.3，API
    
    规范的API文档是代码，你可以在此浏览，也可以查看源码。
    mitmproxy的主要类如下：
    ScriptContext：A handle for interacting with mitmproxy’s Flow Master from within scripts.
    ClientConnection：Describes a client connection.
    ServerConnection：Describes a server connection.
    HTTPFlow：A collection of objects representing a single HTTP transaction.
    HTTPRequest：An HTTP request.
    HTTPResponse：An HTTP response.
    Error：A communications error.
    netlib.http.Headers：A dictionary-like object for managing HTTP headers.
    netlib.certutils.SSLCert：Exposes information SSL certificates.
    mitmproxy.flow.FlowMaster：The “heart” of mitmproxy, usually subclassed as mitmproxy.dump.DumpMaster or mitmproxy.console.ConsoleMaster.
    
######5.4，Script Context
    
   该脚本环境应使用在脚本中与全球mitmproxy状态进行交互。
   
   log(message, level='info'): 记录一个事件。
   
   正常情况下，只记录等级为level的事件。这可以用“-v”开关来控制。信息如何被处理，取决于前端。mitmdump将把它们打印到stdout，mitmproxy为显示发送output到evenlog(E快捷键)。
   
   kill_flow(f): 立即杀死一个flow，没有进一步的数据，被发送到客户端或者服务器。
   
   duplicate_flow(f): 重复返回指定flow。这个flow也会注入当前状态，并准备好以进行编辑、重放。
   
   replay_request(f): 回放当前flow的request，响应将被添加到当前flow对象。
   
   app_registry: 
   
   add_contentview(view_obj): 
   
   remove_contentview(view_obj): 
   
######5.5，Running scripts in parallel：并行运行的脚本

我们有一个原始的flow，所以当一个脚本block，其他的requests将不被处理。阻碍的脚本被运行，通过使用mitmproxy.script.concurrent decorator可以解决，但是这通常被认为是过于理想的。如果你的脚本不阻塞，那就可以避免装饰器的开销。
    
    examples/nonblocking.py
    
    ```
    import time
    from mitmproxy.script import concurrent
    
    @concurrent  # Remove this and see what happens
    def request(context, flow):
        print("handle request: %s%s" % (flow.request.host, flow.request.path))
        time.sleep(5)
        print("start  request: %s%s" % (flow.request.host, flow.request.path))
        
    ```
    
######5.6，Make scripts configurable with arguments：使脚本配置带参数

有时候你想通过运行时参数运行inline脚本。这件事可以简单的完成，通过用引号包围脚本调用。例如: `mitmdump -s 'script.py --foo 42'。参数在随后启动事件中曝光。

    examples/modify_response_body.py
    
    ```
    # Usage: mitmdump -s "modify_response_body.py mitmproxy bananas"
    # (this script works best with --anticache)
    from mitmproxy.models import decoded
    
    def start(context, argv):
        if len(argv) != 3:
            raise ValueError('Usage: -s "modify_response_body.py old new"')
        # You may want to use Python's argparse for more sophisticated argument
        # parsing.
        context.old, context.new = argv[1], argv[2]
        
    def response(context, flow):
        with decoded(flow.response):  # automatically decode gzipped responses.
            flow.response.content = flow.response.content.replace(
                context.old,
                context.new)
    ```
    
######5.7，Running scripts on saved flows：运行脚本上保存flows

    有时候，我们想在flow objects上，运行一个已完成的脚本。这将发生在你启动一个脚本，然后从一个文件加载一个已存储flows束(见scripted data transformation这个例子)。它也会发生在你运行单个脚本的时候。
    
    在这种情况下，没有任何客户端连接，并且时间按以下顺序执行：start, request, responseheaders, response, error, done。如果flow没有一个response或者error与它关联。与它匹配的事件将被跳过。
    
######5.8，Spaces in the script path：脚本路径空间

    通常，空间被解释为内嵌脚本和它的参数之间的分隔符。例如：-s 'foo.py 42'。因此，脚本路径必须被包裹在一个单独的对引号如果包含空格：-s'\'./富酒吧/ baz.py\'42'.