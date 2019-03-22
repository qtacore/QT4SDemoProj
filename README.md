## QT4SDemo工程

此工程是为了示范qt4s框架使用方式的demo工程。

### 快速上手

拉取测试代码并安装依赖：

```shell
git clone https://github.com/qtacore/QT4SDemo.git
cd QT4SDemo
python -m pip install -r requirements
```

命令行执行测试用例

```shell
python manage.py runtest demotest.http_demo
```

可以看到，在命令行用例的执行情况，执行了一个测试用例，并且都通过了。

我们上面是在命令行执行的测试用例，代码库包含了eclipse工程的配置文件，可以导入eclipse来编写和调试用例。

### 编写测试用例

#### 环境准备

* 下载最新的QTAIDE，进行安装
* 通过QTAIDE指定git路径https://github.com/qtacore/QT4SDemo.git ，导入工程

#### 编写用例

我们先看下工程中已有的测试用例demotest.http_demo.HttpDemoTest，代码如下：

```python
from testbase.testcase import TestCase
from qt4s.channel.http import HttpChannel


class HttpDemoTest(TestCase):
    '''http demo testcase
    '''
    timeout = 5
    owner = 'foo'
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        self.start_step('构造一个通道')
        chan = HttpChannel(host="www.qq.com")

        self.start_step('发送请求并获取回包')
        rsp = chan.get("/")

        self.start_step('检查回包内容')
        self.assert_("返回码错误", rsp.status_code == 200)
        self.assert_("reason错误", rsp.reason == "OK")
```

可以看到，一个用例就是一个类，这个类继承自TestCase。

一个用例，有4个属性：

* timeout，用例执行最大的超时时间
* owner，用例的作者
* priority，用例的优先级
* status，用例的状态

用例定义了run_test方法，当用例执行的时候，就是从run_test入口开始的。更多用例相关的内容，如用例的初始化和清理，可以参考：[设计测试用例](https://qta-testbase.readthedocs.io/zh/latest/testcase.html)。

这里我们主要关注一个后台测试用例的步骤，上面代码中，可以清晰看到，用例包含了三个步骤：

* 构造通道，实例化了一个HttpChannel对象，指定了服务端的host和port
* 发送请求并获取回包，调用HttpChannel通道的get请求，获取了rsp
* 检查回包，对回包的内容进行检查，使用了断言

基本上，对每个后台的请求收发，都可以按照上面的模式进行套用。可以看到通过对通道和请求的封装，用例的内容是非常简单的（去掉步骤和log打印，实际代码也就4行）。

### 调试用例

在QTAIDE里面内置了对用例的调试支持，直接点击IDE右上角的执行按钮，即可执行用例。

也可以在命令行执行测试用例，如上面“快速入手”教程里面提供的方式：

```shell
python manage.py runtest demotest.http_demo.HttpDemoTest
```

更加详细的命令行执行测试用例的方式可以参考文档：[执行测试](https://qta-testbase.readthedocs.io/zh/latest/testrun.html)。

