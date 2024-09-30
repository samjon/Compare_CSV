You need to create config.ini:
```
[email address]
from_mail = sender_address@mail.ru
from_passwd = you_pass
server_addr = mail.address.ru
comu_mail = recipient_address@mail.ru
```
the config.ini file must be placed in the directory with the program
Description:
Программа проверяет в текущей директории наличие файлов cvs, если их больше 2-х, то проверяет их на отличие, если файлы отличаются, то создаётся файл с изменениями и отправляется на электронную почту указанную в файле config.ini, после программы удаляет все файлы csv в текущей директории
