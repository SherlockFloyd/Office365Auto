# Office365Auto

自动调用Azure接口实现对Office365E5续订

本项目不授权任何商业用途，仅个人学习交流使用

# AutoApiP

AutoApi 系列：~~AutoApi~~、AutoApiSecret、~~AutoApiSR、AutoApiS~~、AutoApiP

## 置顶

- **不保证续期**
- 设置了**周日(UTC 时间)不启动**自动调用

### 跳转

- Cron：https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=in-process&pivots=programming-language-python

## 步骤

- 准备工具：
  - E5 开发者账号（非个人/私人账号）
  - rclone 软件，[下载地址 rclone.org ](https://downloads.rclone.org/)，(windows 64）

#### 微软方面的准备工作

- **第一步，注册应用，获取应用 id、secret**

  - 1）点击打开[仪表板](https://aad.portal.azure.com/)，左边点击**所有服务**，找到**应用注册**，点击+**新注册**

  - 2）填入名字，受支持账户类型前三任选，重定向填入 http://localhost:53682/ ，点击**注册**

  - 3）复制应用程序（客户端）ID 到记事本备用(**获得了应用程序 ID**！)，点击左边管理的**证书和密码**，点击+**新客户端密码**，点击添加，复制新客户端密码的**值**保存（**获得了应用程序密码**！）

  - 4）点击左边管理的**API 权限**，点击+**添加权限**，点击常用 Microsoft API 里的**Microsoft Graph**(就是那个蓝色水晶)，
    点击**委托的权限**，然后在下面的条例选中下列需要的权限，最后点击底部**添加权限**

  **赋予 api 权限的时候，选择以下几个**

                Calendars.ReadWrite、Contacts.ReadWrite、Directory.ReadWrite.All、

                Files.ReadWrite.All、MailboxSettings.ReadWrite、Mail.ReadWrite、

                Notes.ReadWrite.All、People.Read.All、Sites.ReadWrite.All、

                Tasks.ReadWrite、User.ReadWrite.All

  - 5）添加完自动跳回到权限首页，点击**代表授予管理员同意**

- **第二步，获取 refresh_token(微软密钥)**

  - 1）rclone.exe 所在文件夹，shift+右键，在此处打开 powershell，输入下面**修改后**的内容，回车后跳出浏览器，登入 e5 账号，点击接受，回到 powershell 窗口，看到一串东西。
              ./rclone authorize "onedrive" "应用程序(客户端)ID" "应用程序密码"

  - 2）在那一串东西里找到 "refresh_token"：" ，从双引号开始选中到 ","expiry":2022 为止（就是 refresh_token 后面双引号里那一串，不要双引号），右键复制保存（**获得了微软密钥**）

---

#### GITHUB 方面的准备工作

- **第一步，fork 本项目**

  登陆/新建 github 账号，回到本项目页面，点击右上角 fork 本项目的代码到自己账号，会出现一个一样的项目，接下来的操作均在此项目下进行。

- **第二步，新建 github 密钥**

  - 1）进入你的个人设置页面 (右上角头像 Settings，不是仓库里的 Settings)，选择 Developer settings -> Personal access tokens -> Generate new token

  - 2）设置名字为 **GH_TOKEN** , 然后勾选 repo，点击 Generate token ，最后**复制保存**生成的 github 密钥（**获得了 github 密钥**，一旦离开页面下次就看不到了！）

- **第三步，新建 secret**

  - 1）依次点击页面上栏右边的 Setting -> 左栏 Secrets -> 右上 New repository secret，新建 4 个 secret： **GH_TOKEN、MS_TOKEN、CLIENT_ID、CLIENT_SECRET**

    **(以下填入内容注意前后不要有空格空行)**

  GH_TOKEN

  ```shell
  github密钥 (第三步获得)，例如获得的密钥是abc...xyz，则在secret页面直接粘贴进去，不用做任何修改，只需保证前后没有空格空行
  ```

  MS_TOKEN

  ```shell
  微软密钥（第二步获得的refresh_token）
  ```

  CLIENT_ID

  ```shell
  应用程序ID (第一步获得)
  ```

  CLIENT_SECRET

  ```shell
  应用程序密码 (第一步获得)
  ```

---

#### 调用

- 1）点击两次右上角的星星（star）启动 action,，再点击上面的 Action，选择 Auto Api Pro 就能看到每次的运行日志，看看运行状况

（必需点进去 Test Api 看下，api 有没有调用到位，有没有出错。外面的 Auto Api 打勾只能说明运行是正常的，我们还需要确认 api 调用成功了，就像图里的一样）

- 2）再点两次星星，如果还能成功运行就 ok 了（这一步是为了保证重新上传到 secret 的 token 是正确的）

### 教程完

---

## 额外设置 （看不懂请忽略）##

- **定时启动修改**

- **多账号/应用支持**

- **超级参数设置**

#### 定时启动修改

我设定的每小时自动运行一次（周日不启动），每次调用 6 轮（点击右上角星星/star 也可以立马调用一次）：

- 定时自动启动修改地方：在.github/workflow/autoapi.yml(只修改这一个)文件里

#### 多账号/应用支持

如果想输入第二账号或者应用，请按上述获取**第二个应用的 id、密码、微软密钥：**

再按以下步骤：

1)增加 secret

依次点击页面上栏右边的 Setting -> 左栏 Secrets -> 右上 New repository secret，新增加 secret：APP_NUM、MS_TOKEN_2、CLIENT_ID_2、CLIENT_SECRET_2

APP_NUM

```shell
账号/应用数量(现在例如是2，3个就是3，日后如果要增加请删掉新建APP_NUM)
```

MS_TOKEN_2

```shell
第二个账号的微软密钥（第二步refresh_token），（第三个就是MS_TOKEN_3，如此类推）
```

CLIENT_ID_2

```shell
第二个账号的应用程序ID(第一步)
```

CLIENT_SECRET_2

```shell
第二个账号的应用程序密码(第一步)
```

2)修改.github/workflows/里的两个 yml 文件（**超过 5 个账号需要更改，5 个及以下暂时不用修改文件，忽略这一步**）

#### 超级参数设置

index.py 文件开头有个 config_list，里面是以下参数配置

· 轮数：

             就是一次运行要跑多少轮api，也就是启动一次会重复跑几圈

· 是否启动随机时间（默认关闭）：

            这个是每一轮结束，要不要等一个随机时间再开始调用下一轮。后面两个参数就是生成随机时间的，例如设置600，1200，就会延时600-1200s之间。

· 是否开启随机 api 顺序（默认开启）：

            不开启就是初版10个api，固定顺序。开启就是28个api抽12个随机排序。

· 是否开启各 api 延时（默认关闭）：

            这个是每个api之间要不要开启延时。后面两参数参考“随机时间”

· 是否开启各账号延时（默认关闭）：

            这个是每个账号/应用之间要不要开启延时。后面两参数参考“随机时间”

（延时的设置是会延长运行时间的，全关闭大概每次运行 1min，开启就会适当延长）

—————————————完—————————————

End:感谢 wangziyingwen 维护的代码
