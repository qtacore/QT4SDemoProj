## QT4SDemo工程

此工程是为了示范qt4s框架使用方式的demo工程。

### 快速上手

安装qt4s库，qt4s暂时还未上传到pypi，因此使用源码安装：

```shell
git clone https://github.com/qtacore/QT4S_censored
cd QT4S_censored
python setup.py install
cd ..
```

安装qtaf，直接用pip安装：

```shell
pip install qtaf
```

拉取测试代码并执行测试用例：

```shell
git clone https://github.com/qtacore/QT4SDemo.git
cd QT4SDemo
python manage.py runtest demotest.http_demo
```

可以看到，在命令行用例的执行情况，执行了一个测试用例，并且都通过了。

我们上面是在命令行执行的测试用例，代码库包含了eclipse工程的配置文件，可以导入eclipse来编写和调试用例。

### 编写测试用例

#### 环境准备

* java官网下载最新的匹配自己电脑cpu架构的jre并安装
* eclipse官网下载最新的匹配自己电脑cpu架构的eclipse在线安装程序,可能需要自己安装pydev模块。
* 安装ActivePython2.7版本，参考[ActivePython下载](https://www.activestate.com/products/activepython/downloads/)。

通常64位电脑，都选择x64版本即可。

#### 编写用例

使用eclipse的导入功能，将QT4SDemo工程导入到eclipse，然后就可以编写测试用例了。

我们先看下工程中已有的测试用例demotest.hello.HelloTest2，代码如下：

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

可以看到，一个用例就是一个类，这个类继承自TestCase（HelloTestBase继承自TestCase）。

一个用例，有4个属性：

* timeout，用例执行最大的超时时间
* owner，用例的作者
* priority，用例的优先级
* status，用例的状态

用例定义了run_test方法，当用例执行的时候，就是从run_test入口开始的。更多用例相关的内容，可以参考：[测试用例](https://qta-testbase.readthedocs.io/zh/latest/testcase.html)。

这里我们主要关注一个后台测试用例的步骤，上面代码中，可以清晰看到，用例包含了三个步骤：

* 构造通道，实例化了一个HttpChannel对象，指定了服务端的host和port
* 发送请求并获取回包，调用HttpChannel通道的get请求，获取了rsp
* 检查回包，对回包的内容进行检查，使用了断言

基本上，对每个后台的请求收发，都可以按照上面的模式进行套用。可以看到通过对通道和请求的封装，用例的内容是非常简单的（去掉步骤和log打印，实际代码也就4行）。

### 调试用例

在eclipse里面，可以在\_\_main\_\_里面实例化用例对象，并执行debug_run()，例如：

```python
if __name__ == "__main__":
    HttpDemoTest().debug_run()
```

也可以在命令行执行测试用例，如上面“快速入手”教程里面提供的方式：

```shell
python manage.py runtest demotest.http_demo.HttpDemoTest
```

更加详细的执行测试用例的方式可以参考文档：[执行测试](https://qta-testbase.readthedocs.io/zh/latest/testrun.html)。

