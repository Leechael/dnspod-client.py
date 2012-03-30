### dnspod-client.py

You haven't like to login than click, click, click... to simply replace old IP of hosts? (OR something you want to do but UI make you sucks)

Nope, I can -not- do for you.


#### Dependencies

* requests - good design leading to handy tool.
* simplejson - what come first in my mind when I need decode JSON.

Do:

```
pip install requests simplejson
```

Added prefix `sudo` if os tell you not allow to do that (like vixen? kidding.)


#### Configure

Create directory `~/.dnspodrc` and create file `config` inside the directory:

```
mkdir ~/.dnspodrc && cd ~/.dnspodrc && vim config
```

Replace vim to your favor editor -except Emacs.-

Example comes here:

```
[common]
login_email = your_name@domain.com
login_password = password_not_using_to_login_csdn
```

If you NOT create configuration file, the script will be vixen.


#### Usage

```
python replace_ip.py 192.168.0.101 10.0.1.101
```

All records configured with IP 192.168.0.101 will be replace the value by 10.0.1.101.


#### License

Copyright (c) 2012 Leechael Yim.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the <organization>.  The name of the
University may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

